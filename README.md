# Robot Evolap

Suivi d'un motif par flot optique de Lucas-Kanade (numpy pur, pyramidal et itératif) et
pilotage pan/tilt pour garder le motif au centre de l'image.

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
python -m evolap                                 # démo synthétique (sans caméra)
python -m evolap --source 0                      # webcam, sélection de la fenêtre à la souris
python -m evolap --source video.mp4 --window 200 150 100 100 --output suivi.mp4
python -m evolap --no-display                    # sans interface graphique
```

Touche `q` ou `Échap` pour quitter.

## Structure

| Module | Rôle |
|---|---|
| `evolap/geometry.py` | fenêtre `[Px, Py, L, H]`, grille de points, patchs |
| `evolap/imageproc.py` | conversion en niveaux de gris |
| `evolap/lk.py` | Lucas-Kanade, contrôle aller-retour, filtrage par déplacement médian |
| `evolap/tracker.py` | `PatternTracker` : suit la fenêtre image après image |
| `evolap/motor.py` | `PanTiltController` + interface `MotorDriver` |

## Brancher le vrai moteur

Le moteur par défaut est simulé. Pour le matériel, implémenter `MotorDriver.set_speed(pan, tilt)`
(vitesses dans `[-1, 1]`) et le passer à `PanTiltController`.

## Tests

```bash
python -m pytest
```
