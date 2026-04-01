"""
Ce code contient la classe de la troisème map, contenant ses attributs (eléments de la map) et ses méthodes
"""
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from codes.class_slot import *
from codes.commun import *
from codes.map4_code import *

class Map3(Entity):
    """Classe pour la troisième map du jeu

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
        active: bool
            regarde si la map est toujours active (si on doit charger la map suivante ou non)
        ecran : entité et/ou bool
            Permet d'afficher quelconque ecran devant le joueur
        papier : entité et/ou bool
            Permet d'afficher quelconque feuille devant le joueur
        affichage_ordi: str
            Permet d'afficher le prompt entré par le joueur
        inventaire: list
            Contient l'inventaire du joueur
        logiciel: entité/bool
            Regarde si le joueur est dans le logiciel prompt ou non
        point: entité/bool
            Le bouton "point" de l'ordinateur
        msg_code: entité (Text) et/ou bool
            Contient le code entré par le joueur
        code_joueur: list
            Le code entré par le joueur
    
    Méthodes:
    ----------

    Publiques:

        initialisation: charge les éléments de la map
        ecriture_code: vérifie le cod einformatique entré par le joueur dans l'ordinateur
        accès_terminal: permet d'accéder au terminal de prompt
        verif_ordi: vérifie le code entré par le joueur pour démarrer l'ordinateur
        input: déclenche des actions en fonction des touches appuyées du joueur
        update: actualise chaque evenement de la map

    """


    def __init__(self):
        super().__init__()

        self.enabled = False
        self.e_lettre = None
        self.pause = False
        self.menu = None
        self.active = False
        self.ecran = None
        self.papier = None
        self.affichage_ordi = ""
        self.inventaire = [None, None, None]
        self.logiciel = None
        self.point = None
        self.msg_code = None
        self.code_joueur = []
    
    def initialisation(self) -> None:
        self.active = True  # active cette map

        Sky()

        self.ambient = AmbientLight(color=color.rgb(60, 60, 60))
        self.flashlight = DirectionalLight(parent = camera, rotation=(40,40,40),color=color.black)

        self.player = FirstPersonController(scale=2.5, collider="box", position=(32.1098, 0, 45.6853), rotation_y = 180, speed=10)
        self.player.cursor.color = color.white

        Entity(model="murs_map3.obj", collider="mesh", double_sided = True, scale=2.5, texture="murs_map3.mtl")

        self.pil= Entity(model="pillier.obj", collider="box", scale=2.5, texture="pillier.mtl")
        duplicate(self.pil, x=self.pil.x-15)
        duplicate(self.pil, x=self.pil.x-30)

        self.table = Entity(model="table_cant", position=(-15, 0, 70), collider="box")
        duplicate(self.table, x=self.table.x - 15)
        duplicate(self.table, x=self.table.x-30)
        duplicate(self.table, z=self.table.z + 25)
        duplicate(self.table, z=self.table.z + 25, x=self.table.x-15)
        duplicate(self.table, z=self.table.z + 25, x=self.table.x-30)


        Entity(model="biblio1.obj", scale=2.5, collider="box", texture="biblio1.mtl")
        Entity(model="biblio2.obj", scale=2.5, collider="box", texture="biblio2.mtl")
        Entity(model="biblio3.obj", scale=2.5, collider="box", texture="biblio3.mtl")
        Entity(model="biblio4.obj", scale=2.5, collider="box", texture="biblio4.mtl")
        Entity(model="biblio5.obj", scale=2.5, collider="box", texture="biblio5.mtl")
        Entity(model="biblio6.obj", scale=2.5, collider="box", texture="biblio6.mtl")
        Entity(model="biblio7.obj", scale=2.5, collider="box", texture="biblio7.mtl")
        Entity(model="biblio8.obj", scale=2.5, collider="box", texture="biblio8.mtl")
        Entity(model="biblio9.obj", scale=2.5, collider="box", texture="biblio9.mtl")

        Entity(model="ordi.obj", scale = 2.5, collider="mesh", texture="ordi.mtl")
        Entity(model="chaise", collider="box", scale=2.5)
        Entity(model="shelves.obj",scale=2.5,texture="shelves.mtl",collider="mesh")
        Entity(model="carton.obj", texture="carton.mtl", scale=2.5, double_sided = True)

        self.porte1 = Entity(model="porte_biblio1", texture="porte_biblio1.mtl", scale=2.5, collider="box")
        self.porte2 = Entity(model="porte_biblio2", texture="porte_biblio2.mtl", scale=2.5, collider="box")

        # Les plaques servent à détecter la présence du joueur à côté des bibliothèques, portes et l'ordinateur
        self.plaque = Entity(model="plane", collider="box", scale=(4,0.1,6), position=(48,0.1,-31), visible=False)
        self.plaque2 = Entity(model="plane", collider="box", scale=(17,1,8), position=(18,0,-12), visible=False)
        self.plaque3 = Entity(model="plane", collider="box", scale=(12,1,8), position=(-22,0,-45), visible=False)
        self.plaque4 = Entity(model="plane", collider="box", scale=(30,1,8), position=(-21.4032,0,-94.7952), visible=False)
        self.plaque5 = Entity(model="plane", collider="box", scale=(6,1,25), position=(9.7,0,34), visible=False)
        self.plaque6 = Entity(model="plane", collider="box", scale=(6,1,25), position=(-2,0,35), visible=False)
        self.plaque7 = Entity(model="plane", collider="box", scale=(23,1,4), position=(-17,0,3), visible=False)
        self.plaque8 = Entity(model="plane", collider="box", scale=(18,1,25), position=(-39,0,-35), visible=False)
        self.plaque9 = Entity(model="plane", collider="box", scale=(4,1,20), position=(-14,0,-35), visible=False)
        self.plaque10 = Entity(model="plane", collider="box", scale=(20,1,4), position=(19,0,-30), visible=False)
        self.plaque11 = Entity(model="plane", collider="box", scale=(20,1,4), position=(20,0,-42), visible=False)
        self.plaque12 = Entity(model="plane", collider="box", scale=(4,1,30), position=(41,0,9), visible=False)

        self.cle = Entity(model="keys", scale=0.4, collider="box", color=color.dark_gray, position=(-43,0.2,26), visible = True)

        self.jackson = Entity(model="quad", texture="monstre_biblio_screamer", position=(57,5,-31), scale=6, double_sided = True, rotation_y = -90)

        self.livre = Entity(model="livre", position=(63,-3,-15), scale=1.5, colldier="box", rotation_y = -90)
        Entity(model="cube", position=(-21.5048, 0, -115.334), color=color.white*100, scale=(30,100,2), collider="box")

        self.footstep = Audio("footsteps.mp3", autoplay = False)
        self.son_sortie = Audio("finaly_heaven.mp3", autoplay = False)
        Audio("porte_audio.mp3")
        
        slot1.affichage()
        slot2.affichage()
        slot3.affichage()
    
    def ecriture_code(self) -> None:
        """Méthode qui permet au joueur d'écrire le code point-tiret ainsi que de vérifier s'il a bon
        En fonction du bouton appuyé, l'écran affiche soit un point soit un tiret puis vérifie
        """
        Audio("keyboard.mp3")
        if self.point.hovered:
            self.affichage_ordi += "."
        if self.tiret.hovered:
            self.affichage_ordi += "-"
        self.msg_code.text = self.affichage_ordi
        Audio("keyboard.mp3")
        # Active la vérification si le nombre de caractère est la même que la bonne réponse
        if len(self.affichage_ordi) == 19:
            # Si le joueur a bon, alors nous procédons à la fin de l'épreuve
            if self.affichage_ordi == "-.-..--.-.---...--.":
                Audio("bip.mp3")
                Audio("alarm.mp3")
                self.ambient.color = color.lime
                destroy(self.msg_code)
                destroy(self.ecran)
                destroy(self.point)
                self.player.enabled = True
                destroy(self.tiret)
                self.code_joueur = []
            #Sinon on remet le compte à zéro
            else:
                Audio("no.mp3")
                destroy(self.msg_code)
                destroy(self.ecran)
                destroy(self.point)
                self.player.enabled = True
                destroy(self.tiret)
                self.code_joueur = []
                self.affichage_ordi = ""


    def accès_terminal(self) -> None:
        """
        Méthode permettant de donner l'accès au joueur pour coder en affichant les boutons
        """
        Audio("keyboard.mp3")
        destroy(self.logiciel)
        self.ecran.texture = "Terminal"
        self.point = Button(icon="bouton_point", position=(-0.095,-0.025),scale=0.1, on_click = self.ecriture_code)  # Lorsque le bouton est cliqué (on_click), il renvoie vers la méthode ecriture_code
        self.tiret = Button(icon="bouton_trait", position=(0.1,-0.025), scale=0.1, on_click = self.ecriture_code)  # De même


    def verif_ordi(self) -> None:
        """
        Méthode qui regarde si le mot de passe entré par le joueur est correct
        """
        if len(self.code_joueur) == 6:
            if self.code_joueur == [3,4,1,2,1,2]:
                Audio("start_computer.mp3")
                self.logiciel = Button(icon="bouton_acces", scale=0.1, position=(0,-0.13), on_click=self.accès_terminal)
                self.ecran.texture = "Acc"
                self.code_joueur = []
            else:
                Audio("no.mp3")
                self.code_joueur = []
                
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
        # Activation ou désactivation de la flashlight
        if key == "f":
            if self.flashlight.color == color.rgb(40, 40, 40):
                self.flashlight.color = color.black
                Audio("flashlight_clicking.mp3")
            else:
                self.flashlight.color = color.rgb(40, 40, 40)
                Audio("flashlight_clicking.mp3")
        # Regarde si le joueur souhaite appuyer sur un slot pour accéder à son inventaire
        if key in ['1', '2', '3'] and not self.ecran:
            dico_chiffre = {'1' : slot1, "2" : slot2, "3" : slot3}
            slot_appuye(dico_chiffre[key], self.player, self.inventaire)
        # Si le joueur est devant un écran
        if self.ecran:
            if self.e_lettre:
                destroy(self.e_lettre)
            # La touche [e] est utilisée ici pour quitter l'ordinateur, on supprime donc toute l'interface et on remet tout à zéro
            if key =="e":
                self.code_joueur = []
                self.affichage_ordi = ""
                if self.ecran:
                    destroy(self.ecran)
                if self.logiciel:
                    destroy(self.logiciel)
                if self.point:
                    destroy(self.point)
                    destroy(self.tiret)
                if self.msg_code:
                    destroy(self.msg_code)
                self.player.enabled = True
            # L'entré du code du joueur
            elif key in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                self.code_joueur.append(int(key))
                Audio("keyboard.mp3")
                self.verif_ordi()  # vérifie le code du joueur
        # Si le joueur se déplace, on met les bruits de pas
        elif held_keys["a"] or held_keys["w"] or held_keys["s"] or held_keys["d"]:
            if not self.footstep.playing:
                self.footstep.play()
        # Si le joueur n'est pas devant l'écran et qu'il intéragit avec des objets
        elif key == "e":
            # Si le joueur veut intéragir avec la porte de la salle de stockage et qu'elle n'est pas déjà ouverte
            if self.player.intersects(self.plaque).hit and self.porte2.rotation_y != -90:
                if "keys" in self.inventaire:
                    self.inventaire[0] = None
                    self.porte2.rotation_y -=90
                    self.porte2.z -= 78
                    self.porte2.x += 22
                    destruction()
                    slot1.texture = "slot_normal_vide"
                    slot1.image.texture = "slot_normal_vide"
                    Audio("porte_audio.mp3")
                    destroy(self.player)
                    self.player = FirstPersonController(scale=2.5, collider="box", position=(46.1884,0,-31.1671), rotation_y = 90, enabled=False)  # On recrée le joueur pour le mettre en place correctement pour le jumpscare
                    self.player.cursor.color = color.white
                    Audio("jackson.mp3", volume=10)
                else:
                    print_on_screen("I need to find a key", position=(-0.15,-0.4), scale=1.5, duration=2.5)
            # Si le joueur est devantla porte de sortie pas déjà ouverte
            elif self.player.intersects(self.plaque3).hit and self.porte1.rotation_y != -90:
                # Regarde si le joueur a réussit l'épreuve de l'ordinateur, le joueur peut l'ouvrir
                if self.affichage_ordi == "-.-..--.-.---...--.":
                    Audio("slam.mp3")
                    self.porte1.rotation_y -= 90
                    self.porte1.x -= 68.5
                    self.porte1.z -= 31.5
                    self.son_sortie.play()
                else:
                    print_on_screen("The door is locked", position=(-0.15,-0.4), scale=1.5, duration=2.5)
            # Si le joueur est devant l'odinateur
            elif self.player.intersects(self.plaque2).hit:
                # Imbolise le joueur et affiche l'écran
                destroy(self.player)
                print_on_screen("Press e to quit and press numbers on keyboard.",scale=1, position=(-0.15,-0.4), duration=3)
                self.player = FirstPersonController(scale=2.5, collider="box", position=(16,0,-11.8012), rotation_y=180, enabled = False,  speed=10)
                self.player.cursor.color = color.white
                Audio("bip.mp3")
                self.ecran = Entity(model = "quad", scale=(1,0.7), parent=camera.ui, origin = (0,0), texture="Mdp")
                self.msg_code = Text(text = self.affichage_ordi, scale=1.5, position=(-0.25,0.28), color=color.green)
            # Si le joueur prend la clé
            elif distance(self.player, self.cle) < 4 and self.cle.visible:  # Regarde si la clé n'est pas déjà prise par le joueur
                self.cle.visible = False
                print_on_screen("Where can I use this ?", duration=3, position=(-0.15,-0.4), scale=1.5)
                Audio("rattling-keys.mp3")
                self.inventaire[0] = "keys"
                slot1.texture = "icone_clé"
                slot1.image.texture = "icone_clé"
            # Si le joueur ouvre le manuel du code point-tiret ou la ferme
            elif self.player.intersects(self.plaque5).hit:
                if not self.papier:
                    Audio("paper.mp3")
                    self.player.enabled = False
                    self.papier = Entity(model = "quad", scale=(0.4, 0.6), parent=camera.ui, origini=(0,0), texture= "manuel_code")
                else:
                    Audio("paper.mp3")
                    self.player.enabled = True
                    destroy(self.papier)
        # Si le joueur est immobile, on coupe les bruits de pas
        else:
            self.footstep.stop()

    def update(self) -> None:
        if self.active:
            # On regarde si le joueur a ouvert la porte et que le screamer est créé
            if self.porte2.rotation_y == -90 and self.jackson:
                if abs(self.jackson.x - 40) > 0.1:
                    self.jackson.x -= time.dt * 10  # On le fait avancer vers le joueur
                # Si le screamer est fini (qu'il a atteint la position requise), alors on le supprime et le joueur peut bouger de nouveau
                else:
                    self.player.enabled = True
                    destroy(self.jackson)

            # Les conditions suivantes affichent la lettre [e] si le joueur est proche d'un objet qu'il peut intéragir avec
            # la deuxième porte de la map
            if self.player.intersects(self.plaque).hit and self.porte2.rotation_y != -90:
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # La première porte de la map
            elif self.player.intersects(self.plaque3).hit and self.porte1.rotation_y != -90:
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # L'ordinateur
            elif self.player.intersects(self.plaque2).hit:
                if not self.e_lettre and not self.ecran and self.affichage_ordi != "-.-..--.-.---...--.":
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # La clé
            elif distance(self.player, self.cle) < 4 and self.cle.visible:
                self.cle.color = color.white*100
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # Le livre, on affiche pas la lettre mais on affiche le message à l'écran
            elif abs(self.player.x - self.livre.x) < 10 and abs(self.livre.z - self.player.z) < 10:
                print_on_screen("341212", duration=0.25, position=(0,-0.4), scale=1)
            # Change de map si le joueur atteint la suite
            elif self.player.intersects(self.plaque4).hit:
                self.ambient.color = color.rgb(60, 60, 60)
                self.son_sortie.stop()
                self.footstep.stop()
                scene.clear()
                self.active = False
                map4.initialisation()
                map4.enabled = True
            # Le manuel
            elif self.player.intersects(self.plaque5).hit:
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # Les différentes bibliothèques
            elif self.player.intersects(self.plaque6).hit:
                print_on_screen("'Do no reach the light' (...)", duration=0.25, position=(-0.15,-0.4), scale=1.5)
            elif self.player.intersects(self.plaque7).hit:
                print_on_screen("'Dark is the night: Temnaya noch' (Mark Bernes)", duration=0.25, position=(-0.3,-0.4), scale=1.5)
            elif self.player.intersects(self.plaque8).hit:
                print_on_screen("'Heartaches' (Al Bowlly, 1931)", duration=0.25, position=(-0.15,-0.4), scale=1.5)
            elif self.player.intersects(self.plaque9).hit:
                print_on_screen("'You' (1)", duration=0.25, position=(-0.15,-0.4), scale=1.5)
            elif self.player.intersects(self.plaque10).hit:
                print_on_screen("'Are' (2)", duration=0.25, position=(-0.15,-0.4), scale=1.5)
            elif self.player.intersects(self.plaque11).hit:
                print_on_screen("'Dead' (3)", duration=0.25, position=(-0.15,-0.4), scale=1.5)
            elif self.player.intersects(self.plaque12).hit:
                print_on_screen("'Dream Sweet in Sea Major' (Miracle Musical, 2012)", duration=0.25, position=(-0.3,-0.4), scale=1.5)
            else:
                self.cle.color = color.dark_gray
                (self.livre).color  = color.white
                if self.e_lettre != None:
                    destroy(self.e_lettre)


map3 = Map3()