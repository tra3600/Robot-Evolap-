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

# Exemple d'utilisation
fenetre = [100, 150, 200, 100]
centre_fenetre = centre(fenetre)
print(centre_fenetre)  # Devrait afficher (200.0, 200.0)

