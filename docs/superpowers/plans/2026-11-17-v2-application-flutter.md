# V2 : application desktop Flutter — Plan d'implémentation

> **Pour les agents qui codent :** SOUS-COMPÉTENCE REQUISE : utiliser superpowers:subagent-driven-development (recommandé) ou superpowers:executing-plans pour exécuter ce plan tâche par tâche. Les étapes utilisent des cases à cocher (`- [ ]`) pour le suivi.

**Objectif :** une application desktop (Mac, Windows, Debian) où l'utilisateur choisit son micro et la source du son de l'ordinateur dans des listes, clique sur **Lancer** pour démarrer l'enregistrement, puis sur **Arrêter** pour obtenir la transcription (avec ou sans intervenants). Un bouton séparé, optionnel, lance le compte rendu par Claude.

**Architecture :** l'interface Flutter ne fait **aucun traitement audio**. Elle pilote un **moteur Python** (`script/engine.py`) lancé en sous-processus. Le moteur réutilise le code v1 déjà testé (`audio_capture.py`, la transcription Whisper, la diarisation sherpa-onnx). Les deux parties échangent des **lignes JSON** : des événements sur la sortie standard du moteur, et la commande `stop` sur son entrée standard. Ce protocole est le **contrat** entre les deux parties, et il est décrit dans `docs/protocol.md`.

**Stack technique :** Flutter desktop (Dart), packages `provider` et `shared_preferences`. Python ≥ 3.9 avec `soundcard`, `soundfile`, `faster-whisper`, `sherpa-onnx` et `numpy`. Tests avec `pytest`, `flutter test` et `flutter analyze`. CI GitHub Actions (macOS, Windows, Ubuntu). Empaquetage du moteur avec PyInstaller.

**Spec :** pas de document séparé. Les exigences viennent des demandes de l'utilisateur, résumées ici :
1. Choisir son micro et sa source « son de l'ordinateur » dans la liste des périphériques disponibles.
2. Bouton **Lancer** → enregistrement. Bouton **Arrêter** → transcription locale.
3. Bouton séparé → compte rendu par Claude (`meeting-agent`).
4. Mêmes réglages que les scripts v1 : modèle Whisper, mode simple ou intervenants, `--speakers`, `--threshold`, `--nameFolder`.
5. Fonctionne sur Mac, Windows et Debian.
6. Contraintes de souveraineté de la v1 : rien ne quitte le poste, sauf le compte rendu Claude, fait explicitement.

## Contraintes globales

- Les scripts v1 (`script/meeting-whisper.py`, `script/meeting-whisper-final.py`, `script/meeting-agent.py`) **continuent de fonctionner à l'identique** en ligne de commande, avec les mêmes options et les mêmes fichiers produits.
- Le moteur reste compatible **Python 3.9**, la version du Mac de référence.
- **Aucun appel réseau** de l'application ou du moteur, sauf : le téléchargement des modèles (Hugging Face, GitHub releases) et l'appel `claude -p` **déclenché par l'utilisateur après confirmation**.
- `reunions/`, l'audio et les transcriptions ne sont **jamais** commités. Le `.gitignore` v1 reste en place.
- L'interface est **en français**. Les codes d'erreur du protocole sont en anglais (`snake_case`), les messages affichés en français.
- L'application détecte le système (`Platform.isMacOS` / `isWindows` / `isLinux`) et passe elle-même `--os mac|windows|debian` au moteur. L'utilisateur n'a jamais à le choisir.
- macOS : l'application est distribuée **hors App Store, sans App Sandbox**. Le sandbox empêcherait de lancer le moteur et d'utiliser BlackHole. Elle déclare `NSMicrophoneUsageDescription` et l'entitlement `com.apple.security.device.audio-input`.
- Version de Flutter : la version stable installée au démarrage du projet, notée dans `AGENTS.md` et dans le CI. On n'en change pas en cours de route.
- Dépendances Dart limitées à `provider`, `shared_preferences` et `path`, plus `flutter_test` en développement. Toute nouvelle dépendance doit être justifiée dans la description de la PR.

## Points de vigilance

Les cinq situations les plus susceptibles de poser problème à un utilisateur, sans être couvertes par la spec. Chacune a son test dans la tâche indiquée.

1. **L'application est fermée ou plante pendant un enregistrement** → le moteur doit s'arrêter, sinon le micro reste allumé en arrière-plan. Test : `test_engine_exits_when_stdin_closes` (Tâche 3) et `kill on dispose` (Tâche 5).
2. **Un périphérique disparaît pendant l'enregistrement** (iPhone éloigné, casque débranché) → événement `error` `record_failed`, le fichier partiel est conservé et l'application ne reste pas bloquée sur « Enregistrement… ». Test : `test_device_failure_emits_error_and_keeps_partial_file` (Tâche 2).
3. **Micro bloqué par les autorisations du système** (piste à zéro absolu) → avertissement `mic_silent` avec un message qui indique le réglage de confidentialité. Test : `test_all_zero_mic_track_warns_mic_silent` (Tâche 2).
4. **Modèle non téléchargé et mode hors ligne, ou pas de réseau** → erreur `model_unavailable`, pas de trace Python brute dans l'interface. Test : `test_missing_model_offline_emits_model_unavailable` (Tâche 3).
5. **Double clic sur Lancer, ou Arrêter cliqué pendant le démarrage** → un seul moteur actif, et un `stop` envoyé avant `started` est pris en compte. Tests : `second start while recording is ignored` (Tâche 6) et `test_stop_before_started_still_stops` (Tâche 3).

---

## Arborescence cible

