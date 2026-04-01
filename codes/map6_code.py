"""
Ce code contient la classe de la sixième map, contenant ses attributs (eléments de la map) et ses méthodes
"""
from ursina import *
import math
from ursina.prefabs.first_person_controller import FirstPersonController
from codes.class_slot import *
from codes.commun import *

class Map6(Entity):
    """Classe pour la cinquième map du jeu

    Attributs:
    ---------------

    Publics:

        fin: bool
            Vérifie si le joueur a atteint la fin
        inventaire: list
            contient l'inventaire du joueur
        enabled: bool
            Permet d'afficher la map ou non
        active: bool
            regarde si la map est toujours active (si on doit charger la map suivante ou non)
        e_lettre : entité et/ou bool
            Permet d'afficher la lettre [e] auprès des objets qui peuvent être en interaction avec le joueur afin d'indiquer leur présence
        menu: entité et/ou bool
            Permet d'afficher le menu de pause pour le joueur
        pause : bool
            Permet de savoir si le joueur a mis en pause ou non
        lecture : bool
            Permet de savoir si le joueur est en train ou non d'écouter une entité parler (ou lui-même)
    
    Méthodes:
    ----------

    Publiques:

        initialisation: charge les éléments de la map
        arret_lecture: permet d'arreter l'écoute du joueur au monstre
        quitter: Fait quitter le joueur après la fin
        fin_jeu: Met la vidéo et l'audio de l'outro
        donne_cle: Méthode qui donne la clé au joueur après la parole du monstre
        monstre_fin_parole: Méthode traduisant les paroles du monstre en ajoutant la musique, la voix et les sous-titres
        arrive_salon: S'active lorsque le joueur arrive dans le salon : début de l'évènement
        mort_maison: S'active lorsque le joueur meurt dans la maison : audio, message et respawn
        dot_product: Méthode qui définiel e produit scalaire des calculs vectoriels
        son_cassette: Joue le son de l'audio cassette
        input: déclenche des actions en fonction des touches appuyées du joueur
        update: actualise chaque evenement de la map

    """


    def __init__(self):
        super().__init__()

        self.fin = False
        self.inventaire = [None, None, None]
        self.enabled = False
        self.active = False
        self.e_lettre = None
        self.menu = None
        self.pause = False
        self.lecture =False

    def initialisation(self) -> None:
        app = Ursina()

        self.active = True

        self.flashlight = DirectionalLight(parent = camera, rotation=(45,-45,45),color=color.black)
        self.ambient = AmbientLight(color=color.rgb(40, 40, 40))

        self.player = FirstPersonController(collider="box", rotation_y = 180, z=8)
        self.player.cursor.color = color.white

        Entity(model="maison_murs.obj",color = color.rgb(65, 97, 27),collider="mesh", scale=2)
        Entity(model="maison_sol.obj", texture ="plancher.jpg",color = color.rgb(204,102,0), collider="mesh",scale=2)
        Entity(model="maison_plafond.obj", texture="", color = "",collider = "mesh", scale = 2)
        Entity(model="escalier.obj", texture="escalier.mtl", collider="box", scale=2, double_sided = True)
        Entity(model="poubelles", texture="poubelles.mtl", scale=2, double_sided = True)
        Entity(model="plane", color=color.white*200, scale=5.5, position=(9.76824,4.5,-0.236166), double_sided=True)
        self.porte = Entity(model="porte_maison", texture="porte_maison.mtl", scale=2, collider="box")
        Entity(model="fauteuil_salon1", texture="fauteuil_salon1.mtl", collider="box", scale=2, double_sided = True)
        Entity(model="fauteuil_salon2", texture="fauteuil_salon2.mtl", collider="box", scale=2, double_sided = True)
        Entity(model="commode_salon", texture="commode_salon.mtl", collider="box", scale=2)
        Entity(model="table_salon", texture="table_salon.mtl", collider="mesh", scale=2)
        Entity(model="salon_biblio", texture="salon_biblio.mtl", collider="box", scale=2)
        Entity(model="placard", texture="placard.mtl", collider="box", scale=2)
        Entity(model="lit", texture="lit.mtl", collider="box", scale=2, double_sided = True)
        Entity(model="commode", texture="commode.mtl", collider="box", scale=2)
        Entity(model="table_lit", texture="table_lit.mtl", scale=2, collider="box")
        Entity(model="cuisine_comptoir", texture="cuisine_comptoir", collider="mesh", scale=2)
        Entity(model="table_manger", texture="table_manger.mtl", collider="box", scale=2)
        Entity(model="cuisine", texture="cuisine.mtl", scale=2,collider="mesh", double_sided=True)
        self.refrigerateur = Entity(model="porte_refrigerateur", texture="porte_refrigerateur.mtl", scale=2, collider="box")
        self.barricades = Entity(model="barricades", texture="barricades.mtl", scale=2)
        self.porte_chambre = duplicate(self.porte, x=5, z=-9)
        self.porte_fin = duplicate(self.porte, x=-6, rotation_y = 90)
        self.porte_salon = duplicate(self.porte, x=-12, z=-5.1, rotation_y = 90)
        Entity(model="painting", color=color.rgb(47, 27, 97), position=(-2.8,2,4.5), rotation_y = 90)
        Entity(model="radio", color=color.rgb(97, 79, 27), position=(2.44758,1,-9.13458), rotation_y = 180)
        Entity(model="painting", color=color.rgb(47, 27, 97), position=(-0.2,2,-7.5), rotation_y=-90)
        self.monstre = Entity(model="angel.obj", texture="angel.jpg", position=(4,2,0), scale=4, visible=True)
        self.cle = Entity(model="keys", position=(-4.96472,0.1,11.2672), scale=0.1, collider="box", color=color.dark_gray, visible = True)
        self.hammer = Entity(model="marteau.obj", texture="marteau.jpg", collider="box", position=(3.48807,1,11.0499), scale=1, rotation_y = 90, visible=True)

        self.plaque = Entity(model="plane", scale=2, position=(-5,0.1,10), collider="box", visible=False)
        self.plaque1 = duplicate(self.plaque, position=(5.13423,0.1,1.87719))
        self.plaque2 = duplicate(self.plaque, position=(-0.831006,0.1,-4.96066))
        self.plaque3 = duplicate(self.plaque, position=(5.44056,0.1,-0.117339))

        self.statue = Audio("statue.mp3", autoplay=False, volume=20)
        self.footstep= Audio("footstep_wood.mp3", autoplay=False, volume=10)

        slot1.affichage()
        slot2.affichage()
        slot3.affichage()

        print_on_screen("Is this my house ? What is that thing ?", duration=3, position=(-0.35,-0.4), scale=1.5)
    
    def arret_lecture(self, aut) -> None:
        """Méthode qui donne l'autorisation au joueur de quitter ou non

        :param aut: valeur booléenne qui permet de savoir si le joueur est en train d'écouter ou non une entité parler 

        S'il est en train d'écouter, alors le joueur ne peut pas quitter, sinon il peut

        Exemple:
            Si lecture=True, alors les actions du joueur sont limités (ne peut pas ouvrir le menu)
            Sinon, cela revient à dire que l'entité ou lui-même a fini de parler, et donc qu'il peut ouvrir le menu à son gré
        """
        self.lecture = aut

    def quitter(self) -> None:
        quit()

    def fin_jeu(self, s) -> None:
        """
        Met la vidéo et l'audio de l'outro

        :param s: l'écran noir qui est devant le joueur

        """
        destroy(s)
        video = Entity(model="quad", texture="outro.mp4", parent=camera.ui, scale = (camera.aspect_ratio, 1))
        son_outro = Audio("outro_son.mp3", volume=20)
        invoke(self.quitter, delay=187)


    def donne_cle(self) -> None:
        Audio("grab.mp3")
        slot1.texture = "icone_clé"
        slot1.image.texture = "icone_clé"
        self.player.enabled = True
        destroy(self.monstre_fin)


    def monstre_fin_parole(self) -> None:
        """
        Méthode traduisant les paroles du monstre en ajoutant la musique, la voix et les sous-titres
        """
        Audio("ending_voice.mp3", volume=30)
        Audio("Eternal_End.mp3")
        invoke(lambda : parole("Finally home.", None, 1, 0, color.red, -0.1, True, self), delay=1)
        invoke(lambda : parole("No one cares about the flowers until they are withered to death.", None, 5, 0, color.red, -0.3, True, self), delay=2)
        invoke(lambda : parole("Was it all worth it? Was it all done?", None, 5, 0, color.red, -0.2, True, self), delay=8)
        invoke(lambda : parole("Have you finally made it, did you find your 'friends' ?", None, 5, 0, color.red, -0.3, True, self), delay=13)
        invoke(lambda : parole("Come on, it was a fun game with you and me.", None, 5, 0, color.red, -0.3, True, self), delay=18)
        invoke(lambda : parole("Now you just want to leave.", None, 3, 0, color.red, -0.2, True, self), delay=23)
        invoke(lambda : parole("Nostalgia can be a dangerous weapon, and you decided to use it.", None, 6, 0, color.red, -0.35, True, self), delay=26)
        invoke(lambda : parole("But why forcing them, obliging them to follow your act ?", None, 6, 0, color.red, -0.3, True, self), delay=32)
        invoke(lambda : parole("They cried", None, 1, 0, color.red, 0, True, self), delay=38)
        invoke(lambda : parole("they suffered", None, 1, 0, color.red, 0, True, self), delay=39)
        invoke(lambda : parole("and they agonized", None, 2, 0, color.red, 0, True, self), delay=40)
        invoke(lambda : parole("I can fix you.", None, 2, 0, color.red, 0, True, self), delay=42)
        invoke(lambda : parole("Take this key, go upstairs and you'll finally find freedom and peace.", None, 7, 0, color.red, -0.3, True, self), delay=44)
        invoke(lambda : parole("Destiny and justice made their job.", None, 7, 0, color.red, -0.2, True,self), delay=51)
        invoke(self.donne_cle, delay=69)


    def arrive_salon(self) -> None:
        self.lecture = True
        Audio("entrance_fin.mp3")
        self.fin = True
        scene.fog_density = 0.05  # Ajoute l'effet brouillard dans l'environnement
        self.ambient.color = color.red
        self.monstre_fin = Entity(model="sphere", position=(6.23611,2,-7.38375), texture="fog_texture.png", scale=3, rotation_y=90)
        invoke(self.monstre_fin_parole, delay=4)  # Débute les paroles du monstre


    def mort_maison(self) -> None:
        """
        S'active lorsque le joueur meurt dans la maison : audio, message et respawn
        """
        self.screen = Entity(model="quad", parent=camera.ui, color=color.black, scale=(1.8, 1))
        Audio("james.mp3", volume=80)
        message_mort()
        self.player.position = (0,0,8)
        self.monstre.position = (4,2,0)
        destroy(self.screen, 5)


    def dot_product(self, vec1, vec2) -> None:
        """Méthode qui définiel e produit scalaire des calculs vectoriels
        Elle est utilisée pour calculer l'angle entre la direction du joueur et celle du monstre. Cet angle est utilisé pour déterminer si le monstre doit poursuivre le joueur ou non. 
        Si le joueur est dans le champ de vision du monstre, le monstre poursuit le joueuer sinon, il change de direction ou s'arrête.

        :param vec1: premier vecteur
        :param vec2: deuxieme vecteur

        La boucle zip() permet de créer des paires d'élémentsentre les deux vecteurs ce qui permet de multiplier chaque paire ensemble et de calculer le produit scalaire
        a et b sont les éléments respectivfs des vecteurs vec1 et vec2.
        Ces deux parcourent chaque paire d'élement créés par la fonction zip()
        La fonction sum() additionne tous les produits pour obtenir le résultat du produit scalaire

        """
        return sum(a*b for a, b in zip(vec1, vec2))

    def son_cassette(self) -> None:
        Audio("tape-cassette.mp3")
    
    def input(self, key) -> None:
        # Pour le bruit des pas
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
        if key == 'escape' and not self.lecture and not self.menu:  # Si le joueur n'est pas dans une dialogue, que le jeu a débuté, que le meunu n'existe pas déjà, qu'il n'est pas dans une épreuve et pas devant un écran
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
        if key in ['1', '2', '3'] and not self.lecture:
            dico_chiffre = {'1' : slot1, "2" : slot2, "3" : slot3}
            slot_appuye(dico_chiffre[key], self.player, self.inventaire)
        if not self.fin:
            # Si le joueur intéragit avec les objets (la touche [e])
            if key == "e":
                # Interaction avec la porte de réfrigérateur
                if self.player.intersects(self.plaque).hit and self.refrigerateur.rotation_y != 90:
                    # On l'ouvre
                    Audio("son_ouverture.mp3")
                    self.refrigerateur.rotation_y = 90
                    self.refrigerateur.position = (-16.5,0,5)
                # Interaction avec la clé si la porte du réfrigérateur est ouvert et que la clé n'est pas déjà prise par le joueur
                elif distance(self.cle, self.player) < 2 and self.refrigerateur.rotation_y == 90 and self.cle.visible:
                    print_on_screen("My room's key.", duration=1, scale=1.5, position=(-0.15,-0.4))
                    self.cle.visible = False
                    slot1.texture = "icone_clé"
                    slot1.image.texture = "icone_clé"
                    self.inventaire[0] = "keys"
                    Audio("rattling-keys.mp3", volume=20)
                # Interaction avec la porte de la chambre, la plauqe permet de détecter la présence du joueur s'il est dessus
                elif self.player.intersects(self.plaque1).hit and self.porte_chambre.rotation_y != -90:
                    # Si la clé est prise par le joueur (cela se traduit si la clé n'est plus visible sur la map)
                    if not self.cle.visible:
                        destruction()
                        Audio("porte_audio.mp3")
                        self.porte_chambre.rotation_y = -90
                        self.porte_chambre.position=(16.3,0,4)
                        slot1.texture = "slot_normal_vide"
                        slot1.image.texture = "slot_normal_vide"
                        self.inventaire[0] = None
                    else:
                        print_on_screen("My room's locked", duration=2, position=(-0.35,-0.4), scale=1.5)
                # Interaction avec la porte du salon : si le marteau est pris par le joueur et que la porte n'est pas déjà ouverte
                elif self.player.intersects(self.plaque2).hit and not self.hammer.visible and self.porte_salon.rotation_y != 0:
                    destroy(self.barricades)
                    self.porte_salon.rotation_y = 0
                    self.porte_salon.position = (1,0,-16)
                    Audio("wood.mp3")
                    Audio("porte_audio.mp3")
                    destroy(self.player)
                    destroy(self.e_lettre)
                    self.player = FirstPersonController(collider="box", rotation_y = 90, position=(-0.9,0,-5), enabled=False)
                    invoke(self.arrive_salon, delay=2)  # On débute l'évènemetn qui se situe dans le salon
                # Interaction avec le marteau qui se situe dans la chambre : si la prote de la chambre est ouverte et que le marteau n'est pas pris par le joueur
                elif distance(self.hammer, self.player) < 2 and self.porte_chambre.rotation_y == -90 and self.hammer.visible:
                    self.hammer.visible = False
                    self.monstre.visible = False
                    Audio("grab.mp3")

    def update(self) -> None:
        if not self.fin:
            # Cela empèche le joueur de nocliper en dehors de la map, si oui on le respawn
            if self.player.y > 4.8:
                self.player.position=(0,0,0)
            
            # Regarde si le joueur est proche du monstre, si oui il meurt
            if self.monstre.visible and distance(self.monstre, self.player) < 3:
                self.mort_maison()

            # Condtion qui permet de bouger le monstre si le joueur ne le regarde pas 
            if (held_keys["a"] or held_keys["w"] or held_keys["s"] or held_keys["d"]) and self.monstre.visible:  # regarde si le monstre est présent et que le joueru bouge (les touches)

                direction_to_player = self.player.position - self.monstre.position
                direction_to_monster = self.monstre.position - self.player.position
                dot_prod_to_player = self.dot_product(self.player.forward, direction_to_player.normalized())
                dot_prod_to_monster = self.dot_product(self.player.forward, direction_to_monster.normalized())
                dot_prod_to_player = max(-1, min(1, dot_prod_to_player))
                dot_prod_to_monster = max(-1, min(1, dot_prod_to_monster))
                angle_to_player = math.degrees(math.acos(dot_prod_to_player))
                angle_to_monster = math.degrees(math.acos(dot_prod_to_monster))

                if angle_to_monster > angle_to_player:
                    ray = raycast(self.monstre.position + (0, 1, 0), self.monstre.forward, distance=1)
                    if ray.hit:
                        self.monstre.rotation_y = random.uniform(0, 360)
                    else:
                        if not self.statue.playing:
                            self.statue.play()
                        movement_vector = direction_to_player.normalized() * 7 * time.dt
                        self.monstre.x += movement_vector[0]
                        self.monstre.z += movement_vector[2]
                else:
                    self.statue.stop()

            # Les conditions suivantes affichent la lettre [e]
            # La porte du réfrigérateur
            if self.player.intersects(self.plaque).hit and self.refrigerateur.rotation_y != 90:
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # La clé
            elif self.cle.visible and distance(self.cle, self.player) < 2 and self.refrigerateur.rotation_y == 90:
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # La porte de la chambre
            elif self.player.intersects(self.plaque1).hit and not self.cle.visible and self.porte_chambre.rotation_y != -90:
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # le marteau
            elif distance(self.hammer, self.player) < 2 and self.porte_chambre.rotation_y == -90 and self.hammer.visible:
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            # la porte du salon
            elif self.player.intersects(self.plaque2).hit and not self.hammer.visible and self.porte_salon.rotation_y != 0:
                if not self.e_lettre:
                    self.e_lettre = Entity(model = "quad", texture = "E.png", parent=camera.ui, origin=(-0.2, 0), alpha = 0.5, scale = (0.5,0.25))
            else:
                destroy(self.e_lettre)
        else:
            # Empèche le joueur de noclip
            if self.player.y > 4.8:
                self.player.position=(0,0,0)

            # Si le joueur est à côté de la porte du fin, on finit le jeu
            if self.player.intersects(self.plaque3).hit and self.porte_fin.rotation_y != 0:
                self.porte_fin.rotation_y = 0
                Audio("porte_audio.mp3")
                self.porte_fin.x = 7
                self.porte_fin.z = -11
                self.player.enabled =False
                Audio("tension.mp3")
                invoke(self.son_cassette, delay=17)
                screen = Entity(model="quad", parent=camera.ui, color=color.black, scale=(1.8, 1))
                invoke(lambda : self.fin_jeu(screen), delay=19)


map6 = Map6()