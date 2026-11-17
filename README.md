# local-meeting-transcriber

Outils en ligne de commande pour enregistrer une réunion (ta voix + le son de la visio) sur Mac, Windows ou Debian, et en obtenir la transcription **en local**, voire un compte rendu.

| Script | Ce qu'il produit | Claude | Données envoyées |
|---|---|---|---|
| [`script/meeting-whisper.py`](script/meeting-whisper.py) | Transcription horodatée | ❌ | Aucune |
| [`script/meeting-whisper-final.py`](script/meeting-whisper-final.py) | Transcription **avec intervenants** (`Utilisateur 1`, `Utilisateur 2`…) | ❌ | Aucune |
| [`script/meeting-agent.py`](script/meeting-agent.py) | Transcription + **compte rendu** (résumé, décisions, actions, questions) | ✅ | La transcription, envoyée à Anthropic (US) |

Sans compte rendu, utilise **meeting-whisper-final** : tout reste sur le poste.

Architecture détaillée et points de souveraineté : [docs/](docs/)

---

## 1. Installation (une seule fois)

Récupère le projet (remplace `<URL_DU_DEPOT>` par l'adresse du dépôt GitHub, bouton *Code* sur la page du dépôt) :

```bash
git clone <URL_DU_DEPOT>/local-meeting-transcriber.git
cd local-meeting-transcriber
```

Puis installe les dépendances :

```bash
pip3 install --user soundcard sounddevice soundfile faster-whisper numpy sherpa-onnx
```

Le dossier `reunions/` (enregistrements et transcriptions) est exclu de git par le `.gitignore` : **tes réunions ne sont jamais poussées sur GitHub**.

- `sherpa-onnx` n'est nécessaire que pour `meeting-whisper-final.py`.
- Utilise `pip3`, pas `pip` : sur macOS, la commande `pip` n'existe pas par défaut.
- Les messages « script … is not on PATH » à l'installation n'empêchent rien de fonctionner.

Pour `meeting-agent.py` uniquement : installe Claude Code (`npm install -g @anthropic-ai/claude-code`, ou voir la documentation officielle de Claude Code), lance `claude` une fois et connecte-toi **avec le compte de ton entreprise**. Vérifie le compte avec `/status`. Ne définis pas de `ANTHROPIC_API_KEY`.

### Premier lancement

Le premier lancement télécharge les modèles, ce qui prend quelques minutes :
- Whisper depuis Hugging Face (environ 480 Mo pour `small`). L'avertissement « unauthenticated requests to the HF Hub » n'empêche rien de fonctionner.
- Pour `meeting-whisper-final.py` : les modèles de diarisation depuis GitHub (environ 33 Mo).

Ensuite, ajoute `HF_HUB_OFFLINE=1` devant les commandes pour interdire tout accès à Hugging Face.

### Autorisation du micro

À la première utilisation, macOS demande l'accès au micro pour le Terminal ou VS Code. Il faut accepter, sinon l'enregistrement sera silencieux.

---

## 2. Lancer un script : chemin relatif ou absolu

Chaque script peut se lancer de deux façons :

| Forme | Exemple | Quand l'utiliser |
|---|---|---|
| **Relatif** `./script/…` | `python3 ./script/meeting-whisper.py --list` | Après `cd` dans le dossier `local-meeting-transcriber` |
| **Absolu** `<DOSSIER_PARENT>/local-meeting-transcriber/script/…` | `python3 <DOSSIER_PARENT>/local-meeting-transcriber/script/meeting-whisper.py --list` | Depuis n'importe quel dossier |

> **`<DOSSIER_PARENT>`** = le chemin du dossier **qui contient** `local-meeting-transcriber`, par exemple `/Users/<ton-utilisateur>/Downloads`. Remplace-le, chevrons `< >` compris. Pour l'obtenir, glisse le dossier `local-meeting-transcriber` dans le terminal : le chemin complet s'affiche.

> ⚠️ Le dossier `reunions/` est créé **dans le dossier où tu te trouves** au moment du lancement, pas à côté du script. Avec le chemin absolu lancé depuis un autre dossier, les fichiers iront dans `<dossier courant>/reunions/`. Pour les garder au même endroit, fais d'abord `cd <DOSSIER_PARENT>/local-meeting-transcriber`. De même, un chemin passé à `--file` est relatif au dossier courant.

## 3. Choisir son micro

Les exemples suivants utilisent la forme relative, depuis la racine du projet.

```bash
cd <DOSSIER_PARENT>/local-meeting-transcriber
python3 ./script/meeting-whisper-final.py --list
```

Exemple de sortie (le `>` marque l'entrée par défaut de macOS) :
```
  0 iPhone13_Aubin Microphone, Core Audio (1 in, 0 out)
> 1 MacBook Air Microphone, Core Audio (1 in, 0 out)
< 2 MacBook Air Speakers, Core Audio (0 in, 2 out)
```

### Quel micro mettre dans `--device` ?

`--device` désigne toujours un **micro**, c'est-à-dire une entrée audio : ce qui est enregistré. Les haut-parleurs et le casque (sorties) ne sont jamais enregistrés. Le script écoute **un seul** micro, jamais tous à la fois.

**1. Voir le micro utilisé actuellement par défaut :**
```bash
python3 -c "import sounddevice as sd; print(sd.query_devices(kind='input')['name'])"
```
→ `MacBook Air Microphone`

**2. Lister tous les micros disponibles (noms à copier tels quels dans `--device`) :**
```bash
python3 -c "import sounddevice as sd; print('\n'.join(d['name'] for d in sd.query_devices() if d['max_input_channels'] > 0))"
```
→ `MacBook Air Microphone`, `Microsoft Teams Audio`… et `iPhone13_Aubin Microphone` quand l'iPhone est à proximité.

**Comment ça marche :** la bibliothèque `sounddevice` demande à macOS (CoreAudio) la liste de ses périphériques audio.
- `kind='input'` renvoie l'**entrée par défaut**, celle choisie dans *Réglages Système > Son > Entrée*. C'est celle qu'utilise le script quand on ne précise pas `--device`.
- `max_input_channels > 0` ne garde que les périphériques qui **enregistrent**, autrement dit les micros. C'est la colonne `(1 in, …)` de `--list`.

Ces commandes ne font que lire la liste : elles n'enregistrent rien.

**3. Choisir :**

| Ce que tu lances | Micro écouté |
|---|---|
| `--device "MacBook Air Microphone"` | Celui-là. Une partie du nom suffit (`--device "MacBook"`) |
| `--device 1` | Le n° 1 de `--list`. ⚠️ Ce numéro **change** quand un appareil apparaît ou disparaît : l'iPhone, par exemple, n'est listé que lorsqu'il est à proximité |
| sans `--device` | Le micro par défaut de macOS (étape 1) |

→ Passe toujours le **nom**, pas le numéro.

| Micro | Pour une transcription |
|---|---|
| Micro intégré du Mac, micro USB | ✅ Recommandé |
| AirPods / casque Bluetooth | ⚠️ macOS réduit la qualité du son quand leur micro est actif |
| iPhone (Continuité) | ⚠️ Fonctionne, mais disparaît s'il s'éloigne ou se verrouille |
| `Microsoft Teams Audio` | ❌ Périphérique virtuel de Teams, pas un vrai micro |
| `BlackHole` | Son de l'ordinateur (visio), voir plus bas |

**Si l'enregistrement est silencieux** (transcription vide) : active **Terminal** ou **Visual Studio Code** dans *Réglages Système > Confidentialité et sécurité > Microphone*, puis relance le script.

### Prompt prêt à l'emploi (Claude Code, Copilot Chat en mode agent…)

Ouvre ton assistant IA sur le dossier `local-meeting-transcriber` et colle ce texte. L'assistant doit pouvoir lancer des commandes dans le terminal (mode agent) :

```text
Dans ce projet local-meeting-transcriber, trouve le micro à utiliser pour enregistrer une réunion et donne-moi la commande prête à lancer. Ne modifie aucun fichier et n'enregistre rien.

1. Depuis la racine du projet, lance ces commandes (lecture seule) :
   python3 -c "import sounddevice as sd; print(sd.query_devices(kind='input')['name'])"
   python3 -c "import sounddevice as sd; print('\n'.join(d['name'] for d in sd.query_devices() if d['max_input_channels'] > 0))"

2. Réponds avec :
   - le micro utilisé actuellement par défaut (nom exact) ;
   - la liste des micros disponibles, en précisant pour chacun s'il est conseillé pour une transcription :
     micro intégré ou USB = conseillé ; AirPods/Bluetooth = qualité réduite ; iPhone = instable ;
     "Microsoft Teams Audio" = pas un vrai micro ; BlackHole = son de l'ordinateur, pas la voix ;
   - le micro que tu recommandes et pourquoi ;
   - la commande complète, prête à copier, avec le NOM exact du micro recommandé (jamais son numéro) :
     HF_HUB_OFFLINE=1 python3 ./script/meeting-whisper-final.py --device "<nom exact>" --nameFolder <nom-du-projet>

3. Si la liste ne contient aucun micro, dis-moi de vérifier
   Réglages Système > Confidentialité et sécurité > Microphone (Terminal / VS Code).
```

### Capturer le son de la visio

> ⚠️ **Avec un casque, le micro n'entend pas les autres participants.** Pour capturer le son de l'ordinateur, installe BlackHole (`brew install blackhole-2ch`), crée un « périphérique à sorties multiples » (casque + BlackHole) dans *Configuration audio et MIDI* et choisis-le comme sortie son, puis lance le script avec `--device "BlackHole"`.
>
> Pour enregistrer **ta voix et la visio ensemble**, il faut un « périphérique agrégé » (micro + BlackHole). **Les scripts actuels ne le gèrent pas encore** : ils enregistrent en mono et ne gardent que le 1er canal, donc seulement le micro.

---

## 4. `meeting-whisper-final.py`, transcription avec intervenants (recommandé)

### Commandes de lancement

```bash
# Chemin relatif (depuis le dossier local-meeting-transcriber)
cd <DOSSIER_PARENT>/local-meeting-transcriber
HF_HUB_OFFLINE=1 python3 ./script/meeting-whisper-final.py --device "MacBook Air Microphone" --speakers 4 --nameFolder projetX
HF_HUB_OFFLINE=1 python3 ./script/meeting-whisper-final.py --file ./reunions/2026-11-17_1257.wav --speakers 2 --nameFolder projetX

# Chemin absolu (depuis n'importe où)
HF_HUB_OFFLINE=1 python3 <DOSSIER_PARENT>/local-meeting-transcriber/script/meeting-whisper-final.py --device "MacBook Air Microphone" --speakers 4 --nameFolder projetX
HF_HUB_OFFLINE=1 python3 <DOSSIER_PARENT>/local-meeting-transcriber/script/meeting-whisper-final.py --file <DOSSIER_PARENT>/local-meeting-transcriber/reunions/2026-11-17_1257.wav --speakers 2 --nameFolder projetX
```

### Pendant une réunion

1. Lance la commande au début de la réunion.
2. **Ctrl+C** à la fin.
3. Attends le message « Transcription enregistrée dans … ».

Résultat dans `reunions/projetX/1/`, puis `2/`, `3/`… pour les réunions suivantes :

```
[0:00:00] Utilisateur 1 : Bonjour à tous, on commence la réunion sur le budget du projet.
[0:00:06] Utilisateur 2 : Merci. De mon côté, la partie interface est terminée.
```

### Sur un fichier existant (audio ou vidéo)

```bash
HF_HUB_OFFLINE=1 python3 ./script/meeting-whisper-final.py --file ~/Downloads/reunion.mp4 --speakers 3 --nameFolder projetX
```

### Options

| Option | Rôle |
|---|---|
| `--device "<nom>"` | Micro à enregistrer |
| `--file <chemin>` | Transcrit un fichier existant au lieu d'enregistrer. Avec `--nameFolder`, une copie du fichier est rangée dans le dossier |
| `--nameFolder <nom>` | Range les fichiers dans `reunions/<nom>/<n>/`. Un simple nom, sans `/` |
| `--speakers N` | Nombre d'intervenants s'il est connu, **le plus fiable** |
| `--threshold 0.5` | Sans `--speakers` : baisse le seuil (0.4) si deux personnes sont fusionnées, monte-le (0.6) si une personne apparaît en double. Évite les valeurs extrêmes : à 0.1, une voix est coupée en deux |
| `--model small` | `tiny` / `base` / `small` / `medium` / `large-v3`. Plus gros = plus précis, mais plus lent |

**Durée :** compte environ 15 min de calcul pour l'identification des voix sur 1 h de réunion, plus le temps de transcription. Le Mac doit rester allumé.

---

## 5. `meeting-whisper.py`, transcription simple

Même fonctionnement, sans identification des intervenants, donc plus rapide.

```bash
# Chemin relatif (depuis le dossier local-meeting-transcriber)
cd <DOSSIER_PARENT>/local-meeting-transcriber
HF_HUB_OFFLINE=1 python3 ./script/meeting-whisper.py --device "MacBook Air Microphone"     # Ctrl+C pour arrêter
HF_HUB_OFFLINE=1 python3 ./script/meeting-whisper.py --file ./reunions/2026-11-17_1257.wav --model medium

# Chemin absolu (depuis n'importe où)
HF_HUB_OFFLINE=1 python3 <DOSSIER_PARENT>/local-meeting-transcriber/script/meeting-whisper.py --device "MacBook Air Microphone"
HF_HUB_OFFLINE=1 python3 <DOSSIER_PARENT>/local-meeting-transcriber/script/meeting-whisper.py --file <DOSSIER_PARENT>/local-meeting-transcriber/reunions/2026-11-17_1257.wav --model medium
```

Résultat : `reunions/<date>_<heure>_transcription.txt`, ou `<fichier>_transcription.txt` à côté du fichier passé avec `--file`.

Options : `--list`, `--device`, `--file`, `--model`.

---

## 6. `meeting-agent.py`, transcription et compte rendu par Claude

```bash
# Chemin relatif (depuis le dossier local-meeting-transcriber)
cd <DOSSIER_PARENT>/local-meeting-transcriber
python3 ./script/meeting-agent.py --device "MacBook Air Microphone"     # Ctrl+C pour arrêter

# Chemin absolu (depuis n'importe où)
python3 <DOSSIER_PARENT>/local-meeting-transcriber/script/meeting-agent.py --device "MacBook Air Microphone"
```

Après le Ctrl+C, le script transcrit en local, envoie **le texte** à Claude (`claude -p`) et écrit dans `reunions/` :
- `<date>.wav` : l'audio ;
- `<date>_transcription.txt` : la transcription ;
- `<date>_notes.md` : le résumé, les décisions, les actions et les questions ouvertes.

Options : `--list`, `--device`, `--model`.

> ⚠️ Avant de l'utiliser sur une réunion confidentielle, lis [docs/architecture-meeting-agent.md](docs/architecture-meeting-agent.md). La transcription est traitée par Anthropic aux États-Unis, et il faut vérifier que c'est bien le compte de l'entreprise qui est connecté.

---

## 7. Bonnes pratiques

- **Préviens les participants** que la réunion est enregistrée. C'est une obligation RGPD.
- Les fichiers de `reunions/` ne sont ni chiffrés ni purgés automatiquement. Supprime-les quand tu n'en as plus besoin, et ne place pas le projet dans un dossier synchronisé (iCloud, OneDrive).
- Pendant l'enregistrement, laisse le terminal ouvert. Après le Ctrl+C, attends la fin du traitement.

## 8. Erreurs potentielles

Le système se choisit avec `--os mac` (défaut), `--os windows` ou `--os debian`. ✅ = erreur rencontrée et résolue sur un vrai poste. Les sections Windows et Debian n'ont **pas encore été testées sur une vraie machine**.

### 8.1 Mac

**Installation**

| Symptôme | Cause | Solution |
|---|---|---|
| ✅ `zsh: command not found: pip` | Sur macOS, la commande s'appelle `pip3` | `pip3 install --user …` |
| ✅ `brew install pip` → « No available formula with the name "pip" » | pip est livré avec Python, pas séparément | Inutile : utilise `pip3`, ou `brew install python` pour un Python récent |
| ✅ « The script … is installed in '…/bin' which is not on PATH » | Des outils annexes sont installés hors du PATH | Sans conséquence, à ignorer |
| ✅ « You are using pip version 21.2.4 » | pip est ancien | Sans conséquence |
| `error: externally-managed-environment` | Python installé par Homebrew, qui bloque `pip install` global | Crée un environnement virtuel : `python3 -m venv .venv && source .venv/bin/activate` |
| ✅ **BlackHole absent de `--list` après `brew install blackhole-2ch`** | Installation interrompue (souvent à l'étape du mot de passe), ou macOS n'a pas rechargé ses pilotes | 1. Vérifie `brew list --cask \| grep blackhole` → doit afficher `blackhole-2ch`. 2. Vérifie `ls /Library/Audio/Plug-Ins/HAL/` → doit contenir `BlackHole2ch.driver`. Sinon, relance `brew install blackhole-2ch` et tape ton mot de passe (rien ne s'affiche pendant la saisie, c'est normal). 3. Recharge le service audio : `sudo killall coreaudiod`, ou redémarre le Mac |
| `brew install blackhole-2ch` refusé ou bloqué | Mac d'entreprise (MDM) qui interdit les pilotes | Demande l'accord du service informatique |

**Premier lancement**

| Symptôme | Cause | Solution |
|---|---|---|
| ✅ « You are sending unauthenticated requests to the HF Hub » | Téléchargement du modèle Whisper sans compte Hugging Face | Sans conséquence : attends la fin du téléchargement (environ 480 Mo pour `small`) |
| Le téléchargement reste bloqué à 0 % | Le système de téléchargement Xet de Hugging Face est bloqué | Ctrl+C, puis relance avec `HF_HUB_DISABLE_XET=1` devant la commande |
| ✅ `LocalEntryNotFoundError … outgoing traffic has been disabled` | `HF_HUB_OFFLINE=1` alors que ce modèle (`--model`) n'a jamais été téléchargé | Lance une première fois **sans** `HF_HUB_OFFLINE=1` |
| ✅ `RuntimeWarning: … encountered in matmul` / `mel_spec = …` | Avertissement de calcul de numpy | Sans conséquence |
| ✅ « Tip: experimental MPS backend is available » | Simple conseil de ctranslate2 | Sans conséquence |

**Enregistrement**

| Symptôme | Cause | Solution |
|---|---|---|
| ✅ « Aucune source de son de l'ordinateur trouvée : … BlackHole n'est pas installé » | BlackHole absent ou non détecté | Voir la ligne BlackHole ci-dessus, ou `--audio none` pour enregistrer le micro seul |
| ✅ « La piste du son de l'ordinateur est silencieuse » | La sortie son de macOS ne passe pas par BlackHole | Choisis le **périphérique à sorties multiples** (casque + BlackHole) comme sortie son |
| Tu n'entends plus la visio | Sortie son réglée sur BlackHole **seul** | Choisis le périphérique à sorties multiples, pas BlackHole directement |
| Transcription vide, micro silencieux | macOS bloque l'accès au micro | *Réglages Système > Confidentialité et sécurité > Microphone* : active Terminal ou VS Code |
| ✅ « Périphérique « … » introuvable » | Nom mal écrit | `--list` et copie le nom exact (une partie du nom suffit) |
| ✅ Le mauvais micro est enregistré avec `--mic 1` | Les numéros changent (l'iPhone apparaît ou disparaît) | Utilise le **nom** : `--mic "MacBook Air Microphone"` |
| ✅ « Système détecté : mac, mais --os vaut … » | Mauvais `--os` | Retire `--os`, ou mets `--os mac` |
| ✅ « macOS does not support loopback recording functionality » | `--os windows` ou `--os debian` lancé sur un Mac | Utilise `--os mac` |
| Son dégradé avec AirPods / casque Bluetooth | macOS bascule en mode « appel » quand leur micro est actif | Utilise le micro du Mac : `--mic "MacBook Air Microphone"` |
| `Commande « claude » introuvable` (meeting-agent) | Claude Code n'est pas installé ou pas dans le PATH | Installe Claude Code, puis vérifie avec `which claude` |

### 8.2 Windows

Commandes : `py` au lieu de `python3`, `.\script\…` au lieu de `./script/…`, et en PowerShell `$env:HF_HUB_OFFLINE=1; py .\script\…` au lieu de `HF_HUB_OFFLINE=1 python3 …`.

**Installation**

| Symptôme | Cause | Solution |
|---|---|---|
| `python3` ouvre le Microsoft Store, ou « Python est introuvable » | Python n'est pas installé, ou seul le raccourci du Store existe | Installe Python depuis python.org en cochant **« Add python.exe to PATH »**, puis utilise `py` |
| `pip` introuvable | pip n'est pas dans le PATH | `py -m pip install soundcard soundfile faster-whisper numpy sherpa-onnx` |
| Activation de `.venv\Scripts\Activate.ps1` refusée (« l'exécution de scripts est désactivée ») | Stratégie d'exécution de PowerShell | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, ou utilise `cmd` |
| Erreur de DLL au chargement de faster-whisper / ctranslate2 / onnxruntime | Il manque les bibliothèques Microsoft Visual C++ | Installe le **Microsoft Visual C++ Redistributable** (x64) |
| Avertissement Hugging Face sur les « symlinks » / le « Developer Mode » | Windows limite les liens symboliques | Sans conséquence : le cache prend juste un peu plus de place |
| BlackHole introuvable | BlackHole n'existe que sur Mac | Inutile sous Windows : le son de l'ordinateur est capté nativement (loopback) |

**Enregistrement**

| Symptôme | Cause | Solution |
|---|---|---|
| Transcription vide, micro silencieux | Windows bloque l'accès au micro | *Paramètres > Confidentialité et sécurité > Microphone* : active **« Autoriser les applications de bureau à accéder à votre microphone »** |
| « Système détecté : windows, mais --os vaut « mac » » + pas de son de la visio | `--os` oublié : le défaut est `mac` | Ajoute `--os windows` |
| « La piste du son de l'ordinateur est silencieuse » | Teams / Zoom joue sur une autre sortie que la sortie par défaut de Windows | Règle la même sortie dans Teams/Zoom et dans Windows, ou passe-la à `--audio "<nom de la sortie>"` (voir `--list --os windows`) |
| Erreur d'ouverture du périphérique ou piste vide alors qu'une application utilise le son | Une application a pris le contrôle **exclusif** du périphérique | *Panneau de configuration Son > Propriétés du périphérique > Avancé* : décoche « Autoriser les applications à prendre le contrôle exclusif » |
| Ctrl+C n'arrête pas l'enregistrement | Terminal particulier | Essaie Ctrl+Pause, ou lance depuis Windows Terminal / PowerShell |
| Accents illisibles dans la console | Ancienne console en page de code non UTF-8 | Utilise Windows Terminal, ou tape `chcp 65001` avant de lancer. Les fichiers `.txt` sont écrits en UTF-8 quoi qu'il arrive |
| Son dégradé avec un casque Bluetooth | Mode « mains libres » activé quand son micro est utilisé | Utilise un autre micro avec `--mic` |
| `Commande « claude » introuvable` (meeting-agent) | Le dossier global de npm n'est pas dans le PATH | Vérifie `where claude`. Ajoute `%AppData%\npm` au PATH si besoin |

### 8.3 Debian (et dérivés : Ubuntu…)

Commandes identiques à Mac (`python3`, `./script/…`, `HF_HUB_OFFLINE=1 python3 …`), avec `--os debian`.

**Installation**

| Symptôme | Cause | Solution |
|---|---|---|
| `error: externally-managed-environment` avec `pip install` | Debian 12+ interdit `pip install` hors environnement virtuel (PEP 668) | `sudo apt install python3-venv python3-pip`, puis `python3 -m venv .venv && source .venv/bin/activate && pip install soundcard soundfile faster-whisper numpy sherpa-onnx`. Réactive avec `source .venv/bin/activate` à chaque nouveau terminal |
| `OSError: cannot load library 'libpulse.so.0'` | `soundcard` a besoin de la bibliothèque PulseAudio | `sudo apt install libpulse0`. Avec PipeWire : `sudo apt install pipewire-pulse` |
| `OSError: sndfile library not found` | `libsndfile` absent | `sudo apt install libsndfile1` |
| `npm install -g` refusé, ou Claude Code qui ne démarre pas (meeting-agent) | Version de Node.js trop ancienne dans les dépôts Debian, ou droits d'écriture | Installe une version récente de Node.js (dépôt officiel Node.js) ou l'installeur officiel de Claude Code. N'utilise pas `sudo npm` |
| BlackHole introuvable | BlackHole n'existe que sur Mac | Inutile : le son de l'ordinateur est capté via la source « monitor » |

**Enregistrement**

| Symptôme | Cause | Solution |
|---|---|---|
| `--list --os debian` n'affiche aucune source de son de l'ordinateur | Pas de serveur son PulseAudio/PipeWire (serveur sans interface graphique, session SSH, ALSA seul) | Installe et démarre PipeWire (`pipewire-pulse`) ou PulseAudio. Vérifie avec `pactl list short sources` : une source finissant par `.monitor` doit apparaître |
| « La piste du son de l'ordinateur est silencieuse » | Le son de la visio sort sur une autre sortie que la sortie par défaut | `pactl get-default-sink` pour voir la sortie par défaut. Règle-la dans les paramètres son, ou passe le bon « Monitor of … » à `--audio` |
| Aucun micro ou erreur d'accès | Script lancé avec `sudo`, qui n'a pas accès à la session son de l'utilisateur | Lance le script **sans** `sudo` |
| Micro muet | Micro coupé ou volume à 0 dans le mixeur | `pavucontrol` (`sudo apt install pavucontrol`), onglet *Périphériques d'entrée* |
| « Système détecté : debian, mais --os vaut « mac » » | `--os` oublié | Ajoute `--os debian` |

## Structure

```
local-meeting-transcriber/
├── README.md
├── .gitignore               # exclut reunions/, l'audio, les transcriptions, .venv…
├── script/
│   ├── audio_capture.py         # module commun : micro + son de l'ordinateur (mac/windows/debian)
│   ├── meeting-agent.py
│   ├── meeting-whisper.py
│   └── meeting-whisper-final.py
├── docs/
│   ├── architecture-meeting-agent.md
│   ├── architecture-meeting-whisper.md
│   └── architecture-meeting-whisper-final.md
└── reunions/            # créé automatiquement : audio et transcriptions
```
