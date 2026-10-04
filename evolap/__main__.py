"""Ligne de commande : python -m evolap [--source 0|video.mp4|demo] [--window X Y L H]."""

import argparse
import sys

import cv2
import numpy as np

from .motor import PanTiltController, SimulatedMotor
from .tracker import PatternTracker


def scene_demo(n_frames=120, taille=(480, 640), seed=0):
    """Génère une scène texturée qui dérive : (frames, fenêtre initiale autour du centre)."""
    rng = np.random.default_rng(seed)
    h, w = taille
    texture = cv2.GaussianBlur(rng.integers(0, 256, (h * 2, w * 2), dtype=np.uint8), (0, 0), 3)
    for i in range(n_frames):
        dx = int(60 * np.sin(i / 20))
        dy = int(30 * np.sin(i / 14))
        vue = texture[h // 2 + dy:h // 2 + dy + h, w // 2 + dx:w // 2 + dx + w]
        yield cv2.cvtColor(vue, cv2.COLOR_GRAY2BGR)


def ouvre_source(source):
    if source == "demo":
        return scene_demo()
    cap = cv2.VideoCapture(int(source) if source.isdigit() else source)
    if not cap.isOpened():
        sys.exit(f"Impossible d'ouvrir la source : {source}")

    def frames():
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            yield frame
        cap.release()
    return frames()


def main(argv=None):
    p = argparse.ArgumentParser(prog="evolap", description=__doc__)
    p.add_argument("--source", default="demo", help="indice de caméra, fichier vidéo ou 'demo'")
    p.add_argument("--window", type=int, nargs=4, metavar=("X", "Y", "L", "H"),
                   help="fenêtre initiale ; sinon sélection à la souris (ou centrée en mode sans affichage)")
    p.add_argument("--no-display", action="store_true", help="pas de fenêtre graphique")
    p.add_argument("--output", help="enregistre la vidéo annotée (mp4)")
    args = p.parse_args(argv)

    frames = ouvre_source(args.source)
    premiere = next(frames, None)
    if premiere is None:
        sys.exit("Aucune image reçue.")
    h, w = premiere.shape[:2]

    if args.window:
        fenetre = list(args.window)
    elif args.no_display:
        fenetre = [w // 2 - 50, h // 2 - 50, 100, 100]
    else:
        fenetre = list(cv2.selectROI("Evolap", premiere, showCrosshair=False))
        if fenetre[2] == 0 or fenetre[3] == 0:
            sys.exit("Aucune fenêtre sélectionnée.")

    tracker = PatternTracker(fenetre)
    moteur = SimulatedMotor(verbose=args.no_display)
    pilote = PanTiltController(moteur, w, h)
    writer = cv2.VideoWriter(args.output, cv2.VideoWriter_fourcc(*"mp4v"), 25, (w, h)) if args.output else None

    try:
        tracker.update(premiere)
        for frame in frames:
            fen, ok = tracker.update(frame)
            if ok:
                pilote.suit(tracker.centre)
            else:
                moteur.stop()
            if writer or not args.no_display:
                vue = frame.copy()
                x, y, lw, lh = (int(v) for v in fen)
                cv2.rectangle(vue, (x, y), (x + lw, y + lh), (0, 255, 0) if ok else (0, 0, 255), 2)
                if writer:
                    writer.write(vue)
                if not args.no_display:
                    cv2.imshow("Evolap", vue)
                    if cv2.waitKey(1) & 0xFF in (27, ord("q")):
                        break
    finally:
        moteur.stop()
        if writer:
            writer.release()
        if not args.no_display:
            cv2.destroyAllWindows()
    print(f"Terminé : {len(moteur.history)} commandes moteur, fenêtre finale {[round(v, 1) for v in tracker.fenetre]}")


if __name__ == "__main__":
    main()