```
local-meeting-transcriber/
├── AGENTS.md                         # harness : règles pour TOUS les agents (source de vérité)
├── CLAUDE.md                         # contient « @AGENTS.md » (import pour Claude Code)
├── .github/
│   ├── copilot-instructions.md       # renvoie vers AGENTS.md
│   └── workflows/ci.yml              # pytest + flutter analyze/test/build × 3 OS
├── .claude/settings.json             # permissions des agents Claude Code
├── tools/check_no_meeting_data.py    # garde-fou : refuse un commit contenant audio/transcriptions
├── docs/
│   ├── protocol.md                   # CONTRAT moteur ↔ application
│   └── architecture-app.md           # architecture v2
├── script/
│   ├── audio_capture.py              # MODIFIÉ : stop_event, on_level, backend factice
│   ├── transcription.py              # NOUVEAU : logique extraite des scripts v1
│   ├── summary.py                    # NOUVEAU : appel claude -p extrait de meeting-agent
│   ├── protocol.py                   # NOUVEAU : émission des événements JSON
│   ├── engine.py                     # NOUVEAU : point d'entrée piloté par l'application
│   └── meeting-*.py                  # v1, réécrits pour importer transcription/summary
├── tests/                            # pytest (moteur)
│   ├── conftest.py
│   ├── test_protocol.py
│   ├── test_audio_capture.py
│   └── test_engine.py
└── app/                              # Flutter
    ├── pubspec.yaml
    ├── lib/
    │   ├── main.dart
    │   ├── engine/events.dart        # événements typés (sealed class)
    │   ├── engine/engine_client.dart # lance le moteur, lit le JSON, envoie stop
    │   ├── engine/engine_locator.dart# trouve python + engine.py, ou le binaire embarqué
    │   ├── state/settings.dart       # réglages persistés
    │   ├── state/session_controller.dart  # machine à états de la session
    │   └── ui/{setup_page,recording_page,result_page,error_messages}.dart, ui/widgets/level_meter.dart
    ├── macos/ windows/ linux/
    └── test/…                        # miroir de lib/
```

---

## Phase 0 : le harness des agents

### Tâche 0 : Harness, garde-fous et CI

**Fichiers :**
- Créer : `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.claude/settings.json`, `tools/check_no_meeting_data.py`, `.github/workflows/ci.yml`, `tests/conftest.py`, `tests/test_guard.py`

**Interfaces :**
- Produit : la commande `python3 tools/check_no_meeting_data.py <fichiers…>`, qui renvoie le code 1 et liste les fichiers interdits. La variable d'environnement `LMT_AUDIO_BACKEND=fake`, utilisée par tous les tests (définie dans la Tâche 2, déclarée ici dans le CI).

- [ ] **Étape 1 : écrire `AGENTS.md`** avec exactement ces sections :
  - **But du projet** : 3 lignes, reprises de l'objectif ci-dessus.
  - **Arborescence** : copie de l'arborescence cible.
  - **Commandes** : `pytest -m "not slow"` (rapide, sans modèles), `pytest` (complet, télécharge les modèles), `cd app && flutter analyze && flutter test`, `cd app && flutter run -d macos|windows|linux`.
  - **Règles non négociables** :
    1. Ne jamais lire, déplacer, commiter ni envoyer le contenu de `reunions/`, ni aucun `.wav` ou `*_transcription*.txt` réel.
    2. Aucun nouvel appel réseau. Seuls sont autorisés : le téléchargement des modèles et `claude -p` derrière la confirmation de l'interface.
    3. `docs/protocol.md` est le contrat. Pour le modifier : d'abord la doc, puis les tests Python **et** Dart, puis le code des deux côtés, dans le même commit.
    4. Les scripts v1 doivent garder le même comportement en ligne de commande.
    5. Interface en français, codes d'erreur en anglais.
    6. Pas de `git push`, pas de nouvelle dépendance sans justification.
  - **Tester sans matériel audio** : `LMT_AUDIO_BACKEND=fake`.
  - **Définition de « terminé » pour une tâche** : tests de la tâche verts, `pytest -m "not slow"` vert, `flutter analyze` sans avertissement, `flutter test` vert, garde-fou OK, case cochée dans ce plan.
  - **Pièges par système** : des liens vers docs/config-mac.md, config-windows.md et config-debian.md (sections « Erreurs possibles »).
- [ ] **Étape 2 : écrire `CLAUDE.md`** avec une seule ligne, `@AGENTS.md`, et `.github/copilot-instructions.md` avec : « Lis et applique AGENTS.md à la racine du dépôt. »
- [ ] **Étape 3 : écrire `.claude/settings.json`**. Autoriser `Bash(pytest:*)`, `Bash(flutter analyze:*)`, `Bash(flutter test:*)`, `Bash(python3 tools/check_no_meeting_data.py:*)`. Interdire `Bash(git push:*)`, `Read(reunions/**)` et `Edit(reunions/**)`.
- [ ] **Étape 4 : écrire le test qui échoue** dans `tests/test_guard.py` :

```python
def test_guard_rejects_meeting_files(tmp_path):
    r = run_guard(["reunions/x/1/a.wav", "notes_transcription.txt", "script/engine.py"])
    assert r.returncode == 1
    assert "reunions/x/1/a.wav" in r.stdout and "notes_transcription.txt" in r.stdout
    assert "script/engine.py" not in r.stdout

def test_guard_accepts_code_only():
    assert run_guard(["script/engine.py", "app/lib/main.dart"]).returncode == 0
```

