from ursina import *

class ObjetInventaire():

    """Classe pour l'affichage de l'objet dans l'inventaire du joueur

    Attributs:
    --------------

    Publics:

        rot: Vec3
            La rotation de l'objet
        y: float ou int
            La position sur l'axe y de l'objet
        color: couleur prédéfinie sur ursina ou bien rgb
            La couleur de l'objet
    
    Méthode:
    --------------

    Publique:

        affichage: permet d'afficher l'objet

    """


    def __init__(self):
        self.rot = Vec3(10, 90, 0)
        self.y = -1
        self.color = color.white
        self.image = None
    
    def affichage(self, n, p, i) -> None:
        """Fonction permettant d'afficher l'objet

        :param n: permet d'afficher l'objet en fonction de l'empacement choisi par le joueur depuis son inventaire
        :param p: le joueur (pour parenter l'objet plus tard)
        :param i: l'inventaire (pour prendre le modèle de l'objet)

        """
        self.image = Entity(model = i[n], parent=p.camera_pivot, scale=0.25, position=(0.7, self.y, 2.5), rotation=self.rot, color=self.color)
