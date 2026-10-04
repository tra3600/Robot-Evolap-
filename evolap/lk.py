"""Flot optique de Lucas-Kanade itératif, pyramidal, en numpy pur.

Convention : une image est indexée img[y, x] ; un point est un tuple (x, y) flottant.
"""

import numpy as np

MIN_EIGEN = 1e-3  # valeur propre minimale (par pixel) de ATA en dessous de laquelle le point est rejeté


def _echantillonne(img, xs, ys):
    """Interpolation bilinéaire de img aux coordonnées (xs, ys). NaN hors de l'image."""
    h, w = img.shape
    hors = (xs < 0) | (ys < 0) | (xs > w - 1) | (ys > h - 1)
    x = np.clip(xs, 0, w - 1.0001)
    y = np.clip(ys, 0, h - 1.0001)
    x0 = np.floor(x).astype(int)
    y0 = np.floor(y).astype(int)
    fx, fy = x - x0, y - y0
    val = (img[y0, x0] * (1 - fx) * (1 - fy) + img[y0, x0 + 1] * fx * (1 - fy)
           + img[y0 + 1, x0] * (1 - fx) * fy + img[y0 + 1, x0 + 1] * fx * fy)
    return np.where(hors, np.nan, val)


def _reduit(img):
    """Image sous-échantillonnée d'un facteur 2 (moyenne 2x2)."""
    h, w = (img.shape[0] // 2) * 2, (img.shape[1] // 2) * 2
    return img[:h, :w].reshape(h // 2, 2, w // 2, 2).mean(axis=(1, 3))


def _pyramide(img, niveaux):
    pyr = [np.asarray(img, dtype=np.float32)]
    for _ in range(niveaux - 1):
        if min(pyr[-1].shape) < 32:
            break
        pyr.append(_reduit(pyr[-1]))
    return pyr


def calc_LK_terms(imgJ_x, imgJ_y, imgI, imgJ, xs, ys, d):
    """Termes de LK pour un patch : gradients de J en (x+d), et écart temporel J(x+d) - I(x)."""
    Ix = _echantillonne(imgJ_x, xs + d[0], ys + d[1])
    Iy = _echantillonne(imgJ_y, xs + d[0], ys + d[1])
    Itdt = _echantillonne(imgJ, xs + d[0], ys + d[1]) - _echantillonne(imgI, xs, ys)
    return Ix, Iy, Itdt


def resoud_LK(A, b):
    """Résout ATA.d = AT.b. Retourne (dx, dy) ou None si ATA est mal conditionnée."""
    ATA = A.T @ A
    n = max(len(A), 1)
    if np.linalg.eigvalsh(ATA)[0] / n < MIN_EIGEN:
        return None
    dx, dy = np.linalg.solve(ATA, A.T @ b)
    return float(dx), float(dy)


def _suit_point(pyrI, pyrJ, gradsJ, pt, demi, iterations, eps):
    """Suit un point de pyrI[0] vers pyrJ[0]. Retourne (x, y) ou None en cas d'échec."""
    ij = np.arange(-demi, demi + 1, dtype=np.float32)
    offx, offy = np.meshgrid(ij, ij)
    d = np.zeros(2)
    for niveau in range(len(pyrI) - 1, -1, -1):
        echelle = 2.0 ** niveau
        xs = pt[0] / echelle + offx
        ys = pt[1] / echelle + offy
        gx, gy = gradsJ[niveau]
        d = d * 2 if niveau < len(pyrI) - 1 else d
        for _ in range(iterations):
            Ix, Iy, It = calc_LK_terms(gx, gy, pyrI[niveau], pyrJ[niveau], xs, ys, d)
            valide = ~(np.isnan(Ix) | np.isnan(Iy) | np.isnan(It))
            if valide.sum() < 0.5 * valide.size:
                return None
            A = np.stack([Ix[valide], Iy[valide]], axis=1).astype(np.float64)
            b = -It[valide].astype(np.float64)
            delta = resoud_LK(A, b)
            if delta is None:
                return None
            d = d + delta
            if abs(delta[0]) < eps and abs(delta[1]) < eps:
                break
    return (pt[0] + d[0], pt[1] + d[1])


def recherche_points(imgI, imgJ, pts, patch_size=15, niveaux=4, iterations=10, eps=0.01):
    """Retrouve dans imgJ les points pts de imgI.

    Retourne (fpts, trouve) : fpts[i] est le point déplacé (ou le point d'origine si l'échec),
    trouve[i] indique si le suivi a convergé.
    """
    pyrI = _pyramide(imgI, niveaux)
    pyrJ = _pyramide(imgJ, niveaux)
    gradsJ = [(np.gradient(p, axis=1), np.gradient(p, axis=0)) for p in pyrJ]
    demi = patch_size // 2
    fpts, trouve = [], []
    for pt in pts:
        res = _suit_point(pyrI, pyrJ, gradsJ, pt, demi, iterations, eps)
        fpts.append(res if res is not None else tuple(pt))
        trouve.append(res is not None)
    return fpts, trouve


def verification_retour(imgI, imgJ, pts, tol=1.0, **kw):
    """Contrôle aller-retour : suit pts de I vers J puis de J vers I.

    Un point est valide si les deux suivis réussissent et si le retour tombe à moins de tol pixel
    du point initial. Retourne (fpts, statut).
    """
    fpts, ok = recherche_points(imgI, imgJ, pts, **kw)
    retour, ok_retour = recherche_points(imgJ, imgI, fpts, **kw)
    statut = [
        bool(a and b and np.hypot(r[0] - p[0], r[1] - p[1]) <= tol)
        for p, r, a, b in zip(pts, retour, ok, ok_retour)
    ]
    return fpts, statut


def mediane(a):
    """Médiane d'une liste non vide."""
    return float(np.median(a))


def verification_pts(pts, fpts, statut, tol_min=2.0):
    """Ne garde que les déplacements cohérents avec le mouvement médian.

    Retourne (pts_valides, fpts_valides, deplacement_median) ; deplacement_median vaut None
    s'il ne reste aucun point.
    """
    idx = [i for i, s in enumerate(statut) if s]
    if not idx:
        return [], [], None
    dep = np.array([[fpts[i][0] - pts[i][0], fpts[i][1] - pts[i][1]] for i in idx])
    med = np.median(dep, axis=0)
    ecart = np.hypot(*(dep - med).T)
    seuil = max(tol_min, 3 * mediane(ecart))
    garde = [i for i, e in zip(idx, ecart) if e <= seuil]
    dep_med = np.median(np.array([[fpts[i][0] - pts[i][0], fpts[i][1] - pts[i][1]] for i in garde]), axis=0)
    return [pts[i] for i in garde], [fpts[i] for i in garde], (float(dep_med[0]), float(dep_med[1]))


def calculer_correlation(image1, image2, point, patch_size):
    """Corrélation croisée normée (ZNCC, dans [-1, 1]) des patchs autour de point dans les deux images."""
    x, y = int(round(point[0])), int(round(point[1]))
    demi = patch_size // 2
    if min(x, y) < demi or y + demi >= image1.shape[0] or x + demi >= image1.shape[1]:
        return 0.0
    p1 = image1[y - demi:y + demi + 1, x - demi:x + demi + 1].astype(np.float64)
    p2 = image2[y - demi:y + demi + 1, x - demi:x + demi + 1].astype(np.float64)
    p1, p2 = p1 - p1.mean(), p2 - p2.mean()
    den = np.sqrt((p1 ** 2).sum() * (p2 ** 2).sum())
    return float((p1 * p2).sum() / den) if den > 0 else 0.0
