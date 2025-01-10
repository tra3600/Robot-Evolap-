def demande_valeur(text):
    """
    Simule la récupération d'une valeur entière demandée à l'utilisateur.
    Pour ce contexte, nous allons utiliser la fonction input() et gérer les erreurs.
    """
    while True:
        try:
            valeur = int(input(text))
            return valeur
        except ValueError:
            print("Veuillez entrer une valeur entière.")

def demande_fenetre():
    """
    Demande à l'utilisateur de définir la zone d'intérêt et renvoie un tableau
    contenant les 4 informations recueillies [Px, Py, L, H].
    """
    Px = demande_valeur("Entrez la coordonnée x du point supérieur gauche (Px) : ")
    Py = demande_valeur("Entrez la coordonnée y du point supérieur gauche (Py) : ")
    L = demande_valeur("Entrez la largeur de la fenêtre (L) : ")
    H = demande_valeur("Entrez la hauteur de la fenêtre (H) : ")
    return [Px, Py, L, H]

# Exemple d'utilisation
""" fenetre = demande_fenetre()
print(fenetre)"""


def verification_fenetre(image_width, image_height, fenetre):
    """
    Vérifie que la fenêtre soit bien à l'intérieur de l'image.
    
    Paramètres:
    - image_width: largeur de l'image
    - image_height: hauteur de l'image
    - fenetre: tableau contenant les informations [Px, Py, L, H]
    
    Retourne:
    - True si la fenêtre est définie correctement, False sinon.
    """
    Px, Py, L, H = fenetre
    if Px < 0 or Py < 0 or Px + L > image_width or Py + H > image_height:
        return False
    return True
"""""
# Exemple d'utilisation
image_width = 800
image_height = 600
fenetre = [100, 100, 200, 150]  # Modifiez ces valeurs pour tester
print(verification_fenetre(image_width, image_height, fenetre))  # Devrait afficher True ou False
"""

def centre(fenetre):
    """
    Calcule le centre de la fenêtre définie par fenetre=[Px, Py, L, H].
    
    Paramètres:
    fenetre (list): Liste contenant les coordonnées du point supérieur gauche (Px, Py),
                    la largeur (L) et la hauteur (H) de la fenêtre.
    
    Retourne:
    tuple: Coordonnées (x, y) du centre de la fenêtre.
    """
    Px, Py, L, H = fenetre
    centre_x = Px + L / 2
    centre_y = Py + H / 2
    return (centre_x, centre_y)
"""
# Exemple d'utilisation
fenetre = [100, 150, 200, 100]
centre_fenetre = centre(fenetre)
print(centre_fenetre)  # Devrait afficher (200.0, 200.0)
"""

import numpy as np

def grayscale(imagecolor):
    """
    Convertit une image en couleur en niveaux de gris.
    
    Paramètres:
    - imagecolor: Tableau à trois dimensions représentant une image en couleur (3 x m x n).
    
    Retourne:
    - image: Tableau à deux dimensions (m x n) représentant l'image en niveaux de gris.
    """
    # Dimensions de l'image
    m, n = imagecolor.shape[1], imagecolor.shape[2]
    
    # Initialisation de l'image en niveaux de gris
    image = np.zeros((m, n), dtype=int)
    
    # Conversion en niveaux de gris
    for i in range(m):
        for j in range(n):
            max_val = max(imagecolor[0][i][j], imagecolor[1][i][j], imagecolor[2][i][j])
            min_val = min(imagecolor[0][i][j], imagecolor[1][i][j], imagecolor[2][i][j])
            image[i][j] = (max_val + min_val) // 2
    
    return image

# Exemple d'utilisation
# Création d'une image en couleur aléatoire pour tester la fonction
imagecolor = np.random.randint(0, 256, (3, 800, 600), dtype=int)

# Conversion en niveaux de gris
image_grayscale = grayscale(imagecolor)
print(image_grayscale.shape)  # Devrait afficher (800, 600)


