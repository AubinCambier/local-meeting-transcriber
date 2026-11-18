# Guide Debian 🐧 : installer et utiliser local-meeting-transcriber

> **Tu es au bon endroit si** ton ordinateur est sous **Debian 12 ou plus récent**, ou une distribution dérivée (**Ubuntu 22.04+**, Linux Mint…), **avec une interface graphique** (bureau GNOME, KDE…).
> Sur Mac : [config-mac.md](config-mac.md). Sous Windows : [config-windows.md](config-windows.md).
>
> **Avant de commencer**, tu dois avoir fait l'**étape 1 du [README](../README.md#4-étape-1--récupérer-le-projet)** : récupérer le projet dans un dossier nommé `local-meeting-transcriber`.

> 🧪 **À savoir :** la version Debian est écrite et documentée, mais **elle n'a pas encore été testée sur une vraie machine Debian**. Si une étape ne se passe pas comme décrit, note le message exact et signale-le, pour qu'on complète ce guide.

Suis les étapes **dans l'ordre**. Chaque étape indique **quoi faire**, **comment vérifier que ça a marché**, et donne un **prompt pour un assistant IA** si tu veux de l'aide. Tu préfères qu'un agent fasse tout avec toi ? Va directement au [prompt global](#prompt-global--lagent-fait-tout-avec-toi), en bas de page.

## Les 3 différences à retenir sous Debian

| Sur Mac | **Sous Debian** |
|---|---|
| `pip3 install --user …` | Debian l'interdit : on utilise un **environnement virtuel** (`.venv`), à **activer dans chaque nouveau terminal** avec `source .venv/bin/activate` |
| (rien) | **Ajoute toujours `--os debian`** à tes commandes. Sans ça, l'outil se croit sur Mac et **ne capte pas le son de la visio** |
| BlackHole | **Rien à installer** : le son de l'ordinateur est capté par la source « monitor » de PipeWire/PulseAudio |

> ⚠️ **Ne lance jamais les scripts avec `sudo`** : ils n'auraient plus accès à ton micro ni à ton son. `sudo` ne sert que pour `apt install`.

## Le parcours en un coup d'œil

