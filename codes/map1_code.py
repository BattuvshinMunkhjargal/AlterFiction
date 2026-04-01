"""
Ce code contient la classe de la première map, contenant ses attributs (eléments de la map) et ses méthodes
"""

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from codes.class_slot import *
from codes.commun import *
from codes.map2_code import *

class Map1(Entity):
    """Classe pour la première map du jeu

    Attributs:
    ---------------

    Publics:

        e_lettre : entité et/ou bool
            Permet d'afficher la lettre [e] auprès des objets qui peuvent être en interaction avec le joueur afin d'indiquer leur présence
        lecture : bool
            Permet de savoir si le joueur est en train ou non d'écouter une entité parler (ou lui-même)
        papier : entité et/ou bool
            Permet d'afficher quelconque feuille devant le joueur
        ecran : entité et/ou bool
            Permet d'afficher quelconque ecran devant le joueur
        epreuve_fini : bool
            Savoir si le joueur a fini une épreuve ou non
        pause : bool
            Permet de savoir si le joueur a mis en pause ou non
        debut_affichage: bool
            Permet de savoir si on débute l'affichage du jeu (après l'introduction)
        menu: entité et/ou bool
            Permet d'afficher le menu de pause pour le joueur
        evenement: bool
            Permet de savoir si le joueur est dnas un evènement
        enabled: bool
            Permet d'afficher la map ou non
        code_joueur: list
            Le code entré par le joueur

        Les suivants sont des éléments de la map et les sons

        liste_porte: list
            Contient toutes les portes de la map
        inventaire: list
            contient l'inventaire du joueur
    
    Méthodes:
    ----------

    Publiques:

        debut: Annonce le début du jeu
        intro : permet de lancer l'introduction du jeu
        arret_lecture : permet d'arreter l'écoute du joueur au monstre
        transition_son : ajoute l'effet de son de transition
        disparition_monstre: fait disparaitre le monstre
        porte_code: vérifie le code entré par le joueur
        fin_cantine: marque la fin de l'épreuve
        cuisine_cantine: ajoute la texture de la cantine
        suite_cantine: met la suite de l'épreuve
        epreuve_cantine: lance l'épreuve de la cantine
        evenement_cantine: lance l'evènement de la cantine
        reussit_cantine: regarde si le joueur a réussit l'épreuve
        animation_cantine: lance l'animation de la cantine
        input: déclenche des actions en fonction des touches appuyées du joueur
        update: actualise chaque evenement de la map

    """

    def __init__(self):
        super().__init__()

        app = Ursina()

        self.e_lettre = None
        self.lecture = False 
        self.papier = None
        self.ecran = None
        self.epreuve = False
        self.epreuve_fini = False
        self.pause = False
        self.debut_affichage = False
        self.menu = None
        self.evenement = False
        self.enabled = True

        self.code_joueur = []

        Sky(color=color.black)

        self.player = FirstPersonController(position=(-10, 0, 11), enabled = False, scale = 2.5, collider="box", rotation_y = 90, animation = False, animation1 = False, speed=10)
        self.player.cursor.color = color.white

        self.flashlight = DirectionalLight(parent = camera, rotation=(45,-45,45),color=color.black)
        AmbientLight(color=color.rgb(10, 10, 10))

        Entity(model ="map_1", collider = "box", double_sided = True, color=rgb(181, 172, 162))
        Entity(model="cube", collider = "box", scale=(200,2,200), position=(-10,15,-40), color=color.gray)
        self.porte_start = Entity(model="porte", texture="porte.mtl", position=(7.55,-0.5,-14), collider="box", rotation_y = 180)
        self.porte_a = Entity(model="porte", collider="box", texture="porte.mtl", position =(-84, -0.5, -64.7), rotation_y = 270)
        self.porte_b = Entity(model="porte", collider="box", texture="porte.mtl", position =((-83.8, -0.5, -95.8)), rotation_y = 270)
        self.porte_c = Entity(model="porte", collider="box", texture="porte.mtl", position=(-98.5, -0.5, -110), ferme = False)
        Entity(model="porte", collider="box", texture="porte.mtl", position=(35, -0.5, -40))
        Entity(model="casier", collider="box", color=rgb(50,44,43), double_sided = True)
        Entity(model="casier1", collider="box", double_sided = True, color=rgb(50,44,43))
        Entity(model="casier2",  collider="box", double_sided = True, color=rgb(50,44,43))
        Entity(model="casier3", collider="box", double_sided = True, color=rgb(50,44,43))
        Entity(model="casier4", collider="box", double_sided = True, color=rgb(50,44,43))
        Entity(model="casier5", collider="box", double_sided = True, color=rgb(50,44,43))
        Entity(model="casier6", collider="box", double_sided = True, color=rgb(50,44,43))
        Entity(model="casier7", collider="box", double_sided = True, color=rgb(50,44,43))
        Entity(model="casier8", collider="box", double_sided = True, color=rgb(50,44,43))
        Entity(model="casier9",collider="box", double_sided = True, color=rgb(50,44,43))
        Entity(model="casier10", collider="box", double_sided = True, color=rgb(50,44,43))
        Entity(model="casier11", collider="box", double_sided = True, color=rgb(50,44,43))
        Entity(model="casier12", collider="box", double_sided = True, color=rgb(50,44,43))
        Entity(model="casier13",  collider="box", double_sided = True, color=rgb(50,44,43))
        Entity(model="casier_a", collider="box", double_sided = True, color=rgb(50,44,43))
        Entity(model="casier_b", collider="box", double_sided = True, color=rgb(50,44,43))
        Entity(model="casier_s",collider="box", double_sided = True, color=rgb(50,44,43))
        Entity(model="tableau1", collider="box", color=rgb(41, 94, 28))
        Entity(model="tableau2", collider="box", color=rgb(41, 94, 28))
        Entity(model="tableau3", collider="box", color=rgb(41, 94, 28))
        Entity(model="table_prof1.obj", collider="box", texture="table_prof1.mtl")
        Entity(model="table_prof2.obj", collider="box", texture="table_prof2.mtl")
        Entity(model="table_prof3.obj", collider="box", texture="table_prof3.mtl")
        self.cantine = Entity(model="cantine.obj", texture="cantine.mtl", collider="box", double_sided = True, color=color.dark_gray)
        self.cantine1 = duplicate(self.cantine, position=(0,0,-26))
        self.cantine2 = duplicate(self.cantine, position=(0,0,13))
        self.murs_map1 = Entity(model="murs_map1", color=rgb(169, 142, 45), collider="mesh")
        self.table = Entity(model="table", collider="box", texture="table.mtl", doubled_sided = True, color=rgb(27, 15, 2), position=(-9,0,-3), rotation=(0,180,0))
        duplicate(self.table, position=(-3, 0, -3))
        duplicate(self.table, position=(3, 0, -3))
        duplicate(self.table, position=(-9, 0, -9))
        duplicate(self.table, position=(-3, 0, -9))
        duplicate(self.table, position=(3, 0, -9))
        duplicate(self.table, position=(-9, 0, 3))
        duplicate(self.table, position=(-3, 0, 3))
        duplicate(self.table, position=(3, 0, 3))
        duplicate(self.table, position=(-9, 0, 9))
        duplicate(self.table, position=(-3, 0, 9))
        duplicate(self.table, position=(3, 0, 9))
        duplicate(self.table, position=(-64, 0, -65))
        duplicate(self.table, position=(-70, 0, -65))
        duplicate(self.table, position=(-76, 0, -65))
        duplicate(self.table, position=(-64, 0, -71))
        duplicate(self.table, position=(-70, 0, -71))
        duplicate(self.table, position=(-76, 0, -71))
        duplicate(self.table, position=(-64, 0, -77))
        duplicate(self.table, position=(-70, 0, -77))
        duplicate(self.table, position=(-76, 0, -77))
        duplicate(self.table, position=(-64, 0, -59))
        duplicate(self.table, position=(-70, 0, -59))
        duplicate(self.table, position=(-76, 0, -59))
        duplicate(self.table, position=(-64, 0, -53))
        duplicate(self.table, position=(-70, 0, -53))
        duplicate(self.table, position=(-76, 0, -53))
        duplicate(self.table, position=(-62, 0, -95))
        duplicate(self.table, position=(-68, 0, -95))
        duplicate(self.table, position=(-74, 0, -95))
        duplicate(self.table, position=(-62, 0, -101))
        duplicate(self.table, position=(-68, 0, -101))
        duplicate(self.table, position=(-74, 0, -101))
        duplicate(self.table, position=(-62, 0, -107))
        duplicate(self.table, position=(-68, 0, -107))
        duplicate(self.table, position=(-74, 0, -107))
        duplicate(self.table, position=(-62, 0, -89))
        duplicate(self.table, position=(-68, 0, -89))
        duplicate(self.table, position=(-74, 0, -89))
        duplicate(self.table, position=(-62, 0, -83))
        duplicate(self.table, position=(-68, 0, -83))
        duplicate(self.table, position=(-74, 0, -83))
        self.cle1 = Entity(model="keys", position=(12.5, 0.2, 13), scale=0.25, collider="box", color=color.dark_gray, visible=True)
        self.pad = Entity(model="keypad", scale=2, position=(-93, 4, -110), collider="box", texture="texture_keypad")
        self.cantinier = Entity(model="png_cantinier", scale=7, position=(-27, 5, -74), texture="texture_cantinier", rotation_y = -90)
        self.table_cant = Entity(model="table_cant", collider="box")
        duplicate(self.table_cant, x = self.table_cant.x + 15)
        duplicate(self.table_cant, x = self.table_cant.x + 30)
        duplicate(self.table_cant, x = self.table_cant.x + 45)
        duplicate(self.table_cant, x = self.table_cant.x + 60)
        duplicate(self.table_cant, x = self.table_cant.x + 15, z = self.table_cant.z - 15)
        duplicate(self.table_cant, x = self.table_cant.x + 30, z = self.table_cant.z - 15)
        duplicate(self.table_cant, x = self.table_cant.x + 45, z = self.table_cant.z - 15)
        duplicate(self.table_cant, x = self.table_cant.x + 60, z = self.table_cant.z - 15)
        duplicate(self.table_cant, z = self.table_cant.z - 30)
        duplicate(self.table_cant, x = self.table_cant.x + 15, z = self.table_cant.z - 30)
        duplicate(self.table_cant, x = self.table_cant.x + 30, z = self.table_cant.z - 30)
        duplicate(self.table_cant, x = self.table_cant.x + 45, z = self.table_cant.z - 30)
        duplicate(self.table_cant, x = self.table_cant.x + 60, z = self.table_cant.z - 30)
        self.livre_fond1 = Entity(model="livre", position=(-78, 0.3, -58), collider="box")
        self.livre_fond2 = duplicate(self.livre_fond1, position=(-76, 0.3, -112))
        self.livre_r = duplicate(self.livre_fond1, position=(-70, 0.3, -94))
        self.livre_cours = duplicate(self.livre_fond1, position=(-64, 0.3, -107))
        self.livre_math = duplicate(self.livre_fond1, position=(-66, 0.3, -70))
        self.livre_poeme = duplicate(self.livre_fond1, position=(-66, 0.3, -83))

        self.plaque1 = Entity(model="plane", collider="box", position=(-80,0.1,-125), scale=(4,0.1,30), visible = False)

        self.footstep = Audio("footsteps.mp3", autoplay = False)
        self.slam = Audio("slam.mp3", autoplay = False)
        self.electricité = Audio("electric-sparks.mp3", autoplay = False)

        self.liste_porte = [self.porte_start, self.porte_a, self.porte_b, self.porte_c]

        self.inventaire = [None, None, None]

    def debut(self) -> None:
        """
        Cette méthode permet de changer la valeur de l'attribut debut_affichage afin d'annoncer le début du jeu
        """
        self.debut_affichage = True

    def intro(self) -> None:
        """Méthode de l'introduction
        Elle affiche la vidéo de l'introduction du jeu puis donne le départ à l'affichage des slots de l'inventaire et le début du jeu
        Ne renvoie rien
        """
        self.video = Entity(model="quad", texture="intro_nsi.mp4", parent=camera.ui, scale = (camera.aspect_ratio, 1))
        self.son_intro = Audio("intro_nsi_son.mp3")
        destroy(self.video, 104)  # Détruit la video après qu'elle soit finie, soit 104 secondes
        destroy(self.son_intro, 104)  # De même pour le son de la vidéo
        invoke(affichage_slot, delay=104)  # Débute l'affichage des slots après 104 secondes
        invoke(self.player.enable, delay=104)  # Débute la création du joueur
        invoke(self.debut, delay=104)  # Annonce le début du jeu

    def arret_lecture(self, aut) -> None:
        """Méthode qui donne l'autorisation au joueur de quitter ou non

        :param aut: valeur booléenne qui permet de savoir si le joueur est en train d'écouter ou non une entité parler 

        S'il est en train d'écouter, alors le joueur ne peut pas quitter, sinon il peut

        Exemple:
            Si lecture=True, alors les actions du joueur sont limités (ne peut pas ouvrir le menu)
            Sinon, cela revient à dire que l'entité ou lui-même a fini de parler, et donc qu'il peut ouvrir le menu à son gré
        """
        self.lecture = aut

    def transition_son(self) -> None:
        Audio("transition_son.mp3")


    def disparition_monstre(self) -> None:
        Audio("disparition.mp3")
        destroy(self.cantinier)


    def porte_code(self) -> None:
        """
        Regarde si le code entré par le joueur est correcte
        """
        if len(self.code_joueur) == 4:
            if self.code_joueur == [9, 2, 6, 4]:
                # Si le code est bon, on ouvre la porte
                self.porte_c.rotation_y -= 90
                self.porte_c.x += 3.5
                self.porte_c.z -= 3.5
                self.porte_c.ferme = True
                self.player.enabled = True
                destroy(self.ecran)
                Audio("porte_audio.mp3")
            else:
                self.code_joueur = []
                no = Audio("no.mp3")
                destroy(no, 2)


    def fin_cantine(self) -> None:
        """
        Méthode qui invoque la fin de l'épreuve de la cantine
        """
        self.epreuve_fini = True
        parole("Now I can let you through that door.", "kw.mp3", 4, 4, color.rgb(177, 158, 16), -0.20, True, self)
        invoke(lambda : parole("but", "kw.mp3", 1, 4, color.rgb(177, 158, 16), 0, True, self), delay=5)
        invoke(lambda : parole("careful", "kw.mp3", 1, 6, color.rgb(177, 158, 16), 0, False, self), delay=7)
        invoke(self.disparition_monstre, delay=10)
        invoke(lambda: fin_epreuve(self.player), delay=12)


    def cuisine_cantine(self) -> None:
        """
        Change la texture de l'image devant le joueur lors de l'épreuve dans la cantine
        """
        self.c1.texture = "cantine9"


    def suite_cantine(self) -> None:
        """
        Invoque la suite de l'épreuve de la cantine : passage vers la cuisson
        """
        self.c1.texture = "cantine8"
        Audio("son_ouverture.mp3")
        invoke(self.cuisine_cantine, delay=2)
        invoke(self.transition_son, delay=2)


    def epreuve_cantine(self) -> None:
        """
        Début de l'épreuve de la cantine
        """
        self.c1 = Entity(model="quad", parent=camera.ui, texture="cantine1", scale=(1.8, 1))
        self.epreuve = True
        invoke(lambda : parole("Check the shelf under the counter.", "kw.mp3", 3, 6, color.rgb(177, 158, 16), -0.20, False, self), delay=2)


    def evenement_cantine(self) -> None:
        """
        Déclenche l'évènement de la cantine : le screamer en l'occurrence
        """
        self.evenement = True
        self.player.enabled = False
        video = Entity(model="quad", texture="jumpscare_map1.mp4", parent=camera.ui, scale = (camera.aspect_ratio, 1))
        son_video = Audio("jumpscare_map1_son.mp3", volume=120)
        destroy(video, 3.5)
        destroy(son_video,3.5)
        invoke(lambda : parole("Another miserable human...", "kw.mp3", 3, 0, color.rgb(177, 158, 16), -0.20, False, self), delay = 5)
        invoke(lambda: fin_epreuve(self.player), delay=6)


    def reussit_cantine(self) -> None:
        self.epreuve = False
        steak = Entity(model="quad", texture="steak", parent=camera.ui, scale=.5)
        Audio("noice.mp3")
        s1 = Sequence(0, Func(steak.blink, duration=3))  # Création du type d'animation de l'image
        s1.start() 
        destroy(steak, 3)
        destroy(self.c1, 3)
        invoke(self.fin_cantine, delay=4)


    def animation_cantine(self) -> None:
        self.player.animation = True
    
    def input(self, key) -> None:
        if self.enabled:
            # Regarde si le joueur souhaite quitter ou non après avoir appuyé le bouton échap pour ouvrir le menu
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
            if key == 'escape' and not self.lecture and self.debut_affichage and not self.menu and not self.epreuve and not self.ecran and not self.papier and not self.evenement:  # Si le joueur n'est pas dans une dialogue, que le jeu a débuté, que le meunu n'existe pas déjà, qu'il n'est pas dans une épreuve et pas devant un écran
                self.menu = Entity(model="quad", texture="MENU", parent=camera.ui, scale=(0.5, 0.8))
                self.player.enabled =False
                self.pause = True
            # Permet au joueur de skip l'intro si besoin
            if key == "o" and not self.debut_affichage:
                self.debut_affichage = True
                self.player.enabled = True
                destroy(self.video)  # Détruit la video 
                self.son_intro.stop()  # De même pour le son de la vidéo
                invoke(affichage_slot)  # Débute l'affichage des slots 
            # Activation ou désactivation de la flashlight
            if key == "f":
                if self.flashlight.color == color.rgb(40, 40, 40):
                    self.flashlight.color = color.black
                    Audio("flashlight_clicking.mp3")
                else:
                    self.flashlight.color = color.rgb(40, 40, 40)
                    Audio("flashlight_clicking.mp3")
            # Regarde si le joueur souhaite appuyer sur un slot pour accéder à son inventaire
            if key in ['1', '2', '3'] and not self.epreuve and not self.lecture and not self.ecran and self.debut_affichage:
                dico_chiffre = {'1' : slot1, "2" : slot2, "3" : slot3}
                slot_appuye(dico_chiffre[key], self.player, self.inventaire)
            # Si le joueur est devant un écran (ici le pad pour l'entré du code pour la porte)
            if self.ecran:
                destroy(self.e_lettre)
                # Le bouton [e] est fait pour quitter l'écran
                if key == "e":
                    self.player.enabled = True
                    self.code_joueur = []
                    destroy(self.ecran)
                # S'il utilise sa souris pour cliquer sur l'un des chiffres, on ajoute le numéro associé à l'emplacement
                elif key == 'left mouse down':
                    liste_code_ecran = [[-0.00462961, -0.237963], [-0.0861111, 0.0435185], [0.00185182, 0.0425926], [0.0824074, 0.0444444], [-0.0898148, -0.0546296], [0.00370375, -0.0537037], [0.0824074, -0.0574074], [-0.087037,-0.148148], [-0.000925912, -0.144444], [0.0861111, -0.146296]]
                    for i in liste_code_ecran:
                        if abs(mouse.x - i[0]) < 0.05 and abs(mouse.y - i[1]) < 0.05:
                            self.code_joueur.append(liste_code_ecran.index(i))
                    Audio("bip.mp3")
                    self.porte_code()  # Vérifie le code du joueur avec la réponse
            # Si le joueur est dans une épreuve et qu'il utilise sa souris gauche
            elif held_keys['left mouse'] and self.epreuve:
                # Nous avons ici les conditions qui détectent la texture de l'interface et la position du souris du joueur afin de procéder à la suite des épreuves en assocaint des sons, évènements et paroles
                if abs(mouse.x + 0.127778) < 0.03 and abs(mouse.y +0.305556) < 0.03 and str(self.c1.texture) == "cantine1.png" and not self.lecture:  # La variable lecture permet d'accéder à la suite si et seulement si le joueur a fini d'écouter le monstre
                    self.c1.texture = "cantine2"
                    self.lecture = True
                    Audio("son_ouverture.mp3")
                    self.electricité.play()
                    invoke(lambda : parole("Oh, the wires are broken. Take the tape and fix it.", "kw.mp3", 3, 9, color.rgb(177, 158, 16), -0.3, False, self))
                elif abs(mouse.x - 0.711111) < 0.04 and abs(mouse.y - 0.119444) < 0.3 and str(self.c1.texture) == "cantine2.png" and not self.lecture:
                    self.c1.texture = "cantine3"
                    self.lecture = True
                    Audio("grab.mp3")
                elif abs(mouse.x + 0.469444) < 0.01 and abs(mouse.y + 0.299074) < 0.01 and str(self.c1.texture) == "cantine3.png":
                    self.c1.texture = "cantine4"
                    self.lecture = True
                    self.electricité.stop()
                    invoke(lambda : parole("Good. The power is still off, check the other part of the shelf", "kw.mp3", 3, 7, color.rgb(177, 158, 16), -0.35, False, self))
                elif abs(mouse.x - 0.0666667) < 0.03 and abs(mouse.y + 0.30463) < 0.03 and str(self.c1.texture) == "cantine4.png" and not self.lecture:
                    self.c1.texture = "cantine5"
                    self.lecture = True
                    Audio("son_ouverture.mp3")
                    Audio("olliver.mp3")
                    invoke(lambda : parole("Turn on the generator.", "kw.mp3", 2, 11, color.rgb(177, 158, 16), -0.2, False, self), delay=2)
                elif abs(mouse.x - 0.387037) < 0.03 and abs(mouse.y + 0.256481) < 0.03 and str(self.c1.texture) == "cantine5.png" and not self.lecture:
                    self.c1.texture = "cantine6"
                    self.lecture = True
                    bip = Audio("bip.mp3").play()
                    destroy(bip, 1)
                    invoke(lambda : parole("Take hearth now.", "olliver.mp3", 1, 0, color.red, -0.1, False, self), delay=1)
                elif abs(mouse.x - 0.451852) < 0.05 and abs(mouse.y + 0.414815) < 0.05 and str(self.c1.texture) == "cantine6.png" and not self.lecture:
                    self.c1.texture = "cantine7"
                    self.lecture = True
                    Audio("grab.mp3")
                    invoke(lambda : parole("Good, now we need to cook them.", "kw.mp3", 2, 1, color.rgb(177, 158, 16), -0.2, False, self), delay=1)
                    invoke(self.suite_cantine, delay=2)  # Invoque la suite de l'épreuve (changement de texture)
                elif abs(mouse.x + 0.0574074) < 0.4 and abs(mouse.y - 0.0787037) < 0.1 and str(self.c1.texture) == "cantine9.png" and not self.lecture:
                    self.c1.texture = "cantine10"
                    self.lecture = True
                    invoke(lambda : parole("Perfect. Flip them.", "kw.mp3", 2, 1, color.rgb(177, 158, 16), -0.2, False, self), delay=1)
                    Audio("frying.mp3")
                elif abs(mouse.x + 0.0574074) < 0.4 and abs(mouse.y - 0.0787037) < 0.1 and str(self.c1.texture) == "cantine10.png" and not self.lecture:
                    Audio("frying.mp3")
                    self.lecture = True
                    invoke(lambda : parole("It's time to salt it.", "kw.mp3", 3, 4, color.rgb(177, 158, 16), -0.2, False, self), delay=1)
                    self.c1.texture = "cantine11"
                elif abs(mouse.x - 0.677778) < 0.02 and abs(mouse.y - 0.0175926) < 0.05 and str(self.c1.texture) == "cantine11.png" and not self.lecture:
                    Audio("grab.mp3")
                    self.c1.texture = "cantine12"
                elif abs(mouse.x + 0.0574074) < 0.4 and abs(mouse.y - 0.0787037) < 0.1 and str(self.c1.texture) == "cantine12.png":
                    Audio("shaker.mp3")
                    self.c1.texture = "cantine13"
                    invoke(self.reussit_cantine, delay=8)  # Fin de l'épreuve de la cantine
            # Ici, la condition traduit l'interaction que le joueur a sur son environement : la touche [e] est utilisée pour intéragir avec les objets        
            elif key == "e":
                # Interaction avec la porte de la classe (début) et si elle n'est pas déjà ouverte
                if distance(self.player, self.porte_start) < 3 and self.porte_start.rotation_y != 270:
                    # S'il a la clé, on peut ouvrir la porte
                    if "keys" in self.inventaire:
                        self.porte_start.rotation_y += 90
                        self.porte_start.z -= 3
                        self.porte_start.x -= 3.5
                        self.inventaire[0] = None  # Enlève la clé depuis son inventaire
                        slot1.texture = "slot_normal_vide"
                        destruction()
                        destroy(slot1.image)
                        slot1.affichage()
                        Audio("porte_audio.mp3")
                    # Sinon, on lui dit qu'il ne peut pas et qu'il doit trouver une clé
                    else:
                        print_on_screen("The door is locked...",scale=1.5, position=(-0.15,-0.4), duration=3)
                # Interaction avec la première porte de la classe avec les livres : regarde si la porte n'est pas déjà ouverte
                elif distance(self.player, self.porte_a) < 3 and self.porte_a.rotation_y != 180:
                    self.porte_a.rotation_y -= 90
                    self.porte_a.z += 3.6
                    self.porte_a.x += 3.2
                    Audio("porte_audio.mp3")
                # Interaction avec la deuxième porte de la classe avec les livres : regarde si la porte n'est pas déjà ouverte
                elif distance(self.player, self.porte_b) < 3 and self.porte_b.rotation_y != 180:
                    self.porte_b.rotation_y -= 90
                    self.porte_b.z += 3.6
                    self.porte_b.x += 3.2
                    Audio("porte_audio.mp3")
                # Interaction avec la clé, si la porte n'est pas déjà ouverte et que la clé est bien présente
                elif self.porte_start.rotation_y != 270 and self.cle1.visible and distance(self.player, self.cle1) < 2:
                    print_on_screen("I got a key", scale=1.5, position=(-0.15,-0.4), duration=3)
                    self.cle1.visible = False
                    slot1.texture = "icone_clé"
                    slot1.image.texture = "icone_clé"
                    Audio("rattling-keys.mp3", volume=20)
                    self.inventaire[0] = "keys"
                # Interaction avec le pad du couloir afin d'ouvrir la porte avec le mot de passe
                elif distance(self.player, self.pad) < 6 and self.porte_c.rotation_y != -90 and not self.porte_c.ferme:
                    print_on_screen("Press e to quit and use mouse to click.",scale=1, position=(-0.15,-0.4), duration=3)
                    if not self.ecran:
                        self.ecran = Entity(model = "quad", scale=(0.4, 0.6), parent=camera.ui, origin = (0,0), texture="ecran_pad")
                        self.player.enabled = False
                # Si aucune de ces interactions n'a eu lieu, cela revient à dire que le joueur a intéragit avec les livres
                else:
                    dico_livre = {self.livre_fond1 : "plainte", self.livre_fond2 : "unknow", self.livre_r : "Diary", self.livre_cours : "Biology", self.livre_math : "math", self.livre_poeme : "Gate_fantasy"}  # Dictionnaire contenant les textures des livres
                    liste_livre = [self.livre_fond1, self.livre_fond2, self.livre_r, self.livre_cours, self.livre_math, self.livre_poeme]
                    # Boucle qui regarde quel livre est souhaité par le joueur
                    for i in liste_livre:
                        if distance(self.player, i) < 5:
                            # Si le papier n'est pas déjà ouverte, on l'ouvre
                            if not self.papier:
                                Audio("paper.mp3")
                                self.player.enabled = False
                                self.papier = Entity(model = "quad", scale=(0.4, 0.6), parent=camera.ui, origini=(0,0), texture= dico_livre[i])
                            # Sinon, on le détruit
                            else:
                                Audio("paper.mp3")
                                self.player.enabled = True
                                destroy(self.papier)

    def update(self) -> None:
        if self.enabled:
        # Bruits des pas du joueur
            if held_keys["a"] or held_keys["w"] or held_keys["s"] or held_keys["d"]:
                if not self.footstep.playing:
                    self.footstep.play()
            else:
                self.footstep.stop()

            # Première animation du joueur dans la map
            if self.player.animation:
                # On regarde si le joueur a atteint la position prévue en changeant sa rotation_y du joueur
                if abs(self.player.rotation_y - 25) > 1:
                    self.player.rotation_y += time.dt * 70
                else:
                    # Si l'aniamtion est finie, on peut débuter la seconde animation du joueur
                    self.player.animation = False
                    self.player.animation1 = True
            
            # Regarde si le joueur est proche de la position, en l'occurrence proche de la porte de fin, alors on peut passer à la deuxième map
            if distance(self.player, (36.2322, 0, -43.149)) < 5 and self.epreuve_fini:
                map2.enabled = True
                self.enabled = False
                self.footstep.stop()
                scene.clear()  # On supprime toute la première map
                map2.initialisation()
            
            # Deuxième animation du joueur, de même pour la première
            if self.player.animation1:
                if abs(self.player.rotation_y + 90) > 1:  # Jusqu'à ce que le joueur ne soit pas proche de la cible attendue (ici rotaiton_y=-90), alors on continue de le faire tourner
                    self.player.rotation_y -= time.dt * 70
                else:
                    # Dès l'animation finie, on fait en sorte que le joueur ne puisse plus refaire l'animation
                    self.player.animation1 = False

            # Regarde si le joueur est proche de la position requise pour déclencher l'évènement
            if self.enabled and abs(self.player.x - 56) < 26 and abs(self.player.z + 90) < 20 and self.porte_c.rotation_y == 0 and not self.evenement:
                self.evenement_cantine()

            # Regarde si le joueur a passé la porte du couloir, ainsi on referme la prote derrière lui
            if self.player.intersects(self.plaque1).hit and self.porte_c.x == -95:
                self.porte_c.position = (-98.5, -0.5, -110)
                self.porte_c.rotation_y += 90
                if self.porte_c.rotation_y != 90:
                    self.slam.play()
                    invoke(self.slam.stop, delay=2)

            # Regarde si le joueur est proche de la position pour lancer l'épreuve de la cantine
            if self.enabled and abs(self.player.x + 15) < 8 and abs(self.player.z + 74) < 10 and self.evenement:
                destroy(self.player)
                self.player = FirstPersonController(position=(-15, 0, -74), scale = 2.5, enabled = False, rotation_y = -90, animation = False, animation1 = False, speed=10)
                self.player.cursor.color = color.white
                self.evenement = False
                self.lecture = True  # limite les libertés du joueur : il est en train d'écouter et ne peut donc pas quitter en appuyant sur le menu
                # Début des paroles du monstre cantinier
                invoke(lambda : parole("Again...", "kw.mp3", 3, 1, color.rgb(177, 158, 16), -0.2, True, self), delay=1)
                invoke(lambda : parole("Yes, I saw your friends earlier...", "kw.mp3", 3, 4, color.rgb(177, 158, 16), -0.2, True, self), delay=4)
                invoke(lambda : parole("There were just like you... lost", "kw.mp3", 3, 7, color.rgb(177, 158, 16), -0.2, True, self), delay=9)
                invoke(lambda : parole("Where am I ?", "None", 3, 0, color.white, -0.2, True, self), delay=12)
                invoke(lambda : parole("Somewhere...", "kw.mp3", 3, 12, color.rgb(177, 158, 16), -0.2, True, self), delay=16)
                invoke(lambda : parole("How do I get out of this place ?", "None", 3, 0, color.white, -0.2, True, self), delay=20)
                invoke(lambda : parole("You just need to pass this door.", "kw.mp3", 3, 16, color.rgb(177, 158, 16), -0.2, True, self), delay=24)
                invoke(self.animation_cantine, delay=25)
                invoke(lambda : parole("But.", "kw.mp3", 2, 2, color.rgb(177, 158, 16), -0.1, True, self), delay=28)
                invoke(lambda : parole("Just before I let you through, you got to help me.", "kw.mp3", 4, 6, color.rgb(177, 158, 16), -0.3, True, self), delay=31)
                invoke(lambda : parole("For what ?", "None", 2, 0, color.white, -0.2, True, self), delay=36)
                invoke(self.epreuve_cantine, delay=39)

            # Les prochaines conditions affichent la lettre [e] si le joueur est proche des objets/entités pour indiquer l'interaction possible avec le joueur
            # Regarde si le joueur est proche de la clé et qu'elle est visible, si oui, on affiche l'icone [e] pour indiquer l'action possible d'intéraction du joueur
            elif self.cle1.visible and distance(self.cle1, self.player) < 2:
                    self.cle1.color = color.white*100
                    if not self.e_lettre:
                        self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # Regarde s'il est à côté de la porte du couloir fermée
            elif self.enabled and self.porte_c.rotation_y != -90 and distance(self.pad, self.player) < 6 and not self.porte_c.ferme:
                if not self.e_lettre and not self.ecran:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # Regarde s'il est à côté du premier livre
            elif self.enabled and abs(self.player.z - self.livre_fond1.z) < 3 and abs(self.livre_fond1.x - self.player.x) < 3 and self.porte_c.rotation_y != -90 and not self.porte_c.ferme:
                self.livre_fond1.color = color.white*100
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # Deuxième livre
            elif self.enabled and abs(self.player.z - self.livre_fond2.z) < 3 and abs(self.livre_fond2.x - self.player.x) < 4 and self.porte_c.rotation_y != -90 and not self.porte_c.ferme:
                self.livre_fond2.color = color.white*100
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # Troisième livre
            elif self.enabled and abs(self.player.z - self.livre_r.z) < 5 and abs(self.livre_r.x - self.player.x) < 5 and self.porte_c.rotation_y != -90 and not self.porte_c.ferme:
                self.livre_r.color = color.white*100
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # Quatrième livre
            elif self.enabled and abs(self.player.z - self.livre_cours.z) < 5 and abs(self.livre_cours.x - self.player.x) < 5 and self.porte_c.rotation_y != -90 and not self.porte_c.ferme:
                self.livre_cours.color = color.white*100
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # Cinquième livre
            elif self.enabled and abs(self.player.z - self.livre_math.z) < 4 and abs(self.livre_math.x - self.player.x) < 4 and  self.porte_c.rotation_y != -90 and not self.porte_c.ferme:
                self.livre_math.color = color.white*100
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # Sixième livre
            elif self.enabled and abs(self.player.z - self.livre_poeme.z) < 4 and abs(self.livre_poeme.x - self.player.x) < 5 and self.porte_c.rotation_y != -90 and not self.porte_c.ferme:
                self.livre_poeme.color = color.white*100
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # Sinon, on regarde si le joueur est à côté des portes
            else:         
                for i in self.liste_porte:
                    if self.enabled and distance(i, self.player) < 2:
                        # On regarde si la porte du début peut etre en interaction avec le joueur
                        if self.porte_start.rotation_y != 270 and not self.e_lettre and not self.cle1.visible:
                            self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
                            break
                        elif i != self.porte_start:
                            # Si le joueur est à côté d'une porte non ouverte et qu'il n'est pas la porte du début
                            if i.rotation_y != 180 and not self.e_lettre:
                                self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
                            break 
                
                # Sinon, le joueur n'a pas intéragit, donc on supprime l'image [e] si elle est présente
                if self.e_lettre and distance(self.porte_start, self.player) > 2 and distance(self.porte_a, self.player) > 2 and distance(self.porte_b, self.player) > 2:
                    destroy(self.e_lettre)

                self.cle1.color = color.dark_gray
                self.livre_fond1.color = color.white
                self.livre_fond2.color = color.white
                self.livre_r.color = color.white
                self.livre_cours.color = color.white
                self.livre_math.color = color.white
                self.livre_poeme.color = color.white

map1 = Map1()