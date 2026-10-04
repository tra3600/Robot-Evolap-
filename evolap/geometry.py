"""Fenêtre d'intérêt [Px, Py, L, H] et grilles de points. Les points sont des tuples (x, y)."""

import numpy as np


def demande_valeur(texte):
    """Demande un entier à l'utilisateur jusqu'à obtenir une saisie valide."""
    while True:
        try:
            return int(input(texte))
        except ValueError:
            print("Veuillez entrer une valeur entière.")


def demande_fenetre():
    """Demande la fenêtre d'intérêt et renvoie [Px, Py, L, H]."""
    px = demande_valeur("Coordonnée x du point supérieur gauche (Px) : ")
    py = demande_valeur("Coordonnée y du point supérieur gauche (Py) : ")
    largeur = demande_valeur("Largeur de la fenêtre (L) : ")
    hauteur = demande_valeur("Hauteur de la fenêtre (H) : ")
    return [px, py, largeur, hauteur]


def verification_fenetre(image_width, image_height, fenetre):
    """True si la fenêtre est non vide et entièrement contenue dans l'image."""
    px, py, largeur, hauteur = fenetre
    if largeur <= 0 or hauteur <= 0:
        return False
    return px >= 0 and py >= 0 and px + largeur <= image_width and py + hauteur <= image_height


def centre(fenetre):
    """Centre (x, y) de la fenêtre [Px, Py, L, H]."""
    px, py, largeur, hauteur = fenetre
    return (px + largeur / 2, py + hauteur / 2)


def construction_coordonnees_pts(fenetre, numM, numN):
    """Grille de numM x numN points régulièrement répartis dans la fenêtre (bords inclus).

    Un seul point sur un axe est placé au milieu de la fenêtre.
    Retourne une liste de (x, y) parcourue ligne par ligne.
    """
    if numM < 1 or numN < 1:
        raise ValueError("numM et numN doivent être >= 1")
    px, py, largeur, hauteur = fenetre
    xs = np.linspace(px, px + largeur, numM) if numM > 1 else [px + largeur / 2]
    ys = np.linspace(py, py + hauteur, numN) if numN > 1 else [py + hauteur / 2]
    return [(float(x), float(y)) for y in ys for x in xs]


def creation_patch(P, patch_size):
    """Points (x, y) d'un patch patch_size x patch_size centré sur P (patch_size impair)."""
    demi = patch_size // 2
    px, py = P
    return [(px + i, py + j) for j in range(-demi, demi + 1) for i in range(-demi, demi + 1)]