| # | Étape | Une seule fois ? | Durée |
|---|---|---|---|
| 1 | [Ouvrir un terminal](#étape-1--ouvrir-un-terminal) | À chaque utilisation | 1 min |
| 2 | [Installer les paquets système](#étape-2--installer-les-paquets-système) | ✅ Une fois | 3 min |
| 3 | [Aller dans le dossier du projet](#étape-3--aller-dans-le-dossier-du-projet) | À chaque utilisation | 1 min |
| 4 | [Créer l'environnement virtuel et installer les bibliothèques](#étape-4--créer-lenvironnement-virtuel-et-installer-les-bibliothèques) | ✅ Une fois | 5 min |
| 5 | [Activer l'environnement virtuel](#étape-5--activer-lenvironnement-virtuel) | ⚠️ **À chaque nouveau terminal** | 10 s |
| 6 | [Vérifier le son de l'ordinateur](#étape-6--vérifier-le-son-de-lordinateur-la-visio) | ✅ Une fois | 2 min |
| 7 | [Choisir son micro](#étape-7--choisir-son-micro) | ✅ Une fois | 2 min |
| 8 | [Premier essai](#étape-8--premier-essai-30-secondes) | ✅ Une fois | 10 min |
| 9 | [Utilisation pour une vraie réunion](#étape-9--utilisation-pour-une-vraie-réunion) | À chaque réunion | — |
| 10 | [Après la réunion](#étape-10--après-la-réunion) | À chaque réunion | 1 min |
| 11 | [*(Optionnel)* Compte rendu par Claude](#étape-11-optionnel--compte-rendu-par-claude) | ✅ Une fois | 10 min |

**Comment lire les commandes de cette page :**
- Un bloc gris = **une commande à copier**. Colle-la dans le terminal avec **Ctrl + Maj + V** (et non Ctrl + V), puis appuie sur **Entrée**.
- Ne copie pas le début de ligne `marie@pc:~$` : il fait partie de l'invite, pas de la commande.
- Remplace tout ce qui est entre `< >` (par exemple `<DOSSIER_DU_PROJET>`), **en retirant les `< >`**.

---

## Étape 1 : ouvrir un terminal

1. Appuie sur la touche **Super** (la touche avec le logo Windows), ou ouvre le menu des applications.
2. Tape **`Terminal`**, puis appuie sur **Entrée**. *(Raccourci sur beaucoup de systèmes : **Ctrl + Alt + T**.)*
3. Une fenêtre s'ouvre avec une ligne du type **`marie@pc:~$`** : c'est ici que tu tapes les commandes.

*Alternative :* dans **VS Code**, menu *Terminal > Nouveau terminal*.

✅ **Vérification :** tu vois une ligne qui se termine par `$`.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Debian (ou Ubuntu) et je débute avec le terminal. Explique-moi, étape par étape, comment ouvrir un terminal
(touche Super puis « Terminal », Ctrl + Alt + T, ou VS Code > Terminal > Nouveau terminal), comment y coller une commande
(Ctrl + Maj + V) et la valider, et ce que signifie le « $ » en fin d'invite. Ne lance aucune commande.
```

---

## Étape 2 : installer les paquets système

Ces paquets fournissent Python, l'outil de création d'environnement virtuel et les bibliothèques audio.

```bash
sudo apt update && sudo apt install -y python3 python3-venv python3-pip libpulse0 libsndfile1 pulseaudio-utils
```
Le terminal demande **ton mot de passe** : tape-le (rien ne s'affiche pendant la saisie, c'est normal), puis **Entrée**.

> ℹ️ `pulseaudio-utils` fournit seulement la commande `pactl` (pour vérifier le son). Il ne remplace pas PipeWire si ton système l'utilise.

✅ **Vérification :**
```bash
python3 --version
```
Tu dois voir `Python 3.11.x` (Debian 12) ou un numéro **≥ 3.9**.

Puis vérifie que le serveur son fonctionne :
```bash
pactl info
```
Tu dois voir une ligne **`Nom du serveur`** (ou `Server Name`) contenant **`PulseAudio`**, par exemple `PulseAudio (on PipeWire 0.3.65)`. Si tu vois **`Connection failure`**, consulte les [erreurs possibles](#erreurs-possibles-sous-debian).

> ⚠️ Si `sudo` répond `marie n'apparaît pas dans le fichier sudoers` : tu n'as pas les droits d'administration. Demande à ton service informatique d'installer ces paquets.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Debian (ou Ubuntu). Vérifie si Python 3.9+ (`python3 --version`), le module venv (`python3 -m venv --help`)
et le serveur son (`pactl info`) sont disponibles. S'il manque quelque chose, donne-moi la commande
`sudo apt update && sudo apt install -y python3 python3-venv python3-pip libpulse0 libsndfile1 pulseaudio-utils`
à lancer moi-même (elle demande mon mot de passe), puis refais la vérification quand je te le dis.
```

---

## Étape 3 : aller dans le dossier du projet

1. Tape **`cd `** (c, d, puis **un espace**). **N'appuie pas encore sur Entrée.**
2. Dans le gestionnaire de fichiers, **fais glisser le dossier `local-meeting-transcriber`** dans la fenêtre du terminal : son chemin s'écrit tout seul.
   *(Ou tape le chemin, par exemple `~/Documents/local-meeting-transcriber`.)*
3. Appuie sur **Entrée**.

Ça donne par exemple :
```bash
cd /home/marie/Documents/local-meeting-transcriber
```

✅ **Vérification :**
```bash
ls
```
Tu dois voir au moins **`README.md`**, **`docs`** et **`script`**. Sinon, tu es dans le mauvais dossier. Souvent, le ZIP a créé un dossier « en trop » : fais `cd local-meeting-transcriber-main` ou `cd local-meeting-transcriber`, puis `ls`.

> 📝 Ce chemin, c'est ton **`<DOSSIER_DU_PROJET>`**. Pour l'afficher à tout moment : `pwd`.
>
> ⚠️ **À refaire à chaque nouveau terminal.** Les enregistrements sont créés dans le dossier où se trouve le terminal.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Debian. Vérifie que le terminal est dans le dossier du projet local-meeting-transcriber : lance `pwd` puis `ls`,
et confirme que README.md, docs et script sont présents. Sinon, aide-moi à trouver le bon dossier et donne-moi la commande
`cd` exacte. Ne modifie aucun fichier.
```

---

## Étape 4 : créer l'environnement virtuel et installer les bibliothèques

Debian interdit d'installer des bibliothèques Python « pour tout le système » (erreur `externally-managed-environment`). On crée donc un **environnement virtuel** : un dossier `.venv` **à l'intérieur du projet**, qui contient ses propres bibliothèques. Il est déjà exclu de git.

Depuis le dossier du projet (étape 3), lance ces 3 commandes **une par une** :

```bash
python3 -m venv .venv
```
```bash
source .venv/bin/activate
```
```bash
pip install soundcard soundfile faster-whisper numpy sherpa-onnx
```

- Après la 2ᵉ commande, le début de ta ligne affiche **`(.venv)`** : l'environnement est actif.
- La 3ᵉ commande télécharge et installe les outils d'enregistrement et de transcription. Compte quelques minutes, beaucoup de lignes défilent : c'est normal.
- Dans l'environnement virtuel, `pip` (sans 3) est correct.

✅ **Vérification :** l'avant-dernière ligne commence par **`Successfully installed`**. Puis lance :
```bash
python3 -c "import soundcard, soundfile, faster_whisper, numpy, sherpa_onnx; print('Tout est installé')"
```
Tu dois voir **`Tout est installé`**.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Debian, dans le dossier local-meeting-transcriber. Crée un environnement virtuel et installe les dépendances
en suivant l'étape 4 de docs/config-debian.md : `python3 -m venv .venv`, `source .venv/bin/activate`, puis
`pip install soundcard soundfile faster-whisper numpy sherpa-onnx` (demande-moi mon accord avant).
Vérifie ensuite avec `python3 -c "import soundcard, soundfile, faster_whisper, numpy, sherpa_onnx; print('Tout est installé')"`.
N'utilise jamais sudo avec pip. En cas d'erreur, consulte « Erreurs possibles sous Debian ».
```

---

## Étape 5 : activer l'environnement virtuel

> ⚠️ **C'est l'oubli le plus fréquent sous Debian.** L'environnement virtuel ne reste actif que **dans le terminal où tu l'as activé**. À **chaque nouveau terminal**, refais :

```bash
cd <DOSSIER_DU_PROJET>
source .venv/bin/activate
```

✅ **Vérification :** ta ligne commence par **`(.venv)`**. Si tu l'oublies, les scripts affichent `ModuleNotFoundError: No module named 'soundcard'`.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Debian. J'ai l'erreur « ModuleNotFoundError: No module named ... » en lançant un script de local-meeting-transcriber.
Vérifie si l'environnement virtuel .venv du projet existe et s'il est activé (`echo $VIRTUAL_ENV`), puis donne-moi
les commandes exactes pour l'activer (étape 5 de docs/config-debian.md).
```

---

## Étape 6 : vérifier le son de l'ordinateur (la visio)

**Rien à installer.** Sous Debian, chaque sortie son a une source « **monitor** » qui permet d'enregistrer ce qu'elle joue. L'outil enregistre automatiquement le monitor de la **sortie son par défaut**. Il faut juste que la visio sorte bien **par cette sortie**.

1. Ouvre **Paramètres > Son**.
2. Dans **Sortie**, choisis le casque ou les haut-parleurs sur lesquels **tu écoutes tes visios**.
3. Dans ton application de visio (Teams, Zoom, Meet dans le navigateur…), règle le **haut-parleur** sur **le même appareil** ou sur **« Par défaut »**.

✅ **Vérification** (dans le dossier du projet, `.venv` actif) :
```bash
python3 ./script/meeting-whisper-final.py --os debian --list
```
En bas, sous **`Son de l'ordinateur (--audio), pour --os debian :`**, une ligne **`Monitor of …`** doit apparaître avec **`← par défaut`**.

*Vérification complémentaire :*
```bash
pactl get-default-sink
pactl list short sources | grep monitor
```
La première commande affiche ta sortie par défaut. La seconde doit afficher une ligne qui finit par **`.monitor`** pour cette sortie.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Debian, dans le dossier local-meeting-transcriber, avec le .venv activé. Lance
`python3 ./script/meeting-whisper-final.py --os debian --list`, `pactl get-default-sink` et
`pactl list short sources | grep monitor` (lecture seule). Dis-moi quelle sortie sera enregistrée comme « son de
l'ordinateur », et rappelle-moi que ma visio doit sortir par cette même sortie (étape 6 de docs/config-debian.md).
```

---

## Étape 7 : choisir son micro

Dans le dossier du projet, `.venv` actif :
```bash
python3 ./script/meeting-whisper-final.py --os debian --list
```

Exemple de résultat :
```
Micros (--mic) :
  0  Built-in Audio Analog Stereo  ← par défaut
  1  Jabra Evolve2 65 Mono

Son de l'ordinateur (--audio), pour --os debian :
     Monitor of Built-in Audio Analog Stereo  ← par défaut
```

**Comment lire ce résultat :**
- **Micros** : ce qui peut capter **ta voix**. `← par défaut` indique celui qui sera utilisé si tu ne précises rien (le micro choisi dans *Paramètres > Son > Entrée*).
- **Son de l'ordinateur** : les sources « Monitor of … », c'est-à-dire ce que joue chaque sortie.

**Quel micro choisir ?**

| Micro | Pour une transcription |
|---|---|
| Micro intégré (« Built-in Audio »…), micro USB, micro de casque filaire ou USB | ✅ **Recommandé** |
| Casque Bluetooth | ⚠️ Qualité réduite quand son micro est utilisé (profil « HSP/HFP »). Préfère le micro de l'ordinateur |
| « Monitor of … » | ❌ Ce n'est pas un micro : c'est le son de l'ordinateur |

**Utilise toujours le nom du micro, jamais son numéro.** Une partie du nom suffit :
```bash
--mic "Built-in Audio"
```

Si le micro est muet ou trop faible : installe **`pavucontrol`** (`sudo apt install pavucontrol`), lance-le, et vérifie l'onglet *Périphériques d'entrée* (pas de micro coupé, volume suffisant).

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Debian, dans le dossier local-meeting-transcriber, avec le .venv activé. Lance
`python3 ./script/meeting-whisper-final.py --os debian --list` (lecture seule). Puis dis-moi :
- le micro utilisé par défaut ;
- pour chaque micro, s'il est conseillé (intégré, USB ou filaire = conseillé ; Bluetooth = qualité réduite ;
  « Monitor of » = pas un micro) ;
- quelle source sera enregistrée comme son de l'ordinateur ;
- l'option exacte à utiliser : --mic "<nom exact>".
```

---

## Étape 8 : premier essai (30 secondes)

Ce premier essai **télécharge les modèles** (~500 Mo, une seule fois) et vérifie que **ta voix et le son de l'ordinateur** sont bien enregistrés.

1. Ouvre une vidéo YouTube avec quelqu'un qui parle, **en pause**, sur la sortie choisie à l'étape 6.
2. Dans le terminal (dossier du projet, **`(.venv)` visible**), lance (remplace le nom du micro par le tien, étape 7) :
   ```bash
   python3 ./script/meeting-whisper-final.py --os debian --mic "Built-in Audio" --nameFolder essai
   ```
   *(Réunions en présentiel uniquement : ajoute `--audio none` à la fin.)*
3. Quand tu vois **`Enregistrement — micro : « … » + son de l'ordinateur : « Monitor of … »… Ctrl+C pour arrêter.`** :
   - lance la vidéo ;
   - parle aussi un peu toi-même (« Ceci est un test du micro »).
4. Au bout de 30 secondes, clique dans le terminal et appuie sur **Ctrl + C**.
5. **Attends** : le premier lancement télécharge les modèles (plusieurs minutes). Tu verras passer :
   - `Identification des intervenants (sherpa-onnx)…`
   - `Transcription locale (whisper small)…`
   - puis les lignes de transcription.
6. C'est fini quand tu vois **`Transcription enregistrée dans reunions/essai/1/…`**.

**Messages normaux, à ignorer :** `You are sending unauthenticated requests to the HF Hub`, `RuntimeWarning: … encountered in matmul`.

✅ **Vérification :**
- la transcription contient **ta phrase** et **des phrases de la vidéo** ;
- le dossier contient 4 fichiers (`….wav`, `…_micro.wav`, `…_audio.wav`, `…_transcription_intervenants.txt`). Ouvre-le avec :
  ```bash
  xdg-open reunions/essai/1
  ```

| Problème | Cause probable |
|---|---|
| `ModuleNotFoundError` | `.venv` non activé (étape 5) |
| Ta voix manque | Mauvais micro ou micro coupé (étape 7, `pavucontrol`) |
| La vidéo manque + message « piste du son de l'ordinateur est silencieuse » | La vidéo ne sort pas par la sortie par défaut (étape 6) |
| Message « Système détecté : debian, mais --os vaut « mac » » | Tu as oublié `--os debian` |

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Debian, dans le dossier local-meeting-transcriber. Je viens de faire le premier essai de l'étape 8
de docs/config-debian.md avec :
python3 ./script/meeting-whisper-final.py --os debian --mic "<mon micro>" --nameFolder essai
Voici ce que le terminal a affiché : <colle ici la sortie>
Analyse le résultat : ma voix et le son de l'ordinateur ont-ils été enregistrés ? Si non, trouve la cause avec le tableau
de l'étape 8 et la section « Erreurs possibles sous Debian », et dis-moi précisément quoi corriger.
Tu peux lister reunions/essai/ mais n'ouvre pas les fichiers audio ou texte sans mon accord.
```

---

## Étape 9 : utilisation pour une vraie réunion

### Avant la réunion (checklist)

1. ☐ **Préviens les participants** que la réunion est enregistrée (obligation RGPD).
2. ☐ **Visio :** la sortie son par défaut est l'appareil que tu écoutes, et c'est le même dans la visio (étape 6).
3. ☐ Ouvre un terminal, puis : `cd <DOSSIER_DU_PROJET>` et `source .venv/bin/activate` (**`(.venv)` visible**).
4. ☐ Lance la commande **au début** de la réunion.

### Les commandes

Toutes les commandes se lancent **depuis `<DOSSIER_DU_PROJET>`**, **`.venv` actif**, **avec `--os debian`**.

**Transcription avec intervenants (recommandé) :**
```bash
HF_HUB_OFFLINE=1 python3 ./script/meeting-whisper-final.py --os debian --mic "Built-in Audio" --speakers 4 --nameFolder projetX
```
- `--speakers 4` : le nombre de personnes qui parlent, **toi compris**. Si tu ne sais pas, enlève cette option.
- `--nameFolder projetX` : range la réunion dans `reunions/projetX/1/`, puis `2/`, `3/`… Choisis un nom simple, sans espace ni `/` (par exemple `comite-direction`).
- `HF_HUB_OFFLINE=1` : interdit tout accès à Internet pour les modèles. Possible uniquement **après** le premier essai (étape 8).

**Transcription simple (plus rapide, sans intervenants) :**
```bash
HF_HUB_OFFLINE=1 python3 ./script/meeting-whisper.py --os debian --mic "Built-in Audio"
```

**Réunion en présentiel (pas de visio) :** ajoute `--audio none`.
```bash
HF_HUB_OFFLINE=1 python3 ./script/meeting-whisper-final.py --os debian --mic "Built-in Audio" --audio none --speakers 5 --nameFolder projetX
```

**Transcrire un fichier audio ou vidéo existant** (`.wav`, `.mp3`, `.m4a`, `.mp4`…). Astuce : tape la commande jusqu'à `--file `, puis glisse le fichier dans le terminal.
```bash
HF_HUB_OFFLINE=1 python3 ./script/meeting-whisper-final.py --os debian --file /home/marie/Téléchargements/reunion.mp4 --speakers 3 --nameFolder projetX
```

**Sans activer le `.venv` (chemin absolu) :** utilise le Python de l'environnement virtuel directement.
```bash
cd <DOSSIER_DU_PROJET>
HF_HUB_OFFLINE=1 <DOSSIER_DU_PROJET>/.venv/bin/python <DOSSIER_DU_PROJET>/script/meeting-whisper-final.py --os debian --mic "Built-in Audio" --nameFolder projetX
```
> ⚠️ Fais quand même le `cd` d'abord : le dossier `reunions/` est créé **dans le dossier où se trouve le terminal**.

### Pendant et à la fin de la réunion

1. Laisse le terminal ouvert (tu peux le réduire), et évite la mise en veille.
2. À la fin : clique dans le terminal, puis **Ctrl + C**.
3. **N'éteins pas l'ordinateur et ne ferme pas le terminal** avant le message `Transcription enregistrée dans …` (ou `Fichiers enregistrés dans …` avec `meeting-agent.py`). Pour 1 h de réunion, compte 15 à 30 minutes de traitement.

Toutes les options : [README, section Référence commune](../README.md#8-référence-commune).

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Debian, dans le dossier local-meeting-transcriber, l'installation est terminée et le .venv est activé.
Je vais faire une réunion : <visio avec casque / visio sans casque / présentiel>, avec <N ou « je ne sais pas »> participants,
et je veux ranger le résultat dans le dossier <nom>. Lance `python3 ./script/meeting-whisper-final.py --os debian --list`
pour vérifier mon micro et la source monitor, puis donne-moi la commande exacte à lancer moi-même (avec --os debian),
en suivant l'étape 9 de docs/config-debian.md. Rappelle-moi la checklist et comment arrêter.
```

---

## Étape 10 : après la réunion

1. **Ouvre le dossier du résultat** (adapte le nom) :
   ```bash
   xdg-open reunions/projetX
   ```
   Le fichier à lire est `…_transcription_intervenants.txt` (ou `…_transcription.txt`).
2. **Supprime les enregistrements** dont tu n'as plus besoin : ce sont des données personnelles.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Debian, dans le dossier local-meeting-transcriber. Liste les dossiers et fichiers de reunions/
(noms et tailles uniquement, sans ouvrir leur contenu), indique-moi où est la transcription de ma dernière réunion
et donne-moi la commande `xdg-open` pour ouvrir son dossier. Ne supprime rien sans mon accord explicite.
```

---

## Étape 11 *(optionnel)* : compte rendu par Claude

> ⚠️ **Avec cette option, le texte de la transcription est envoyé à Anthropic (États-Unis).** Pour une réunion confidentielle, lis d'abord [architecture-meeting-agent.md](architecture-meeting-agent.md) et utilise le **compte de ton entreprise**.

1. Installe Claude Code en suivant la **documentation officielle de Claude Code pour Linux**. La version de Node.js fournie par Debian est souvent trop ancienne pour `npm install -g @anthropic-ai/claude-code`, et il ne faut **jamais** utiliser `sudo npm`.
2. Lance `claude` une fois et connecte-toi **avec le compte de ton entreprise**. Tape `/status` pour vérifier, puis `/exit`.
3. **Ne définis pas** de variable `ANTHROPIC_API_KEY`.
4. Utilisation, dans le dossier du projet, `.venv` actif :
   ```bash
   python3 ./script/meeting-agent.py --os debian --mic "Built-in Audio"
   ```
   Après le **Ctrl + C**, tu obtiens dans `reunions/` la transcription **et** un fichier `…_notes.md`.

✅ **Vérification :** `which claude` affiche un chemin.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Debian. Vérifie si Claude Code est installé (`which claude`) et quelle version de Node.js est présente
(`node --version`). S'il manque quelque chose, explique-moi comment installer Claude Code d'après sa documentation officielle,
sans utiliser sudo npm, et attends mon accord. Rappelle-moi de me connecter avec le compte de mon entreprise (/status).
Ne crée jamais de variable ANTHROPIC_API_KEY.
```

---

## Erreurs possibles sous Debian

> Ces solutions viennent des problèmes connus sous Debian/Ubuntu. **Elles n'ont pas encore été vérifiées sur une vraie machine** : si tu rencontres une erreur absente du tableau, note le message exact.

### Installation

| Ce que tu vois | Cause | Solution |
|---|---|---|
| `error: externally-managed-environment` | Debian interdit `pip install` hors environnement virtuel | Étape 4 (`.venv`). N'utilise **pas** `--break-system-packages` |
| `The virtual environment was not created successfully because ensurepip is not available` | Paquet `python3-venv` absent | `sudo apt install python3-venv`, puis supprime le dossier `.venv` raté (`rm -rf .venv`) et recommence l'étape 4 |
| `ModuleNotFoundError: No module named 'soundcard'` (ou autre) | `.venv` non activé dans ce terminal | Étape 5 : `source .venv/bin/activate` |
| `OSError: cannot load library 'libpulse.so.0'` | Bibliothèque PulseAudio absente | `sudo apt install libpulse0` |
| `OSError: sndfile library not found` | Bibliothèque libsndfile absente | `sudo apt install libsndfile1` |
| `pactl: command not found` | Outils PulseAudio absents | `sudo apt install pulseaudio-utils` |
| `… n'apparaît pas dans le fichier sudoers` | Pas de droits d'administration | Demande au service informatique d'installer les paquets de l'étape 2 |
| `ERROR: Could not find a version that satisfies the requirement …` | Python trop ancien ou architecture non prise en charge (ARM 32 bits…) | Vérifie `python3 --version` (≥ 3.9) et `uname -m` (`x86_64` ou `aarch64` attendus) |

### Premier lancement

| Ce que tu vois | Cause | Solution |
|---|---|---|
| `You are sending unauthenticated requests to the HF Hub` | Téléchargement sans compte Hugging Face | **Normal**, attends |
| Téléchargement bloqué (rien ne bouge pendant plus de 5 min) | Système de téléchargement « Xet » bloqué | Ctrl+C, puis relance la même commande précédée de `HF_HUB_DISABLE_XET=1 ` |
| `LocalEntryNotFoundError … outgoing traffic has been disabled` | `HF_HUB_OFFLINE=1` alors que le modèle n'est pas téléchargé | Relance **sans** `HF_HUB_OFFLINE=1` |
| Téléchargement refusé par le proxy de l'entreprise | Réseau d'entreprise filtré | Demande d'autoriser `huggingface.co` et `github.com`, ou configure `https_proxy` selon les consignes de ton service informatique |

### Enregistrement

| Ce que tu vois | Cause | Solution |
|---|---|---|
| `Système détecté : debian, mais --os vaut « mac »` et la visio n'est pas enregistrée | `--os debian` oublié | Ajoute **`--os debian`** à la commande |
| `--list --os debian` n'affiche aucune source « Monitor of … » | Pas de serveur son PipeWire/PulseAudio actif (machine sans interface graphique, connexion SSH, ALSA seul) | Utilise une session de bureau normale. Vérifie `pactl info`. Sur une installation minimale : `sudo apt install pipewire-pulse wireplumber`, puis redémarre la session |
| `pactl info` → `Connection failure: Connection refused` | Serveur son non démarré pour ton utilisateur | Redémarre la session. Vérifie `systemctl --user status pipewire-pulse` |
| `La piste du son de l'ordinateur est silencieuse` | La visio sort par une autre sortie que la sortie par défaut | Étape 6 : `pactl get-default-sink`, puis même sortie dans les Paramètres et dans la visio. Ou passe le bon monitor avec `--audio "Monitor of <nom>"` (voir `--list`) |
| Transcription vide, ta voix absente | Micro coupé ou volume à 0 | `pavucontrol` → *Périphériques d'entrée* (étape 7) |
| Aucun micro, ou erreur d'accès au son | Script lancé avec `sudo` | Relance **sans** `sudo` |
| `Périphérique « … » introuvable. Lance --list…` | Nom mal écrit | `--os debian --list` (étape 7), puis copie le nom exact |
| Son de mauvaise qualité avec un casque Bluetooth | Profil « mains libres » (HSP/HFP) quand le micro du casque est utilisé | Utilise le micro de l'ordinateur avec `--mic` |
| Le collage dans le terminal ne marche pas avec Ctrl + V | Dans un terminal Linux, le raccourci de collage est différent | **Ctrl + Maj + V** |
| `Commande « claude » introuvable` (`meeting-agent.py`) | Claude Code non installé | Étape 11 |

🤖 **Prompt pour un assistant IA (en cas d'erreur) :**
```text
Je suis sous Debian, dans le dossier local-meeting-transcriber. J'ai lancé : <la commande>
Et j'obtiens cette erreur : <colle le message complet>
Cherche la cause dans la section « Erreurs possibles sous Debian » de docs/config-debian.md. Explique la cause en une phrase,
puis la solution étape par étape. Demande mon accord avant toute installation ou commande avec sudo, et n'utilise jamais
sudo pour lancer les scripts ou pip. Si l'erreur n'est pas dans le tableau, dis-le clairement au lieu d'inventer.
```

---

## Prompt global : l'agent fait tout avec toi

Ce prompt transforme ton assistant IA (Claude Code, GitHub Copilot Chat **en mode agent**, Cursor…) en guide complet : il te pose des questions précises, vérifie ton installation, installe ce qui manque **avec ton accord**, et te prépare la commande finale (ou la lance lui-même pour un fichier existant).

**Comment l'utiliser :**
1. Ouvre le dossier `local-meeting-transcriber` dans ton éditeur (VS Code : *Fichier > Ouvrir le dossier…*).
2. Ouvre ton assistant IA en mode agent.
3. Copie **tout** le bloc ci-dessous et colle-le.

```text
Tu es mon assistant pour installer et utiliser l'outil local-meeting-transcriber sur mon ordinateur Debian (ou Ubuntu).
Le dossier ouvert est la racine du projet. Avant tout, lis README.md et docs/config-debian.md : ce sont tes références.

RÈGLES À RESPECTER EN PERMANENCE
- Réponds en français, avec des phrases simples, comme à quelqu'un qui n'est pas développeur.
- Pose les questions ci-dessous UNE PAR UNE, dans l'ordre, et attends ma réponse avant de continuer.
  Propose toujours les choix numérotés indiqués. N'invente pas mes réponses.
- Avant chaque commande, explique en une phrase ce qu'elle fait.
- Sous Debian : utilise l'environnement virtuel .venv du projet (pour tes propres commandes, utilise directement
  `.venv/bin/python`), et ajoute TOUJOURS `--os debian` aux commandes des scripts.
  N'utilise JAMAIS sudo pour pip ni pour lancer les scripts.
- Les commandes avec sudo (sudo apt install …) demandent mon mot de passe : donne-les-moi pour que je les lance dans mon
  propre terminal, puis vérifie le résultat quand je te le dis.
- Demande mon accord explicite avant : toute installation, toute modification d'un réglage système.
- Ne modifie, ne supprime et ne crée aucun fichier du projet, sauf le dossier .venv à l'étape 4 si je l'accepte.
  N'ouvre pas, ne lis pas et n'envoie jamais le contenu du dossier reunions/ (enregistrements et transcriptions) sans
  que je te le demande.
- Ne crée jamais de variable ANTHROPIC_API_KEY.
- En cas d'erreur, cherche d'abord dans la section « Erreurs possibles sous Debian » de docs/config-debian.md. Si l'erreur
  n'y est pas, montre-moi le message exact et dis-le clairement, au lieu d'inventer une solution.

QUESTIONS À ME POSER (une par une, dans cet ordre)
Q1. Que veux-tu faire ?
    1) Installer ou vérifier l'outil seulement
    2) Enregistrer une réunion qui va commencer
    3) Transcrire un fichier audio ou vidéo que j'ai déjà
Q2. Quel résultat veux-tu ?
    1) Transcription avec qui parle (« Utilisateur 1, 2… ») - recommandé
    2) Transcription simple, plus rapide
    3) Transcription + compte rendu par Claude (attention : le texte est envoyé à Anthropic, aux États-Unis)
    (Si je réponds 3 avec Q1 = 3, explique-moi que meeting-agent.py ne sait pas transcrire un fichier existant, et repose Q2.)
Q3. (Seulement si Q1 = 2) Quel type de réunion ?
    1) Visio avec un casque ou des écouteurs
    2) Visio sans casque (son sur les haut-parleurs)
    3) Réunion en présentiel, sans visio
Q4. (Sauf si Q1 = 1) Combien de personnes vont parler, moi compris ? (un nombre, ou « je ne sais pas »)
Q5. (Seulement si Q2 = 1) Dans quel dossier ranger le résultat ? (un nom simple sans espace ni « / », par exemple comite-projet, ou « aucun »)
Q6. (Sauf si Q1 = 1) Tu préfères :
    1) Rapide (modèle small, conseillé)
    2) Plus précis mais plus lent (modèle medium)
Q7. (Seulement si Q1 = 3) Quel est le chemin complet du fichier ? (glisse-le dans le chat ou colle son chemin)

CE QUE TU FAIS ENSUITE, DANS CET ORDRE (en suivant les étapes de docs/config-debian.md)
1. `pwd` et `ls -a` : vérifie qu'on est bien à la racine du projet (README.md, docs, script) et regarde si .venv existe.
2. `python3 --version`, `python3 -m venv --help > /dev/null && echo venv OK`, `pactl info` (étape 2).
   S'il manque quelque chose, donne-moi la commande sudo apt de l'étape 2 à lancer moi-même.
3. Si .venv n'existe pas : propose de le créer et d'installer les dépendances (étape 4) :
   `python3 -m venv .venv` puis `.venv/bin/pip install soundcard soundfile faster-whisper numpy sherpa-onnx`.
   Vérifie avec `.venv/bin/python -c "import soundcard, soundfile, faster_whisper, numpy, sherpa_onnx; print('Tout est installé')"`.
4. `.venv/bin/python ./script/meeting-whisper-final.py --os debian --list` : recommande-moi un micro (étape 7) et dis-moi
   quelle source « Monitor of … » sera enregistrée comme son de l'ordinateur. Si Q3 = 1 ou 2, rappelle-moi que la sortie son
   par défaut et celle de mon application de visio doivent être le même appareil (étape 6).
5. Vérifie si le modèle choisi est déjà téléchargé : `ls ~/.cache/huggingface/hub/` doit contenir
   models--Systran--faster-whisper-small (ou -medium). S'il est absent : préviens-moi que le premier lancement téléchargera
   le modèle (~480 Mo pour small, ~1,5 Go pour medium) et n'ajoute PAS HF_HUB_OFFLINE=1. S'il est présent : ajoute
   HF_HUB_OFFLINE=1 au début de la commande.
6. Construis la commande finale, avec : le script correspondant à Q2 (./script/meeting-whisper-final.py /
   ./script/meeting-whisper.py / ./script/meeting-agent.py), --os debian, --mic "<nom exact du micro>", --audio none si
   Q3 = 3, --speakers <N> si Q4 est un nombre (script final uniquement), --nameFolder <nom> si Q5 n'est pas « aucun »,
   --model medium si Q6 = 2, --file "<chemin>" si Q1 = 3.
7. Si Q1 = 3 (fichier existant) : demande-moi si tu dois lancer la commande toi-même (avec .venv/bin/python). Si oui,
   lance-la et montre-moi où se trouve le résultat.
   Si Q1 = 2 (enregistrement) : NE LANCE PAS l'enregistrement toi-même (il doit être arrêté avec Ctrl+C dans mon terminal).
   Donne-moi les lignes à copier dans mon terminal, dans cet ordre : `cd <chemin du projet>`, `source .venv/bin/activate`,
   puis la commande (avec python3). Rappelle-moi :
   - la checklist « Avant la réunion » de l'étape 9 (prévenir les participants, même sortie son dans les Paramètres et dans la visio) ;
   - d'appuyer sur Ctrl + C à la fin ;
   - d'attendre le message « Transcription enregistrée dans … » (ou « Fichiers enregistrés dans … » pour meeting-agent.py) avant de fermer le terminal.
8. Termine par un récapitulatif en 5 lignes : ce qui est installé, le micro choisi, la commande, où sera le résultat,
   comment arrêter.
```
