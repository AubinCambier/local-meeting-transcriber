#!/usr/bin/env python3
"""
Transcription de réunion 100 % locale AVEC identification des intervenants :
Whisper transcrit, sherpa-onnx sépare les voix (Utilisateur 1, Utilisateur 2…).
Aucun appel à Claude. Réseau utilisé uniquement au premier lancement pour télécharger
les modèles (Whisper depuis Hugging Face, diarisation depuis GitHub).

Prérequis :
  pip3 install soundcard soundfile faster-whisper numpy sherpa-onnx

Usage (Mac par défaut ; ajouter --os windows ou --os debian sinon) :
  python3 script/meeting-whisper-final.py --list                        # liste les micros et sources de son
  python3 script/meeting-whisper-final.py                               # micro par défaut + son de l'ordi ; Ctrl+C
  python3 script/meeting-whisper-final.py --mic "MacBook" --audio none  # un micro précis, sans le son de l'ordi
  python3 script/meeting-whisper-final.py --file reunions/xxx.wav       # transcrit un fichier existant
  python3 script/meeting-whisper-final.py --file xxx.wav --speakers 3   # si on connaît le nombre de voix
  python3 script/meeting-whisper-final.py --nameFolder projetX          # range dans reunions/projetX/1/, puis 2/…
  HF_HUB_OFFLINE=1 python3 script/meeting-whisper-final.py              # interdit l'accès à Hugging Face
"""
import argparse, datetime, os, shutil, sys, tarfile, urllib.request
import audio_capture as ac

SAMPLE_RATE = 16000  # fréquence attendue par Whisper et sherpa-onnx

MODELS_DIR = os.path.expanduser("~/.cache/sherpa-onnx")
MODELS_URL = "https://github.com/k2-fsa/sherpa-onnx/releases/download"
SEGMENTATION = "sherpa-onnx-pyannote-segmentation-3-0"
EMBEDDING = "wespeaker_en_voxceleb_resnet34_LM.onnx"

def fetch_models():
    """Télécharge les modèles de diarisation une seule fois dans ~/.cache/sherpa-onnx."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    seg = os.path.join(MODELS_DIR, SEGMENTATION, "model.onnx")
    emb = os.path.join(MODELS_DIR, EMBEDDING)
    if not os.path.exists(seg):
        print("Téléchargement du modèle de segmentation…")
        archive = os.path.join(MODELS_DIR, SEGMENTATION + ".tar.bz2")
        urllib.request.urlretrieve(f"{MODELS_URL}/speaker-segmentation-models/{SEGMENTATION}.tar.bz2", archive)
        with tarfile.open(archive) as t:
            t.extract(f"{SEGMENTATION}/model.onnx", MODELS_DIR)
        os.remove(archive)
    if not os.path.exists(emb):
        print("Téléchargement du modèle d'empreinte vocale…")
        # "recongition" : faute de frappe présente dans l'URL officielle
        urllib.request.urlretrieve(f"{MODELS_URL}/speaker-recongition-models/{EMBEDDING}", emb)
    return seg, emb

def diarize(audio, speakers, threshold):
    import sherpa_onnx
    print("Identification des intervenants (sherpa-onnx)…")
    seg, emb = fetch_models()
    threads = os.cpu_count() or 1
    config = sherpa_onnx.OfflineSpeakerDiarizationConfig(
        segmentation=sherpa_onnx.OfflineSpeakerSegmentationModelConfig(
            pyannote=sherpa_onnx.OfflineSpeakerSegmentationPyannoteModelConfig(model=seg),
            num_threads=threads),
        embedding=sherpa_onnx.SpeakerEmbeddingExtractorConfig(model=emb, num_threads=threads),
        clustering=sherpa_onnx.FastClusteringConfig(num_clusters=speakers, threshold=threshold),
        min_duration_on=0.3,
        min_duration_off=0.5,
    )
    if not config.validate():
        sys.exit("Configuration de diarisation invalide (modèles manquants ?)")
    result = sherpa_onnx.OfflineSpeakerDiarization(config).process(audio).sort_by_start_time()
    return [(r.start, r.end, r.speaker) for r in result]

def speaker_at(turns, t):
    """Intervenant qui parle à l'instant t (ou le plus proche si t tombe dans un silence)."""
    best, dist = None, float("inf")
    for start, end, spk in turns:
        if start <= t <= end:
            return spk
        d = min(abs(t - start), abs(t - end))
        if d < dist:
            best, dist = spk, d
    return best