- [ ] **Étape 5 : `pytest tests/test_guard.py -v`**. Résultat attendu : ÉCHEC (fichier `tools/check_no_meeting_data.py` absent).
- [ ] **Étape 6 : implémenter `tools/check_no_meeting_data.py`**. Il refuse tout chemin qui commence par `reunions/` ou qui correspond à `*.wav|*.aiff|*.m4a|*.mp3|*.mp4|*_transcription*.txt|*_notes.md`.
- [ ] **Étape 7 : `pytest tests/test_guard.py -v`**. Résultat attendu : RÉUSSITE.
- [ ] **Étape 8 : écrire `.github/workflows/ci.yml`.** Matrice `macos-latest`, `windows-latest` et `ubuntu-latest`. Étapes :
  1. le garde-fou sur `git diff --name-only origin/main...` ;
  2. installer Python 3.9 et les dépendances ;
  3. `pytest -m "not slow"` avec `LMT_AUDIO_BACKEND=fake` ;
  4. installer Flutter avec la version notée dans `AGENTS.md` ;
  5. `flutter analyze` et `flutter test` dans `app/` ;
  6. `flutter build macos|windows|linux` selon l'OS.

  Sur Ubuntu, il faut aussi : `sudo apt-get install -y libpulse0 libgtk-3-dev ninja-build clang cmake pkg-config`. Les étapes Flutter sont ignorées tant que `app/` n'existe pas (`if: hashFiles('app/pubspec.yaml') != ''`).
- [ ] **Étape 9 : commit.** `git add AGENTS.md CLAUDE.md .github .claude tools tests && git commit -m "chore: harness agents, garde-fou données, CI"`

---

## Phase 1 : le moteur Python

### Tâche 1 : Le contrat — `docs/protocol.md` et `script/protocol.py`

**Fichiers :**
- Créer : `docs/protocol.md`, `script/protocol.py`, `tests/test_protocol.py`

**Interfaces :**
- Produit : `emit(type: str, **fields) -> None`, qui écrit **une** ligne JSON UTF-8 sur stdout et la vide immédiatement (flush). `fail(code: str, message: str, exit_code: int = 1) -> NoReturn`. La constante `ERROR_CODES`.

Le contrat à écrire tel quel dans `docs/protocol.md`. Sur stdout, uniquement du JSON, une ligne par événement. Les journaux vont sur stderr.

| Commande | Événements émis |
|---|---|
| `engine.py devices --os <os>` | `{"type":"devices","detected_os":"mac","mics":[{"index":0,"name":"…","default":true}],"system":[{"name":"BlackHole 2ch","default":true}]}` |
| `engine.py check` | `{"type":"check","claude":bool,"models":{"small":bool,"medium":bool,…},"diarization_models":bool}` |
| `engine.py record --os --mic? --audio? --mode simple\|speakers --model --speakers --threshold --name-folder?` | `started{mic,audio\|null,folder}` → `level{mic,audio\|null}` toutes les 200 ms → (stdin `stop`) → `stopped{wav,duration_s}` → `progress{stage,percent\|null}` → `segment{start,speaker\|null,text}`… → `done{transcript_path,speakers\|null}` |
| `engine.py transcribe --file … (mêmes options sans micro)` | `progress` → `segment`… → `done` |
| `engine.py summarize --transcript <chemin>` | `progress{stage:"summarize"}` → `done{notes_path}` |
| à tout moment | `warning{code,message}`, `error{code,message}` puis code de sortie 1 |

- Valeurs de `stage` : `download_model`, `diarize`, `transcribe`, `summarize`.
- Codes `warning` : `os_mismatch`, `no_system_source`, `system_silent`, `mic_silent`.
- Codes `error` : `device_not_found`, `record_failed`, `model_unavailable`, `claude_missing`, `claude_failed`, `bad_arguments`.
- Entrée standard : la ligne `stop` arrête l'enregistrement. Si l'entrée standard est fermée (EOF), le moteur arrête l'enregistrement et quitte **sans transcrire**, avec `stopped` puis le code de sortie 0.

- [ ] **Étape 1 : écrire `docs/protocol.md`** avec le tableau et les listes ci-dessus, et un exemple de session complète.
- [ ] **Étape 2 : écrire les tests qui échouent :**

```python
def test_emit_writes_one_json_line(capsys):
    emit("segment", start=1.5, speaker="Utilisateur 1", text="Bonjour à tous")
    line = capsys.readouterr().out
    assert line.endswith("\n") and line.count("\n") == 1
    assert json.loads(line) == {"type": "segment", "start": 1.5, "speaker": "Utilisateur 1", "text": "Bonjour à tous"}

def test_emit_keeps_accents_unescaped(capsys):
    emit("warning", code="mic_silent", message="Micro muet : vérifie les réglages")
    assert "vérifie" in capsys.readouterr().out

def test_fail_rejects_unknown_code():
    with pytest.raises(ValueError): fail("oops", "x")
```

- [ ] **Étape 3 : `pytest tests/test_protocol.py -v`**. Résultat attendu : ÉCHEC (import impossible).
- [ ] **Étape 4 : implémenter `script/protocol.py`.** Utiliser `json.dumps(..., ensure_ascii=False)` et `sys.stdout.reconfigure(encoding="utf-8")` au moment de l'import, ce qui est indispensable sous Windows.
- [ ] **Étape 5 : `pytest tests/test_protocol.py -v`**. Résultat attendu : RÉUSSITE.
- [ ] **Étape 6 : commit.** `git commit -m "feat(engine): contrat JSON lines moteur/application"`

### Tâche 2 : `audio_capture.py` pilotable, avec un backend factice

**Fichiers :**
- Modifier : `script/audio_capture.py`
- Tester : `tests/test_audio_capture.py`

**Interfaces :**
- Consomme : la v1 de `audio_capture` (`resolve`, `microphones`, `system_sources`, `default_system_source`).
- Produit :
  - `record(os_name, mic_name, audio_name, base, stop_event: threading.Event | None = None, on_level: Callable[[float, float | None], None] | None = None, on_warning: Callable[[str, str], None] | None = None) -> str`. Sans `stop_event`, le comportement v1 (Ctrl+C) est inchangé.
  - `devices_dict(os_name) -> dict`, au format de l'événement `devices` sans le champ `type`.
  - `class RecordError(Exception)`, avec l'attribut `partial_path`.
  - Le backend factice, activé par `LMT_AUDIO_BACKEND=fake`. Il fournit les périphériques `"Fake Mic"` (sinusoïde de 440 Hz, amplitude 0,1), `"Fake Silent Mic"` (zéros absolus), `"Fake System"` (bruit, amplitude 0,05) et `"Fake Broken Mic"` (lève une `OSError` après 0,3 s).

