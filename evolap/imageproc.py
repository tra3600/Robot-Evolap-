"""Traitement d'image : conversion en niveaux de gris."""

import numpy as np


def grayscale(imagecolor):
    """Niveaux de gris (max + min) / 2 d'une image couleur.

    Accepte une image (H, W, 3) (convention OpenCV/numpy) ou (3, H, W).
    Une image déjà 2D est renvoyée en float32. Retourne un tableau float32 (H, W).
    """
    img = np.asarray(imagecolor)
    if img.ndim == 2:
        return img.astype(np.float32)
    if img.ndim != 3:
        raise ValueError("image 2D ou 3D attendue")
    if img.shape[-1] != 3 and img.shape[0] == 3:
        img = np.moveaxis(img, 0, -1)
    if img.shape[-1] != 3:
        raise ValueError("l'image doit avoir 3 canaux")
    img = img.astype(np.float32)
    return (img.max(axis=-1) + img.min(axis=-1)) / 2
