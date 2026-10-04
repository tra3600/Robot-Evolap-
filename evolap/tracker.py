"""Suivi d'une fenêtre d'intérêt image après image."""

from .geometry import centre, construction_coordonnees_pts, verification_fenetre
from .imageproc import grayscale
from .lk import verification_pts, verification_retour


class PatternTracker:
    """Suit un motif contenu dans une fenêtre [Px, Py, L, H].

    update(frame) déplace la fenêtre du mouvement médian des points retrouvés et renvoie
    (fenetre, ok). ok vaut False si le motif est perdu (la fenêtre reste alors inchangée).
    """

    def __init__(self, fenetre, numM=5, numN=5, patch_size=15, min_points=4, tol_retour=1.0):
        self.fenetre = [float(v) for v in fenetre]
        self.numM, self.numN = numM, numN
        self.patch_size = patch_size
        self.min_points = min_points
        self.tol_retour = tol_retour
        self._prev = None

    @property
    def centre(self):
        return centre(self.fenetre)

    def update(self, frame):
        gris = grayscale(frame)
        h, w = gris.shape
        if not verification_fenetre(w, h, self.fenetre):
            raise ValueError(f"fenêtre {self.fenetre} hors de l'image {w}x{h}")
        if self._prev is None:
            self._prev = gris
            return self.fenetre, True
        pts = construction_coordonnees_pts(self.fenetre, self.numM, self.numN)
        fpts, statut = verification_retour(self._prev, gris, pts,
                                           tol=self.tol_retour, patch_size=self.patch_size)
        _, _, dep = verification_pts(pts, fpts, statut)
        self._prev = gris
        n_ok = sum(statut)
        if dep is None or n_ok < self.min_points:
            return self.fenetre, False
        px, py, largeur, hauteur = self.fenetre
        px = min(max(px + dep[0], 0.0), w - largeur)
        py = min(max(py + dep[1], 0.0), h - hauteur)
        self.fenetre = [px, py, largeur, hauteur]
        return self.fenetre, True