- [ ] **Étape 1 : écrire les tests qui échouent** (tous avec `monkeypatch.setenv("LMT_AUDIO_BACKEND", "fake")`) :

```python
def test_devices_dict_lists_fake_devices():
    d = devices_dict("mac")
    assert [m["name"] for m in d["mics"]][:1] == ["Fake Mic"] and d["mics"][0]["default"]
    assert d["system"][0] == {"name": "Fake System", "default": True}

def test_record_stops_on_event_and_mixes(tmp_path):
    stop = threading.Event(); threading.Timer(0.5, stop.set).start()
    wav = record("mac", "Fake Mic", "Fake System", str(tmp_path / "r"), stop_event=stop)
    assert wav.endswith("r.wav") and (tmp_path / "r_micro.wav").exists() and (tmp_path / "r_audio.wav").exists()
    assert 0.3 < sf.info(wav).duration < 1.5

def test_record_reports_levels(tmp_path):
    levels = []; stop = threading.Event(); threading.Timer(0.6, stop.set).start()
    record("mac", "Fake Mic", "none", str(tmp_path / "r"), stop_event=stop, on_level=lambda m, a: levels.append((m, a)))
    assert len(levels) >= 2 and all(a is None and m > 0 for m, a in levels)

def test_all_zero_mic_track_warns_mic_silent(tmp_path):
    warns = []; stop = threading.Event(); threading.Timer(0.4, stop.set).start()
    record("mac", "Fake Silent Mic", "none", str(tmp_path / "r"), stop_event=stop, on_warning=lambda c, m: warns.append(c))
    assert "mic_silent" in warns

def test_device_failure_emits_error_and_keeps_partial_file(tmp_path):
    with pytest.raises(RecordError) as e:
        record("mac", "Fake Broken Mic", "none", str(tmp_path / "r"), stop_event=threading.Event())
    assert os.path.exists(e.value.partial_path)
```

- [ ] **Étape 2 : `LMT_AUDIO_BACKEND=fake pytest tests/test_audio_capture.py -v`**. Résultat attendu : ÉCHEC.
- [ ] **Étape 3 : implémenter.**
  - Le backend factice est un petit module interne qui imite l'interface `soundcard` utilisée : `.name`, `.recorder(samplerate)`, `.record(numframes)`.
  - `on_level` reçoit le RMS du dernier bloc, au plus toutes les 200 ms.
  - Les avertissements v1, jusqu'ici affichés sur stderr, passent par `on_warning` quand il est fourni : codes `no_system_source`, `system_silent`, `mic_silent`. Le code `mic_silent` correspond à une piste micro dont **toutes** les valeurs sont à 0.
  - Les erreurs de capture lèvent `RecordError`, au lieu de `sys.exit`, quand `stop_event` est fourni.
- [ ] **Étape 4 : relancer les tests.** Résultat attendu : RÉUSSITE. Vérifier aussi la non-régression v1 : `python3 script/meeting-whisper.py --list` affiche la même chose qu'avant.
- [ ] **Étape 5 : commit.** `git commit -m "feat(audio): arrêt pilotable, niveaux, backend factice"`

### Tâche 3 : Extraire la transcription, puis le point d'entrée `engine.py`

**Fichiers :**
- Créer : `script/transcription.py`, `script/summary.py`, `script/engine.py`, `tests/test_engine.py`
- Modifier : `script/meeting-whisper.py`, `script/meeting-whisper-final.py`, `script/meeting-agent.py`. Ils importent désormais `transcription` et `summary`. Leurs options et leurs sorties ne changent pas.

**Interfaces :**
- Consomme : `protocol.emit/fail` (Tâche 1), `audio_capture.record/devices_dict/RecordError` (Tâche 2).
- Produit :
  - `transcription.transcribe_simple(path: str, model_size: str, on_segment: Callable[[float, str], None]) -> str` ;
  - `transcription.transcribe_speakers(path, model_size, speakers: int, threshold: float, on_segment: Callable[[float, str, str], None], on_progress: Callable[[str], None]) -> tuple[str, int]` ;
  - `transcription.ModelUnavailable(Exception)` ;
  - `summary.summarize(transcript: str) -> str`, qui lève `summary.ClaudeMissing` ou `summary.ClaudeFailed` ;
  - la CLI `engine.py` décrite dans `docs/protocol.md`.

- [ ] **Étape 1 : écrire les tests qui échouent.** Ils lancent le moteur en vrai sous-processus, avec `LMT_AUDIO_BACKEND=fake`, et un helper `run_engine(args, stdin_lines, delay)` qui renvoie la liste des événements décodés :

