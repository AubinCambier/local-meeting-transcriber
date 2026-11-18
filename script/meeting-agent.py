#!/usr/bin/env python3
"""
Mini "Granola" perso : enregistre l'audio de l'ordi, transcrit en local (Whisper),
puis fait résumer par Claude via Claude Code (`claude -p`), donc sur ton abonnement Pro.

Prérequis :
  pip3 install soundcard soundfile faster-whisper numpy
  npm install -g @anthropic-ai/claude-code   puis `claude` une fois et se connecter avec son compte Pro
  -> NE PAS définir ANTHROPIC_API_KEY, sinon c'est facturé à l'API.

Usage (Mac par défaut ; ajouter --os windows ou --os debian sinon) :
  python3 script/meeting-agent.py --list                        # liste les micros et sources de son
  python3 script/meeting-agent.py                               # micro par défaut + son de l'ordi ; Ctrl+C
  python3 script/meeting-agent.py --mic "MacBook" --audio none  # un micro précis, sans le son de l'ordi
"""
import argparse, datetime, os, shutil, subprocess, sys
import audio_capture as ac

PROMPT = """Tu es mon assistant de prise de notes de réunion.
Voici la transcription brute (peut contenir des erreurs de reconnaissance).
Produis en français, en Markdown :
1. Un résumé en 50 lignes max
2. Les décisions prises
3. Les actions à faire (qui / quoi / quand si mentionné)
4. Les questions restées ouvertes
"""

def transcribe(path, model_size):
    from faster_whisper import WhisperModel
    print(f"Transcription locale (whisper {model_size})…")
    model = WhisperModel(model_size, device="auto", compute_type="int8")
    segments, _ = model.transcribe(path, language="fr", vad_filter=True)
    lines = []
    for s in segments:
        ts = str(datetime.timedelta(seconds=int(s.start)))
        lines.append(f"[{ts}] {s.text.strip()}")
    return "\n".join(lines)

def summarize(transcript):
    env = dict(os.environ)
    env.pop("ANTHROPIC_API_KEY", None)  # force l'usage de l'abonnement
    print("Résumé par Claude (claude -p)…")
    claude = shutil.which("claude")  # sous Windows (npm), la commande est claude.cmd
    if not claude:
        sys.exit("Commande « claude » introuvable : installe Claude Code "
                 "(voir docs/config-mac.md étape 13, config-windows.md ou config-debian.md étape 11).")
    r = subprocess.run([claude, "-p", PROMPT], input=transcript,
                       capture_output=True, text=True, encoding="utf-8", env=env)
    if r.returncode != 0:
        sys.exit(f"Erreur claude : {r.stderr}")
    return r.stdout

def main():
    ap = argparse.ArgumentParser()
    ac.add_args(ap)
    ap.add_argument("--model", default="small", help="tiny/base/small/medium/large-v3")
    args = ap.parse_args()

    ac.check_os(args.os)
    if args.list:
        ac.list_devices(args.os); return

    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    os.makedirs("reunions", exist_ok=True)

    wav = ac.record(args.os, args.mic, args.audio, os.path.join("reunions", stamp))
    transcript = transcribe(wav, args.model)
    open(f"reunions/{stamp}_transcription.txt", "w", encoding="utf-8").write(transcript)
    notes = summarize(transcript)
    open(f"reunions/{stamp}_notes.md", "w", encoding="utf-8").write(notes)
    print(notes)
    print(f"\nFichiers enregistrés dans reunions/{stamp}_*")

if __name__ == "__main__":
    main()
