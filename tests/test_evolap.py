import cv2
import numpy as np
import pytest

from evolap import (PatternTracker, PanTiltController, SimulatedMotor, centre,
                    construction_coordonnees_pts, creation_patch, grayscale,
                    recherche_points, verification_fenetre, verification_retour)
from evolap.__main__ import scene_demo, main


def texture(seed=0, shape=(240, 320)):
    rng = np.random.default_rng(seed)
    return cv2.GaussianBlur(rng.integers(0, 256, shape, dtype=np.uint8), (0, 0), 3).astype(np.float32)


def decale(img, dx, dy):
    m = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(img, m, (img.shape[1], img.shape[0]), flags=cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_REFLECT)


def test_geometrie():
    assert verification_fenetre(800, 600, [100, 100, 200, 150])
    assert not verification_fenetre(800, 600, [700, 100, 200, 150])
    assert not verification_fenetre(800, 600, [0, 0, 0, 10])
    assert centre([100, 150, 200, 100]) == (200.0, 200.0)
    pts = construction_coordonnees_pts([100, 150, 200, 100], 4, 3)
    assert len(pts) == 12 and pts[0] == (100, 150) and pts[-1] == (300, 250)
    assert construction_coordonnees_pts([0, 0, 10, 10], 1, 1) == [(5.0, 5.0)]
    assert len(creation_patch((50, 50), 5)) == 25


def test_grayscale_formats():
    img = np.random.default_rng(1).integers(0, 256, (10, 20, 3), dtype=np.uint8)
    g = grayscale(img)
    assert g.shape == (10, 20)
    assert np.allclose(grayscale(np.moveaxis(img, -1, 0)), g)
    assert g[0, 0] == (int(img[0, 0].max()) + int(img[0, 0].min())) / 2


@pytest.mark.parametrize("dx,dy", [(3.0, -2.0), (-1.5, 4.0), (12.0, 7.0)])
def test_lk_retrouve_translation(dx, dy):
    I = texture()
    J = decale(I, dx, dy)
    pts = construction_coordonnees_pts([100, 80, 100, 60], 3, 3)
    fpts, trouve = recherche_points(I, J, pts)
    assert all(trouve)
    for p, f in zip(pts, fpts):
        assert abs(f[0] - p[0] - dx) < 0.3 and abs(f[1] - p[1] - dy) < 0.3


def test_lk_zone_uniforme_echoue():
    plat = np.full((100, 100), 128, dtype=np.float32)
    _, trouve = recherche_points(plat, plat, [(50, 50)])
    assert trouve == [False]


def test_verification_retour_et_bords():
    I = texture()
    J = decale(I, 2, 2)
    _, statut = verification_retour(I, J, [(160, 120), (1, 1)])
    assert statut == [True, False]  # le point au bord n'est pas suivable


def test_tracker_suit_motif():
    base = texture(shape=(300, 400))
    tracker = PatternTracker([150, 100, 80, 80])
    tracker.update(base)
    for k in range(1, 6):
        fen, ok = tracker.update(decale(base, 3 * k, -2 * k))
        assert ok
    assert abs(fen[0] - (150 + 15)) < 1.5 and abs(fen[1] - (100 - 10)) < 1.5


def test_tracker_fenetre_invalide():
    with pytest.raises(ValueError):
        PatternTracker([390, 100, 80, 80]).update(texture(shape=(300, 400)))


def test_controleur():
    moteur = SimulatedMotor()
    c = PanTiltController(moteur, 640, 480)
    assert c.commande((320, 240)) == (0.0, 0.0)
    pan, tilt = c.suit((480, 60))
    assert pan == pytest.approx(0.5) and tilt == pytest.approx(-0.75)
    assert moteur.history == [(pan, tilt)]


def test_cli_demo(capsys):
    main(["--source", "demo", "--no-display"])
    assert "Terminé" in capsys.readouterr().out