```python
def test_devices_command_outputs_single_devices_event():
    ev = run_engine(["devices", "--os", "mac"])
    assert [e["type"] for e in ev] == ["devices"] and ev[0]["mics"][0]["name"] == "Fake Mic"

def test_record_stop_then_done(tmp_path, tiny_transcriber):   # tiny_transcriber : transcription simulée (fixture)
    ev = run_engine(["record", "--os", "mac", "--mic", "Fake Mic", "--audio", "none", "--mode", "simple"],
                    stdin_lines=["stop"], delay=0.8, cwd=tmp_path)
    types = [e["type"] for e in ev]
    assert types[0] == "started" and "level" in types and types.index("stopped") < types.index("done")
    assert os.path.exists(tmp_path / ev[-1]["transcript_path"])

def test_stop_before_started_still_stops(tmp_path, tiny_transcriber):
    ev = run_engine([...même commande...], stdin_lines=["stop"], delay=0.0, cwd=tmp_path)
    assert ev[-1]["type"] == "done"

def test_engine_exits_when_stdin_closes(tmp_path):
    p = start_engine(["record", ...], cwd=tmp_path); time.sleep(0.5); p.stdin.close()
    assert p.wait(timeout=5) == 0 and "done" not in [e["type"] for e in read_events(p)]

def test_unknown_mic_emits_device_not_found():
    ev = run_engine(["record", "--os", "mac", "--mic", "Inexistant", "--audio", "none"], stdin_lines=["stop"])
    assert ev[-1] == {"type": "error", "code": "device_not_found", "message": ANY}

def test_missing_model_offline_emits_model_unavailable(tmp_path, monkeypatch):
    # HF_HUB_OFFLINE=1 + HF_HOME vide → le modèle « small » est introuvable
    ev = run_engine(["transcribe", "--file", FIXTURE_WAV, "--model", "small"], env={"HF_HUB_OFFLINE": "1", "HF_HOME": str(tmp_path)})
    assert ev[-1]["code"] == "model_unavailable"

@pytest.mark.slow
def test_speakers_mode_on_two_voice_fixture():
    ev = run_engine(["transcribe", "--file", "tests/fixtures/dialogue_2_voix.wav", "--mode", "speakers", "--speakers", "2"])
    assert ev[-1]["speakers"] == 2 and {e["speaker"] for e in ev if e["type"] == "segment"} == {"Utilisateur 1", "Utilisateur 2"}
```

  `tests/fixtures/dialogue_2_voix.wav` est généré **une fois** avec les voix de synthèse macOS (Jacques et Amélie, 6 répliques, la procédure v1), puis commité. C'est la **seule** exception audio du garde-fou : ajouter `tests/fixtures/` à la liste blanche de `check_no_meeting_data.py`, avec son test.

- [ ] **Étape 2 : `LMT_AUDIO_BACKEND=fake pytest tests/test_engine.py -v -m "not slow"`**. Résultat attendu : ÉCHEC.
- [ ] **Étape 3 : extraire `transcription.py` et `summary.py`** depuis les scripts v1, sans changer leur logique. Réécrire les 3 scripts v1 pour qu'ils les importent.
- [ ] **Étape 4 : implémenter `engine.py`.**
  - Analyse des arguments avec `argparse` et des sous-commandes.
  - Pour `record` : un thread lecteur de stdin met `stop_event` à `True` sur la ligne `stop` (stop transcrit ensuite) ou sur EOF (fermeture de stdin : drapeau `abandon`, pas de transcription).
  - Correspondance des exceptions et des codes : `RecordError` → `record_failed`, `ModelUnavailable` → `model_unavailable`, `ClaudeMissing` → `claude_missing`, `ClaudeFailed` → `claude_failed`.
  - Toute autre exception → `record_failed`, avec un message court. La trace complète part sur stderr.
- [ ] **Étape 5 : relancer les tests.** Résultat attendu : RÉUSSITE. Puis `pytest -m slow tests/test_engine.py` sur le Mac de référence. Puis la non-régression v1 : `python3 script/meeting-whisper-final.py --file tests/fixtures/dialogue_2_voix.wav --speakers 2` produit 2 intervenants, comme en v1.
- [ ] **Étape 6 : commit.** `git commit -m "feat(engine): engine.py JSON lines + extraction transcription/summary"`

---

## Phase 2 : l'application Flutter

### Tâche 4 : Squelette de l'application et autorisations par système

**Fichiers :**
- Créer : `app/` via `flutter create --platforms=macos,windows,linux --org com.localmeeting --project-name local_meeting_transcriber app`
- Modifier : `app/macos/Runner/Info.plist`, `app/macos/Runner/DebugProfile.entitlements`, `app/macos/Runner/Release.entitlements`, `app/pubspec.yaml`

- [ ] **Étape 1 : créer le projet**, ajouter `provider`, `shared_preferences` et `path`, et remplacer le compteur par un `MaterialApp` intitulé « Local Meeting Transcriber ».
- [ ] **Étape 2 : configurer macOS.**
  - `NSMicrophoneUsageDescription` = « L'application enregistre votre micro pour transcrire vos réunions, en local. »
  - Entitlements : `com.apple.security.app-sandbox` = **false**, `com.apple.security.device.audio-input` = true.
- [ ] **Étape 3 : vérification manuelle, bloquante, sur Mac.** C'est le **plus gros risque technique** du projet. Depuis l'application lancée avec `flutter run -d macos`, un bouton de test temporaire lance `engine.py record` avec le vrai micro pendant 3 secondes. Le résultat attendu : macOS demande l'autorisation micro **pour l'application**, et le niveau du micro est supérieur à 0.

  En cas d'échec (macOS attribue l'autorisation au mauvais processus), **arrêter et remonter le problème** avant de continuer. Piste de repli : signer le moteur avec le même identifiant d'équipe que l'application.
- [ ] **Étape 4 : `cd app && flutter analyze && flutter test && flutter build macos`**. Résultat attendu : 0 problème et un build réussi.
- [ ] **Étape 5 : commit.** `git commit -m "feat(app): squelette Flutter desktop + permissions micro"`

### Tâche 5 : Événements typés et `EngineClient`

**Fichiers :**
- Créer : `app/lib/engine/events.dart`, `app/lib/engine/engine_client.dart`, `app/lib/engine/engine_locator.dart`, `app/test/engine/events_test.dart`, `app/test/engine/engine_client_test.dart`

