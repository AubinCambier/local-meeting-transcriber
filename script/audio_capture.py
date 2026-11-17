"""
Capture audio commune aux scripts meeting-* : micro (ta voix) + son de l'ordinateur (la visio),
sur Mac, Windows ou Debian.

Son de l'ordinateur selon --os :
  mac      -> BlackHole (pilote à installer, macOS ne sait pas capter le son du système seul)
  windows  -> loopback WASAPI des haut-parleurs par défaut (natif)
  debian   -> source « monitor » PulseAudio/PipeWire de la sortie par défaut (natif)

Les deux sources sont enregistrées en parallèle dans <base>_micro.wav et <base>_audio.wav,
puis mélangées dans <base>.wav (le fichier transcrit).
"""
import platform, sys, threading, warnings
import numpy as np
import soundcard as sc
import soundfile as sf

RATE = 48000          # fréquence native de la plupart des cartes son ; Whisper rééchantillonne à la lecture
BLOCK = RATE // 10    # blocs de 100 ms
SYSTEMS = ("mac", "windows", "debian")

def add_args(ap):
    """Options audio communes aux 3 scripts."""
    ap.add_argument("--os", choices=SYSTEMS, default="mac",
                    help="système utilisé : décide comment capter le son de l'ordinateur (défaut : mac)")
    ap.add_argument("--mic", "--device", dest="mic",
                    help="micro (nom ou numéro de --list) ; défaut : micro par défaut du système")
    ap.add_argument("--audio", help="source du son de l'ordinateur (nom), ou 'none' ; défaut : selon --os")
    ap.add_argument("--list", action="store_true", help="liste les micros et sources de son de l'ordinateur")

def detected_os():
    return {"Darwin": "mac", "Windows": "windows", "Linux": "debian"}.get(platform.system(), "?")

def check_os(os_name):
    real = detected_os()
    if real != os_name:
        print(f"⚠️  Système détecté : {real}, mais --os vaut « {os_name} ». "
              f"Ajoute --os {real} si le son de l'ordinateur n'est pas capté.", file=sys.stderr)

def microphones():
    """Vrais micros (hors BlackHole et hors sources loopback)."""
    return [m for m in sc.all_microphones() if "blackhole" not in m.name.lower()]

def system_sources(os_name):
    if os_name == "mac":
        return [m for m in sc.all_microphones() if "blackhole" in m.name.lower()]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return [m for m in sc.all_microphones(include_loopback=True) if m.isloopback]

def default_system_source(os_name):
    if os_name == "mac":
        found = system_sources("mac")
        return found[0] if found else None
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return sc.get_microphone(sc.default_speaker().name, include_loopback=True)

def list_devices(os_name):
    default_mic = sc.default_microphone().name
    print("Micros (--mic) :")
    for i, m in enumerate(microphones()):
        mark = "  ← par défaut" if m.name == default_mic else ""
        print(f"  {i}  {m.name}{mark}")
    print(f"\nSon de l'ordinateur (--audio), pour --os {os_name} :")
    try:
        default = default_system_source(os_name)
    except Exception:
        default = None
    sources = system_sources(os_name)
    for m in sources:
        mark = "  ← par défaut" if default and m.name == default.name else ""
        print(f"     {m.name}{mark}")
    if not sources:
        hint = "installe BlackHole (voir README)" if os_name == "mac" else "aucune source trouvée"
        print(f"     (aucune : {hint})")

def _find(name, loopback=False):
    if name.isdigit():
        mics = microphones()
        if int(name) >= len(mics):
            sys.exit(f"Micro n° {name} introuvable. Lance --list pour voir les micros.")
        return mics[int(name)]
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return sc.get_microphone(name, include_loopback=loopback)
    except IndexError:
        sys.exit(f"Périphérique « {name} » introuvable. Lance --list pour voir les noms disponibles.")

def resolve(os_name, mic_name, audio_name):
    mic = _find(mic_name) if mic_name else sc.default_microphone()
    if audio_name and audio_name.lower() == "none":
        audio = None
    elif audio_name:
        audio = _find(audio_name, loopback=os_name != "mac")
    else:
        try:
            audio = default_system_source(os_name)
        except Exception:
            audio = None
        if audio is None:
            print("⚠️  Aucune source de son de l'ordinateur trouvée : seul le micro sera enregistré"
                  + (" (BlackHole n'est pas installé)." if os_name == "mac" else "."), file=sys.stderr)
    return mic, audio

def _capture(dev, path, stop, errors):
    try:
        with sf.SoundFile(path, "w", RATE, 1) as f, dev.recorder(samplerate=RATE) as r:
            while not stop.is_set():
                f.write(r.record(numframes=BLOCK).mean(axis=1))
    except Exception as e:
        errors.append(f"{dev.name} : {e}")
        stop.set()

def record(os_name, mic_name, audio_name, base):
    """Enregistre jusqu'au Ctrl+C et renvoie le chemin du .wav à transcrire."""
    mic, audio = resolve(os_name, mic_name, audio_name)
    tracks = [(mic, f"{base}_micro.wav" if audio else f"{base}.wav")]
    if audio:
        tracks.append((audio, f"{base}_audio.wav"))

    stop, errors = threading.Event(), []
    threads = [threading.Thread(target=_capture, args=(d, p, stop, errors), daemon=True) for d, p in tracks]
    print(f"Enregistrement — micro : « {mic.name} »"
          + (f" + son de l'ordinateur : « {audio.name} »" if audio else "") + "… Ctrl+C pour arrêter.")
    for t in threads:
        t.start()
    try:
        # join avec délai : sinon Ctrl+C n'interrompt pas l'attente sous Windows
        while not stop.is_set():
            threads[0].join(timeout=0.5)
    except KeyboardInterrupt:
        print("\nArrêt de l'enregistrement.")
    stop.set()
    for t in threads:
        t.join()
    if errors:
        sys.exit("Erreur d'enregistrement : " + " ; ".join(errors))

    if not audio:
        return f"{base}.wav"
    voice, _ = sf.read(tracks[0][1], dtype="float32")
    system, _ = sf.read(tracks[1][1], dtype="float32")
    if len(system) == 0 or np.sqrt(np.mean(system ** 2)) < 1e-4:
        print("⚠️  La piste du son de l'ordinateur est silencieuse : la sortie son passe-t-elle bien par "
              + ("le périphérique à sorties multiples (BlackHole) ?" if os_name == "mac" else "les haut-parleurs par défaut ?"),
              file=sys.stderr)
    n = max(len(voice), len(system))
    mix = np.pad(voice, (0, n - len(voice))) + np.pad(system, (0, n - len(system)))
    mix /= max(1.0, float(np.abs(mix).max()))  # évite la saturation
    sf.write(f"{base}.wav", mix, RATE)
    return f"{base}.wav"
