# Guide Windows 🪟 : installer et utiliser local-meeting-transcriber

> **Tu es au bon endroit si** ton ordinateur est sous **Windows 10 ou 11**.
> Sur Mac : [config-mac.md](config-mac.md). Sous Debian/Ubuntu : [config-debian.md](config-debian.md).
>
> **Avant de commencer**, tu dois avoir fait l'**étape 1 du [README](../README.md#4-étape-1--récupérer-le-projet)** : récupérer le projet dans un dossier nommé `local-meeting-transcriber`.

> 🧪 **À savoir :** la version Windows est écrite et documentée, mais **elle n'a pas encore été testée sur un vrai PC Windows**. Si une étape ne se passe pas comme décrit, note le message exact et signale-le, pour qu'on complète ce guide.

Suis les étapes **dans l'ordre**. Chaque étape indique **quoi faire**, **comment vérifier que ça a marché**, et donne un **prompt pour un assistant IA** si tu veux de l'aide. Tu préfères qu'un agent fasse tout avec toi ? Va directement au [prompt global](#prompt-global--lagent-fait-tout-avec-toi), en bas de page.

## Les 3 différences à retenir sous Windows

| Sur Mac ou dans les autres docs | **Sous Windows** |
|---|---|
| `python3` | **`py`** |
| `./script/…` | **`.\script\…`** |
| (rien) | **Ajoute toujours `--os windows`** à tes commandes. Sans ça, l'outil se croit sur Mac et **ne capte pas le son de la visio** |

Et une bonne nouvelle : **pas de BlackHole à installer**. Windows sait capter le son de l'ordinateur tout seul (fonction « loopback »).

## Le parcours en un coup d'œil

