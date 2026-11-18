# local-meeting-transcriber

**Enregistre tes réunions et obtiens leur transcription écrite, directement sur ton ordinateur.**
Fonctionne sur **Mac**, **Windows** et **Debian** (Linux). Enregistre **ta voix** (le micro) **et le son de la visio** (Teams, Zoom, Meet…).

> 🔒 **Tes réunions restent sur ton ordinateur.** L'audio et la transcription ne sont envoyés nulle part. La seule exception est le compte rendu automatique par Claude, une option que tu dois choisir explicitement (voir plus bas).

---

## Sommaire

1. [Ce que fait cet outil](#1-ce-que-fait-cet-outil)
2. [Comment ça marche](#2-comment-ça-marche)
3. [Ce dont tu as besoin](#3-ce-dont-tu-as-besoin)
4. [Étape 1 : récupérer le projet](#4-étape-1--récupérer-le-projet)
5. [À savoir avant le premier lancement : les modèles et Hugging Face](#5-à-savoir-avant-le-premier-lancement--les-modèles-et-hugging-face)
6. [**Étape 2 : choisis ton système d'exploitation**](#6-étape-2--choisis-ton-système-dexploitation) ← la suite se passe ici
7. [Prompt global : un agent IA fait tout avec toi](#7-prompt-global--un-agent-ia-fait-tout-avec-toi)
8. [Référence commune (options, fichiers produits)](#8-référence-commune)
9. [Bonnes pratiques et protection des données](#9-bonnes-pratiques-et-protection-des-données)
10. [Petit lexique](#10-petit-lexique)

---

## 1. Ce que fait cet outil

Le projet contient **3 scripts**. Choisis celui qui correspond à ce que tu veux obtenir :

| Tu veux… | Script à utiliser | Résultat | Données envoyées sur Internet |
|---|---|---|---|
| **La transcription avec le nom de qui parle** (recommandé) | `meeting-whisper-final.py` | `[0:00:06] Utilisateur 2 : Merci. De mon côté…` | **Aucune** |
| La transcription simple, plus rapide | `meeting-whisper.py` | `[0:00:06] Merci. De mon côté…` | **Aucune** |
| La transcription **et** un compte rendu (résumé, décisions, actions) | `meeting-agent.py` | Transcription + fichier de notes | ⚠️ **Le texte de la transcription est envoyé à Anthropic (Claude), aux États-Unis** |

Si tu hésites, prends **`meeting-whisper-final.py`**.

> ℹ️ « Utilisateur 1 », « Utilisateur 2 »… : l'outil **distingue** les voix, mais ne connaît pas les noms des personnes. C'est à toi de savoir qui est « Utilisateur 1 ».

---

## 2. Comment ça marche

```
   🎤 Ton micro (ta voix) ─────────────┐
                                       ├──► enregistrement (.wav) ──► Whisper (sur ton ordinateur) ──► transcription (.txt)
   🔊 Son de l'ordinateur (la visio) ──┘
```

1. Tu lances une commande au début de la réunion.
2. L'outil enregistre **en même temps** ton micro et le son de l'ordinateur, puis les mélange.
3. À la fin de la réunion, tu appuies sur **Ctrl+C** (les deux touches en même temps) dans la fenêtre du terminal.
4. L'outil transcrit l'enregistrement **sur ton ordinateur**, avec Whisper, un modèle de reconnaissance vocale. Ça prend quelques minutes.
5. Tu retrouves l'audio et le texte dans le dossier `reunions/`, à l'intérieur du projet.

**Pourquoi capter « le son de l'ordinateur » ?** Avec un casque, ton micro n'entend pas les autres participants : leur voix va directement dans tes oreilles. Il faut donc aussi enregistrer ce qui sort de l'ordinateur. Chaque système fait ça différemment, c'est pourquoi la suite dépend de ton système d'exploitation.

---

## 3. Ce dont tu as besoin

| Élément | Pourquoi | Où l'installer |
|---|---|---|
| Un ordinateur Mac, Windows ou Debian | — | — |
| **Python** (version 3.9 ou plus récente) | Le langage dans lequel les scripts sont écrits | Expliqué dans la page de ton système (étape 2) |
| **5 bibliothèques Python** (`soundcard`, `soundfile`, `faster-whisper`, `numpy`, `sherpa-onnx`) | Enregistrer le son, transcrire, reconnaître les voix | Expliqué dans la page de ton système |
| **Mac uniquement : BlackHole** | Capter le son de la visio (macOS ne sait pas le faire seul) | Expliqué dans la page Mac |
| Environ **2 Go d'espace disque** | Bibliothèques + modèle de transcription | — |
| Une connexion Internet **pour l'installation et le premier lancement seulement** | Télécharger les bibliothèques et les modèles | — |
| *(Optionnel)* Claude Code + un compte Claude | Uniquement pour `meeting-agent.py` (compte rendu) | Expliqué dans la page de ton système |

Compte **30 à 45 minutes** pour la toute première installation, dont la plus grande partie en téléchargements.

---

## 4. Étape 1 : récupérer le projet

Cette étape est **la même pour tous les systèmes**. Choisis **une** des deux méthodes.

### Méthode A : télécharger le ZIP (la plus simple, aucun outil nécessaire)

1. Sur la page GitHub du projet, clique sur le bouton vert **`<> Code`**, puis sur **`Download ZIP`**.
2. **Extrais** le fichier `.zip` téléchargé (il est en général dans *Téléchargements*) :
   - **Mac** : double-clic sur le `.zip` ;
   - **Windows** : clic droit sur le `.zip` > **Extraire tout…** > **Extraire**. Un simple double-clic ne fait qu'ouvrir un aperçu, et les scripts ne fonctionneront pas depuis cet aperçu ;
   - **Debian/Ubuntu** : clic droit sur le `.zip` > **Extraire ici**.
3. ⚠️ Le dossier s'appelle probablement **`local-meeting-transcriber-main`**. **Renomme-le en `local-meeting-transcriber`** : toute la documentation utilise ce nom.
4. Déplace ce dossier à un endroit stable, par exemple dans **Documents**.
   - ⚠️ **Évite** les dossiers synchronisés dans le cloud (iCloud Drive, OneDrive, Google Drive) : tes enregistrements de réunion y seraient copiés.

### Méthode B : avec git (si tu connais déjà git)

```bash
git clone <URL_DU_DEPOT>
cd local-meeting-transcriber
```

`<URL_DU_DEPOT>` : l'adresse affichée quand tu cliques sur `<> Code` sur GitHub (onglet *HTTPS*).

### Vérification

Ouvre le dossier `local-meeting-transcriber` : tu dois y voir **`README.md`**, **`script`** et **`docs`**. Si ce n'est pas le cas, tu es dans le mauvais dossier (souvent un dossier « en trop » autour, créé par le ZIP).

> 📝 Retiens l'emplacement de ce dossier : on l'appellera **`<DOSSIER_DU_PROJET>`** dans toute la documentation. Exemples :
> - Mac : `/Users/<ton-nom>/Documents/local-meeting-transcriber`
> - Windows : `C:\Users\<ton-nom>\Documents\local-meeting-transcriber`
> - Debian : `/home/<ton-nom>/Documents/local-meeting-transcriber`

---

## 5. À savoir avant le premier lancement : les modèles et Hugging Face

La transcription utilise des **modèles d'intelligence artificielle** qui tournent **sur ton ordinateur**. Ils ne sont pas inclus dans le projet, car ils sont trop gros. Ils sont **téléchargés automatiquement au premier lancement**, puis réutilisés à chaque fois.

| Modèle | Rôle | Téléchargé depuis | Taille |
|---|---|---|---|
| Whisper `small` (par défaut) | Transformer la voix en texte | **Hugging Face** (site qui héberge des modèles d'IA open source) | ~480 Mo |
| Whisper `medium` / `large-v3` (si tu les choisis) | Transcription plus précise mais plus lente | Hugging Face | ~1,5 Go / ~3 Go |
| Modèles de reconnaissance des voix | Distinguer « Utilisateur 1 », « Utilisateur 2 »… (`meeting-whisper-final.py` uniquement) | GitHub | ~33 Mo |

**Ce qu'il faut savoir :**
- Le **premier lancement est plus long** (plusieurs minutes de téléchargement). C'est normal, et ça n'arrive qu'une fois par modèle.
- Le message **« You are sending unauthenticated requests to the HF Hub »** est **normal** : tu n'as pas besoin de compte Hugging Face. Ignore-le.
- **Seuls les modèles sont téléchargés.** Ton audio et ta transcription ne sont **jamais** envoyés à Hugging Face ni à GitHub.
- Une fois les modèles téléchargés, tu peux **interdire tout accès à Hugging Face** avec le réglage `HF_HUB_OFFLINE=1`. La façon de l'écrire dépend du système : elle est donnée dans chaque page.
  - ⚠️ N'utilise **pas** ce réglage au tout premier lancement, sinon le modèle ne peut pas se télécharger (erreur `LocalEntryNotFoundError`).

---

## 6. Étape 2 : choisis ton système d'exploitation

**La suite dépend de ton système d'exploitation** : les commandes, l'installation de Python et la façon de capter le son de la visio sont différentes. **Clique sur ta page** et suis-la dans l'ordre, sans sauter d'étape :

| Ton ordinateur | Ta page | Ce qui est spécifique |
|---|---|---|
| 🍎 **Mac** (MacBook, iMac…) | 👉 **[docs/config-mac.md](docs/config-mac.md)** | Installation de **BlackHole** pour capter la visio |
| 🪟 **Windows** (10 ou 11) | 👉 **[docs/config-windows.md](docs/config-windows.md)** | Rien à installer pour la visio. Toujours ajouter `--os windows` |
| 🐧 **Debian** (et Ubuntu, Linux Mint…) | 👉 **[docs/config-debian.md](docs/config-debian.md)** | Environnement virtuel Python obligatoire. Toujours ajouter `--os debian` |

> ❓ **Tu ne sais pas quel est ton système ?** Une pomme 🍎 en haut à gauche de l'écran : c'est un **Mac**. Un bouton Démarrer avec le logo Windows en bas à gauche : c'est **Windows**. Sinon, c'est probablement **Linux** : demande à ton service informatique s'il s'agit de Debian ou d'Ubuntu.

Chaque page contient, **pour chaque étape** :
- les commandes exactes à copier-coller ;
- comment vérifier que l'étape a marché ;
- un **prompt prêt à l'emploi** pour qu'un assistant IA (Claude Code, GitHub Copilot en mode agent…) t'aide sur cette étape ;
- les **erreurs possibles** sur ton système et leur solution.

---

## 7. Prompt global : un agent IA fait tout avec toi

Si tu utilises un assistant IA capable de lancer des commandes (**Claude Code**, **GitHub Copilot Chat en mode agent**, Cursor…), il peut t'accompagner de A à Z : installation, vérifications, choix du micro et commande finale.

1. Ouvre ton assistant **dans le dossier `local-meeting-transcriber`** (dans VS Code : *Fichier > Ouvrir le dossier…*).
2. Copie le prompt global de **ta** page :
   - Mac : [section « Prompt global » de config-mac.md](docs/config-mac.md#prompt-global--lagent-fait-tout-avec-toi)
   - Windows : [section « Prompt global » de config-windows.md](docs/config-windows.md#prompt-global--lagent-fait-tout-avec-toi)
   - Debian : [section « Prompt global » de config-debian.md](docs/config-debian.md#prompt-global--lagent-fait-tout-avec-toi)
3. Colle-le dans l'assistant et réponds à ses questions.

L'agent te pose **des questions précises et toujours les mêmes** (ce que tu veux faire, type de réunion, nombre de participants…). Il **demande ton accord avant toute installation** et ne touche **jamais** au contenu de tes réunions.

---

## 8. Référence commune

Cette section est **identique pour tous les systèmes**. Seule la façon d'écrire la commande change (`python3` ou `py`, `/` ou `\`), comme expliqué dans ta page.

### Options des scripts

| Option | Rôle | Si tu ne la mets pas | Scripts |
|---|---|---|---|
| `--os mac` / `--os windows` / `--os debian` | Indique ton système, pour savoir comment capter le son de la visio | `mac`. ⚠️ **Sous Windows et Debian, il faut toujours l'ajouter** | les 3 |
| `--list` | Affiche les micros et les sources de son de l'ordinateur disponibles, puis s'arrête. N'enregistre rien | — | les 3 |
| `--mic "<nom>"` | Le micro à enregistrer (ta voix). Mets le **nom** affiché par `--list` (une partie du nom suffit) | Le micro par défaut de ton système | les 3 |
| `--audio "<nom>"` | La source du son de l'ordinateur (la visio) | Choisie automatiquement selon `--os` | les 3 |
| `--audio none` | N'enregistre **que** le micro (réunion en présentiel) | — | les 3 |
| `--model small` | Taille du modèle : `tiny`, `base`, `small`, `medium`, `large-v3`. Plus gros = plus précis mais plus lent | `small` | les 3 |
| `--file <chemin>` | Transcrit un fichier audio ou vidéo **existant** au lieu d'enregistrer | — | `meeting-whisper.py`, `meeting-whisper-final.py` |
| `--speakers <nombre>` | Nombre de personnes qui parlent (toi compris), si tu le connais. **C'est le réglage le plus fiable** | Détection automatique | `meeting-whisper-final.py` |
| `--threshold 0.5` | Sans `--speakers` : baisse à `0.4` si deux personnes sont fusionnées, monte à `0.6` si une personne apparaît en double. N'utilise pas de valeurs extrêmes (à `0.1`, une même voix est coupée en deux) | `0.5` | `meeting-whisper-final.py` |
| `--nameFolder <nom>` | Range la réunion dans `reunions/<nom>/1/`, puis `2/`, `3/`… Un simple nom, sans `/` ni `\` | Fichiers rangés directement dans `reunions/` | `meeting-whisper-final.py` |

> ⚠️ `--device` est l'ancien nom de `--mic`. Il fonctionne encore, mais utilise `--mic`.

### Fichiers produits

Ils se trouvent dans le dossier **`reunions/`**, créé **dans le dossier où tu te trouves** quand tu lances la commande. Lance donc toujours les commandes **depuis `<DOSSIER_DU_PROJET>`**.

| Fichier | Contenu |
|---|---|
| `AAAA-MM-JJ_HHMM.wav` | L'enregistrement complet (micro + son de l'ordinateur mélangés), celui qui est transcrit |
| `AAAA-MM-JJ_HHMM_micro.wav` | Ton micro seul (uniquement si le son de l'ordinateur était capté aussi) |
| `AAAA-MM-JJ_HHMM_audio.wav` | Le son de l'ordinateur seul (idem) |
| `…_transcription.txt` | La transcription (`meeting-whisper.py`, `meeting-agent.py`) |
| `…_transcription_intervenants.txt` | La transcription avec « Utilisateur 1 », « Utilisateur 2 »… (`meeting-whisper-final.py`) |
| `…_notes.md` | Le compte rendu de Claude (`meeting-agent.py`) |

### Durées indicatives (sur un ordinateur portable récent)

| Pour 1 h de réunion | Durée de traitement après le Ctrl+C |
|---|---|
| `meeting-whisper.py`, modèle `small` | Quelques minutes à ~15 min |
| `meeting-whisper-final.py`, modèle `small` | ~15 min pour reconnaître les voix + le temps de transcription |
| Modèle `medium` ou `large-v3` | Nettement plus long |

Pendant le traitement, **laisse le terminal ouvert et l'ordinateur allumé**.

### Documentation technique

- Architecture et souveraineté de chaque script : [docs/architecture-meeting-whisper.md](docs/architecture-meeting-whisper.md), [docs/architecture-meeting-whisper-final.md](docs/architecture-meeting-whisper-final.md), [docs/architecture-meeting-agent.md](docs/architecture-meeting-agent.md)
- Plan de la future application (v2) : [docs/superpowers/plans/](docs/superpowers/plans/)

### Structure du projet

```
local-meeting-transcriber/
├── README.md                 ← tu es ici
├── .gitignore                # empêche l'envoi de reunions/ et de l'audio sur GitHub
├── script/
│   ├── audio_capture.py      # module commun : micro + son de l'ordinateur (mac/windows/debian)
│   ├── meeting-whisper.py
│   ├── meeting-whisper-final.py
│   └── meeting-agent.py
├── docs/
│   ├── config-mac.md         # guide Mac
│   ├── config-windows.md     # guide Windows
│   ├── config-debian.md      # guide Debian
│   └── architecture-*.md     # documentation technique
└── reunions/                 # créé automatiquement : tes enregistrements et transcriptions
```

---

## 9. Bonnes pratiques et protection des données

- **Préviens toujours les participants** que la réunion est enregistrée. C'est une obligation légale (RGPD).
- Les fichiers de `reunions/` **ne sont ni chiffrés ni supprimés automatiquement**. Supprime-les quand tu n'en as plus besoin.
- **Ne mets pas le projet dans un dossier synchronisé** (iCloud Drive, OneDrive, Google Drive).
- Le dossier `reunions/` est **exclu de git** par le fichier `.gitignore` : tes réunions ne sont jamais envoyées sur GitHub, même si tu fais un `git push`.
- **`meeting-agent.py` envoie le texte de la transcription à Anthropic (États-Unis).** Avant de l'utiliser pour une réunion confidentielle, lis [docs/architecture-meeting-agent.md](docs/architecture-meeting-agent.md) et vérifie que tu es connecté avec le **compte de ton entreprise**.

---

## 10. Petit lexique

| Mot | Signification |
|---|---|
| **Terminal** | Une fenêtre où l'on tape des commandes au clavier (au lieu de cliquer). Chaque page explique comment l'ouvrir |
| **Commande** | Une ligne de texte à copier dans le terminal, puis à valider avec la touche **Entrée** |
| **Ctrl+C** | Appuyer sur **Ctrl** et **C** en même temps dans le terminal : arrête l'enregistrement. Sur Mac aussi, c'est bien **Ctrl** (pas Cmd) |
| **Chemin** | L'adresse d'un dossier ou d'un fichier, par exemple `/Users/marie/Documents/local-meeting-transcriber` |
| **`<DOSSIER_DU_PROJET>`** | À remplacer par le chemin de **ton** dossier `local-meeting-transcriber`, **sans les `< >`** |
| **Micro** | Ce qui capte ta voix : micro intégré, micro du casque, micro USB… |
| **Son de l'ordinateur** | Ce qui sort de tes haut-parleurs ou de ton casque : la voix des autres participants pendant une visio |
| **Modèle** | Le « cerveau » de reconnaissance vocale, téléchargé une fois puis utilisé sur ton ordinateur |
| **Agent / assistant IA** | Claude Code, GitHub Copilot en mode agent… : une IA qui peut lire le projet et lancer des commandes pour toi, avec ton accord |