def construction_coordonnees_pts(fenetre, numM, numN):
    """
    Construit les coordonnées des points d'intérêt répartis régulièrement dans la fenêtre.
    
    Paramètres:
    fenetre (list): Liste contenant les coordonnées du point supérieur gauche (Px, Py),
                    la largeur (L) et la hauteur (H) de la fenêtre.
    numM (int): Nombre de points souhaités horizontalement.
    numN (int): Nombre de points souhaités verticalement.
    
    Retourne:
    list: Tableau de points d'intérêt dans l'ordre [P1x, P1y, P2x, P2y, ...].
    """
    Px, Py, L, H = fenetre
    dx = L // (numM - 1)
    dy = H // (numN - 1)
    
    points = []
    for j in range(numN):
        for i in range(numM):
            x = Px + i * dx
            y = Py + j * dy
            points.append((x, y))
    
    return points
"""
# Exemple d'utilisation
fenetre = [100, 150, 200, 100]
numM = 4
numN = 3
points = construction_coordonnees_pts(fenetre, numM, numN)
print(points)
"""

def construction_coordonnees_pts(fenetre, numM, numN):
    """
    Construit les coordonnées des points d'intérêt répartis régulièrement dans la fenêtre.
    
    Paramètres:
    fenetre (list): Liste contenant les coordonnées du point supérieur gauche (Px, Py),
                    la largeur (L) et la hauteur (H) de la fenêtre.
    numM (int): Nombre de points souhaités horizontalement.
    numN (int): Nombre de points souhaités verticalement.
    
    Retourne:
    list: Tableau de points d'intérêt dans l'ordre [P1x, P1y, P2x, P2y, ...].
    """
    Px, Py, L, H = fenetre
    dx = L // (numM - 1)
    dy = H // (numN - 1)
    
    points = []
    for j in range(numN):
        for i in range(numM):
            x = Px + i * dx
            y = Py + j * dy
            points.append((x, y))
    
    return points

# Exemple d'utilisation
fenetre = [100, 150, 200, 100]
numM = 4
numN = 3
points = construction_coordonnees_pts(fenetre, numM, numN)
print(points)


def creation_patch(P, patch_size):
    """
    Crée un patch de taille patch_size x patch_size autour du point P.
    
    Paramètres:
    P (list): Coordonnées [Px, Py] du point central.
    patch_size (int): Taille du patch (nombre de points choisis horizontalement et verticalement).
    
    Retourne:
    list: Tableau de coordonnées des points dans le patch.
    """
    Px, Py = P
    half_size = patch_size // 2
    patch = []
    
    for j in range(-half_size, half_size + 1):
        for i in range(-half_size, half_size + 1):
            patch.append((Px + i, Py + j))
    
    return patch

# Exemple d'utilisation
P = [50, 50]
patch_size = 5
patch = creation_patch(P, patch_size)
print(patch)


def calc_LK_terms(pixP, imgI, imgJ):
    ux, uy = pixP
    Ix = (imgI[ux+1, uy] - imgI[ux-1, uy]) / 2
    Iy = (imgI[ux, uy+1] - imgI[ux, uy-1]) / 2
    Itdt = imgJ[ux, uy] - imgI[ux, uy]
    return Ix, Iy, Itdt

def calc_Ab(imgI, imgJ, patch):
    """
    Calcule les matrices A et b pour un patch donné.
    
    Paramètres:
    imgI (2D array): Image précédente en niveaux de gris.
    imgJ (2D array): Image courante en niveaux de gris.
    patch (list): Liste des coordonnées des points dans le patch.
    
    Retourne:
    tuple: Matrice A et vecteur b.
    """
    A = []
    b = []
    
    for pixP in patch:
        Ix, Iy, Itdt = calc_LK_terms(pixP, imgI, imgJ)
        A.append([Ix, Iy])
        b.append(-Itdt)
    
    return np.array(A), np.array(b)

# Exemple d'utilisation
imgI = np.random.randint(0, 256, (800, 600))
imgJ = np.random.randint(0, 256, (800, 600))
patch = creation_patch([50, 50], 5)
A, b = calc_Ab(imgI, imgJ, patch)
print(A)
print(b)


def resoud_LK(A, b):
    """
    Résout le système ATA.d = AT.b pour obtenir les déplacements dx et dy.
    
    Paramètres:
    A (2D array): Matrice A.
    b (1D array): Vecteur b.
    
    Retourne:
    tuple: Les composantes dx et dy du déplacement.
    """
    AT = A.T
    ATA = np.dot(AT, A)
    ATb = np.dot(AT, b)
    d = np.linalg.solve(ATA, ATb)
    return d[0], d[1]

# Exemple d'utilisation
dx, dy = resoud_LK(A, b)
print(dx, dy)