def transcribe(path, model_size, speakers, threshold):
    from faster_whisper import WhisperModel, decode_audio
    audio = decode_audio(path, sampling_rate=SAMPLE_RATE)
    turns = diarize(audio, speakers, threshold)

    print(f"Transcription locale (whisper {model_size})…")
    model = WhisperModel(model_size, device="auto", compute_type="int8")
    segments, _ = model.transcribe(audio, language="fr", vad_filter=True, word_timestamps=True)

    # Chaque mot est attribué à un intervenant ; on regroupe les mots consécutifs
    # du même intervenant en une réplique.
    labels, lines, current = {}, [], None
    for s in segments:
        for w in s.words:
            spk = speaker_at(turns, (w.start + w.end) / 2)
            if spk not in labels:
                labels[spk] = f"Utilisateur {len(labels) + 1}"
            if current is None or current["spk"] != spk:
                current = {"spk": spk, "start": w.start, "words": []}
                lines.append(current)
            current["words"].append(w.word)

    out = []
    for l in lines:
        ts = str(datetime.timedelta(seconds=int(l["start"])))
        line = f"[{ts}] {labels[l['spk']]} : {''.join(l['words']).strip()}"
        print(line)
        out.append(line)
    print(f"\n{len(labels)} intervenant(s) détecté(s).")
    return "\n\n".join(out)

def output_folder(name):
    """reunions/ par défaut ; avec --nameFolder, crée reunions/<name>/<n>/ où n suit le plus grand numéro existant."""
    if not name:
        os.makedirs("reunions", exist_ok=True)
        return "reunions"
    if name != os.path.basename(name) or name in (".", ".."):
        sys.exit("--nameFolder doit être un simple nom de dossier (sans / ni ..)")
    parent = os.path.join("reunions", name)
    os.makedirs(parent, exist_ok=True)
    nums = [int(d) for d in os.listdir(parent) if d.isdigit() and os.path.isdir(os.path.join(parent, d))]
    folder = os.path.join(parent, str(max(nums, default=0) + 1))
    os.makedirs(folder)
    return folder

def main():
    ap = argparse.ArgumentParser()
    ac.add_args(ap)
    ap.add_argument("--file", help="fichier audio existant à transcrire (pas d'enregistrement)")
    ap.add_argument("--model", default="small", help="tiny/base/small/medium/large-v3")
    ap.add_argument("--speakers", type=int, default=-1, help="nombre d'intervenants s'il est connu (sinon auto)")
    ap.add_argument("--threshold", type=float, default=0.5,
                    help="seuil en mode auto : plus bas = plus d'intervenants détectés")
    ap.add_argument("--nameFolder", help="range les fichiers dans reunions/<nameFolder>/<n>/ (n = numéro suivant)")
    args = ap.parse_args()

    ac.check_os(args.os)
    if args.list:
        ac.list_devices(args.os); return

    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    folder = output_folder(args.nameFolder)
    if args.file:
        wav = args.file
        name = os.path.splitext(os.path.basename(wav))[0]
        out_dir = folder if args.nameFolder else os.path.dirname(wav)
        out = os.path.join(out_dir, name + "_transcription_intervenants.txt")
        if args.nameFolder:
            shutil.copy2(wav, folder)
    else:
        wav = ac.record(args.os, args.mic, args.audio, os.path.join(folder, stamp))
        out = os.path.join(folder, f"{stamp}_transcription_intervenants.txt")

    transcript = transcribe(wav, args.model, args.speakers, args.threshold)
    open(out, "w", encoding="utf-8").write(transcript)
    print(f"\nTranscription enregistrée dans {out}")

if __name__ == "__main__":
    main()
