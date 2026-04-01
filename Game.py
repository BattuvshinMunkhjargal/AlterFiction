"""
Ceci est le code du jeu AlterFiction par TAPE ENTERTAINMENT dans le cadre du projet de fin d'année de NSI en Première
Auteurs : Eddy WANG CHENG, Ithushan INPAKUMAR et Battuvshin MUNKHJARGAL

IMPORTANT, VEUILLEZ LIRE README.txt: DE NOUVELLES INFORMATIONS CONCERNANT LE JEU SONT AJOUTEES SUITE A CETTE NOUVELLE VERSION
NB : Veuillez à lire le blocnote README.txt avant de joueur le jeu, il contient des informations importantes pour une meilleure expérience du jeu.
"""

from ursina import *
from codes.class_slot import *
from codes.class_objet_inventaire import *
from codes.map1_code import map1
from codes.map2_code import map2
from codes.map3_code import map3
from codes.map4_code import map4
from codes.map5_code import map5
from codes.map6_code import map6

inventaire = [None, None, None]  # Cette variable permet de stocker l'inventaire du joueur

def input(key) -> None:
    """
    La fonction input permet de déclencher des évènements en fonction de la touche entrée par le joueur sur son clavier
    
    :param key: prend en entré la touche appuyée par le joueur sur son clavier
    """
    # Si le joueur est dans la première map
    if map1.enabled:
        map1.input(inventaire)
    # Si le joueur est dans la deuxième map
    elif map2.enabled and not map2.fin:
        map2.input(key)
    # Si le joueur est dans la troisième map
    elif map2.fin and map3.active:
        map3.input(key)
    # Si le joueur est dans la quatrième map
    elif map4.active:
        map4.input(key)
    # Si le joueur est dans la cinquième map
    elif map5.active:
        map5.input(key)
    # Si le joueur est dans la sixième map
    elif map6.active:
        map6.input(key)


def update() -> None:
    """
    La fonction permet de modifier l'état de l'environement et des variables à chaque itération de la fonction.
    Cette fonction s'active après chaque frame
    """
    # Si le joueur est dans la première map
    if map1.enabled:   
        map1.update()
    # Si le joueur est dans la deuxième map
    elif map2.enabled and not map2.fin:
        map2.update()
    # Si le joueur est dans la troisème map
    elif map2.fin and map3.active:
        map3.update()
    # Si le joueur est dans la quatrième map
    elif map4.active:
        map4.update()
    # Si le joueur est dans la cinquième map 
    elif map5.active:
        map5.update()
    # Si le joueur est dans la dernière map
    elif map6.active:
        map6.update()
  

# lancement du code Ursina
app = Ursina()

window.fullscreen = True  # met en plein écran 
window.fps_counter.enabled = False  # enlève l'affichage du fps
window.collider_counter.enabled = False  # enlève l'affichage de collision
window.entity_counter.enabled = False  # enlève l'affichage du nombre d'entité

map1.intro()  # Démarre l'introduction

app.run()
