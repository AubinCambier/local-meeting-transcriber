# Guide Mac 🍎 : installer et utiliser local-meeting-transcriber

> **Tu es au bon endroit si** ton ordinateur est un Mac (MacBook, iMac, Mac mini…).
> Sous Windows : [config-windows.md](config-windows.md). Sous Debian/Ubuntu : [config-debian.md](config-debian.md).
>
> **Avant de commencer**, tu dois avoir fait l'**étape 1 du [README](../README.md#4-étape-1--récupérer-le-projet)** : récupérer le projet dans un dossier nommé `local-meeting-transcriber`.

Suis les étapes **dans l'ordre**. Chaque étape indique **quoi faire**, **comment vérifier que ça a marché**, et donne un **prompt pour un assistant IA** si tu veux de l'aide. Tu préfères qu'un agent fasse tout avec toi ? Va directement au [prompt global](#prompt-global--lagent-fait-tout-avec-toi), en bas de page.

## Le parcours en un coup d'œil

| # | Étape | Une seule fois ? | Durée |
|---|---|---|---|
| 1 | [Ouvrir le Terminal](#étape-1--ouvrir-le-terminal) | À chaque utilisation | 1 min |
| 2 | [Vérifier Python](#étape-2--vérifier-python) | ✅ Une fois | 1 à 10 min |
| 3 | [Aller dans le dossier du projet](#étape-3--aller-dans-le-dossier-du-projet) | À chaque utilisation | 1 min |
| 4 | [Installer les bibliothèques](#étape-4--installer-les-bibliothèques-python) | ✅ Une fois | 5 min |
| 5 | [Installer Homebrew](#étape-5--installer-homebrew) | ✅ Une fois | 5 min |
| 6 | [Installer BlackHole](#étape-6--installer-blackhole) | ✅ Une fois | 3 min |
| 7 | [Créer le périphérique à sorties multiples](#étape-7--créer-le-périphérique-à-sorties-multiples) | ✅ Une fois | 3 min |
| 8 | [Autoriser le micro](#étape-8--autoriser-le-micro) | ✅ Une fois | 1 min |
| 9 | [Choisir son micro](#étape-9--choisir-son-micro) | ✅ Une fois (puis si tu changes de micro) | 2 min |
| 10 | [Premier essai](#étape-10--premier-essai-30-secondes) | ✅ Une fois | 10 min |
| 11 | [Utilisation pour une vraie réunion](#étape-11--utilisation-pour-une-vraie-réunion) | À chaque réunion | — |
| 12 | [Après la réunion](#étape-12--après-la-réunion) | À chaque réunion | 1 min |
| 13 | [*(Optionnel)* Compte rendu par Claude](#étape-13-optionnel--compte-rendu-par-claude) | ✅ Une fois | 10 min |

> 💡 **Réunions en présentiel uniquement** (tout le monde dans la même pièce, pas de visio) ? Tu peux sauter les étapes 5, 6 et 7 : le micro suffit. Ajoute alors `--audio none` à tes commandes.

**Comment lire les commandes de cette page :**
- Un bloc gris = **une ou plusieurs commandes à copier**. Colle-les dans le Terminal, puis appuie sur **Entrée**.
- Ne copie pas le symbole `%` affiché au début des lignes du Terminal : il fait partie de l'invite, pas de la commande.
- Remplace tout ce qui est entre `< >` (par exemple `<DOSSIER_DU_PROJET>`), **en retirant les `< >`**.

---

## Étape 1 : ouvrir le Terminal

1. Appuie sur **Cmd + Espace** : la recherche Spotlight s'ouvre.
2. Tape **`Terminal`**, puis appuie sur **Entrée**.
3. Une fenêtre s'ouvre avec une ligne qui se termine par **`%`** : c'est ici que tu tapes les commandes.

*Alternative :* dans **VS Code**, menu *Terminal > Nouveau terminal*.

✅ **Vérification :** tu vois une fenêtre avec une ligne du type `ton-nom@MacBook-Air ~ %`.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sur Mac et je débute avec le Terminal. Explique-moi, étape par étape, comment ouvrir le Terminal
(Spotlight avec Cmd + Espace, ou VS Code > Terminal > Nouveau terminal), comment y coller une commande et la valider,
et ce que signifie le « % » en début de ligne. Ne lance aucune commande.
```

---

## Étape 2 : vérifier Python

Les scripts sont écrits en Python. macOS fournit Python 3 avec les « outils de développement en ligne de commande » d'Apple.

```bash
python3 --version
```

| Ce que tu vois | Ce que ça veut dire | Quoi faire |
|---|---|---|
| `Python 3.9.6` (ou un numéro **≥ 3.9**) | ✅ Python est installé | Passe à l'étape 3 |
| Une fenêtre « La commande python3 nécessite les outils de développement en ligne de commande » | Python n'est pas encore installé | Clique sur **Installer**, accepte la licence, attends la fin (5 à 10 min), puis **relance** `python3 --version` |
| `Python 3.8` ou moins | Version trop ancienne | Installe un Python récent depuis [python.org](https://www.python.org/downloads/macos/) (bouton *Download*), puis ferme et rouvre le Terminal |

> ⚠️ Sur Mac, la commande s'appelle **`python3`** (et **`pip3`**), **pas** `python` ni `pip`. Si tu tapes `pip`, tu obtiens `zsh: command not found: pip`.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sur Mac. Vérifie si Python 3.9 ou plus récent est installé en lançant `python3 --version`.
Si Python est absent ou trop ancien, explique-moi précisément quoi faire (outils de développement Apple ou python.org),
sans rien installer toi-même sans mon accord. Réponds en français, en phrases simples.
```

---

## Étape 3 : aller dans le dossier du projet

Le Terminal doit « se placer » dans le dossier du projet, sinon il ne trouve pas les scripts.

1. Tape **`cd `** (c, d, puis **un espace**). **N'appuie pas encore sur Entrée.**
2. Dans le Finder, **fais glisser le dossier `local-meeting-transcriber`** dans la fenêtre du Terminal : son chemin complet s'écrit tout seul.
3. Appuie sur **Entrée**.

Ça donne par exemple :
```bash
cd /Users/marie/Documents/local-meeting-transcriber
```

✅ **Vérification :**
```bash
ls
```
Tu dois voir au moins **`README.md`**, **`docs`** et **`script`**. Sinon, tu es dans le mauvais dossier : recommence avec le bon.

> 📝 Ce chemin, c'est ton **`<DOSSIER_DU_PROJET>`**. Pour l'afficher à tout moment : `pwd`.
>
> ⚠️ **À refaire à chaque nouvelle fenêtre de Terminal.** Les enregistrements sont créés dans le dossier où se trouve le Terminal : si tu oublies le `cd`, ils atterrissent ailleurs.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sur Mac. Vérifie que le terminal est bien dans le dossier du projet local-meeting-transcriber :
lance `pwd` puis `ls`, et confirme que README.md, docs et script sont présents.
Sinon, aide-moi à trouver le bon dossier et donne-moi la commande `cd` exacte. Ne modifie aucun fichier.
```

---

## Étape 4 : installer les bibliothèques Python

Depuis le dossier du projet (étape 3) :

```bash
pip3 install --user soundcard soundfile faster-whisper numpy sherpa-onnx
```

Ça télécharge et installe les outils d'enregistrement et de transcription. Compte quelques minutes. Beaucoup de lignes défilent : c'est normal.

**Messages normaux, à ignorer :**
- `WARNING: The script … is installed in '…/Library/Python/3.9/bin' which is not on PATH` ;
- `WARNING: You are using pip version 21.2.4; however, version … is available`.

✅ **Vérification :** l'avant-dernière ligne commence par **`Successfully installed`**. Puis lance :
```bash
python3 -c "import soundcard, soundfile, faster_whisper, numpy, sherpa_onnx; print('Tout est installé')"
```
Tu dois voir **`Tout est installé`**. Si tu vois `ModuleNotFoundError: No module named '…'`, relance la commande `pip3 install` ci-dessus et regarde la dernière erreur affichée (voir [Erreurs possibles](#erreurs-possibles-sur-mac)).

🤖 **Prompt pour un assistant IA :**
```text
Je suis sur Mac, dans le dossier local-meeting-transcriber. Installe les dépendances du projet avec
`pip3 install --user soundcard soundfile faster-whisper numpy sherpa-onnx` (demande-moi mon accord avant de lancer),
puis vérifie avec `python3 -c "import soundcard, soundfile, faster_whisper, numpy, sherpa_onnx; print('Tout est installé')"`.
Les avertissements « not on PATH » et « pip version » sont normaux. En cas d'erreur, consulte la section
« Erreurs possibles sur Mac » de docs/config-mac.md et propose-moi la solution correspondante.
```

---

## Étape 5 : installer Homebrew

> Saute cette étape si tu ne fais **que des réunions en présentiel**.

Homebrew est un installateur de logiciels pour Mac. On en a besoin pour installer BlackHole (étape 6).

**Vérifie d'abord s'il est déjà installé :**
```bash
brew --version
```
- Tu vois `Homebrew 4.x.x` (ou plus) → ✅ déjà installé, passe à l'étape 6.
- Tu vois `zsh: command not found: brew` → installe-le :

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

1. Le Terminal demande ton **mot de passe de session Mac**. Tape-le : **rien ne s'affiche pendant la saisie, c'est normal**. Puis appuie sur **Entrée**.
2. Appuie sur **Entrée** quand il demande de confirmer.
3. **Important :** à la fin, sous **« Next steps »**, Homebrew affiche 2 ou 3 commandes à copier (elles commencent par `echo` et `eval`). **Copie-les et lance-les**, sinon la commande `brew` ne sera pas trouvée.
4. Ferme le Terminal, rouvre-le, et relance `brew --version`.

> ⚠️ **Mac d'entreprise :** l'installation peut être bloquée ou nécessiter les droits administrateur. Dans ce cas, demande à ton service informatique d'installer Homebrew et BlackHole.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sur Mac. Vérifie si Homebrew est installé avec `brew --version`.
S'il ne l'est pas, explique-moi comment l'installer depuis https://brew.sh et rappelle-moi de lancer les commandes
affichées sous « Next steps » à la fin. Ne lance pas l'installation toi-même : elle demande mon mot de passe,
je la lancerai dans mon propre terminal. Réponds en français.
```

---

## Étape 6 : installer BlackHole

> Saute cette étape si tu ne fais **que des réunions en présentiel**.

**Pourquoi ?** macOS ne permet pas d'enregistrer le son qui sort de l'ordinateur (la voix des participants d'une visio). **BlackHole** est un petit pilote audio gratuit et open source qui crée une fausse carte son : tout ce qu'on lui envoie peut être enregistré. Il fonctionne **uniquement sur Mac**, et rien n'est envoyé sur Internet.

```bash
brew install blackhole-2ch
```
Le Terminal demande ton **mot de passe Mac** : tape-le (rien ne s'affiche, c'est normal), puis **Entrée**.

Ensuite, redémarre le service audio de macOS pour qu'il détecte BlackHole :
```bash
sudo killall coreaudiod
```
Mot de passe à nouveau. Le son peut se couper une seconde : c'est normal.

✅ **Vérification** (depuis le dossier du projet, étape 3) :
```bash
python3 ./script/meeting-whisper-final.py --list
```
En bas, tu dois voir :
```
Son de l'ordinateur (--audio), pour --os mac :
     BlackHole 2ch  ← par défaut
```
Si tu vois `(aucune : installe BlackHole : voir docs/config-mac.md, étape 6)`, consulte les [erreurs possibles](#erreurs-possibles-sur-mac) (ligne « BlackHole absent »).

🤖 **Prompt pour un assistant IA :**
```text
Je suis sur Mac, dans le dossier local-meeting-transcriber. Vérifie si BlackHole est installé :
lance `brew list --cask | grep blackhole`, `ls /Library/Audio/Plug-Ins/HAL/` (doit contenir BlackHole2ch.driver)
et `python3 ./script/meeting-whisper-final.py --list` (doit afficher « BlackHole 2ch ← par défaut »).
S'il manque, donne-moi les commandes `brew install blackhole-2ch` puis `sudo killall coreaudiod` à lancer moi-même
(elles demandent mon mot de passe), puis refais la vérification quand je te le dis.
```

---

## Étape 7 : créer le périphérique à sorties multiples

> Saute cette étape si tu ne fais **que des réunions en présentiel**.

**Pourquoi ?** Si tu envoies le son de la visio **uniquement** vers BlackHole, l'outil l'enregistre mais **tu ne l'entends plus**. On crée donc un « périphérique à sorties multiples » qui envoie le son **à la fois** dans ton casque (pour toi) **et** dans BlackHole (pour l'enregistrement).

```
                               ┌──► 🎧 ton casque     → tu entends la visio
 Teams / Zoom ──► Sorties ─────┤
                  multiples    └──► BlackHole 2ch     → l'outil l'enregistre
```

**Création (une seule fois) :**
1. **Cmd + Espace**, tape **`Configuration audio et MIDI`**, puis **Entrée**.
2. En bas à gauche de la fenêtre, clique sur **`+`**, puis sur **« Créer un périphérique à sorties multiples »**.
3. Dans la partie droite, coche la case **« Utiliser »** pour :
   - ton casque ou tes haut-parleurs (par exemple « Haut-parleurs MacBook Air », « AirPods »…) ;
   - **« BlackHole 2ch »**.
4. Dans le menu **« Appareil principal »** (« Périphérique principal » selon ta version de macOS), choisis **ton casque ou tes haut-parleurs**, pas BlackHole.
5. Coche **« Correction de la dérive »** sur la ligne **BlackHole 2ch**.
6. Dans la liste de gauche, double-clique sur le nom « Périphérique à sorties multiples » et renomme-le, par exemple **`Casque + BlackHole`**.

> 💡 Si tu utilises plusieurs casques (AirPods au bureau, haut-parleurs à la maison…), crée **un périphérique à sorties multiples par casque**, par exemple `AirPods + BlackHole` et `Haut-parleurs + BlackHole`.

**Avant chaque visio :**
1. Ouvre **Réglages Système > Son > Sortie** et choisis **`Casque + BlackHole`**.
2. Dans Teams, Zoom ou Meet, règle le haut-parleur sur **« Identique au système »** ou sur **`Casque + BlackHole`**.

> ⚠️ **Avec un périphérique à sorties multiples, les touches de volume du clavier ne marchent plus** : c'est une limite de macOS. Règle le volume dans l'application de visio. Après la réunion, remets ta sortie habituelle (étape 12).

✅ **Vérification :** mets **`Casque + BlackHole`** comme sortie, lance une vidéo YouTube : tu dois l'entendre normalement. L'enregistrement réel sera vérifié à l'étape 10.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sur Mac et BlackHole 2ch est installé. Guide-moi pas à pas, clic par clic, pour créer dans
« Configuration audio et MIDI » un périphérique à sorties multiples qui combine mon casque et BlackHole 2ch,
en suivant l'étape 7 de docs/config-mac.md (appareil principal = mon casque, correction de la dérive sur BlackHole).
Attends que je te confirme chaque étape avant de passer à la suivante. Ensuite, vérifie avec
`python3 -c "import soundcard as sc; print([s.name for s in sc.all_speakers()])"` que le nouveau périphérique apparaît.
```

---

## Étape 8 : autoriser le micro

macOS demande ton autorisation la première fois qu'une application utilise le micro.

- Quand la fenêtre **« Terminal souhaite accéder au micro »** apparaît (à l'étape 10), clique sur **Autoriser**.
- Si tu as cliqué sur « Refuser » par erreur, ou si tes transcriptions sont vides :
  1. Ouvre **Réglages Système > Confidentialité et sécurité > Microphone**.
  2. Active **Terminal** (ou **Visual Studio Code**, si tu lances les commandes depuis VS Code).
  3. **Ferme complètement** le Terminal (Cmd + Q), puis rouvre-le.

✅ **Vérification :** dans *Réglages Système > Confidentialité et sécurité > Microphone*, **Terminal** (ou VS Code) est activé.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sur Mac. Mes enregistrements de local-meeting-transcriber sont silencieux ou la transcription est vide.
Explique-moi comment vérifier et activer l'accès au micro pour Terminal (ou VS Code) dans
Réglages Système > Confidentialité et sécurité > Microphone, puis comment relancer correctement le terminal.
```

---

## Étape 9 : choisir son micro

Depuis le dossier du projet :
```bash
python3 ./script/meeting-whisper-final.py --list
```

Exemple de résultat :
```
Micros (--mic) :
  0  iPhone de Marie Microphone
  1  MacBook Air Microphone  ← par défaut
  2  Microsoft Teams Audio

Son de l'ordinateur (--audio), pour --os mac :
     BlackHole 2ch  ← par défaut
```

**Comment lire ce résultat :**
- **Micros** : ce qui peut capter **ta voix**. `← par défaut` indique celui qui sera utilisé si tu ne précises rien (le micro choisi dans *Réglages Système > Son > Entrée*).
- **Son de l'ordinateur** : ce qui capte **la visio**. Sur Mac, c'est BlackHole.

**Quel micro choisir ?**

| Micro | Pour une transcription |
|---|---|
| Micro intégré du Mac (« MacBook Air Microphone »…), micro USB | ✅ **Recommandé** |
| AirPods, casque Bluetooth | ⚠️ macOS dégrade la qualité du son quand leur micro est utilisé. Préfère le micro du Mac |
| iPhone (« iPhone de … Microphone ») | ⚠️ Fonctionne, mais disparaît si l'iPhone s'éloigne ou se verrouille |
| « Microsoft Teams Audio » | ❌ Ce n'est pas un vrai micro (périphérique virtuel de Teams) |

**Utilise toujours le nom du micro, jamais son numéro :** les numéros changent quand un appareil apparaît ou disparaît (l'iPhone, par exemple). Une partie du nom suffit :
```bash
--mic "MacBook Air Microphone"
```

🤖 **Prompt pour un assistant IA :**
```text
Je suis sur Mac, dans le dossier local-meeting-transcriber. Lance `python3 ./script/meeting-whisper-final.py --list`
(lecture seule, n'enregistre rien). Puis dis-moi :
- le micro utilisé par défaut ;
- pour chaque micro listé, s'il est conseillé pour une transcription (micro intégré ou USB = conseillé ;
  AirPods/Bluetooth = qualité réduite ; iPhone = instable ; « Microsoft Teams Audio » = pas un vrai micro) ;
- si BlackHole 2ch est bien détecté comme son de l'ordinateur ;
- le micro que tu me recommandes, et l'option exacte à utiliser : --mic "<nom exact>".
```

---

## Étape 10 : premier essai (30 secondes)

Ce premier essai **télécharge les modèles** (~500 Mo, une seule fois) et vérifie que **ta voix et le son de l'ordinateur** sont bien enregistrés.

1. Mets **`Casque + BlackHole`** comme sortie son (étape 7). Ignore ce point si tu as sauté les étapes 5 à 7.
2. Ouvre une vidéo YouTube avec quelqu'un qui parle, **en pause**.
3. Dans le Terminal, depuis le dossier du projet, lance (remplace le nom du micro par le tien, étape 9) :
   ```bash
   python3 ./script/meeting-whisper-final.py --mic "MacBook Air Microphone" --nameFolder essai
   ```
   *(Réunions en présentiel uniquement : ajoute `--audio none` à la fin.)*
4. Quand tu vois **`Enregistrement — micro : « … » + son de l'ordinateur : « BlackHole 2ch »… Ctrl+C pour arrêter.`** :
   - lance la vidéo ;
   - parle aussi un peu toi-même (« Ceci est un test du micro ») ;
   - si macOS demande l'accès au micro, clique sur **Autoriser**.
5. Au bout de 30 secondes, clique dans la fenêtre du Terminal et appuie sur **Ctrl + C** (bien **Ctrl**, pas Cmd).
6. **Attends** : le premier lancement télécharge les modèles (plusieurs minutes). Tu verras passer :
   - `Identification des intervenants (sherpa-onnx)…`
   - `Transcription locale (whisper small)…`
   - puis les lignes de transcription.
7. C'est fini quand tu vois **`Transcription enregistrée dans reunions/essai/1/…`**.

**Messages normaux, à ignorer :** `You are sending unauthenticated requests to the HF Hub`, `RuntimeWarning: … encountered in matmul`, `Tip: experimental MPS backend is available`.

✅ **Vérification :**
- la transcription contient **ta phrase** et **des phrases de la vidéo** ;
- le dossier `reunions/essai/1/` contient 4 fichiers : `….wav`, `…_micro.wav`, `…_audio.wav` et `…_transcription_intervenants.txt`. Ouvre-le avec :
  ```bash
  open reunions/essai/1
  ```

| Problème | Cause probable |
|---|---|
| Ta voix manque | Micro non autorisé (étape 8) ou mauvais micro (étape 9) |
| La vidéo manque + message « piste du son de l'ordinateur est silencieuse » | La sortie son n'est pas réglée sur `Casque + BlackHole` (étape 7) |
| Message « Aucune source de son de l'ordinateur trouvée » | BlackHole non détecté (étape 6) |

🤖 **Prompt pour un assistant IA :**
```text
Je suis sur Mac, dans le dossier local-meeting-transcriber. Je viens de faire le premier essai de l'étape 10
de docs/config-mac.md avec la commande :
python3 ./script/meeting-whisper-final.py --mic "<mon micro>" --nameFolder essai
Voici ce que le terminal a affiché : <colle ici la sortie du terminal>
Analyse le résultat : ma voix et le son de l'ordinateur ont-ils été enregistrés ? Si non, identifie la cause
avec le tableau de l'étape 10 et la section « Erreurs possibles sur Mac », et dis-moi précisément quoi corriger.
Tu peux lister le contenu de reunions/essai/ mais n'ouvre pas les fichiers audio ou texte sans mon accord.
```

---

## Étape 11 : utilisation pour une vraie réunion

### Avant la réunion (checklist)

1. ☐ **Préviens les participants** que la réunion est enregistrée (obligation RGPD).
2. ☐ **Visio :** sortie son = **`Casque + BlackHole`** (*Réglages Système > Son > Sortie*).
3. ☐ Ouvre le Terminal et place-toi dans le projet : `cd <DOSSIER_DU_PROJET>` (étape 3).
4. ☐ Lance la commande **au début** de la réunion.

### Les commandes

Toutes les commandes se lancent **depuis `<DOSSIER_DU_PROJET>`** (étape 3).

**Transcription avec intervenants (recommandé) :**
```bash
HF_HUB_OFFLINE=1 python3 ./script/meeting-whisper-final.py --mic "MacBook Air Microphone" --speakers 4 --nameFolder projetX
```
- `--speakers 4` : le nombre de personnes qui parlent, **toi compris**. Si tu ne sais pas, enlève cette option.
- `--nameFolder projetX` : range la réunion dans `reunions/projetX/1/`, puis `2/`, `3/`… pour les suivantes. Choisis un nom simple, sans espace ni `/` (par exemple `comite-direction`).
- `HF_HUB_OFFLINE=1` : interdit tout accès à Internet pour les modèles. Possible uniquement **après** le premier essai (étape 10).

**Transcription simple (plus rapide, sans intervenants) :**
```bash
HF_HUB_OFFLINE=1 python3 ./script/meeting-whisper.py --mic "MacBook Air Microphone"
```

**Réunion en présentiel (pas de visio) :** ajoute `--audio none`.
```bash
HF_HUB_OFFLINE=1 python3 ./script/meeting-whisper-final.py --mic "MacBook Air Microphone" --audio none --speakers 5 --nameFolder projetX
```

**Transcrire un fichier audio ou vidéo existant** (`.wav`, `.mp3`, `.m4a`, `.mp4`…). Astuce : tape la commande jusqu'à `--file `, puis glisse le fichier dans le Terminal.
```bash
HF_HUB_OFFLINE=1 python3 ./script/meeting-whisper-final.py --file /Users/marie/Downloads/reunion.mp4 --speakers 3 --nameFolder projetX
```

**Depuis n'importe quel dossier (chemin absolu) :**
```bash
cd <DOSSIER_DU_PROJET>
HF_HUB_OFFLINE=1 python3 <DOSSIER_DU_PROJET>/script/meeting-whisper-final.py --mic "MacBook Air Microphone" --nameFolder projetX
```
> ⚠️ Fais quand même le `cd` d'abord : le dossier `reunions/` est créé **dans le dossier où se trouve le Terminal**.

### Pendant et à la fin de la réunion

1. Laisse la fenêtre du Terminal ouverte (tu peux la réduire).
2. À la fin : clique dans le Terminal, puis **Ctrl + C**.
3. **N'éteins pas l'ordinateur et ne ferme pas le Terminal** avant le message `Transcription enregistrée dans …` (ou `Fichiers enregistrés dans …` avec `meeting-agent.py`). Pour 1 h de réunion, compte 15 à 30 minutes de traitement.

Toutes les options : [README, section Référence commune](../README.md#8-référence-commune).

🤖 **Prompt pour un assistant IA :**
```text
Je suis sur Mac, dans le dossier local-meeting-transcriber, et l'installation est terminée.
Je vais faire une réunion : <visio avec casque / visio sans casque / présentiel>, avec <N ou « je ne sais pas »> participants,
et je veux ranger le résultat dans le dossier <nom>. Lance `python3 ./script/meeting-whisper-final.py --list` pour
vérifier mon micro et BlackHole, puis donne-moi la commande exacte à lancer moi-même dans mon terminal,
en suivant l'étape 11 de docs/config-mac.md. Rappelle-moi la checklist « Avant la réunion » et comment arrêter.
```

---

## Étape 12 : après la réunion

1. **Ouvre le dossier du résultat** (adapte le nom) :
   ```bash
   open reunions/projetX
   ```
   Le fichier à lire est `…_transcription_intervenants.txt` (ou `…_transcription.txt`).
2. **Remets ta sortie son habituelle** (*Réglages Système > Son > Sortie*), pour retrouver les touches de volume.
3. **Supprime les enregistrements** dont tu n'as plus besoin : ce sont des données personnelles.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sur Mac, dans le dossier local-meeting-transcriber. Liste les dossiers et fichiers présents dans reunions/
(noms et tailles uniquement, sans ouvrir leur contenu), indique-moi où se trouve la transcription de ma dernière réunion
et donne-moi la commande `open` pour ouvrir son dossier. Ne supprime rien sans mon accord explicite.
```

---

## Étape 13 *(optionnel)* : compte rendu par Claude

> ⚠️ **Avec cette option, le texte de la transcription est envoyé à Anthropic (États-Unis).** Pour une réunion confidentielle, lis d'abord [architecture-meeting-agent.md](architecture-meeting-agent.md) et utilise le **compte de ton entreprise**.

1. Installe Node.js puis Claude Code :
   ```bash
   brew install node
   npm install -g @anthropic-ai/claude-code
   ```
   Pour d'autres méthodes d'installation, consulte la documentation officielle de Claude Code.
2. Lance `claude` une fois et connecte-toi **avec le compte de ton entreprise**. Dans Claude, tape `/status` pour vérifier le compte, puis `/exit`.
3. **Ne définis pas** de variable `ANTHROPIC_API_KEY`.
4. Utilisation, depuis le dossier du projet :
   ```bash
   python3 ./script/meeting-agent.py --mic "MacBook Air Microphone"
   ```
   Après le **Ctrl + C**, tu obtiens dans `reunions/` la transcription **et** un fichier `…_notes.md` (résumé, décisions, actions, questions ouvertes).

✅ **Vérification :** `which claude` affiche un chemin (par exemple `/opt/homebrew/bin/claude`).

🤖 **Prompt pour un assistant IA :**
```text
Je suis sur Mac. Vérifie si Claude Code est installé (`which claude`) et si Node.js est présent (`node --version`).
S'il manque quelque chose, propose-moi les commandes d'installation de l'étape 13 de docs/config-mac.md et attends
mon accord. Rappelle-moi de me connecter avec le compte de mon entreprise et de vérifier avec /status.
Ne crée jamais de variable ANTHROPIC_API_KEY.
```

---

## Erreurs possibles sur Mac

✅ = erreur réellement rencontrée et résolue sur un Mac.

### Installation

| Ce que tu vois | Cause | Solution |
|---|---|---|
| ✅ `zsh: command not found: pip` | Sur Mac, la commande s'appelle `pip3` | Utilise `pip3 install --user …` |
| ✅ `brew install pip` → `No available formula with the name "pip"` | pip est fourni avec Python, il ne s'installe pas séparément | Inutile : utilise `pip3` |
| ✅ `WARNING: The script … is installed in '…/bin' which is not on PATH` | Des outils annexes sont installés dans un dossier non surveillé | **Sans conséquence**, ignore |
| ✅ `WARNING: You are using pip version 21.2.4` | pip est ancien | **Sans conséquence**, ignore |
| Fenêtre « La commande python3 nécessite les outils de développement… » | Outils Apple non installés | Clique sur **Installer**, attends, recommence (étape 2) |
| `error: externally-managed-environment` | Python installé via Homebrew, qui refuse `pip install --user` | Utilise un environnement virtuel : `python3 -m venv .venv`, puis `source .venv/bin/activate`, puis `pip install soundcard soundfile faster-whisper numpy sherpa-onnx`. Refais `source .venv/bin/activate` dans chaque nouveau Terminal |
| `zsh: command not found: brew` juste après l'installation de Homebrew | Les commandes « Next steps » n'ont pas été lancées | Relance l'installateur, copie les commandes `echo`/`eval` affichées sous « Next steps », ferme et rouvre le Terminal |
| ✅ **BlackHole absent de `--list`** après `brew install blackhole-2ch` | Installation interrompue (souvent au mot de passe), ou macOS n'a pas rechargé ses pilotes | 1. `brew list --cask \| grep blackhole` doit afficher `blackhole-2ch`. 2. `ls /Library/Audio/Plug-Ins/HAL/` doit contenir `BlackHole2ch.driver`. Si l'un manque : relance `brew install blackhole-2ch` et tape ton mot de passe (rien ne s'affiche, c'est normal). 3. `sudo killall coreaudiod`, ou redémarre le Mac |
| `brew install` refusé, « administrator » ou blocage | Mac d'entreprise géré (MDM) | Demande au service informatique d'installer Homebrew et BlackHole |

### Premier lancement

| Ce que tu vois | Cause | Solution |
|---|---|---|
| ✅ `You are sending unauthenticated requests to the HF Hub` | Téléchargement du modèle sans compte Hugging Face | **Normal**, attends la fin |
| Téléchargement bloqué (rien ne bouge pendant plus de 5 min) | Le système de téléchargement « Xet » de Hugging Face est bloqué | Ctrl+C, puis relance la même commande précédée de `HF_HUB_DISABLE_XET=1 ` |
| ✅ `LocalEntryNotFoundError … outgoing traffic has been disabled` | `HF_HUB_OFFLINE=1` alors que ce modèle n'a jamais été téléchargé | Relance **sans** `HF_HUB_OFFLINE=1` (une fois par taille de `--model`) |
| ✅ `RuntimeWarning: … encountered in matmul` | Avertissement de calcul | **Sans conséquence** |
| ✅ `Tip: experimental MPS backend is available` | Simple conseil technique | **Sans conséquence** |
| `ModuleNotFoundError: No module named 'soundcard'` (ou autre) | Bibliothèques non installées, ou installées pour un autre Python | Refais l'étape 4. Si tu utilises un `.venv`, active-le d'abord |

### Enregistrement

| Ce que tu vois | Cause | Solution |
|---|---|---|
| ✅ `Aucune source de son de l'ordinateur trouvée : … BlackHole n'est pas installé` | BlackHole absent ou non détecté | Étape 6. Pour une réunion en présentiel : ajoute `--audio none` |
| ✅ `La piste du son de l'ordinateur est silencieuse` | La sortie son de macOS ne passe pas par BlackHole | Sortie son = `Casque + BlackHole` (étape 7). Dans Teams/Zoom : haut-parleur = « Identique au système » |
| Tu n'entends plus la visio | Sortie réglée sur **BlackHole 2ch** seul | Choisis `Casque + BlackHole`, pas BlackHole directement |
| Les touches de volume ne marchent plus | Limite de macOS avec les périphériques à sorties multiples | Règle le volume dans l'application de visio. Remets ta sortie habituelle après la réunion |
| Transcription vide ou ta voix absente | macOS bloque l'accès au micro | Étape 8 |
| ✅ `Périphérique « … » introuvable. Lance --list…` | Nom de micro mal écrit | `--list` (étape 9), puis copie le nom exact |
| ✅ Mauvais micro enregistré avec `--mic 1` | Les numéros changent (l'iPhone apparaît ou disparaît) | Utilise le **nom** : `--mic "MacBook Air Microphone"` |
| ✅ `Système détecté : mac, mais --os vaut « windows »` | Mauvaise option `--os` | Retire `--os` (le défaut est `mac`) |
| ✅ `macOS does not support loopback recording functionality` | `--os windows` ou `--os debian` utilisé sur un Mac | Retire `--os` |
| Son de mauvaise qualité avec AirPods ou un casque Bluetooth | macOS passe en mode « appel » quand leur micro est actif | `--mic "MacBook Air Microphone"` (garde les AirPods pour écouter) |
| Ctrl + C avec la touche **Cmd** ne fait rien | Sur Mac, c'est bien **Ctrl** (touche `control`) | Ctrl + C |
| `Commande « claude » introuvable` (`meeting-agent.py`) | Claude Code non installé | Étape 13 |

🤖 **Prompt pour un assistant IA (en cas d'erreur) :**
```text
Je suis sur Mac, dans le dossier local-meeting-transcriber. J'ai lancé : <la commande>
Et j'obtiens cette erreur : <colle le message complet>
Cherche la cause dans la section « Erreurs possibles sur Mac » de docs/config-mac.md. Explique-moi la cause en une phrase,
puis la solution étape par étape. Demande mon accord avant toute installation ou commande avec sudo.
Si l'erreur n'est pas dans le tableau, dis-le clairement au lieu d'inventer.
```

---

## Prompt global : l'agent fait tout avec toi

Ce prompt transforme ton assistant IA (Claude Code, GitHub Copilot Chat **en mode agent**, Cursor…) en guide complet : il te pose des questions précises, vérifie ton installation, installe ce qui manque **avec ton accord**, et te prépare la commande finale (ou la lance lui-même pour un fichier existant).

**Comment l'utiliser :**
1. Ouvre le dossier `local-meeting-transcriber` dans ton éditeur (VS Code : *Fichier > Ouvrir le dossier…*).
2. Ouvre ton assistant IA en mode agent.
3. Copie **tout** le bloc ci-dessous et colle-le.

```text
Tu es mon assistant pour installer et utiliser l'outil local-meeting-transcriber sur mon Mac.
Le dossier ouvert est la racine du projet. Avant tout, lis README.md et docs/config-mac.md : ce sont tes références.

RÈGLES À RESPECTER EN PERMANENCE
- Réponds en français, avec des phrases simples, comme à quelqu'un qui n'est pas développeur.
- Pose les questions ci-dessous UNE PAR UNE, dans l'ordre, et attends ma réponse avant de continuer.
  Propose toujours les choix numérotés indiqués. N'invente pas mes réponses.
- Avant chaque commande, explique en une phrase ce qu'elle fait.
- Demande mon accord explicite avant : toute installation, toute commande avec sudo, toute modification d'un réglage système.
- Les commandes qui demandent mon mot de passe (installation de Homebrew, brew install blackhole-2ch, sudo killall coreaudiod) :
  donne-les-moi pour que je les lance dans mon propre terminal, puis vérifie le résultat quand je te le dis.
- Ne modifie, ne supprime et ne crée aucun fichier du projet. N'ouvre pas, ne lis pas et n'envoie jamais le contenu
  du dossier reunions/ (enregistrements et transcriptions) sans que je te le demande.
- Ne crée jamais de variable ANTHROPIC_API_KEY.
- En cas d'erreur, cherche d'abord dans la section « Erreurs possibles sur Mac » de docs/config-mac.md. Si l'erreur n'y est
  pas, montre-moi le message exact et dis-le clairement, au lieu d'inventer une solution.

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
Q7. (Seulement si Q1 = 3) Quel est le chemin du fichier ? (glisse le fichier dans le chat ou colle son chemin complet)

CE QUE TU FAIS ENSUITE, DANS CET ORDRE (en suivant les étapes de docs/config-mac.md)
1. `pwd` et `ls` : vérifie qu'on est bien à la racine du projet (README.md, docs, script).
2. `python3 --version` : Python 3.9 ou plus (étape 2).
3. `python3 -c "import soundcard, soundfile, faster_whisper, numpy, sherpa_onnx; print('Tout est installé')"`.
   S'il manque quelque chose : propose `pip3 install --user soundcard soundfile faster-whisper numpy sherpa-onnx` (étape 4).
4. Si Q3 = 1 ou 2 : vérifie `brew --version` (étape 5), puis BlackHole (étape 6) avec
   `python3 ./script/meeting-whisper-final.py --list` (doit afficher « BlackHole 2ch ← par défaut »).
   Si Q3 = 1 : demande-moi si le périphérique à sorties multiples « Casque + BlackHole » existe déjà. Sinon, guide-moi
   clic par clic (étape 7).
5. `python3 ./script/meeting-whisper-final.py --list` : recommande-moi un micro (étape 9) et explique pourquoi.
6. Vérifie si le modèle choisi est déjà téléchargé : `ls ~/.cache/huggingface/hub/` doit contenir
   models--Systran--faster-whisper-small (ou -medium). S'il est absent, préviens-moi que le premier lancement téléchargera
   le modèle (~480 Mo pour small, ~1,5 Go pour medium) et n'ajoute PAS HF_HUB_OFFLINE=1 à la commande.
   S'il est présent, ajoute HF_HUB_OFFLINE=1 au début de la commande.
7. Construis la commande finale, avec : le script correspondant à Q2 (meeting-whisper-final.py / meeting-whisper.py /
   meeting-agent.py), --mic "<nom exact du micro>", --audio none si Q3 = 3, --speakers <N> si Q4 est un nombre (script
   final uniquement), --nameFolder <nom> si Q5 n'est pas « aucun », --model medium si Q6 = 2, --file "<chemin>" si Q1 = 3.
8. Si Q1 = 3 (fichier existant) : demande-moi si tu dois lancer la commande toi-même. Si oui, lance-la et montre-moi
   où se trouve le résultat.
   Si Q1 = 2 (enregistrement) : NE LANCE PAS l'enregistrement toi-même (il doit être arrêté avec Ctrl+C dans mon terminal).
   Donne-moi la commande à copier dans le Terminal, précédée de `cd <chemin du projet>`, puis rappelle-moi :
   - la checklist « Avant la réunion » de l'étape 11 (prévenir les participants, sortie son « Casque + BlackHole » en visio) ;
   - d'appuyer sur Ctrl + C (Ctrl, pas Cmd) à la fin ;
   - d'attendre le message « Transcription enregistrée dans … » (ou « Fichiers enregistrés dans … » pour meeting-agent.py) avant de fermer le terminal ;
   - de remettre ma sortie son habituelle après la réunion.
9. Termine par un récapitulatif en 5 lignes : ce qui est installé, le micro choisi, la commande, où sera le résultat,
   comment arrêter.
```
