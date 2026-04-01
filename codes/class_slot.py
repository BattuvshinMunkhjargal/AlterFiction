from ursina import *

class InventaireSlot():
    """Classe pour les images des slots de l'inventaire du joueur

    Attributs:
    ---------------

    Publics:

        texture : str
            La texture que l'image prend
        scale : float
            La taille de l'image
        x : float
            La position x
        y : float
            La position y
        image : Entity (ursina)
            L'image de l'objet qui apparaîtra sur l'écran
        agrandie : bool
            Savoir si l'image est agrandie ou non
    
    Méthodes:
    ----------

    Publiques:

        retrecissement : permet de rétrécir l'image du slot
        grossissement : permet de grossir l'image du slot
        affichage : affiche l'image du slot sur l'interface du joueur

    """
    def __init__(self, x, texture):
        """Constructeur de la calsse InventaireSlot

        :param texture: prend en compte la texture que le slot doit prendre

        """
        self.texture = texture
        self.scale = 0.1
        self.x = x
        self.y = 4.5
        self.image = None
        self.agrandie = False
    
    def retrecissement(self) -> None:
        """Méthode de rétrécissement de l'image du slot

        Cela réduit sa taille, change sa position y et change la valeur booléene agrandie de l'obet

        """
        self.scale /= 1.5
        self.y = 4.5
        self.agrandie = False
        slot1.x = 8.4
        slot2.x = 7.4
        slot3.x = 6.4
    
    def grossissement(self) -> None:
        """Méthode d'agrandissement de l'image du slot

        Cela augmente sa taille, change sa position y et change la valeur booléeene agrandie de l'objet
        Puis, il doit aussi changer l'emplacement des autres slots en fonction du slot souhaité changer.

        """
        self.scale *= 1.5
        self.y = 2.85
        self.agrandie = True
        if self == slot1:
            slot1.x = 5.44
            slot2.x = 6.9
            slot3.x = 5.9
            slot2.agrandie = False
            slot3.agrandie = False
        elif self == slot2:
            slot1.x = 8.4
            slot2.x = 4.79
            slot3.x = 5.95
            slot1.agrandie = False
            slot3.agrandie = False
        else:
            slot1.x = 8.4
            slot2.x = 7.4
            slot3.x = 4.1
            slot2.agrandie = False
            slot1.agrandie = False

    def affichage(self) -> None:
        """Méthode de l'affichage de l'image du slot

        Crée une nouvelle entité ursina avec tous ses paramètres

        """
        self.image = Entity(model = "quad", texture = self.texture, scale = (self.scale, self.scale), parent=camera.ui, origin = (self.x, self.y))

slot1 = InventaireSlot(8.4, "slot_normal_vide.png")
slot2 = InventaireSlot(7.4, "slot_normal_vide.png")
slot3 = InventaireSlot(6.4, "slot_normal_vide.png")
