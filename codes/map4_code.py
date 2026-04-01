"""
Ce code contient la classe de la quatrième map, contenant ses attributs (eléments de la map) et ses méthodes
"""
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from codes.class_slot import *
from codes.commun import *
from codes.map5_code import *

class Map4(Entity):
    """Classe pour la quatrième map du jeu

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
        lecture : bool
            Permet de savoir si le joueur est en train ou non d'écouter une entité parler (ou lui-même)
        inventaire: list
            contient l'inventaire du joueur
        active: bool
            regarde si la map est toujours active (si on doit charger la map suivante ou non)
    
    Méthodes:
    ----------

    Publiques:

        initialisation: charge les éléments de la map
        arret_lecture: permet d'arreter l'écoute du joueur au monstre
        animation_joueur: Méthode qui donne le départ pour la première animation du joueur
        seconde_animation_joueur: Méthode qui donne le départ pour la deuxième animation du joueur
        troisieme_animation_joueur: Méthode qui donne le départ pour la troisième animation du joueur
        fin_parole: Méthode qui marque la fin du parole du monstre, ce qui débute le son de l'ambiance et remet l'emplacement du joueur à zéro
        parole_monstre_indication: Méthode qui traduit la suite des paroles du monstre ainsi que l'enclenchement des animations à des temps donnés
        input: déclenche des actions en fonction des touches appuyées du joueur
        update: actualise chaque evenement de la map

    """
    
    def __init__(self):
        super().__init__()

        self.enabled = False
        self.e_lettre = None
        self.pause = False
        self.menu = None
        self.lecture = False
        self.inventaire = [None, None, None]
        self.active = False
    
    def initialisation(self) -> None:
        app = Ursina()

        self.active = True

        Sky(color=color.dark_gray)

        self.player = FirstPersonController(collider="box", rotation_y = 90,  speed=10, z=2, enabled = False, y=-0.5, animation1=False, animation2 = False, animation3 = False, animation4 = False)
        self.player.cursor.color = color.white

        Entity(model="plane", collider="box", scale=400, color=color.dark_gray)

        self.monstre = Entity(model="boule.obj", collider="box", texture="boule_texture", scale=2, position=(2,1.5,2))
        Entity(model="maison.obj", scale=30, texture="maison.jpg",position=(150,5,0))
        self.porte = Entity(model="porte_central1", position=(-40,0,-113), collider="box", rotation_y = 90)
        Entity(model="cube", collider="box", x=10, scale=(2,100,400), visible=False)
        Entity(model="cube", x=200, scale=(2,100,400), collider="box", visible=False)
        Entity(model="cube", x=-200, scale=(2,100,400), collider="box", visible=False)
        Entity(model="cube", z=200, scale=(400,100,2), collider="box", visible=False)
        Entity(model="cube", z=-200, scale=(400,100,2), collider="box", visible=False)
        scene.fog_density = 0.01 
        self.screamer = Audio("davis.mp3", fini = False)

        self.footstep = Audio("footsteps.mp3", autoplay = False)
 
    def arret_lecture(self, aut) -> None:
        """Méthode qui donne l'autorisation au joueur de quitter ou non

        :param aut: valeur booléenne qui permet de savoir si le joueur est en train d'écouter ou non une entité parler 

        S'il est en train d'écouter, alors le joueur ne peut pas quitter, sinon il peut

        Exemple:
            Si lecture=True, alors les actions du joueur sont limités (ne peut pas ouvrir le menu)
            Sinon, cela revient à dire que l'entité ou lui-même a fini de parler, et donc qu'il peut ouvrir le menu à son gré
        """
        self.lecture = aut

    def animation_joueur(self) -> None:
        self.player.animation1 = True


    def seconde_animation_joueur(self) -> None:
        self.player.animation2 = True


    def troisieme_animation_joueur(self) -> None:
        self.player.animation3 = True


    def fin_parole(self) -> None:
        self.player.y = 0
        Audio("ambiance_3_5.mp3")
        self.player.enabled =True


    def parole_monstre_indication(self) -> None:
        invoke(lambda : parole("You're trespassing!", "boulardo.wav", 3, 1, color.rgb(177, 158, 16), -0.2, True, self), delay=1)
        invoke(lambda : parole("My God... One of your type again.", "boulardo.wav", 4, 6, color.rgb(177, 158, 16), -0.3, True, self), delay=5)
        invoke(lambda : parole("Where am I again?  I thought that it was the end!", None, 4, -0.1, color.white, -0.4, True, self), delay=10)
        invoke(lambda : parole("Wait...", None, 2, 0, color.white, 0, True, self), delay=15)
        invoke(self.animation_joueur, delay=16)
        invoke(lambda : parole("Is that my house behind you ?", None, 3, 0, color.white, -0.2, True, self), delay=18)
        invoke(self.seconde_animation_joueur, delay=20)
        invoke(lambda : parole("Maybe.", "boulardo.wav", 2, 10, color.rgb(177, 158, 16), 0, True, self), delay=22)
        invoke(lambda : parole("Let me in please, I want to go", None, 3, 0, color.white, -0.2, True, self), delay=25)
        invoke(lambda : parole("HOME", None, 3, 0, color.red, 0.32, True, self), delay=25)
        invoke(lambda : parole("Well, you can if you turn on the electrical power plant.", "boulardo.wav", 4, 8, color.rgb(177, 158, 16), -0.35, True, self), delay=29)
        invoke(lambda : parole("Where is it?", None, 2, 0, color.white, -0.1, True, self), delay=34)
        invoke(lambda : parole("The door on your right.", "boulardo.wav", 3, 5, color.rgb(177, 158, 16), -0.2, True, self), delay=37)
        invoke(self.troisieme_animation_joueur, delay=38)
        invoke(lambda : parole("Oh and by the way...", "boulardo.wav", 3, 2, color.rgb(177, 158, 16), -0.1, True, self), delay=42)
        invoke(lambda : parole("There is a guy that follows you in 'your' house.", "boulardo.wav", 4, 7, color.rgb(177, 158, 16), -0.2, True, self), delay=46)
        invoke(lambda : parole("Thanks.", None, 2, 0, color.white, -0.1, False, self), delay=51)
        invoke(self.fin_parole, delay=53)
    
    def input(self, key) -> None:
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
        if self.active:
            if held_keys["a"] or held_keys["w"] or held_keys["s"] or held_keys["d"]:
                if not self.footstep.playing:
                    self.footstep.play()
            else:
                self.footstep.stop()
    
    def update(self) -> None:
        if self.active:
            # On débute les paroles du joueur après que le screamer soit fini
            if not self.screamer.playing and not self.screamer.fini:
                self.screamer.fini = True
                self.parole_monstre_indication()

            # Joue la première animation
            if self.player.animation1:
                if abs(self.player.z - 4) > 1:
                    self.player.z += time.dt
                else:
                    self.player.animation1 = False
            # Deuxième animation
            if self.player.animation2:
                if abs(self.player.rotation_y - 135) > 1:
                    self.player.rotation_y += time.dt * 15
                    self.monstre.rotation_y += time.dt * 15
                else:
                    self.player.animation2 = False
            # Troisième animation
            if self.player.animation3:
                if abs(self.player.rotation_y - 180) > 1:
                    self.player.rotation_y += time.dt * 18
                else:
                    self.player.animation3 = False
                    self.player.animation4 = True
            # Quatrième animation
            if self.player.animation4:
                if abs(self.player.rotation_y - 135) > 1:
                    self.player.rotation_y -= time.dt * 18
                else:
                    self.player.animation4 = False
            
            # Regarde si le joueur est proche de la porte, on passe donc à la map suivante
            if distance(self.player, self.porte) < 4:
                self.footstep.stop()
                scene.clear()
                self.active = False
                self.enabled = False
                map5.initialisation()
                map5.enabled = True

map4 = Map4()