**Interfaces :**
- Consomme : `docs/protocol.md` (Tâche 1).
- Produit :
  - `sealed class EngineEvent` avec les sous-classes `DevicesEvent(List<Mic> mics, List<SystemSource> system, String detectedOs)`, `CheckEvent`, `StartedEvent`, `LevelEvent(double mic, double? audio)`, `StoppedEvent(String wav, double durationS)`, `ProgressEvent(String stage, double? percent)`, `SegmentEvent(double start, String? speaker, String text)`, `DoneEvent(String? transcriptPath, int? speakers, String? notesPath)`, `WarningEvent(String code, String message)`, `ErrorEvent(String code, String message)`, `UnknownEvent(Map raw)`. Plus `EngineEvent.fromJson(Map<String, dynamic>)`.
  - `class EngineClient`, construit avec un `ProcessStarter` injectable (`typedef ProcessStarter = Future<Process> Function(String exe, List<String> args, {String? workingDirectory})`). Méthodes :
    - `Future<DevicesEvent> listDevices(String os)` ;
    - `Future<CheckEvent> check()` ;
    - `Stream<EngineEvent> record(RecordOptions o)` ;
    - `Stream<EngineEvent> transcribeFile(String path, RecordOptions o)` ;
    - `Stream<EngineEvent> summarize(String transcriptPath)` ;
    - `void stop()` (écrit `stop\n`) ;
    - `Future<void> dispose()` (ferme stdin, puis tue le processus après 3 s) ;
    - `bool get isRunning`.
  - `class RecordOptions { String os; String? mic; String? audio; String mode; String model; int speakers; double threshold; String? nameFolder; List<String> toArgs(); }`, où `audio == null` signifie le défaut et `"none"` désactive la source.
  - `EngineLocator.resolve() → (String exe, List<String> prefixArgs)`. En développement : `python3` (ou `py` sous Windows) + `<racine>/script/engine.py`. En production : le binaire embarqué (Tâche 10).

- [ ] **Étape 1 : écrire les tests qui échouent.**
  - `events_test.dart` :
    - `segment` est décodé avec un `speaker` null ;
    - un `type` inconnu donne `UnknownEvent`, sans exception ;
    - `error` conserve `code` et `message` ;
    - les accents sont décodés correctement.
  - `engine_client_test.dart`, avec un faux `Process` (contrôleurs de flux pour stdout et stdin) :
    - `record émet les événements dans l'ordre` ;
    - `stop écrit "stop\n" sur stdin` ;
    - `kill on dispose` : `dispose()` pendant un enregistrement ferme stdin, puis tue le processus si celui-ci n'a pas quitté dans les 3 s (horloge simulée avec `fake_async`) ;
    - `une ligne non JSON sur stdout est ignorée` ;
    - `sortie avec code 1 sans événement error → ErrorEvent("record_failed")`.
- [ ] **Étape 2 : `cd app && flutter test test/engine`**. Résultat attendu : ÉCHEC.
- [ ] **Étape 3 : implémenter.** Découpage des lignes avec `utf8.decoder` et `LineSplitter`. Ces deux fichiers n'importent jamais `package:flutter/*` (du Dart pur, donc testable sans interface).
- [ ] **Étape 4 : `flutter test test/engine`**. Résultat attendu : RÉUSSITE.
- [ ] **Étape 5 : commit.** `git commit -m "feat(app): EngineClient + événements typés"`

### Tâche 6 : Réglages persistés et machine à états de la session

**Fichiers :**
- Créer : `app/lib/state/settings.dart`, `app/lib/state/session_controller.dart`, `app/test/state/session_controller_test.dart`, `app/test/state/settings_test.dart`

**Interfaces :**
- Consomme : `EngineClient`, `RecordOptions` et les événements (Tâche 5).
- Produit :
  - `class Settings extends ChangeNotifier`, avec les champs `mic`, `audio`, `mode` (`simple` / `speakers`, défaut `speakers`), `model` (défaut `small`), `speakers` (défaut `-1` = automatique), `threshold` (défaut `0.5`), `nameFolder` (défaut null) et `offline` (défaut `true` une fois les modèles présents). Méthodes `load()` / `save()` via `shared_preferences`.
  - `enum SessionPhase { idle, starting, recording, stopping, transcribing, done, summarizing, error }`.
  - `class SessionController extends ChangeNotifier`, avec :
    - les propriétés `phase`, `elapsed`, `micLevel`, `audioLevel`, `segments` (`List<SegmentEvent>`), `warnings`, `error` (`ErrorEvent?`), `transcriptPath`, `notesPath` ;
    - les méthodes `start()`, `stop()`, `summarize()`, `reset()`.

  Table de transitions, à copier dans un commentaire du fichier :

| Phase actuelle | Action / événement | Phase suivante |
|---|---|---|
| idle, done, error | `start()` | starting |
| starting | `StartedEvent` | recording |
| starting, recording | `stop()` | stopping |
| stopping | `StoppedEvent` | transcribing |
| transcribing | `DoneEvent` | done |
| done | `summarize()` | summarizing → done (`notesPath` renseigné) |
| toute phase | `ErrorEvent` | error |
| starting … transcribing | `start()` | **ignoré** |

- [ ] **Étape 1 : écrire les tests qui échouent**, avec un faux `EngineClient` :
  - `nominal : start → started → stop → stopped → segments → done` ;
  - `second start while recording is ignored` : un seul appel à `record` ;
  - `stop pendant starting envoie stop et passe à stopping` ;
  - `ErrorEvent device_not_found → phase error, error.code conservé` ;
  - `summarize impossible hors de la phase done` ;
  - `Settings survivent à un redémarrage` (avec `SharedPreferences.setMockInitialValues`) ;
  - `micro mémorisé absent de la liste → retombe sur null (défaut)`.
