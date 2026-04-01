"""
Ce code contient la classe de la cinquième map, contenant ses attributs (eléments de la map) et ses méthodes
"""
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from codes.class_slot import *
from codes.commun import *
from codes.map6_code import *

class Map5(Entity):
    """Classe pour la cinquième map du jeu

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
        inventaire: list
            contient l'inventaire du joueur
        active: bool
            regarde si la map est toujours active (si on doit charger la map suivante ou non)
        eau_epreuve_img: bool et/ou entité (Ursina)
            Affiche l'image de l'épreuve des tuyaux
        code_joueur: list
            Le code entré par le joueur
        papier : entité et/ou bool
            Permet d'afficher quelconque feuille devant le joueur
        ecran : entité et/ou bool
            Permet d'afficher quelconque ecran devant le joueur
        waypoints: list
            comprend les balises que suivra le monstre dans la centrale afin d'avoir un chemin pré-défini
        current_waypoint_index: int
            Permet de connaître la prochaine étape de la position que le monstre  de la centrale doit atteindre (reliée avec la variable waypoints)

        liste_porte: list
            contient toutes les portes de la map
        dico_plaque_porte: dict
            associe chaque plaque à sa porte respective
        liste_plaque: list
            contient toutes les plaques de la map
    
    Méthodes:
    ----------

    Publiques:

        initialisation: charge les éléments de la map
        move_monster_along_pathway: fait avancer le monstre selon le chemin prédéfini
        debut_epreuve_commande: débute l'épreuve de la salle de commande (initialise les éléments)
        bouton_appuye: se déclenche lorsque le joueur a actionné un bouton
        retour_mouse: redonne l'accès à la souris du joueur
        retour_normal_bouton_couleur: remet à l'état normal les boutons (les boutons colorés)
        affiche_instruction_commande: affiche les instructions pour l'épreuve de la salle de commande
        mort_joueur_commande: lorsque le joueur meurt dans l'épreuve de la salle de commande
        commande_reussit: se déclenche lorsque le joueur a réussit l'épreuve de la salle de commande
        avancement_monstre: fait avancer le monstre (salle de commande)
        retour_normale_bouton: remet à l'état normal des boutons (les boutons gris)
        epreuve_bouton: déclenche l'épreuve de la salle de bouton
        etape0: etape 0 de l'épreuve de la salle de commande
        etape1: etape 1 de l'épreuve de la salle de commande
        etape2: etape 2 de l'épreuve de la salle de commande
        verif_code_commande: vérifie la suite de boutons actionnée par le joueur
        retour_porte: remet à l'état normal des portes (les ferme)
        verif_eau: vérifie l'ordre des tuyaux actionnés par le joueur
        mort_central: déclenche la mort lorsque le joueur rencontre le monstre
        input: déclenche des actions en fonction des touches appuyées du joueur
        update: actualise chaque evenement de la map

    """


    def __init__(self):
        super().__init__()

        self.enabled = False
        self.e_lettre = None
        self.pause = False
        self.menu = None
        self.inventaire = [None, None, None]
        self.active = False
        self.eau_epreuve_image = None
        self.code_joueur = []
        self.papier = None
        self.ecran = None

        self.waypoints = [
            (-5, 2, 5.5),     
            (7.75, 2, 5.5),
            (7.75, 2, -5.5),
            (-5, 2, -5.5),
            (7.75, 2, -5.5),
            (7.75, 2, 5.5),
            (-5, 2, 5.5),
        ]
        self.current_waypoint_index = 0
    
    def initialisation(self) -> None:
        app = Ursina()

        self.active = True

        Sky(color=color.black)

        self.player = FirstPersonController(collider="box", rotation_y = 90)
        self.player.cursor.color = color.white

        self.ambient = AmbientLight(color=color.rgb(60, 60, 60))
        self.flashlight = DirectionalLight(parent = camera, rotation=(45,-45,45),color=color.black)

        Entity(model="murs_central.obj", collider="mesh", texture="murs_central.mtl")
        Entity(model="tuyaux", texture="tuyaux.mtl")
        Entity(model="contours_porte", texture="countours_porte.mtl", collider="mesh")
        Entity(model="central_shelves", texture="central_shelves.mtl", collider="mesh")
        Entity(model="carton_central1", texture="carton_central1.mtl", collider="mesh")
        Entity(model="carton_central2", texture="carton_central2.mtl", collider="mesh")
        Entity(model="batteries_groupe1", texture="batteries_groupe1.mtl", collider="box")
        Entity(model="batterie_groupe2", texture="batterie_groupe2.mtl", collider="box")
        Entity(model="batterie", texture="batterie.mtl", collider="box")
        Entity(model="tuyaux_haut", texture="tuyaux_haut.mtl")
        Entity(model="chaise_commande", texture="chaise_commande.mtl", collider="box")
        self.central_commande = Entity(model="central_commande", texture="central_commande.mtl", collider="mesh", epreuve=False, epreuve_finie=False, etape=0)
        Entity(model="employe_etagere1", texture="employe_etagere1.mtl", collider="box")
        Entity(model="employe_etagere", texture="employe_etagere.mtl", collider="box")
        Entity(model="employe_table1", texture="employe_table1.mtl", collider="box")
        Entity(model="employe_table2", texture="employe_table2.mtl", collider="box")
        Entity(model="employe_table3", texture="employe_table3.mtl", collider="box")
        Entity(model="employe_table4", texture="employe_table4.mtl", collider="box")
        self.traitement_eau = Entity(model="traitement_eau", texture="traitement_eau.mtl", collider="box", epreuve_finie = False, epreuve= False)
        Entity(model="range_boss1", texture="range_boss1.mtl", collider="box")
        Entity(model="range_boss2", texture="range_boss2.mtl", collider="box")
        Entity(model="etagere_boss", texture="etagere_boss.mtl", collider="box")
        Entity(model="atelier1", texture="atelier1.mtl", collider="box", color=color.rgb(47, 76, 21))
        Entity(model="atelier2", texture="atelier2.mtl", collider="box", color=color.rgb(47, 76, 21))
        Entity(model="atelier3", texture="atelier3.mtl", collider="box", color=color.rgb(47, 76, 21))
        self.atelier = Entity(model="atelier4", texture="atelier4.mtl", collider="box", fini = False)
        Entity(model="canape1", texture="canape1.mtl", collider="box")
        Entity(model="canape2", texture="canape2.mtl", collider="box")
        Entity(model="canape3", texture="canape3.mtl", collider="box")
        Entity(model="table_invite", texture="table_invite.mtl", collider="box")
        Entity(model="table_boss", texture="table_boss.mtl", collider="box")
        Entity(model="tapis", texture="tapis.mtl")
        self.gen = Entity(model="gen1", texture="gen1.mtl", collider="box", trois_batteries = False, fini =False)
        duplicate(self.gen, z=self.gen.z-4.5)
        duplicate(self.gen, x=self.gen.x-7)
        duplicate(self.gen, x=-7, z=-4.5)

        self.porte1 = Entity(model="porte_central1", texture="porte_central1.mtl", collider="box")
        self.porte2 = Entity(model="porte_central2", texture="porte_central2.mtl", collider="box")
        self.porte3 = Entity(model="porte_central3", texture="porte_central3.mtl", collider="box")
        Entity(model="porte_central4", texture="porte_central4.mtl", collider="box")
        self.porte5 = Entity(model="porte_central5", texture="porte_central5.mtl", collider="box")
        self.porte6 = Entity(model="porte_central6", texture="porte_central6.mtl", collider="box")
        self.porte7 = Entity(model="porte_central7", texture="porte_central7.mtl", collider="box")
        self.porte8 = Entity(model="porte_central8", texture="porte_central8.mtl", collider="box")
        self.porte9 = Entity(model="porte_central9", texture="porte_central9.mtl", collider="box")
        self.porte10 = Entity(model="porte_central10", texture="porte_central10.mtl", collider="box")
        self.porte11 = Entity(model="porte_central11", texture="porte_central11.mtl", collider="box")
        self.porte12 = Entity(model="porte_central12", texture="porte_central12.mtl", collider="box")
        self.porte13 = Entity(model="porte_central13", texture="porte_central13.mtl", collider="box")
        self.porte14 = Entity(model="porte_central14", texture="porte_central14.mtl", collider="box")

        self.plaque1 = Entity(model="plane", scale=(1.5,0.1,3), x=6.5, collider="box", visible=False)
        self.plaque2 = Entity(model="plane", scale=(3,0.1,1), z=-4.2, collider="box", visible=False)
        self.plaque3 = Entity(model="plane", scale=(3,0.1,1), z=4.2, collider="box", visible=False)
        self.plaque5 = Entity(model="plane", scale=(1,0.1,2), position = (-5.5,0,5.5), collider="box", visible=False)
        self.plaque6 = Entity(model="plane", scale=(1,0.1,2), position=(-5.5,0,-5.5), collider="box", visible=False)
        self.plaque7 = Entity(model="plane", scale=(2,0.1,1), position=(-3.5,0,-7), collider="box", visible=False)
        self.plaque8 = Entity(model="plane", scale=(2,0.1,1), z = -7, collider="box", visible=False)
        self.plaque9 = Entity(model="plane", scale=(2,0.1,1), position=(6.2,0,-7), collider="box", visible=False)
        self.plaque10 = Entity(model="plane", scale=(1,0.1,2), position=(10,0,-3.5), collider="box", visible=False)
        self.plaque11 = Entity(model="plane", scale=(1,0.1,2), position=(10,0,3.5), collider="box", visible=False)
        self.plaque12 = Entity(model="plane", scale=(2,0.1,1), position=(7.5,0,7), collider="box", visible=False)
        self.plaque13 = Entity(model="plane", scale=(2,0.1,1), position=(3.7,0,7), collider="box", visible=False)
        self.plaque14 = Entity(model="plane", scale=(2,0,1), position=(-1.5,0,7), collider="box", visible=False)

        self.plaque_eau = Entity(model="plane", scale=(8,0.1,1), position=(-2,0.1,-9), collider="box", visible=False)
        self.plaque_batterie = Entity(model="plane", scale=7.5, position=(14,0.1,-4), visible=False, collider="box")
        self.plaque_commande = Entity(model="plane", scale=4, position=(15,0.1,3.37842), visible=False, collider="box")
        self.plaque_atelier = Entity(model="plane", scale=4, collider="box", position=(5.86188, 0.1, 10.3489), visible=False)
        self.plaque_blueprint = Entity(model="plane", scale=3, collider="box", visible=False, position=(3.8131, 0.1, -9.49606))
        self.plaque_manuel_tuyaux = Entity(model="plane", scale=3, collider="box", visible=False, position=(7.56694, 0.1, -11.9896))
        self.plaque_manuel = Entity(model="plane", scale=4, collider="box", visible=False, position=(-1.66975, 0.1, 12.6974))

        self.manuel_tuyaux = Entity(model="livre", collider="box", position=(5,-0.2,-11), scale=0.5, color = color.rgb(97,79,27), rotation_y = 90)
        self.manuel_commande = Entity(model="livre", collider="box", position=(-4,-0.3,13.5), scale=0.5, color = color.rgb(97,79,27), rotation_y = 90)

        self.monstre = Entity(model="foulardo", texture="foulardo_texture", scale=3, color=color.orange, position=(-5, 2, 6))
        self.blueprint = Entity(model="blueprint", texture="blueprint_texture", position=(4.00302,0.8,-9.41637), visible=True)
        self.boite = Entity(model="metal", texture="metal.jpg", position=(-7.1406, 0.2, 2.39706), visible = True)

        self.footstep = Audio("footsteps_r.mp3", autoplay=False)
        Audio("central_ambiance.mp3", volume=0.5)
        self.grab = Audio("grab.mp3", autoplay=False)

        slot1.affichage()
        slot2.affichage()
        slot3.affichage()

        self.liste_porte = [self.porte1, self.porte2, self.porte3, self.porte5, self.porte6, self.porte7, self.porte8, self.porte9, self.porte10, self.porte11, self.porte12, self.porte13, self.porte14]
        self.dico_plaque_porte = {self.plaque1 : self.porte1, self.plaque2 : self.porte2, self.plaque3 : self.porte3, self.plaque5 : self.porte5, self.plaque6 : self.porte6, self.plaque7 : self.porte7, self.plaque8 : self.porte8, self.plaque9 : self.porte9, self.plaque10 : self.porte10, self.plaque11 : self.porte11, self.plaque12 : self.porte12, self.plaque13 : self.porte13, self.plaque14 : self.porte14}
        self.liste_plaque = [self.plaque1, self.plaque2, self.plaque3, self.plaque5, self.plaque6, self.plaque7, self.plaque8, self.plaque9, self.plaque10, self.plaque11, self.plaque12, self.plaque13, self.plaque14]

        print_on_screen("Ok, what should I do now?", duration=3, position=(-0.35,-0.4), scale=1.5)

    def move_monster_along_pathway(self) -> None:
        """Méthode qui fait avancer un monstre le long d'un chemin prédéfini
        """
        target_position = Vec3(*self.waypoints[self.current_waypoint_index])  # Initialise target_position avec les coordonnées du point de passage actuel dans la liste waypoints

        # Vérifie si le monstre est proche du point de passage
        if distance(self.monstre.position, target_position) < 0.1:
            self.current_waypoint_index = (self.current_waypoint_index + 1) % len(self.waypoints)  # Incrémente l'index du point de passage actuel, en le ramenant à zéro si nécessaire pour boucler sur les points de passage

        direction = target_position - self.monstre.position
        direction.y = 0 
        direction.normalize()  # Normalise le vecteur de direction pour avoir une longueur de 1
        self.monstre.position += direction * 5 * time.dt  


    def debut_epreuve_commande(self) -> None:
        """
        Méthode qui crée toutes les interfaces et éléments associés à l'épreuve de la salle de commande (boutons et images)
        """
        self.player.enabled = False
        self.central_commande.epreuve = True  # Marque le début de l'épreuve (cela revient à dire que le joueur est en train de faire l'épreuve)
        mouse.enabled = False  # Désactive la souris du joueur

        self.ecran = Entity(model="quad", parent=camera.ui, texture="ecran_commande_normal", scale=(1.8, 1))
        self.monstre_ecran = Entity(model="quad", texture="monstre_ecran", scale=0.5, parent=camera.ui, position=(-0.47,0.28))

        # Les boutons colorés
        self.bleu = Button(icon="bouton_bleu", scale=0.13, position=(-0.62,-0.27), on_click = self.bouton_appuye)
        self.rouge = Button(icon="bouton_rouge", scale=0.13, position=(-0.35,-0.27), on_click = self.bouton_appuye)
        self.jaune = Button(icon="bouton_jaune", scale=0.13, position=(-0.1,-0.27), on_click = self.bouton_appuye)
        self.vert = Button(icon="bouton_vert", scale=0.13, position=(0.18,-0.27), on_click = self.bouton_appuye)

        # Les boutons gris
        self.b1 = Button(icon="bouton_gris", scale=0.13, position=(0.49,0.2), on_click = self.bouton_appuye)
        self.b2 = Button(icon="bouton_gris", scale=0.13, position=(0.64,0.2), on_click = self.bouton_appuye)
        self.b3 = Button(icon="bouton_gris", scale=0.13, position=(0.79, 0.2), on_click = self.bouton_appuye)
        self.b4 = Button(icon="bouton_gris", scale=0.13, position=(0.49,0.05), on_click = self.bouton_appuye)
        self.b5 = Button(icon="bouton_gris", scale=0.13, position=(0.64,0.05), on_click = self.bouton_appuye)
        self.b6 = Button(icon="bouton_gris", scale=0.13, position=(0.79,0.05), on_click = self.bouton_appuye)
        self.b7 = Button(icon="bouton_gris", scale=0.13, position=(0.49,-0.1), on_click = self.bouton_appuye)
        self.b8 = Button(icon="bouton_gris", scale=0.13, position=(0.64,-0.1), on_click = self.bouton_appuye)
        self.b9 = Button(icon="bouton_gris", scale=0.13, position=(0.79,-0.1), on_click = self.bouton_appuye)

        invoke(self.etape0, delay=2)


    def bouton_appuye(self) -> None:
        """
        Méthode qui permet de modifier l'état d'un bouton s'il est appuyé
        """
        self.liste_boutons_commande = [self.b1, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7, self.b8, self.b9, self.bleu, self.rouge, self.jaune, self.vert]  # Liste des boutons
        self.liste_bouton_gris = [self.b1, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7, self.b8, self.b9]  # Liste des boutons gris
        self.liste_bouton_couleur = [self.bleu, self.rouge, self.jaune, self.vert]  # Liste des boutons colorés
        self.dico_bouton =  {self.b1 : 1, self.b2 : 2, self.b3 : 3, self.b4 : 4, self.b5 : 5, self.b6 : 6, self.b7 : 7, self.b8 : 8, self.b9 : 9, 
                             self.bleu : "bleu", self.rouge : "rouge", self.jaune : "jaune", self.vert : "vert"}  # Dictionnaire qui permet d'ajouter au code du joueur les éléments en fonction du bouton appuyé

        # On parcourt la liste des boutons pour voir lequel est activé
        for i in self.liste_boutons_commande:
            if i.hovered:
                # Selon les boutons gris ou colorés, il y a des éléments différents à rajouter (le son et la texture)
                if i in self.liste_bouton_gris:
                    i.icon = "bouton_gris_enbleu"
                    Audio("bouton_sound.mp3")
                if i in self.liste_bouton_couleur:
                    Audio("bip.mp3")
                self.code_joueur.append(self.dico_bouton[i])
                break
        self.verif_code_commande()  # On vérifie son code

    def retour_mouse(self) -> None:
        mouse.enabled = True

    def retour_normal_bouton_couleur(self, bouton_c, img) -> None:
        """Remet l'état normal des boutons après l'affichage des instructions

        :param bouton_c: le bouton en question
        :param img: l'icone normal du bouton

        """
        bouton_c.icon = img


    def affiche_instruction_commande(self, bouton_c) -> None:
        """
        Méthode qui affiche les instructions à reproduire par le joueur pour l'épreuve de la salle de commandes

        :param bouton_c: le bouton à remettre dans son état normal

        """
        self.dico_bouton_couleur = {self.bleu : "bleu_son.mp3", self.jaune : "jaune_son.mp3", self.vert : "vert_son.mp3", self.rouge : "rouge_son.mp3"}  # Dictionnaire qui permet de mettre le son voulu en fonction du bouton appuyé
        self.dico_bouton = {self.bleu : "bouton_bleu", self.rouge : "bouton_rouge", self.jaune : "bouton_jaune", self.vert : "bouton_vert"}  # Dictionnaire qui permet de connaître l'icone du bouton
        bouton_c.icon = "bouton_blanc"
        Audio(self.dico_bouton_couleur[bouton_c])
        invoke(lambda : self.retour_normal_bouton_couleur(bouton_c, self.dico_bouton[bouton_c]), delay=0.5)


    def mort_joueur_commande(self) -> None:
        """Méthode qui tue le joueur s'il se trompe sur les instructions de la salle de commande
        On remet à zéro les codes
        """
        self.code_joueur = []
        for i in self.liste_bouton:
            i.icon = "bouton_gris"
        self.screen = Entity(model="quad", parent=camera.ui, color=color.black, scale=(1.8, 1))
        Audio("jackson.mp3", volume=80)
        self.player.enabled = True
        self.central_commande.epreuve = False  # Le joueur n'est plus en train de faire l'épreuve
        self.player.position = (11.8029,0,3.63756)  # On replace le joueur
        destroy(self.screen, 3)
        self.central_commande.etape = 0  # Les étapes sont redevenuent à zéro
        # On détruit l'interface avec les boutons et l'écran de la salle de commande
        for j in [self.b1, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7, self.b8, self.b9, self.vert, self.jaune, self.bleu, self.rouge, self.ecran, self.monstre_ecran]:
            destroy(j)


    def commande_reussit(self) -> None:
        """Méthode qui s'active lorsque le joueur a réussi l'épreuve de la salle de commande
        On met les évènements requis
        """
        Audio("generator_sound.mp3")
        Audio("alarm.mp3")
        self.ambient.color = color.white
        self.central_commande.epreuve_finie = True
        self.central_commande.epreuve = False
        self.code_joueur = []
        self.player.enabled = True
        self.central_commande.etape = 0
        for j in [self.b1, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7, self.b8, self.b9, self.vert, self.jaune, self.bleu, self.rouge, self.ecran, self.monstre_ecran]:
            destroy(j)


    def avancement_monstre(self) -> None:
        """
        Méthode qui fait avancer le monstre de l'écran dans la salle de commande
        """
        Audio("vent.mp3", volume=20)
        self.monstre_ecran.x += 0.28


    def retour_normale_bouton(self, b) -> None:
        """Méthode qui remet l'état normal des boutons gris de la salle de commande

        :param b: le bouton souhaité à revenir dans osn état normal (couleur grise)

        """
        b.icon = "bouton_gris"


    def epreuve_bouton(self, b) -> None:
        """Fonction qui change la couleur des boutons gris pour donenr l'instruction au joueur

        :param b: le bouton en question à mettre en bleu

        """
        b.icon = "bouton_gris_enbleu"
        Audio("bouton_sound.mp3")
        invoke(lambda : self.retour_normale_bouton(b), delay=0.5)  # on remet le bouton dans son état normal


    def etape0(self) -> None:
        invoke(lambda : self.epreuve_bouton(self.b1), delay=1)
        invoke(lambda : self.epreuve_bouton(self.b9), delay=2)
        invoke(lambda : self.epreuve_bouton(self.b5), delay=3)
        invoke(self.retour_mouse, delay=4)


    def etape1(self) -> None:
        mouse.enabled = False
        self.avancement_monstre()
        invoke(lambda : self.epreuve_bouton(self.b1), delay=1)
        invoke(lambda : self.epreuve_bouton(self.b3), delay=2)
        invoke(lambda : self.epreuve_bouton(self.b6), delay=3)
        invoke(lambda : self.epreuve_bouton(self.b7), delay=4)
        invoke(lambda : self.epreuve_bouton(self.b8), delay=5)
        invoke(lambda : self.epreuve_bouton(self.b4), delay=6)
        invoke(lambda : self.affiche_instruction_commande(self.rouge), delay=7)
        invoke(lambda : self.affiche_instruction_commande(self.vert), delay=8)
        invoke(lambda : self.affiche_instruction_commande(self.bleu), delay=9)
        invoke(self.retour_mouse, delay=10)


    def etape2(self) -> None:
        mouse.enabled = False
        self.avancement_monstre()
        invoke(lambda : self.epreuve_bouton(self.b9), delay=0.7)
        invoke(lambda : self.epreuve_bouton(self.b5), delay=1.4)
        invoke(lambda : self.epreuve_bouton(self.b6), delay=2.1)
        invoke(lambda : self.epreuve_bouton(self.b1), delay=2.8)
        invoke(lambda : self.epreuve_bouton(self.b2), delay=3.5)
        invoke(self.avancement_monstre, delay=3.7)
        invoke(lambda : self.epreuve_bouton(self.b7), delay=4.2)
        invoke(lambda : self.epreuve_bouton(self.b4), delay=4.9)
        invoke(lambda : self.epreuve_bouton(self.b8), delay=5.6)
        invoke(lambda : self.epreuve_bouton(self.b3), delay=6.3)
        invoke(lambda : self.affiche_instruction_commande(self.rouge), delay=7)
        invoke(lambda : self.affiche_instruction_commande(self.bleu), delay=7.7)
        invoke(lambda : self.affiche_instruction_commande(self.vert), delay=8.4)
        invoke(lambda : self.affiche_instruction_commande(self.jaune), delay=9.1)
        invoke(lambda : self.affiche_instruction_commande(self.bleu), delay=9.8)
        invoke(self.retour_mouse, delay=10.5)


    def verif_code_commande(self) -> None:
        """
        Méthode qui vérifie si le joueur a respecté les instructions de l'épreuve de la salle de commande
        """
        self.liste_bouton = [self.b1, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7, self.b8, self.b9]

        # En fonction de l'étape que le joueur est
        if self.central_commande.etape == 0:
            # Si le nombre d'élément du code du joueur est la même que la réponse alors on débute la vérification
            if len(self.code_joueur) == 3:
                if self.code_joueur == [1, 9, 5]:
                    Audio("bip.mp3")
                    self.code_joueur = []
                    # On remet les boutons dans leur état normal après que le joueur ait appuyé
                    for i in self.liste_bouton:
                        i.icon = "bouton_gris"
                    self.central_commande.etape += 1
                    self.monstre_ecran.x = -0.47  # le monstre repart à sa position initiale 
                    invoke(self.etape1, delay=1)
                else:
                    self.mort_joueur_commande()  # Si il n'a pas réussi, le joueur est mort
        elif self.central_commande.etape == 1:
            if len(self.code_joueur) == 9:
                if self.code_joueur == [1, 3, 6, 7, 8, 4, "rouge", "vert", "bleu"]:
                    Audio("bip.mp3")
                    self.monstre.x -= 0.28  # le monstre repart à sa position initiale
                    self.code_joueur = []
                    # On remet les boutons dans leur état normal après que le joueur ait appuyé
                    for i in self.liste_bouton:
                        i.icon = "bouton_gris"
                        self.monstre_ecran.x = -0.47 
                    self.central_commande.etape += 1
                    invoke(self.etape2, delay=1)
                else:
                    self.mort_joueur_commande()  # Si il n'a pas réussi, le joueur est mort
        elif self.central_commande.etape == 2:
            if len(self.code_joueur) == 14:
                if self.code_joueur == [9, 5, 6, 1, 2, 7, 4, 8, 3, "rouge", "bleu", "vert", "jaune", "bleu"]:
                    Audio("bip.mp3")
                    self.monstre.x -= 0.56  # le monstre repart à sa position initiale
                    self.code_joueur = []
                    # On remet les boutons dans leur état normal après que le joueur ait appuyé
                    for i in self.liste_bouton:
                        i.icon = "bouton_gris"
                    self.commande_reussit()
                else:
                    self.mort_joueur_commande()  # Si il n'a pas réussi, le joueur est mort

    def retour_porte(self, porte) -> None:
        porte.position = (0,0,0)

    def verif_eau(self) -> None:
        """
        Méthode de l'épreuve des valves qui vérifie la proposition du joueur
        """   
        if len(self.code_joueur) == 6:
            if self.code_joueur == [1,2,4,5,8,7]:
                destroy(self.eau_epreuve_image)
                self.traitement_eau.epreuve = False  # Le joueur n'est plus dans l'épreuve
                self.traitement_eau.epreuve_finie = True  # L'épreuve est finie
                self.player.enabled = True
                self.code_joueur = []
                Audio("steam.mp3")
            else:
                self.traitement_eau.epreuve = False
                print_on_screen("That wasn't the right order.",scale=1.5, position=(-0.15,-0.4), duration=3)
                self.player.enabled = True
                self.player.position=(0,0,0)
                destroy(self.eau_epreuve_image)
                self.code_joueur = []

    def mort_central(self) -> None:
        """
        Méthode qui s'active lorsque le joueur est mort dans la centrale : met le message de mort ainsi que l'audio
        """
        self.screen = Entity(model="quad", parent=camera.ui, color=color.black, scale=(1.8, 1))
        Audio("mort_map2.mp3", volume=80)
        message_mort()
        self.player.position = (0,0,0)
        destroy(self.screen, 5)
        
    def input(self, key) -> None:
        # Bruits de pas
        if held_keys["a"] or held_keys["w"] or held_keys["s"] or held_keys["d"]:
            if not self.footstep.playing:
                self.footstep.play()
        else:
            self.footstep.stop()
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
        if key == 'escape' and not self.menu and not self.traitement_eau.epreuve and not self.central_commande.epreuve:  # Si le meunu n'existe pas déjà
            self.menu = Entity(model="quad", texture="MENU", parent=camera.ui, scale=(0.5, 0.8))
            self.player.enabled =False
            self.pause = True
        # Regarde si le joueur souhaite appuyer sur un slot pour accéder à son inventaire
        if key in ['1', '2', '3'] and not self.traitement_eau.epreuve and not self.central_commande.epreuve:
            dico_chiffre = {'1' : slot1, "2" : slot2, "3" : slot3}
            slot_appuye(dico_chiffre[key], self.player, self.inventaire)
        # Activation ou désactivation de la flashlight
        if key == "f":
            if self.flashlight.color == color.rgb(40, 40, 40):
                self.flashlight.color = color.black
                Audio("flashlight_clicking.mp3")
            else:
                self.flashlight.color = color.rgb(40, 40, 40)
                Audio("flashlight_clicking.mp3")
        # Si le joueur est en train de faire l'épreuve des valves et des tuyaux
        if self.traitement_eau.epreuve:
            if self.player.intersects(self.plaque_eau).hit:
                # On ajoute le numéro correcpond au valve actionné par le joueur
                if held_keys['left mouse']:
                    if distance(mouse.position, (0.268519, -0.231481, 0)) < 0.05:
                        Audio("valve.mp3")
                        self.code_joueur.append(1)
                    elif distance(mouse.position, (-0.266204, -0.171296, 0)) < 0.03:
                        Audio("valve.mp3")
                        self.code_joueur.append(2)
                    elif distance(mouse.position, (-0.445602, -0.167824, 0)) < 0.03:
                        Audio("valve.mp3")
                        self.code_joueur.append(3)
                    elif distance(mouse.position, (-0.444444, 0.186343, 0)) < 0.01:
                        Audio("valve.mp3")
                        self.code_joueur.append(4)
                    elif distance(mouse.position, (-0.128472, 0.186343, 0)) < 0.02:
                        Audio("valve.mp3")
                        self.code_joueur.append(5)
                    elif distance(mouse.position, (0.211806, 0.300926, 0)) < 0.03:
                        Audio("valve.mp3")
                        self.code_joueur.append(6)
                    elif distance(mouse.position, (0.461806, -0.105324, 0)) < 0.02:
                        Audio("valve.mp3")
                        self.code_joueur.append(7)
                    elif distance(mouse.position, (0.763889, 0.28588, 0)) < 0.03:
                        Audio("valve.mp3")
                        self.code_joueur.append(8)
                    self.verif_eau()  # Vérifie le code du joueur
                # La touche [e] est ici pour faire quitter le joueur
                elif key=="e":
                    self.player.enabled = True
                    self.traitement_eau.epreuve = False
                    self.code_joueur = []
                    destroy(self.eau_epreuve_image)
        # Touche [e] pour les interactions
        elif key == "e":
            # Le manuel expliquant l'épreuve des tuyaux, on regarde s'il est à côté
            if self.player.intersects(self.plaque_manuel_tuyaux).hit:
                if not self.papier:
                    Audio("paper.mp3")
                    self.player.enabled = False
                    self.papier = Entity(model = "quad", scale=(0.4, 0.6), parent=camera.ui, origini=(0,0), texture= "water_manuel")
                else:
                    Audio("paper.mp3")
                    self.player.enabled = True
                    destroy(self.papier)
            # L'autre manuel expliquant le processus de la centrale électrique : comment s'en sortir
            elif self.player.intersects(self.plaque_manuel).hit:
                if not self.papier:
                    Audio("paper.mp3")
                    self.player.enabled = False
                    self.papier = Entity(model = "quad", scale=(0.4, 0.6), parent=camera.ui, origini=(0,0), texture= "guide")
                else:
                    Audio("paper.mp3")
                    self.player.enabled = True
                    destroy(self.papier)
            # Regarde si le joueur est à côté de l'épreuve des valves et qu'il n'est pas déjà en train de les faire (sinon cela pourrait cause des problèmes)
            elif self.player.intersects(self.plaque_eau).hit and not self.eau_epreuve_image and not self.traitement_eau.epreuve and not self.traitement_eau.epreuve_finie:
                self.player.enabled = False
                print_on_screen("Press e to quit.",scale=1, position=(-0.15,-0.4), duration=3)
                self.eau_epreuve_image = Entity(model="quad", parent=camera.ui, texture="epreuve_eau", scale=(1.8, 1))
                self.traitement_eau.epreuve = True
            # De même pour l'épreuve de la salle de commande
            elif self.player.intersects(self.plaque_commande).hit and not self.central_commande.epreuve_finie and self.traitement_eau.epreuve_finie and self.atelier.fini:
                self.debut_epreuve_commande()  # Lance le début de l'épreuve de la salle de commande
            # Regarde si le joueur est à côté du blueprint et qu'il est en condition de le prendre (qu'il a déjà placé les trois batteries dans les générateurs)
            elif self.player.intersects(self.plaque_blueprint).hit and self.gen.trois_batteries and self.blueprint.visible:
                self.blueprint.visible = False
                self.grab.play()
                # Boucle qui place l'objet dès la première place vide dans l'inventaire
                for i in self.inventaire:
                    if i == None:
                        self.inventaire[self.inventaire.index(i)] = "blueprint.obj"
                        break
                # Conditions qui change la texture du premier slot vide de l'inventaire 
                if str(slot1.image.texture) == "slot_normal_vide.png":
                    item.scale = 1  # Change la taille de l'objet pour mieux la voir
                    slot1.texture = "blueprint"
                    slot1.image.texture = "blueprint"
                else:
                    item.scale = 1
                    slot2.texture="blueprint"
                    slot2.image.texture = "blueprint"
            # De même pour la boîte
            elif distance(self.boite, self.player) < 2 and self.gen.trois_batteries and self.boite.visible:
                self.boite.visible= False
                self.grab.play()
                # Boucle qui place l'objet dès la première place vide dans l'inventaire
                for i in self.inventaire:
                    if i == None:
                        self.inventaire[self.inventaire.index(i)] = "metal.obj"
                        break
                # Conditions qui change la texture du premier slot vide de l'inventaire
                if str(slot1.image.texture) == "slot_normal_vide.png":
                    slot1.texture = "metal"
                    slot1.image.texture = "metal"
                else:
                    slot2.image.texture = "metal"
                    slot2.texture="metal"
            # Regarde si le joueur est à côté de l'atelier et qu'il a prit les objets nécessaires à la fabrication du dernier batterie
            elif self.player.intersects(self.plaque_atelier).hit and not self.boite.visible and not self.blueprint.visible and not self.atelier.fini:
                destruction()
                Audio("construction.mp3")
                item.scale=0.25
                self.inventaire[0] = "batterie"
                # Change les textures (met la batterie et enlève les autres inutiles)
                slot1.image.texture = "icone_batterie"
                slot1.texture = "icone_batterie"
                slot2.texture = "slot_normal_vide"
                slot2.image.texture = "slot_normal_vide"
                self.inventaire[1] = None
                self.atelier.fini = True  # MArque la fin de fabrication du joueur : il ne peut plus ré-intéragir avec
            else:
                # Sinon, cela revient à dire qu'on change l'état des portes auquel le joueur a intéragit avec
                for i in self.liste_plaque:
                    for j in self.liste_porte:
                        # Si le joueur intercepte une plaque qui est associée à sa porte (par l'index)
                        if self.player.intersects(i).hit and self.liste_plaque.index(i) == self.liste_porte.index(j):
                            # Les portes parallèles à l'axe z ont des actions différentes à ceux parallèles sur l'axe x
                            if self.liste_porte.index(j) == 0 or self.liste_porte.index(j) == 3 or self.liste_porte.index(j) == 4 or self.liste_porte.index(j) == 8 or self.liste_porte.index(j) == 9:
                                # S'ils ne sont aps déjà ouverts, alors on les ouvre
                                if j.z != 2:
                                    j.z += 2
                                    Audio("metal_door.mp3")
                                    break
                            # Sinon, on change l'état de la porte qui se situe parallèlement à l'axe x
                            else:
                                if j.x != 2:
                                    j.x += 2
                                    Audio("metal_door.mp3")
                                    break

    def update(self) -> None:
        if self.active:
            self.move_monster_along_pathway()  # Débute le parcours du monstre

            # Bruits des pas du joueur
            if held_keys["a"] or held_keys["w"] or held_keys["s"] or held_keys["d"]:
                if not self.footstep.playing:
                    self.footstep.play()
            else:
                self.footstep.stop()

            # Regarde si le joueur est proche du générateur et qu'il a les batteries dans osn inventaire
            if distance(self.player, self.gen) < 2 and str(slot1.image.texture) == "icone_batterie.png" and not self.gen.trois_batteries:
                Audio("bip.mp3")
                slot1.texture = "slot_normal_vide"
                slot2.texture = "slot_normal_vide"
                slot3.texture = "slot_normal_vide"
                slot1.image.texture = "slot_normal_vide"
                slot2.image.texture = "slot_normal_vide"
                slot3.image.texture = "slot_normal_vide"
                # On enlève les objets depuis l'inventaire du joueur
                for i in range(len(self.inventaire)):
                    self.inventaire[i] = None
                self.gen.trois_batteries = True  # On change la variable pour dire que le générateur a bien reçu les 3 batteries
                print_on_screen("One battery missing, I need to build the fourth battery", duration=3, position=(-0.35,-0.4), scale=1.5)

            # Regarde si le monstre est trop proche du joueur
            if abs(self.monstre.x - self.player.x) < 2 and abs(self.monstre.z - self.player.z) < 2:
                self.mort_central()  # On invoque la fonction pour la mort du joueur
            # On regarde si le joueur a fini l'épreuve finale et qu'il est revenu au spawn, comme ça on charge la map suivante
            elif distance(self.player, (0,0,0)) < 2 and self.central_commande.epreuve_finie:
                destruction()
                self.map_charge = False
                self.ambient.color = color.rgb(40, 40, 40)
                self.footstep.stop()
                scene.clear()
                self.active = False
                map6.initialisation()
                map6.enabled = True
            # regarde si le joueur a le dernier batterie pour les générateurs et le place s'il est à côté
            elif distance(self.player, self.gen) < 2 and str(slot1.image.texture) == "icone_batterie.png" and self.gen.trois_batteries and not self.gen.fini:
                Audio("bip.mp3")
                slot1.texture = "slot_normal_vide"
                slot1.image.texture = "slot_normal_vide"
                destruction()
                self.inventaire[0] = None
                print_on_screen("the generators are ok", duration=3, position=(-0.15,-0.4), scale=1.5)
            # Regarde si le joueur est proche du manuel des tuyaux
            elif self.player.intersects(self.plaque_manuel_tuyaux).hit:
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # Regarde si le joueur est à côté du blueprint
            elif distance(self.player, self.blueprint) < 1 and self.blueprint.visible and self.gen.trois_batteries:
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # Regarde s'il est à côté du manuel de la salle des commandes
            elif self.player.intersects(self.plaque_manuel).hit:
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # Regarde si le joueur est proche de l'épreuve des tuyaux et qu'il n'est pas en train de faire l'épreuve ni qu'il l'a déjà fini
            elif self.player.intersects(self.plaque_eau).hit and not self.traitement_eau.epreuve and not self.traitement_eau.epreuve_finie:
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # Donne au joueur les trois batteries s'il est à côté de la salle des batteries
            elif self.player.intersects(self.plaque_batterie).hit and not self.gen.trois_batteries and str(slot1.image.texture) != "icone_batterie.png":
                if not self.grab.playing:
                    self.grab.play()
                print_on_screen("I need to put them in the generators.", duration=3, position=(-0.2,-0.4), scale=1.5)
                # Palce pour chaque emplacement de l'inventaire la batterie comme objet
                for i in range(len(self.inventaire)):
                    self.inventaire[i] = "batterie"
                slot1.image.texture = "icone_batterie"
                slot2.image.texture = "icone_batterie"
                slot3.image.texture = "icone_batterie"
                slot1.texture = "icone_batterie"
                slot2.texture = "icone_batterie"
                slot3.texture = "icone_batterie"
            # Regarde si le joueur est proche de l'épreuve de la salle des commande et qu'il a fini tous mes pré-requis (épreuve eau et les batteries) ainsi qu'il n'est pas déjà en trian de faire cette épreuve ni ne l'a déjà fini
            elif self.player.intersects(self.plaque_commande).hit and self.traitement_eau.epreuve_finie and not self.central_commande.epreuve_finie and not self.central_commande.epreuve and self.atelier.fini:
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha= 0.5, scale = (0.5,0.25))
            # Regarde s'ile st proche de la boîte
            elif distance(self.boite, self.player) < 2 and self.gen.trois_batteries and self.boite.visible:
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha= 0.5, scale = (0.5,0.25))
            # Regarde si le joueur est proche de l'atelier
            elif self.player.intersects(self.plaque_atelier).hit and not self.boite.visible and not self.blueprint.visible and not self.atelier.fini:
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha= 0.5, scale = (0.5,0.25))
            # Sinon on regarde s'il est proche d'une porte
            else:
                for element in self.liste_plaque:
                    # On regarde si les portes ne sont pas ouverts afin d'afficher la lettre [e]
                    if self.player.intersects(element). hit and self.dico_plaque_porte[element].z != 2 and self.dico_plaque_porte[element].x != 2:
                        if not self.e_lettre:
                            self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
                        break
                    else:
                        if self.e_lettre:
                            destroy(self.e_lettre)
                        # On remet à l'emplacement normal des portes : on les referme si le joueur n'intéragit avec aucune porte
                        for i in self.liste_porte:
                            if i.x == 2 or i.z == 2:
                                invoke(lambda : self.retour_porte(i), delay=2)
                                break


map5 = Map5()