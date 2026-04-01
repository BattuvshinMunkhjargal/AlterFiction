"""
Ce code commun.py contient toutes les fonctions globales/générales/communes du jeu aux différentes cartes du jeu
"""

from ursina import *
from codes.class_slot import *
from codes.class_objet_inventaire import *
import random
        
def affichage_slot() -> None:
    """
    Fonction qui permet d'afficher les slots de l'inventaire tout en les actualisant en fonction des textures
    """
    global debut_affichage

    debut_affichage = True  # Débute l'affichage des slots de l'inventaire

    # Nous recréons chaque slot afin d'actualiser l'image en fonction des changements de textures
    if slot1.image:
        destroy(slot1.image)
        destroy(slot2.image)
        destroy(slot3.image)

    slot1.affichage()
    slot2.affichage()
    slot3.affichage()


def destruction() -> None:
    """
    Fonction qui détruit l'objet affiché dans l'écran du joueur si le joueur désélectione son slot de l'inventaire
    """
    if item.image:
        destroy(item.image)


def affichage_objet(player, inventaire) -> None:

    """Fonction qui permet d'afficher l'objet que le joueur a dans son inventaire en fonction de son emplacement

    Les conditions permettent de savoir quel objet doit s'afficher en fonction de si un slot est agrandi ou non
    Si aucun des slots sont affichés, alors on détruit l'objet affiché s'il y en a 

    :param player: prend l'entité représentant le joueur (dépend des différentes cartes du jeu)
    :param inventaire: prend en compte l'inventaire actuelle du joueur

    """
    if slot1.agrandie: 
        item.affichage(0, player, inventaire)
    elif slot2.agrandie:
        item.affichage(1, player, inventaire)
    elif slot3.agrandie:
        item.affichage(2, player, inventaire)
    else:
        destruction()


def slot_appuye(slot, player, inventaire) -> None:
    """Fonction permettant de modifier la taille des slots en fonction du souhait du joueur
    
    :param slot: paramètre qui prend en compte quel slot est appuyé par le joueur
    :param player: prend l'entité représentant le joueur (dépend des différentes cartes du jeu)
    :param inventaire: prend en compte l'inventaire actuelle du joueur

    La fonction modifie la taille des slots en fonction de leur états : s'ils sont déjà agrandis ou non

    """
    liste_slot = [slot1, slot2, slot3]  # liste comprenant les trois slots
    temp = []  # liste temporaire qui permet de contenir les slots qui ne sont pas appuyés par le joueur

    # On regarde si le slot appuyé par le joueur est déjà agrandi, si oui alors on le rétrécit (pour la désélectionner)
    if slot.agrandie:
        slot.retrecissement()  # On rétrécit le slot
        destruction()  # On procède à la destruction de l'objet affiché sur l'écran du joueur s'il y en a

    #Sinon, cela revient à dire que le joueur souhaite sélectionner un objet de son inventaire
    else:
        # Nous parcourons la liste des slot afin de les ajouter à la liste temporaire, sauf le slot appuyé par le joueur.
        for j in liste_slot:
            if j == slot:
                continue
            temp.append(j)

        # Si le premier slot de la liste temporaire est déjà agrandi, alors on la rétrécit et on agrandit le slot souhaité par le joueur
        if temp[0].agrandie:
            temp[0].retrecissement()
            slot.grossissement()
            destruction()

        # Si le deuxième slot de la liste temporaire est déjà agrandi, alors on la rétrécit et on agrandit le slot souhaité par le joueur
        elif temp[1].agrandie:
            temp[1].retrecissement()
            slot.grossissement()
            destruction()

        #Sinon, cela revient à dire que le joueur souhaite utiliser l'objet qui se trouve déjà dans le slot souhaité par le joueur
        else:
            slot.grossissement()

    temp = []
    affichage_slot()  # On réaffiche les slots correctement après ces transformations
    affichage_objet(player, inventaire)  # On affiche l'objet depuis l'inventaire si le joueur l'a souhaité

def parole(parole, son, t, deb, clr, x, autorisation, obj) -> None:
    """Fonction qui permet d'afficher les paroles des entités

    :param parole: le texte affiché
    :param son: le bruit qui doit accompagner la parole
    :param t: le temps t de la parole (détruit le son et les sous-titres après ce temps)
    :param deb: le temps pour choisir le début de démarrage de l'audio (choisir le début de l'audio à tel seconde)
    :param clr: la couleur des sous-titres
    :param x: la position sur l'axe x des sous-titres
    :param autorisation: permet de donner l'autorisation au joueur de quitter le jeu ou non (permet d'éviter des erreurs)
    :param obj: prend en compte l'objet de la classe de la map jouée actuellement par le joueur (pour lancer sa méthode plus tard)

    Elle permet d'afficher les sous-titres ainsi que le son s'il y en a besoin

    """
    message = Text(text = parole, scale=1.5, color= clr, position=(x,-0.4))  # Crée les sous-titres
    prl = Audio(son)  # Crée l'audio
    prl.play(start=deb)  # Commence l'audio à tel seconde donnée 
    destroy(prl, t)  # Détruit l'audio après le temps donné
    destroy(message, t)  # Détruit les sous-titres après le temps donné
    invoke(lambda : obj.arret_lecture(autorisation), delay = t)  # Donne l'autorisation ou non au joueur de quitter


def fin_epreuve(player) -> None:
    """
    Redonne la mobilité au joueur après la fin d'une épreuve
    
    :param player: prend en compte l'entité (Ursina) du joueur selon la map

    """
    player.enabled =True

def message_mort() -> None:
    """
    Affiche un message au hasard sur l'écran du joueur lorsqu'il est mort
    """
    i = random.choice(["Skill issue.", "Leave that computer and go touch grass.", "How you died to that ?", "You definitely didn't cook.", "Even my grandma plays better"])
    print_on_screen(i ,scale=1, duration=3, position=(-0.1,0))

item = ObjetInventaire()