- [ ] **Étape 2 : `flutter test test/state`**. Résultat attendu : ÉCHEC.
- [ ] **Étape 3 : implémenter.** Le minuteur `elapsed` démarre sur `StartedEvent` et s'arrête sur `StoppedEvent`.
- [ ] **Étape 4 : `flutter test test/state`**. Résultat attendu : RÉUSSITE.
- [ ] **Étape 5 : commit.** `git commit -m "feat(app): réglages persistés + machine à états de session"`

### Tâche 7 : Écran de configuration (choix des périphériques)

**Fichiers :**
- Créer : `app/lib/ui/setup_page.dart`, `app/lib/ui/error_messages.dart`, `app/test/ui/setup_page_test.dart`, `app/test/ui/error_messages_test.dart`
- Modifier : `app/lib/main.dart`

**Interfaces :**
- Consomme : `Settings`, `SessionController`, `EngineClient.listDevices` et `check`.
- Produit :
  - `String messageFor(String code, {required String os})`, qui renvoie le message français par code (warnings et erreurs). Le contenu est repris de la section « Erreurs possibles » de docs/config-<os>.md pour le système concerné.
  - Les clés de widgets `Key('micDropdown')`, `Key('audioDropdown')`, `Key('modeSwitch')`, `Key('speakersField')`, `Key('nameFolderField')`, `Key('startButton')` et `Key('refreshDevices')`.

Contenu de l'écran :
- liste déroulante **Micro** (le défaut en premier, marqué « (par défaut) ») ;
- liste déroulante **Son de l'ordinateur**, avec les sources plus « Aucun ». Si la liste est vide sur Mac : un encart « BlackHole n'est pas installé », avec la commande `brew install blackhole-2ch` copiable ;
- interrupteur **Identifier les intervenants** ;
- champ **Nombre d'intervenants** (vide = automatique) ;
- **Modèle** : `tiny`, `base`, `small`, `medium` ou `large-v3` ;
- **Dossier** (`nameFolder`) ;
- bouton **Actualiser** ;
- gros bouton **Lancer**.

- [ ] **Étape 1 : écrire les tests qui échouent.**
  - `affiche les micros et sélectionne le défaut` ;
  - `"Aucun" envoie audio="none"` ;
  - `Lancer appelle SessionController.start avec les réglages` ;
  - `Mac sans source → encart BlackHole visible` ;
  - `Windows sans source → pas d'encart BlackHole` ;
  - `nameFolder contenant "/" → bouton Lancer désactivé + message` ;
  - `messageFor couvre tous les codes du protocole pour chaque os` : boucle sur `ERROR_CODES` et les codes de warning, aucun message vide.
- [ ] **Étape 2 : `flutter test test/ui`**. Résultat attendu : ÉCHEC.
- [ ] **Étape 3 : implémenter**, avec l'OS détecté via `Platform` dans `main.dart`, transmis en paramètre (testable).
- [ ] **Étape 4 : `flutter test test/ui`**. Résultat attendu : RÉUSSITE.
- [ ] **Étape 5 : commit.** `git commit -m "feat(app): écran de choix des périphériques"`

### Tâche 8 : Écrans d'enregistrement et de résultat

**Fichiers :**
- Créer : `app/lib/ui/recording_page.dart`, `app/lib/ui/result_page.dart`, `app/lib/ui/widgets/level_meter.dart`, et les tests correspondants dans `app/test/ui/`

**Interfaces :**
- Consomme : `SessionController` (Tâche 6), `messageFor` (Tâche 7).

