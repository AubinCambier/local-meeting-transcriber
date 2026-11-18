# Licences des composants tiers

Ce projet est sous licence MIT (voir [LICENSE](LICENSE)). Il **ne contient ni ne redistribue** aucun des composants ci-dessous :
- les bibliothèques Python sont installées par l'utilisateur avec `pip` ;
- les modèles sont téléchargés depuis leur source officielle au premier lancement ;
- BlackHole est installé séparément par l'utilisateur.

Chaque composant reste soumis à sa propre licence. Si une version future du projet **inclut** l'un d'eux (par exemple des modèles embarqués dans l'application), il faudra joindre sa licence et ses mentions de copyright.

Licences vérifiées le 18 novembre 2026 sur les pages officielles indiquées.

## Bibliothèques Python

| Composant | Licence | Copyright | Source |
|---|---|---|---|
| faster-whisper | MIT | © 2023 SYSTRAN | https://github.com/SYSTRAN/faster-whisper |
| sherpa-onnx | Apache 2.0 | k2-fsa | https://github.com/k2-fsa/sherpa-onnx |
| SoundCard | BSD-3-Clause | © 2016 Bastian Bechtold | https://github.com/bastibe/SoundCard |
| python-soundfile | BSD-3-Clause | © 2013 Bastian Bechtold | https://github.com/bastibe/python-soundfile |
| NumPy | BSD-3-Clause | © 2005-2026 NumPy Developers | https://github.com/numpy/numpy |
| Silero VAD (fourni avec faster-whisper) | MIT | © 2020-present Silero Team | https://github.com/snakers4/silero-vad |

## Modèles d'IA téléchargés au premier lancement

| Modèle | Licence | Origine | Source |
|---|---|---|---|
| Whisper `small` / `medium` / `large-v3`, conversion CTranslate2 | MIT (conversion Systran) ; poids d'origine OpenAI publiés sous Apache 2.0 | OpenAI, converti par SYSTRAN | https://huggingface.co/Systran/faster-whisper-small |
| Segmentation pyannote 3.0 (version ONNX de sherpa-onnx) | MIT | pyannote | https://huggingface.co/pyannote/segmentation-3.0 |
| WeSpeaker ResNet34-LM, entraîné sur VoxCeleb | CC BY 4.0 (licence du jeu de données VoxCeleb, selon la documentation WeSpeaker) | WeSpeaker | https://github.com/wenet-e2e/wespeaker/blob/master/docs/pretrained.md |

### Attributions et citations demandées

- **Whisper** : A. Radford et al., *Robust Speech Recognition via Large-Scale Weak Supervision*, 2022, arXiv:2212.04356.
- **pyannote segmentation 3.0** : A. Plaquet et H. Bredin, *Powerset multi-class cross entropy loss for neural speaker diarization*, Interspeech 2023 ; H. Bredin, *pyannote.audio 2.1 speaker diarization pipeline*, Interspeech 2023.
- **WeSpeaker** : modèle d'empreinte vocale issu du projet WeSpeaker (https://github.com/wenet-e2e/wespeaker).
- **VoxCeleb** : A. Nagrani, J. S. Chung, A. Zisserman, *VoxCeleb: a large-scale speaker identification dataset*, Interspeech 2017 ; J. S. Chung, A. Nagrani, A. Zisserman, *VoxCeleb2: Deep Speaker Recognition*, Interspeech 2018 ; A. Nagrani et al., *VoxCeleb: Large-scale speaker verification in the wild*, Computer Speech & Language, 2019.

## Logiciel installé séparément (Mac)

| Composant | Licence | Point d'attention |
|---|---|---|
| BlackHole (Existential Audio Inc.) | Code source GPL-3.0 ; binaires officiels « All rights reserved » | L'utilisateur l'installe lui-même : aucun problème. **Ne pas l'inclure** dans un installateur ou une application distribuée sans licence d'Existential Audio, sauf si ce projet passe en GPL-3.0. Source : https://github.com/ExistentialAudio/BlackHole |

## Service externe optionnel

`meeting-agent.py` utilise **Claude Code** (Anthropic) pour rédiger le compte rendu. Son utilisation est soumise aux conditions d'Anthropic et du compte de l'utilisateur, pas à une licence open source.
