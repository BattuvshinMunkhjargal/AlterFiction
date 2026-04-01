"""
Ce code contient la classe de la deuxième map, contenant ses attributs (eléments de la map) et ses méthodes
"""
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from codes.class_slot import *
import random
from codes.commun import *
from codes.map3_code import *

class Map2(Entity):
    """Classe pour la deuxième map du jeu

    Attributs:
    ---------------

    Publics:

        enabled: bool
            Permet d'afficher la map ou non
        e_lettre : entité et/ou bool
            Permet d'afficher la lettre [e] auprès des objets qui peuvent être en interaction avec le joueur afin d'indiquer leur présence
        pause : bool
            Permet de savoir si le joueur a mis en pause ou non
        menu: entité et/ou bool
            Permet d'afficher le menu de pause pour le joueur
        fin: bool
            Permet de savoir si on a fini la map
    
    Méthodes:
    ----------

    Publiques:

        initialisation: charge les éléments de la map
        mort_map2: engendre les actions nécessaires si le joueur est mort
        random_sound: joue des sons aléatoirement pour l'ambiance
        verif_cite_monstre: vérifie si lemonstre est à côté du joueur
        input: déclenche des actions en fonction des touches appuyées du joueur
        update: actualise chaque evenement de la map

    """


    def __init__(self):
        super().__init__()

        self.enabled = False
        self.e_lettre = None
        self.pause = False
        self.menu = None
        self.fin = False

    def initialisation(self) -> None:

        # Début de l'initialisation des entités de la deuxième map
        Sky(color = color.black)

        self.flashlight = DirectionalLight(parent=camera, rotation=(45, -45, 45), color=color.black)
        AmbientLight(color=rgb(10, 10, 10))

        self.player = FirstPersonController(scale=2.5, position=(-1, 0, 60), collider="box", rotation_y = 180, speed=10)
        self.player.cursor.color = color.white

        Entity(model="cube", position=(-1, 10, 70), scale=(30, 20, 1), color=rgb(169, 142, 45), texture="grass", collider="box")
        Entity(model="porte", position=(-1, -0.5, 69.3), collider="box")
        Entity(model="map2", collider="mesh", double_sided=True, color=rgb(169, 142, 45), texture="grass")
        Entity(model="plane", double_sided = True, scale=200, y = 20, texture="brick", color=rgb(169, 142, 45), texture_scale=(100,100))
        self.plaque = Entity(model="plane", collider="box", position=(-61.2734, 0.2, -65.6333), scale=(10,0.1,4), visible = False)
        self.monstre = Entity(model="foulardo", texture="foulardo_texture", position=(-5.79026, 5, -4.39675), scale=10)
        Entity(model="porte", position=(-63,-0.5,-70), collider="box")
        Entity(model="cube", position=(-63,10,-70.7), scale=(30,20,1), color=rgb(169, 142, 45), texture="grass", collider="box")

        self.footstep = Audio("footsteps_r.mp3", autoplay=False)
        self.ambiance = Audio("ambiance_map2.mp3", volume=0.25)
        self.monstre_son  = Audio("he_sees_you.mp3", autoplay=False)
        self.filtre = None
        self.son = Audio("voices.mp3", autoplay=False)
        Audio("porte_audio.mp3")
        
        slot1.affichage()
        slot2.affichage()
        slot3.affichage()

    def mort_map2(self) -> None:
        """Méthode qui regarde si le joueur est mort dans le labyrinthe (tué par le monstre)
        Elle enlève le filtre, arrête les audios puis replace le joueur et le monstre, tout en lançant le message de mort et le son
        """
        destroy(self.filtre)
        self.monstre_son.stop()
        screen = Entity(model="quad", parent=camera.ui, color=color.black, scale=(1.8, 1))
        Audio("mort_map2.mp3", volume=80)
        message_mort()
        self.player.position = (-1, 0, 60)
        self.monstre.position = (-5.79026, 5, -4.39675)
        destroy(screen, 5)


    def random_sound(self) -> None:
        """
        Joue un audio aléatoirement dans le labyrinthe pour mettre l'ambiance
        """
        i = random.randint(0,1000)
        if i == 50:
            self.son = Audio("scare_map2.mp3", volume=0.25)
        elif i == 100:
            self.son = Audio("voices.mp3", volume=0.5)


    def verif_cote_monstre(self, son) -> None:
        """Méthode qui vérifie si le monstre est toujours à côté du joueur
        S'il n'est plus à côté, on coupe le son et le filtre
        """
        if distance(self.monstre, self.player) > 20:
            son.stop()
            if self.filtre:
                destroy(self.filtre)
                self.filtre = None
    
    def input(self, key) -> None:
        # Si le joueur est en train de se déplacer
        if held_keys["a"] or held_keys["w"] or held_keys["s"] or held_keys["d"]:
            # Si le son n'est pas déjà en cours de lecture, on l'ouvre
            if not self.footstep.playing:
                self.footstep.play()
        # Si le joueur ne bouge plus, on arrête le son
        else:
            self.footstep.stop()
        # Activation ou désactivation de la flashlight
        if key == "f":
            if self.flashlight.color == color.rgb(40, 40, 40):
                self.flashlight.color = color.black
                Audio("flashlight_clicking.mp3")
            else:
                self.flashlight.color = color.rgb(40, 40, 40)
                Audio("flashlight_clicking.mp3")
        # Regarde si le joueur souhaite appuyer sur un slot pour accéder à son inventaire
        if key in ['1', '2', '3']:
            dico_chiffre = {'1' : slot1, "2" : slot2, "3" : slot3}
            slot_appuye(dico_chiffre[key], self.player, self.inventaire)
        if self.pause:
            if held_keys['left mouse']:
                # S'il ne souhaite pas quitter, on redonne la mobilité au joueur et on efface l'image du menu
                if abs(mouse.x + 0.00462961) < 0.15 and abs(mouse.y - 0.0907407) < 0.05:
                    destroy(self.menu)
                    self.pause = False
                    self.player.enabled = True
                elif abs(mouse.x + 0.00462961) < 0.1 and abs(mouse.y + 0.0935185) < 0.05:
                    quit()
        # On crée l'image du menu si le joueur l'ouvre tant que les conditions sont favorables
        if key == 'escape' and not self.menu:  # Si le meunu n'existe pas déjà
            self.menu = Entity(model="quad", texture="MENU", parent=camera.ui, scale=(0.5, 0.8))
            self.player.enabled =False
            self.pause = True

    def update(self) -> None:
        if not self.fin:
            
            self.verif_cote_monstre(self.monstre_son)  # On vérifie si le monstre est à côté du joueur ou non

            # Ici on met les sons de l'ambiance si elle n'est pas activée
            if not self.son.playing:
                self.random_sound()  # Audio aléatoire pour l'ambiance

            self.ray = raycast(self.monstre.position + (0, 1, 0), self.monstre.forward, distance=1)  # raycast envoyé depuis le monstre pour détecter s'il voit le joueur

            # Regarde si le joueur a atteint la fin, comme ça on charge la map suivante
            if self.player.intersects(self.plaque).hit:
                self.fin = True
                self.ambiance.stop()
                self.monstre_son.stop()
                self.son.stop()
                self.footstep.stop()
                scene.clear()
                map3.initialisation()
            
            # Si le monstre est trop rpoche du joueur, le joueur meurt
            elif self.enabled and distance(self.monstre, self.player) < 7:
                self.mort_map2()
            
            # Si le monstre est proche du joueur seulement pour le détecter
            elif self.enabled and distance(self.monstre, self.player) < 20:

                self.ambiance.stop()

                if self.son:
                    self.son.stop()

                if not self.monstre_son.playing:  # Audio du monstre lorsqu'il croise le joueur
                    self.monstre_son.play()
                    self.filtre = Entity(model="quad", parent=camera.ui, texture = "filter_run.mp4", scale=(1.8, 1), alpha=0.05)

                direction_to_player = (self.player.position - self.monstre.position).normalized()
                self.monstre.position = self.monstre.position + Vec3(direction_to_player.x, 0, direction_to_player.z) * time.dt * 7

            # Si le monstre ne le détecte pas, alors s'il voit un mur devant lui il change de direction
            elif self.enabled and self.ray.hit:
                self.monstre.rotation_y = random.choice([0, 90, -90, 180])  # Choisit aléatoriement une direction pour tourner

            # Sinon, on fait avancer le monstre
            else:
                (self.monstre).x += (self.monstre).forward[0] * time.dt 
                (self.monstre).z += (self.monstre).forward[2] * time.dt 

map2 = Map2()