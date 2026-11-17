#!/usr/bin/env python3
"""
Transcription de réunion 100 % locale : enregistre l'audio de l'ordi et le transcrit
avec Whisper. Aucun appel à Claude ni à un autre service (hors téléchargement initial
du modèle depuis Hugging Face).

Prérequis :
  pip3 install soundcard soundfile faster-whisper numpy

Usage (Mac par défaut ; ajouter --os windows ou --os debian sinon) :
  python3 script/meeting-whisper.py --list                       # liste les micros et sources de son
  python3 script/meeting-whisper.py                              # micro par défaut + son de l'ordi ; Ctrl+C pour arrêter
  python3 script/meeting-whisper.py --mic "MacBook" --audio none # un micro précis, sans le son de l'ordi
  python3 script/meeting-whisper.py --file reunions/xxx.wav      # transcrit un fichier existant
  HF_HUB_OFFLINE=1 python3 script/meeting-whisper.py             # interdit tout accès réseau
"""
import argparse, datetime, os
import audio_capture as ac

def transcribe(path, model_size):
    from faster_whisper import WhisperModel
    print(f"Transcription locale (whisper {model_size})…")
    model = WhisperModel(model_size, device="auto", compute_type="int8")
    segments, _ = model.transcribe(path, language="fr", vad_filter=True)
    lines = []
    for s in segments:
        ts = str(datetime.timedelta(seconds=int(s.start)))
        line = f"[{ts}] {s.text.strip()}"
        print(line)
        lines.append(line)
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ac.add_args(ap)
    ap.add_argument("--file", help="fichier audio existant à transcrire (pas d'enregistrement)")
    ap.add_argument("--model", default="small", help="tiny/base/small/medium/large-v3")
    args = ap.parse_args()

    ac.check_os(args.os)
    if args.list:
        ac.list_devices(args.os); return

    if args.file:
        wav = args.file
        out = os.path.splitext(wav)[0] + "_transcription.txt"
    else:
        stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
        os.makedirs("reunions", exist_ok=True)
        wav = ac.record(args.os, args.mic, args.audio, os.path.join("reunions", stamp))
        out = os.path.join("reunions", f"{stamp}_transcription.txt")

    transcript = transcribe(wav, args.model)
    open(out, "w", encoding="utf-8").write(transcript)
    print(f"\nTranscription enregistrée dans {out}")

if __name__ == "__main__":
    main()