Comportement :
- **Enregistrement** : chronomètre, deux vu-mètres (micro et son de l'ordinateur), bouton **Arrêter** (`Key('stopButton')`). Les avertissements s'affichent en bandeau, par exemple `system_silent` : « Aucun son de la visio… ».
- **Transcription** : indicateur de l'étape en cours (téléchargement du modèle, identification des voix, transcription), et segments affichés au fil de l'eau.
- **Résultat** : texte complet sélectionnable, et les boutons **Copier**, **Ouvrir le dossier** (`open` / `explorer` / `xdg-open`), **Nouvelle réunion** et **Générer le compte rendu (Claude)** (`Key('summarizeButton')`). Ce dernier ouvre **toujours** une boîte de confirmation : « La transcription sera envoyée à Anthropic (États-Unis). Continuer ? ». Il est désactivé, avec une infobulle, si `check.claude == false`.

- [ ] **Étape 1 : écrire les tests qui échouent.**
  - `Arrêter appelle stop()` ;
  - `vu-mètre audio masqué si audio == null` ;
  - `bandeau warning affiche messageFor(code)` ;
  - `segments ajoutés en direct` ;
  - `compte rendu : annuler la confirmation n'appelle pas summarize()` ;
  - `compte rendu : confirmer appelle summarize()` ;
  - `bouton compte rendu désactivé si claude absent` ;
  - `phase error → message + bouton Réessayer qui revient à la configuration`.
- [ ] **Étape 2 : `flutter test test/ui`**. Résultat attendu : ÉCHEC.
- [ ] **Étape 3 : implémenter.**
- [ ] **Étape 4 : `flutter test` (toute la suite)**. Résultat attendu : RÉUSSITE.
- [ ] **Étape 5 : vérification manuelle sur Mac**, avec le vrai moteur. Une réunion de 2 minutes avec BlackHole et le périphérique à sorties multiples doit donner une transcription des deux voix. Puis fermer l'application pendant un enregistrement : `ps aux | grep engine.py` ne doit plus rien afficher au bout de 5 s.
- [ ] **Étape 6 : commit.** `git commit -m "feat(app): écrans enregistrement et résultat"`

### Tâche 9 : Premier lancement et modèles

**Fichiers :**
- Modifier : `script/engine.py` (nouvelle commande `download --model <taille> [--diarization]`), `docs/protocol.md`, `app/lib/ui/setup_page.dart`
- Tester : `tests/test_engine.py`, `app/test/ui/setup_page_test.dart`

**Interfaces :**
- Produit : la commande moteur `download`, qui émet `progress{stage:"download_model", percent}` puis `done{}`.

- [ ] **Étape 1 : tests qui échouent.**
  - Python : `test_download_emits_progress_then_done`, en `slow`, avec le modèle `tiny`.
  - Dart : `modèle absent selon check → bouton "Télécharger le modèle" à la place de Lancer` ; `pendant le téléchargement → barre de progression`.
- [ ] **Étape 2 : implémenter.** Une fois les modèles présents, l'application lance toujours le moteur avec `HF_HUB_OFFLINE=1` (réglage `offline`).
- [ ] **Étape 3 : tests verts, puis commit.** `git commit -m "feat: téléchargement des modèles depuis l'application"`

### Tâche 10 : Empaquetage (application autonome, sans Python installé)

**Fichiers :**
- Créer : `packaging/engine.spec` (PyInstaller), `packaging/build_engine.py`
- Modifier : `app/lib/engine/engine_locator.dart`, `.github/workflows/ci.yml` (job `release` sur les tags `v*`)

- [ ] **Étape 1 : test Dart qui échoue.** `EngineLocator en mode release trouve <bundle>/engine/engine(.exe)`, avec une arborescence simulée.
- [ ] **Étape 2 : écrire `engine.spec`** en mode `--onedir`. Ajouter les imports cachés et les données pour `faster_whisper` (assets, dont `silero_vad_v6.onnx`), `ctranslate2`, `sherpa_onnx`, `onnxruntime`, `soundcard` et `_soundfile_data`.
- [ ] **Étape 3 : `python3 packaging/build_engine.py`**, puis `dist/engine/engine devices --os mac`. Résultat attendu : un événement `devices` valide.
- [ ] **Étape 4 : copier `dist/engine/` dans le bundle**, à l'emplacement attendu sur chaque OS (`Contents/Resources/engine` sur Mac, à côté de l'`.exe` sous Windows, `lib/engine` sous Linux), et adapter `EngineLocator`.
- [ ] **Étape 5 : job CI `release`.** Il construit le moteur et l'application sur les 3 OS et publie les artefacts (`.app` zippée, dossier Windows zippé, archive `.tar.gz` Linux). Pas de signature ni de notarisation Apple dans cette tâche : c'est une décision à prendre plus tard, car ça demande un compte Apple Developer.
- [ ] **Étape 6 : commit.** `git commit -m "build: moteur autonome PyInstaller + artefacts de release"`

### Tâche 11 : Documentation v2 et recette par système

**Fichiers :**
- Créer : `docs/architecture-app.md`, `docs/recette-v2.md`
- Modifier : `README.md` (nouvelle section « Application (v2) » en tête, les sections v1 restent)

- [ ] **Étape 1 : `docs/architecture-app.md`**, avec le même gabarit que les documents v1 :
  - le schéma Flutter ↔ moteur ↔ fichiers ;
  - les services externes, inchangés : Hugging Face et GitHub pour les modèles, Anthropic seulement sur le bouton compte rendu ;
  - les données stockées, y compris les réglages `shared_preferences`, qui ne contiennent pas de données personnelles ;
  - les points de souveraineté.
- [ ] **Étape 2 : `docs/recette-v2.md`**, une liste de vérification à cocher sur une **vraie machine** par système :
  - le micro seul ;
  - le micro et le son de l'ordinateur (BlackHole sur Mac, loopback Windows, monitor Debian) ;
  - le refus de l'autorisation micro ;
  - un périphérique débranché pendant l'enregistrement ;
  - la fermeture de l'application pendant un enregistrement ;
  - une réunion d'1 h (durée et mémoire) ;
  - le mode hors ligne ;
  - le compte rendu Claude avec annulation puis confirmation.
- [ ] **Étape 3 : README.** Installation de l'application par système, captures d'écran, renvoi vers les pages docs/config-<os>.md pour les erreurs.
- [ ] **Étape 4 : commit.** `git commit -m "docs: architecture et recette v2"`

---

## Ordre et parallélisation

```
T0 ─► T1 ─► T2 ─► T3 ─────────────────────────────► T9 ─► T10 ─► T11
            │                                        ▲
            └─► T4 (squelette + VÉRIF MICRO MAC) ─► T5 ─► T6 ─► T7 ─► T8
```

- T4 peut commencer **dès T1 terminée**. C'est même conseillé, pour lever tôt le risque d'autorisation micro sur macOS.
- T5 ne dépend que du contrat (T1) : elle peut avancer en parallèle de T2 et T3, puisque ses tests utilisent un faux processus.
- Un agent par tâche, sur une branche par tâche (`v2/t3-engine`…). Revue avant de fusionner.

## Harness des agents : résumé

| Élément | Rôle | Créé en |
|---|---|---|
| `AGENTS.md` (+ `CLAUDE.md`, `copilot-instructions.md`) | Règles communes à Claude Code, Copilot, Codex… | T0 |
| `docs/protocol.md` | Contrat unique entre le moteur et l'application. Toute modification touche la doc et les tests des deux côtés | T1 |
| `LMT_AUDIO_BACKEND=fake` | Tests sans micro ni carte son (CI, agents) | T2 |
| `tools/check_no_meeting_data.py` + CI | Bloque tout commit de données de réunion | T0 |
| `.claude/settings.json` | Pas de `git push`, pas d'accès à `reunions/` | T0 |
| Marqueur `pytest -m slow` | Sépare les tests qui téléchargent des modèles | T3 |
| Vérifications manuelles bloquantes (T4 étape 3, T8 étape 5) | Ce que le CI ne peut pas tester : vraies autorisations, vrai son | T4, T8 |
| `docs/recette-v2.md` | Validation finale sur Windows et Debian réels | T11 |