| # | Étape | Une seule fois ? | Durée |
|---|---|---|---|
| 1 | [Ouvrir PowerShell](#étape-1--ouvrir-powershell) | À chaque utilisation | 1 min |
| 2 | [Installer Python](#étape-2--installer-python) | ✅ Une fois | 5 min |
| 3 | [Aller dans le dossier du projet](#étape-3--aller-dans-le-dossier-du-projet) | À chaque utilisation | 1 min |
| 4 | [Installer les bibliothèques](#étape-4--installer-les-bibliothèques-python) | ✅ Une fois | 5 min |
| 5 | [Autoriser le micro](#étape-5--autoriser-le-micro) | ✅ Une fois | 1 min |
| 6 | [Vérifier le son de l'ordinateur](#étape-6--vérifier-le-son-de-lordinateur-la-visio) | ✅ Une fois (puis si tu changes de casque) | 2 min |
| 7 | [Choisir son micro](#étape-7--choisir-son-micro) | ✅ Une fois | 2 min |
| 8 | [Premier essai](#étape-8--premier-essai-30-secondes) | ✅ Une fois | 10 min |
| 9 | [Utilisation pour une vraie réunion](#étape-9--utilisation-pour-une-vraie-réunion) | À chaque réunion | — |
| 10 | [Après la réunion](#étape-10--après-la-réunion) | À chaque réunion | 1 min |
| 11 | [*(Optionnel)* Compte rendu par Claude](#étape-11-optionnel--compte-rendu-par-claude) | ✅ Une fois | 10 min |

**Comment lire les commandes de cette page :**
- Un bloc gris = **une commande à copier**. Colle-la dans PowerShell (**clic droit** ou **Ctrl + V**), puis appuie sur **Entrée**.
- Ne copie pas le début de ligne `PS C:\…>` : il fait partie de l'invite, pas de la commande.
- Remplace tout ce qui est entre `< >` (par exemple `<DOSSIER_DU_PROJET>`), **en retirant les `< >`**.

---

## Étape 1 : ouvrir PowerShell

1. Clique sur le bouton **Démarrer** (ou appuie sur la touche **Windows**).
2. Tape **`PowerShell`**, puis clique sur **Windows PowerShell** (ou **Terminal**).
3. Une fenêtre s'ouvre avec une ligne du type **`PS C:\Users\marie>`** : c'est ici que tu tapes les commandes.

*Alternative :* dans **VS Code**, menu *Terminal > Nouveau terminal* (PowerShell par défaut).

> ⚠️ Pas besoin d'ouvrir PowerShell « en tant qu'administrateur ». Ouvre-le normalement.

✅ **Vérification :** tu vois une ligne qui commence par `PS C:\`.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Windows et je débute avec PowerShell. Explique-moi, étape par étape, comment ouvrir PowerShell
(menu Démarrer, ou VS Code > Terminal > Nouveau terminal), comment y coller une commande (clic droit ou Ctrl + V)
et la valider, et ce que signifie « PS C:\…> » en début de ligne. Précise que l'ouvrir en administrateur n'est pas
nécessaire. Ne lance aucune commande.
```

---

## Étape 2 : installer Python

**Vérifie d'abord s'il est déjà installé :**
```powershell
py --version
```

| Ce que tu vois | Ce que ça veut dire | Quoi faire |
|---|---|---|
| `Python 3.12.x` (ou 3.10, 3.11) | ✅ Python est installé | Passe à l'étape 3 |
| `py : Le terme « py » n'est pas reconnu…` | Python n'est pas installé | Installe-le (ci-dessous) |
| `Python 3.8` ou moins | Trop ancien | Installe une version récente (ci-dessous) |

> ⚠️ Sous Windows, n'utilise **pas** `python3` : cette commande ouvre souvent le **Microsoft Store** au lieu de Python. Utilise **`py`**.

**Installation (au choix) :**

- **Méthode A, en une commande** (Windows 10/11 récents) :
  ```powershell
  winget install --id Python.Python.3.12 -e
  ```
  Accepte les conditions (`Y` puis **Entrée**) si demandé.

- **Méthode B, depuis le site officiel :**
  1. Va sur [python.org/downloads](https://www.python.org/downloads/windows/) et télécharge **Python 3.12** (« Windows installer (64-bit) »).
  2. Lance l'installateur.
  3. ⚠️ **Coche « Add python.exe to PATH »** en bas de la première fenêtre. **C'est l'erreur la plus fréquente.**
  4. Clique sur **Install Now**.

Ensuite, **ferme PowerShell et rouvre-le** (indispensable), puis relance `py --version`.

> ℹ️ Python 3.12 est recommandé : certaines bibliothèques de transcription peuvent ne pas encore exister pour les toutes dernières versions de Python.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Windows, dans PowerShell. Vérifie si Python est installé avec `py --version` (pas python3).
S'il est absent ou plus ancien que 3.10, explique-moi comment installer Python 3.12, soit avec
`winget install --id Python.Python.3.12 -e`, soit depuis python.org en cochant « Add python.exe to PATH ».
Demande mon accord avant de lancer quoi que ce soit, et rappelle-moi de fermer puis rouvrir PowerShell ensuite.
```

---

## Étape 3 : aller dans le dossier du projet

PowerShell doit « se placer » dans le dossier du projet, sinon il ne trouve pas les scripts.

1. Tape **`cd `** (c, d, puis **un espace**). **N'appuie pas encore sur Entrée.**
2. Dans l'Explorateur de fichiers, **fais glisser le dossier `local-meeting-transcriber`** dans la fenêtre PowerShell : son chemin s'écrit tout seul.
   *(Ou tape le chemin entre guillemets, par exemple `"C:\Users\marie\Documents\local-meeting-transcriber"`.)*
3. Appuie sur **Entrée**.

Ça donne par exemple :
```powershell
cd "C:\Users\marie\Documents\local-meeting-transcriber"
```

✅ **Vérification :**
```powershell
dir
```
Tu dois voir au moins **`README.md`**, **`docs`** et **`script`**. Sinon, tu es dans le mauvais dossier. Souvent, le ZIP a créé un dossier « en trop » : fais `cd local-meeting-transcriber-main` ou `cd local-meeting-transcriber`, puis `dir`.

> 📝 Ce chemin, c'est ton **`<DOSSIER_DU_PROJET>`**. Pour l'afficher à tout moment : `pwd`.
>
> ⚠️ **À refaire à chaque nouvelle fenêtre PowerShell.** Les enregistrements sont créés dans le dossier où se trouve PowerShell.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Windows, dans PowerShell. Vérifie que je suis bien dans le dossier du projet local-meeting-transcriber :
lance `pwd` puis `dir`, et confirme que README.md, docs et script sont présents.
Sinon, aide-moi à trouver le bon dossier et donne-moi la commande `cd "..."` exacte (avec guillemets). Ne modifie aucun fichier.
```

---

## Étape 4 : installer les bibliothèques Python

Depuis le dossier du projet (étape 3) :

```powershell
py -m pip install soundcard soundfile faster-whisper numpy sherpa-onnx
```

Ça télécharge et installe les outils d'enregistrement et de transcription. Compte quelques minutes. Beaucoup de lignes défilent : c'est normal.

**Messages normaux, à ignorer :**
- `WARNING: The script … is installed in '…\Scripts' which is not on PATH` ;
- `[notice] A new release of pip is available`.

✅ **Vérification :** l'avant-dernière ligne commence par **`Successfully installed`**. Puis lance :
```powershell
py -c "import soundcard, soundfile, faster_whisper, numpy, sherpa_onnx; print('Tout est installé')"
```
Tu dois voir **`Tout est installé`**.

Si tu vois une erreur qui contient **`DLL load failed`** : il manque des composants Microsoft. Installe-les, puis réessaie :
```powershell
winget install --id Microsoft.VCRedist.2015+.x64 -e
```

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Windows, dans PowerShell, dans le dossier local-meeting-transcriber. Installe les dépendances avec
`py -m pip install soundcard soundfile faster-whisper numpy sherpa-onnx` (demande-moi mon accord avant),
puis vérifie avec `py -c "import soundcard, soundfile, faster_whisper, numpy, sherpa_onnx; print('Tout est installé')"`.
En cas d'erreur « DLL load failed », propose `winget install --id Microsoft.VCRedist.2015+.x64 -e`.
Pour toute autre erreur, consulte la section « Erreurs possibles sous Windows » de docs/config-windows.md.
```

---

## Étape 5 : autoriser le micro

Windows peut bloquer l'accès au micro pour les programmes de bureau, dont Python. Dans ce cas, l'enregistrement est **silencieux** et la transcription vide.

1. Ouvre **Paramètres** (touche **Windows + I**).
2. Va dans **Confidentialité et sécurité > Microphone**.
3. Active ces 3 interrupteurs :
   - **Accès au microphone** ;
   - **Autoriser les applications à accéder à votre microphone** ;
   - **Autoriser les applications de bureau à accéder à votre microphone** (tout en bas de la page). **C'est celui-ci qui concerne Python.**

✅ **Vérification :** les 3 interrupteurs sont sur **Activé**.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Windows. Mes enregistrements de local-meeting-transcriber sont silencieux.
Guide-moi pour vérifier, dans Paramètres > Confidentialité et sécurité > Microphone, les 3 réglages de l'étape 5
de docs/config-windows.md, en particulier « Autoriser les applications de bureau à accéder à votre microphone ».
```

---

## Étape 6 : vérifier le son de l'ordinateur (la visio)

**Rien à installer sous Windows.** L'outil enregistre automatiquement ce qui sort de la **sortie son par défaut** de Windows (fonction « loopback »). Il faut juste que la visio sorte bien **par cette sortie**.

1. Ouvre **Paramètres > Système > Son**.
2. Dans **Sortie**, choisis le casque ou les haut-parleurs sur lesquels **tu écoutes tes visios**.
3. Dans ton application de visio (Teams, Zoom…), dans ses paramètres audio, règle le **haut-parleur** sur **le même appareil**, ou sur **« Par défaut »** / **« Identique au système »**.

> ⚠️ **Si Teams envoie le son vers un casque alors que la sortie par défaut de Windows est les haut-parleurs, la visio ne sera pas enregistrée.** Les deux doivent être identiques.

✅ **Vérification** (depuis le dossier du projet) :
```powershell
py .\script\meeting-whisper-final.py --os windows --list
```
En bas, sous **`Son de l'ordinateur (--audio), pour --os windows :`**, ton casque ou tes haut-parleurs doivent apparaître avec **`← par défaut`**.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Windows, dans le dossier local-meeting-transcriber. Lance
`py .\script\meeting-whisper-final.py --os windows --list` (lecture seule) et dis-moi quelle sortie son sera enregistrée
comme « son de l'ordinateur ». Rappelle-moi de vérifier que Paramètres > Système > Son > Sortie et le haut-parleur
de mon application de visio utilisent le même appareil (étape 6 de docs/config-windows.md).
```

---

## Étape 7 : choisir son micro

Depuis le dossier du projet :
```powershell
py .\script\meeting-whisper-final.py --os windows --list
```

Exemple de résultat :
```
Micros (--mic) :
  0  Réseau de microphones (Realtek(R) Audio)  ← par défaut
  1  Casque (Jabra Evolve2 65)

Son de l'ordinateur (--audio), pour --os windows :
     Haut-parleurs (Realtek(R) Audio)  ← par défaut
     Casque (Jabra Evolve2 65)
```

**Comment lire ce résultat :**
- **Micros** : ce qui peut capter **ta voix**. `← par défaut` indique celui qui sera utilisé si tu ne précises rien (le micro choisi dans *Paramètres > Système > Son > Entrée*).
- **Son de l'ordinateur** : ce qui capte **la visio**, c'est-à-dire ta sortie son par défaut (étape 6).

**Quel micro choisir ?**

| Micro | Pour une transcription |
|---|---|
| Micro intégré du PC (« Réseau de microphones »…), micro USB, micro de casque filaire ou USB | ✅ **Recommandé** |
| Casque Bluetooth | ⚠️ Windows passe en mode « mains libres » quand son micro est utilisé, et la qualité baisse. Préfère le micro du PC |
| « Stereo Mix » / « Mixage stéréo » | ❌ Ce n'est pas un micro : c'est le son de l'ordinateur |

**Utilise toujours le nom du micro, jamais son numéro.** Une partie du nom suffit :
```powershell
--mic "Réseau de microphones"
```

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Windows, dans le dossier local-meeting-transcriber. Lance
`py .\script\meeting-whisper-final.py --os windows --list` (lecture seule, n'enregistre rien). Puis dis-moi :
- le micro utilisé par défaut ;
- pour chaque micro, s'il est conseillé (intégré, USB ou filaire = conseillé ; Bluetooth = qualité réduite ;
  « Mixage stéréo » = pas un micro) ;
- quelle sortie sera enregistrée comme son de l'ordinateur ;
- l'option exacte à utiliser : --mic "<nom exact>".
```

---

## Étape 8 : premier essai (30 secondes)

Ce premier essai **télécharge les modèles** (~500 Mo, une seule fois) et vérifie que **ta voix et le son de l'ordinateur** sont bien enregistrés.

1. Ouvre une vidéo YouTube avec quelqu'un qui parle, **en pause**, sur la sortie son choisie à l'étape 6.
2. Dans PowerShell, depuis le dossier du projet, lance (remplace le nom du micro par le tien, étape 7) :
   ```powershell
   py .\script\meeting-whisper-final.py --os windows --mic "Réseau de microphones" --nameFolder essai
   ```
   *(Réunions en présentiel uniquement : ajoute `--audio none` à la fin.)*
3. Quand tu vois **`Enregistrement — micro : « … » + son de l'ordinateur : « … »… Ctrl+C pour arrêter.`** :
   - lance la vidéo ;
   - parle aussi un peu toi-même (« Ceci est un test du micro »).
4. Au bout de 30 secondes, clique dans PowerShell et appuie sur **Ctrl + C**.
5. **Attends** : le premier lancement télécharge les modèles (plusieurs minutes). Tu verras passer :
   - `Identification des intervenants (sherpa-onnx)…`
   - `Transcription locale (whisper small)…`
   - puis les lignes de transcription.
6. C'est fini quand tu vois **`Transcription enregistrée dans reunions\essai\1\…`**.

**Messages normaux, à ignorer :** `You are sending unauthenticated requests to the HF Hub`, un avertissement de Hugging Face qui parle de `symlinks` ou de `Developer Mode`, `RuntimeWarning: … encountered in matmul`.

✅ **Vérification :**
- la transcription contient **ta phrase** et **des phrases de la vidéo** ;
- le dossier contient 4 fichiers (`….wav`, `…_micro.wav`, `…_audio.wav`, `…_transcription_intervenants.txt`). Ouvre-le avec :
  ```powershell
  explorer .\reunions\essai\1
  ```

| Problème | Cause probable |
|---|---|
| Ta voix manque | Micro bloqué (étape 5) ou mauvais micro (étape 7) |
| La vidéo manque + message « piste du son de l'ordinateur est silencieuse » | La vidéo ne sort pas par la sortie par défaut (étape 6) |
| Message « Système détecté : windows, mais --os vaut « mac » » | Tu as oublié `--os windows` |

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Windows, dans le dossier local-meeting-transcriber. Je viens de faire le premier essai de l'étape 8
de docs/config-windows.md avec :
py .\script\meeting-whisper-final.py --os windows --mic "<mon micro>" --nameFolder essai
Voici ce que PowerShell a affiché : <colle ici la sortie>
Analyse le résultat : ma voix et le son de l'ordinateur ont-ils été enregistrés ? Si non, trouve la cause avec le tableau
de l'étape 8 et la section « Erreurs possibles sous Windows », et dis-moi précisément quoi corriger.
Tu peux lister reunions\essai\ mais n'ouvre pas les fichiers audio ou texte sans mon accord.
```

---

## Étape 9 : utilisation pour une vraie réunion

### Avant la réunion (checklist)

1. ☐ **Préviens les participants** que la réunion est enregistrée (obligation RGPD).
2. ☐ **Visio :** sortie son de Windows = l'appareil que tu écoutes, et le même dans Teams/Zoom (étape 6).
3. ☐ Branche ton PC sur secteur et évite la mise en veille pendant la réunion et le traitement.
4. ☐ Ouvre PowerShell et place-toi dans le projet : `cd "<DOSSIER_DU_PROJET>"` (étape 3).
5. ☐ Lance la commande **au début** de la réunion.

### Le mode « hors ligne » sous PowerShell

Après le premier essai (étape 8), tu peux interdire tout accès à Internet pour les modèles. **Sous PowerShell, ça se fait en deux temps :**
```powershell
$env:HF_HUB_OFFLINE=1
```
puis ta commande habituelle. Le réglage reste actif **jusqu'à la fermeture de la fenêtre PowerShell**. Pour l'annuler sans fermer la fenêtre : `Remove-Item Env:HF_HUB_OFFLINE`.

> ⚠️ N'écris **pas** `HF_HUB_OFFLINE=1 py …` sur une seule ligne comme sur Mac : PowerShell ne le comprend pas.

### Les commandes

Toutes les commandes se lancent **depuis `<DOSSIER_DU_PROJET>`** (étape 3), **avec `--os windows`**.

**Transcription avec intervenants (recommandé) :**
```powershell
py .\script\meeting-whisper-final.py --os windows --mic "Réseau de microphones" --speakers 4 --nameFolder projetX
```
- `--speakers 4` : le nombre de personnes qui parlent, **toi compris**. Si tu ne sais pas, enlève cette option.
- `--nameFolder projetX` : range la réunion dans `reunions\projetX\1\`, puis `2\`, `3\`… Choisis un nom simple, sans espace ni `\` (par exemple `comite-direction`).

**Transcription simple (plus rapide, sans intervenants) :**
```powershell
py .\script\meeting-whisper.py --os windows --mic "Réseau de microphones"
```

**Réunion en présentiel (pas de visio) :** ajoute `--audio none`.
```powershell
py .\script\meeting-whisper-final.py --os windows --mic "Réseau de microphones" --audio none --speakers 5 --nameFolder projetX
```

**Transcrire un fichier audio ou vidéo existant** (`.wav`, `.mp3`, `.m4a`, `.mp4`…). Mets le chemin **entre guillemets**. Astuce : glisse le fichier dans PowerShell.
```powershell
py .\script\meeting-whisper-final.py --os windows --file "C:\Users\marie\Downloads\reunion.mp4" --speakers 3 --nameFolder projetX
```

**Depuis n'importe quel dossier (chemin absolu, entre guillemets) :**
```powershell
cd "<DOSSIER_DU_PROJET>"
py "<DOSSIER_DU_PROJET>\script\meeting-whisper-final.py" --os windows --mic "Réseau de microphones" --nameFolder projetX
```
> ⚠️ Fais quand même le `cd` d'abord : le dossier `reunions` est créé **dans le dossier où se trouve PowerShell**.

### Pendant et à la fin de la réunion

1. Laisse la fenêtre PowerShell ouverte (tu peux la réduire).
2. À la fin : clique dans PowerShell, puis **Ctrl + C**.
3. **N'éteins pas le PC et ne ferme pas PowerShell** avant le message `Transcription enregistrée dans …` (ou `Fichiers enregistrés dans …` avec `meeting-agent.py`). Pour 1 h de réunion, compte 15 à 30 minutes de traitement.

Toutes les options : [README, section Référence commune](../README.md#8-référence-commune).

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Windows, dans le dossier local-meeting-transcriber, et l'installation est terminée.
Je vais faire une réunion : <visio avec casque / visio sans casque / présentiel>, avec <N ou « je ne sais pas »> participants,
et je veux ranger le résultat dans le dossier <nom>. Lance `py .\script\meeting-whisper-final.py --os windows --list`
pour vérifier mon micro et la sortie son, puis donne-moi les commandes exactes à lancer moi-même dans PowerShell
(avec --os windows), en suivant l'étape 9 de docs/config-windows.md. Rappelle-moi la checklist et comment arrêter.
```

---

## Étape 10 : après la réunion

1. **Ouvre le dossier du résultat** (adapte le nom) :
   ```powershell
   explorer .\reunions\projetX
   ```
   Le fichier à lire est `…_transcription_intervenants.txt` (ou `…_transcription.txt`). Il s'ouvre avec le Bloc-notes, et les accents s'affichent correctement (UTF-8).
2. **Supprime les enregistrements** dont tu n'as plus besoin : ce sont des données personnelles.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Windows, dans le dossier local-meeting-transcriber. Liste les dossiers et fichiers de reunions\
(noms et tailles uniquement, sans ouvrir leur contenu), indique-moi où est la transcription de ma dernière réunion
et donne-moi la commande `explorer` pour ouvrir son dossier. Ne supprime rien sans mon accord explicite.
```

---

## Étape 11 *(optionnel)* : compte rendu par Claude

> ⚠️ **Avec cette option, le texte de la transcription est envoyé à Anthropic (États-Unis).** Pour une réunion confidentielle, lis d'abord [architecture-meeting-agent.md](architecture-meeting-agent.md) et utilise le **compte de ton entreprise**.

1. Installe Node.js puis Claude Code (ferme et rouvre PowerShell entre les deux) :
   ```powershell
   winget install --id OpenJS.NodeJS.LTS -e
   ```
   ```powershell
   npm install -g @anthropic-ai/claude-code
   ```
   Si l'installation échoue, suis la documentation officielle de Claude Code pour Windows : certaines versions demandent aussi **Git for Windows**.
2. Lance `claude` une fois et connecte-toi **avec le compte de ton entreprise**. Tape `/status` pour vérifier, puis `/exit`.
   - Si PowerShell répond `l'exécution de scripts est désactivée sur ce système`, lance d'abord : `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (réponds `O` pour Oui), puis réessaie.
3. **Ne définis pas** de variable `ANTHROPIC_API_KEY`.
4. Utilisation, depuis le dossier du projet :
   ```powershell
   py .\script\meeting-agent.py --os windows --mic "Réseau de microphones"
   ```
   Après le **Ctrl + C**, tu obtiens dans `reunions\` la transcription **et** un fichier `…_notes.md`.

✅ **Vérification :** `where.exe claude` affiche un chemin. Attention, écris bien `where.exe` : sous PowerShell, `where` tout court fait autre chose.

🤖 **Prompt pour un assistant IA :**
```text
Je suis sous Windows. Vérifie si Node.js (`node --version`) et Claude Code (`where.exe claude`) sont installés.
S'il manque quelque chose, propose-moi les commandes de l'étape 11 de docs/config-windows.md et attends mon accord.
Rappelle-moi de me connecter avec le compte de mon entreprise (/status). Ne crée jamais de variable ANTHROPIC_API_KEY.
```

---

## Erreurs possibles sous Windows

> Ces solutions viennent des problèmes connus sous Windows. **Elles n'ont pas encore été vérifiées sur un vrai PC** : si tu rencontres une erreur absente du tableau, note le message exact.

### Installation

| Ce que tu vois | Cause | Solution |
|---|---|---|
| `python3` ouvre le **Microsoft Store** | Raccourci de Windows qui remplace Python | Utilise **`py`** (étape 2) |
| `py : Le terme « py » n'est pas reconnu…` | Python n'est pas installé | Étape 2, puis ferme et rouvre PowerShell |
| `python` fonctionne mais pas `py` | Python installé sans le lanceur `py` | Utilise `python` à la place de `py` dans toutes les commandes |
| `pip : Le terme « pip » n'est pas reconnu` | pip n'est pas dans le PATH | Utilise **`py -m pip install …`** (étape 4) |
| `WARNING: The script … is not on PATH` | Outils annexes installés hors du PATH | **Sans conséquence**, ignore |
| `DLL load failed while importing …` | Composants Microsoft Visual C++ manquants | `winget install --id Microsoft.VCRedist.2015+.x64 -e`, puis réessaie |
| `ERROR: Could not find a version that satisfies the requirement …` | Python trop récent ou en 32 bits | Installe **Python 3.12 64 bits** (étape 2) |
| `winget : Le terme « winget » n'est pas reconnu` | Windows ancien ou winget désactivé | Utilise la méthode B (site officiel) |

### Premier lancement

| Ce que tu vois | Cause | Solution |
|---|---|---|
| `You are sending unauthenticated requests to the HF Hub` | Téléchargement sans compte Hugging Face | **Normal**, attends |
| Avertissement Hugging Face sur les `symlinks` / le `Developer Mode` | Windows limite les liens symboliques | **Sans conséquence** (le cache prend un peu plus de place) |
| Téléchargement bloqué (rien ne bouge pendant plus de 5 min) | Système de téléchargement « Xet » bloqué | Ctrl+C, puis `$env:HF_HUB_DISABLE_XET=1` et relance la commande |
| `LocalEntryNotFoundError … outgoing traffic has been disabled` | `HF_HUB_OFFLINE` activé alors que le modèle n'est pas téléchargé | `Remove-Item Env:HF_HUB_OFFLINE`, puis relance |
| Le pare-feu ou le proxy de l'entreprise bloque le téléchargement | Réseau d'entreprise filtré | Demande au service informatique d'autoriser `huggingface.co` et `github.com`, ou fais le premier lancement depuis un autre réseau |

### Enregistrement

| Ce que tu vois | Cause | Solution |
|---|---|---|
| `Système détecté : windows, mais --os vaut « mac »` et la visio n'est pas enregistrée | `--os windows` oublié | Ajoute **`--os windows`** à la commande |
| `La piste du son de l'ordinateur est silencieuse` | La visio sort par un autre appareil que la sortie par défaut de Windows | Étape 6 : même appareil dans Windows et dans Teams/Zoom. Ou passe la bonne sortie avec `--audio "<nom>"` (voir `--list`) |
| Transcription vide, ta voix absente | Micro bloqué pour les applications de bureau | Étape 5 |
| `Périphérique « … » introuvable. Lance --list…` | Nom mal écrit | `--os windows --list` (étape 7), puis copie le nom exact |
| Erreur à l'ouverture d'un périphérique, ou piste vide alors que du son est joué | Une application a pris le **contrôle exclusif** de la carte son | Lance `mmsys.cpl` → onglet *Lecture* (et *Enregistrement*) → ton appareil → *Propriétés* → *Avancé* → décoche **« Autoriser les applications à prendre le contrôle exclusif de ce périphérique »** |
| Ctrl + C n'arrête pas l'enregistrement | Certaines consoles transmettent mal Ctrl + C | Essaie **Ctrl + Pause** (ou Ctrl + Attn), et utilise Windows Terminal ou PowerShell |
| Accents illisibles dans PowerShell (`Ã©` au lieu de `é`) | Ancienne console pas en UTF-8 | Utilise **Windows Terminal**, ou lance `chcp 65001` avant. Les fichiers `.txt` sont, eux, toujours corrects |
| Son de mauvaise qualité avec un casque Bluetooth | Mode « mains libres » quand le micro du casque est utilisé | Utilise le micro du PC avec `--mic` |
| `HF_HUB_OFFLINE=1 : Le terme … n'est pas reconnu` | Syntaxe Mac utilisée dans PowerShell | Lance d'abord `$env:HF_HUB_OFFLINE=1`, puis la commande |
| `Commande « claude » introuvable` (`meeting-agent.py`) | Claude Code non installé, ou dossier npm absent du PATH | Étape 11. Vérifie avec `where.exe claude` |

🤖 **Prompt pour un assistant IA (en cas d'erreur) :**
```text
Je suis sous Windows, dans PowerShell, dans le dossier local-meeting-transcriber. J'ai lancé : <la commande>
Et j'obtiens cette erreur : <colle le message complet>
Cherche la cause dans la section « Erreurs possibles sous Windows » de docs/config-windows.md. Explique la cause en une phrase,
puis la solution étape par étape. Demande mon accord avant toute installation ou modification de réglage.
Si l'erreur n'est pas dans le tableau, dis-le clairement au lieu d'inventer.
```

---

## Prompt global : l'agent fait tout avec toi

Ce prompt transforme ton assistant IA (Claude Code, GitHub Copilot Chat **en mode agent**, Cursor…) en guide complet : il te pose des questions précises, vérifie ton installation, installe ce qui manque **avec ton accord**, et te prépare la commande finale (ou la lance lui-même pour un fichier existant).

**Comment l'utiliser :**
1. Ouvre le dossier `local-meeting-transcriber` dans ton éditeur (VS Code : *Fichier > Ouvrir le dossier…*).
2. Ouvre ton assistant IA en mode agent. Son terminal doit être **PowerShell**.
3. Copie **tout** le bloc ci-dessous et colle-le.

```text
Tu es mon assistant pour installer et utiliser l'outil local-meeting-transcriber sur mon PC Windows (PowerShell).
Le dossier ouvert est la racine du projet. Avant tout, lis README.md et docs/config-windows.md : ce sont tes références.

RÈGLES À RESPECTER EN PERMANENCE
- Réponds en français, avec des phrases simples, comme à quelqu'un qui n'est pas développeur.
- Pose les questions ci-dessous UNE PAR UNE, dans l'ordre, et attends ma réponse avant de continuer.
  Propose toujours les choix numérotés indiqués. N'invente pas mes réponses.
- Avant chaque commande, explique en une phrase ce qu'elle fait.
- Sous Windows : utilise `py` (jamais python3), des chemins `.\script\…`, des guillemets autour des chemins,
  et ajoute TOUJOURS `--os windows` aux commandes des scripts. Pour le mode hors ligne, utilise `$env:HF_HUB_OFFLINE=1`
  sur une ligne séparée (jamais la syntaxe Mac `HF_HUB_OFFLINE=1 py …`).
- Demande mon accord explicite avant : toute installation (winget, pip), toute modification d'un réglage Windows.
- Ne modifie, ne supprime et ne crée aucun fichier du projet. N'ouvre pas, ne lis pas et n'envoie jamais le contenu
  du dossier reunions\ (enregistrements et transcriptions) sans que je te le demande.
- Ne crée jamais de variable ANTHROPIC_API_KEY.
- En cas d'erreur, cherche d'abord dans la section « Erreurs possibles sous Windows » de docs/config-windows.md. Si l'erreur
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
Q5. (Seulement si Q2 = 1) Dans quel dossier ranger le résultat ? (un nom simple sans espace ni « \ », par exemple comite-projet, ou « aucun »)
Q6. (Sauf si Q1 = 1) Tu préfères :
    1) Rapide (modèle small, conseillé)
    2) Plus précis mais plus lent (modèle medium)
Q7. (Seulement si Q1 = 3) Quel est le chemin complet du fichier ? (glisse-le dans le chat ou colle son chemin)

CE QUE TU FAIS ENSUITE, DANS CET ORDRE (en suivant les étapes de docs/config-windows.md)
1. `pwd` et `dir` : vérifie qu'on est bien à la racine du projet (README.md, docs, script).
2. `py --version` : Python 3.10 à 3.12 conseillé (étape 2). S'il manque, propose l'installation et rappelle-moi de
   rouvrir PowerShell ensuite.
3. `py -c "import soundcard, soundfile, faster_whisper, numpy, sherpa_onnx; print('Tout est installé')"`.
   S'il manque quelque chose : propose `py -m pip install soundcard soundfile faster-whisper numpy sherpa-onnx` (étape 4).
   En cas de « DLL load failed » : propose `winget install --id Microsoft.VCRedist.2015+.x64 -e`.
4. Rappelle-moi de vérifier l'autorisation du micro pour les applications de bureau (étape 5) et demande-moi de confirmer.
5. `py .\script\meeting-whisper-final.py --os windows --list` : recommande-moi un micro (étape 7) et dis-moi quelle
   sortie sera enregistrée comme son de l'ordinateur. Si Q3 = 1 ou 2, rappelle-moi que la sortie son de Windows et celle
   de mon application de visio doivent être le même appareil (étape 6).
6. Vérifie si le modèle choisi est déjà téléchargé :
   `dir $env:USERPROFILE\.cache\huggingface\hub` doit contenir models--Systran--faster-whisper-small (ou -medium).
   S'il est absent : préviens-moi que le premier lancement téléchargera le modèle (~480 Mo pour small, ~1,5 Go pour medium)
   et n'active PAS le mode hors ligne. S'il est présent : ajoute une première ligne `$env:HF_HUB_OFFLINE=1`.
7. Construis la commande finale, avec : py, le script correspondant à Q2 (.\script\meeting-whisper-final.py /
   .\script\meeting-whisper.py / .\script\meeting-agent.py), --os windows, --mic "<nom exact du micro>",
   --audio none si Q3 = 3, --speakers <N> si Q4 est un nombre (script final uniquement), --nameFolder <nom> si Q5 n'est pas
   « aucun », --model medium si Q6 = 2, --file "<chemin>" si Q1 = 3.
8. Si Q1 = 3 (fichier existant) : demande-moi si tu dois lancer la commande toi-même. Si oui, lance-la et montre-moi
   où se trouve le résultat.
   Si Q1 = 2 (enregistrement) : NE LANCE PAS l'enregistrement toi-même (il doit être arrêté avec Ctrl+C dans ma fenêtre).
   Donne-moi les lignes à copier dans PowerShell, précédées de `cd "<chemin du projet>"`, puis rappelle-moi :
   - la checklist « Avant la réunion » de l'étape 9 (prévenir les participants, même sortie son dans Windows et dans la visio,
     PC branché) ;
   - d'appuyer sur Ctrl + C à la fin ;
   - d'attendre le message « Transcription enregistrée dans … » (ou « Fichiers enregistrés dans … » pour meeting-agent.py) avant de fermer PowerShell.
9. Termine par un récapitulatif en 5 lignes : ce qui est installé, le micro choisi, la commande, où sera le résultat,
   comment arrêter.
```
