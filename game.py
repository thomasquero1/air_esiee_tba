# game_main.py
from player import Player
from room import Room
from actions import Actions
from command import Command
from character import Character
import random
from item import Item
from config import DEBUG
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import io
import sys
import re
from PIL import Image, ImageDraw, ImageFont, ImageTk
import threading
import time


class _StdoutRedirector:
    """Redirige stdout vers un widget Text de Tkinter avec support ANSI."""
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.setup_colors()
    
    def setup_colors(self):
        """Configure les tags de couleur pour le widget Text."""
        # Codes ANSI → Couleur
        self.text_widget.tag_config("green", foreground="#00ff00")      # \033[92m
        self.text_widget.tag_config("red", foreground="#ff0000")        # \033[91m
        self.text_widget.tag_config("yellow", foreground="#ffff00")     # \033[93m
        self.text_widget.tag_config("cyan", foreground="#00ffff")       # \033[96m
        self.text_widget.tag_config("magenta", foreground="#ff00ff")    # \033[95m
        self.text_widget.tag_config("white", foreground="#ffffff")      # \033[97m
        self.text_widget.tag_config("default", foreground="#ffffff")    # Texte par défaut en blanc
        # Ne pas forcer le background ici: il est défini dans la GUI
    
    def parse_ansi(self, text):
        """
        Parse les codes ANSI et retourne une liste de tuples (texte, tag).
        Exemple: "\\033[92mBON\\033[0m test" → [("BON", "green"), (" test", "default")]
        """
        import re
        
        # Motif pour les codes ANSI : \033[XXm
        ansi_pattern = r'\033\[(\d+)m'
        
        # Correspondance codes ANSI → tags Tkinter
        color_map = {
            '92': 'green',      # Vert
            '91': 'red',        # Rouge
            '93': 'yellow',     # Jaune
            '96': 'cyan',       # Cyan
            '95': 'magenta',    # Magenta
            '97': 'white',      # Blanc
            '0': 'default',     # Réinitialisation
        }
        
        result = []
        current_tag = 'default'
        last_end = 0
        
        # Trouver tous les codes ANSI
        for match in re.finditer(ansi_pattern, text):
            # Ajouter le texte avant le code
            if match.start() > last_end:
                txt = text[last_end:match.start()]
                if txt:
                    result.append((txt, current_tag))
            
            # Mettre à jour le tag courant
            code = match.group(1)
            current_tag = color_map.get(code, 'default')
            last_end = match.end()
        
        # Ajouter le texte restant
        if last_end < len(text):
            txt = text[last_end:]
            if txt:
                result.append((txt, current_tag))
        
        return result if result else [(text, 'default')]
    
    def write(self, string):
        if string:
            # Parser les codes ANSI
            segments = self.parse_ansi(string)
            
            # Insérer chaque segment avec son tag
            for text, tag in segments:
                self.text_widget.insert(tk.END, text, tag)
            
            self.text_widget.see(tk.END)
            self.text_widget.update()
    
    def flush(self):
        pass


class GameGUI:
    """Interface graphique pour le jeu."""
    
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Air ESIEE - Copilote A320")
        self.root.geometry("1600x900")
        self.root.configure(bg="#1a1a1a")
        
        # Rediriger stdout
        self.output_buffer = io.StringIO()
        self.old_stdout = sys.stdout
        
        # Dictionnaire pour mapper les salles aux images
        self.room_image_map = {
            "Cockpit": "Cockpit.jpg",
            "Siège": "CopilotSeat.jpg",
            "Panneau central": "CentralPanel.jpg",
            "Panneau haut": "TopPanel.jpg",
            "Panneau bas": "BottomPanel.jpg",
            "Altimètre": "Altimeter.jpg",
            "Radar": "Radar.jpg",
            "Crew": "CrewZone.jpg",
            "Business": "BusinessCabin.jpg",
            "Economy": "EconomyCabin.jpg",
            "Back Crew": "BackCrewZone.jpg",
        }
        
        # Créer les frames
        self.create_widgets()
        self.current_fade = 0
        self.displaying = False
        
    def create_widgets(self):
        """Crée les widgets principaux."""
        # Frame gauche - Affichage (50%)
        left_frame = tk.Frame(self.root, bg="#0a0a0a")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Label pour affichage de l'image
        self.image_label = tk.Label(left_frame, bg="#000000")
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.photo_image = None
        
        # Frame droite - Console et contrôles (50%)
        right_frame = tk.Frame(self.root, bg="#1a1a1a")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Zone de texte (console)
        text_label = tk.Label(right_frame, text="Console du Jeu", bg="#1a1a1a", fg="#ffffff", 
                             font=("Courier", 10, "bold"))
        text_label.pack(anchor=tk.W, pady=5)
        
        self.text_output = tk.Text(right_frame, height=25, width=80, 
                                   bg="#0a0a0a", fg="#ffffff", 
                                   font=("Courier", 8), wrap=tk.WORD)
        self.text_output.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar pour la console
        scrollbar = tk.Scrollbar(right_frame, command=self.text_output.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_output.config(yscrollcommand=scrollbar.set)
        
        # Frame pour entrée de commande
        input_frame = tk.Frame(right_frame, bg="#1a1a1a")
        input_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(input_frame, text="> ", bg="#1a1a1a", fg="#ffffff", 
                font=("Courier", 10, "bold")).pack(side=tk.LEFT)
        
        self.command_input = tk.Entry(input_frame, bg="#0a0a0a", fg="#ffffff", 
                         font=("Courier", 10), insertbackground="#ffffff")
        self.command_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.command_input.bind("<Return>", self.on_command_enter)
        
        # Rediriger stdout
        sys.stdout = _StdoutRedirector(self.text_output)
    
    def load_room_image(self, room_name):
        """Charge l'image d'une salle depuis le dossier images."""
        import os
        image_filename = self.room_image_map.get(room_name)
        if not image_filename:
            return self.create_placeholder_image(room_name)
        
        image_path = os.path.join(os.path.dirname(__file__), "images", image_filename)
        
        if os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                return img
            except Exception as e:
                print(f"Erreur lors du chargement de l'image {image_filename}: {e}")
                return self.create_placeholder_image(room_name)
        else:
            # Image non trouvée, créer un placeholder
            return self.create_placeholder_image(room_name)
    
    def create_placeholder_image(self, room_name):
        """Crée une image de placeholder si l'image n'existe pas."""
        img = Image.new("RGB", (880, 660), color="#001a33")
        draw = ImageDraw.Draw(img)
        
        draw.rectangle([50, 50, 830, 610], outline="#00ff00", width=3)
        draw.text((250, 250), f"{room_name}", fill="#00ff00")
        draw.text((200, 300), "Image non trouvée", fill="#ff6600")
        draw.text((150, 350), "Mettez une image dans le dossier 'images/'", fill="#ffff00")
        
        return img
    
    def display_room(self, fade_transition=True):
        """Affiche la salle actuelle."""
        if self.displaying:
            return
        
        self.displaying = True
        room = self.game.player.current_room
        
        # Charger l'image de la salle
        img = self.load_room_image(room.name)
        self.show_room_image(room, img)
        
        # Afficher la description
        print(room.get_long_description())
        self.displaying = False
    
    def show_room_image(self, room, img):
        """Affiche l'image de la salle."""
        # Redimensionner l'image pour s'adapter au label
        label_width = 750
        label_height = 660
        
        # Calculer le ratio d'aspect
        img_ratio = img.width / img.height
        label_ratio = label_width / label_height
        
        if img_ratio > label_ratio:
            # L'image est plus large, adapter par la largeur
            new_width = label_width
            new_height = int(label_width / img_ratio)
        else:
            # L'image est plus haute, adapter par la hauteur
            new_height = label_height
            new_width = int(label_height * img_ratio)
        
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(img_resized)
        self.image_label.config(image=self.photo_image)
    
    def on_command_enter(self, event):
        """Gère la saisie de commande."""
        command = self.command_input.get()
        self.command_input.delete(0, tk.END)
        
        if command.strip():
            print(f"> {command}")
            self.game.process_command(command)
            
            # Vérifier si le jeu est terminé
            if self.game.finished:
                # Afficher le grade final
                self.game._display_final_grade()
                # Désactiver l'entrée de commande
                self.command_input.config(state=tk.DISABLED)
                print("\n[Jeu terminé - Fenêtre fermeture dans 5 secondes...]")
                # Fermer après 5 secondes
                self.root.after(5000, self.root.destroy)
                return
            
            # Mettre à jour l'affichage
            if command.split()[0] == "go":
                self.display_room(fade_transition=True)
            elif command.split()[0] == "look":
                self.display_room(fade_transition=False)
    
    def run(self):
        """Lance l'application GUI."""
        # Affichage initial
        self.display_room(fade_transition=False)
        self.root.mainloop()


class Game:
    def __init__(self):
        self.finished = False
        self.player = None
        self.commands = {}
        self.rooms = []


        # Structure des directions valides et aliases
        self.valid_directions = {"N", "S", "E", "W"}
        self.direction_aliases = {
            "N": "N", "NORD": "N", "Nord": "N", "nord": "N",
            "S": "S", "SUD": "S", "Sud": "S", "sud": "S",
            "E": "E", "EST": "E", "Est": "E", "est": "E",
            "O": "W", "W": "W", "OUEST": "W", "Ouest": "W", "ouest": "W"
        }


    def setup(self):
        """Initialisation du jeu : commandes, salles et joueur."""
        # Commandes
        self.commands["look"] = Command("look", "", Actions.look, 0)
        self.commands["go"] = Command("go", "<direction>", Actions.go, 1)
        self.commands["back"] = Command("back", "", Actions.back, 0)
        self.commands["take"] = Command("take", "<objet>", Actions.take, 1)
        self.commands["use"] = Command("use", "<objet>", Actions.use, 1)
        self.commands["talk"] = Command("talk", "<personnage>", Actions.talk, 1)
        self.commands["inventory"] = Command("inventory", "", Actions.inventory, 0)
        self.commands["help"] = Command("help", "", Actions.help, 0)
        self.commands["quit"] = Command("quit", "", Actions.quit, 0)
        self.commands["history"] = Command("history", "", Actions.history, 0)
        self.commands["inventory"] = Command("inventory", "", Actions.inventory, 0)
        self.commands["drop"] = Command("drop", "<objet>", Actions.drop, 1)


        # Création des salles
        cockpit = Room("Cockpit", "dans le cockpit debout")
        self.rooms.append(cockpit)
        seat = Room("Siège", "à votre siège de copilote")
        self.rooms.append(seat)
        panel_center = Room("Panneau central", "avec ECAM,📟 ECAM STATUS :- Seatbelt : OFF\n - No Smoking : ON\n"" - X-Bleed : OFF\n")
        self.rooms.append(panel_center)
        panel_top = Room("Panneau haut", "avec Lights et autres contrôles (éléctricité, carburant...))\n Tension batteries: 20V, Carburant restant: 3000kg, Taxi light ON")
        self.rooms.append(panel_top)
        panel_bottom = Room("Panneau bas", "Manettes de gaz, volets, communications\n Volet a 1\n -- Throttle set to idle\n - Radio tuned to tower")
        self.rooms.append(panel_bottom)
        altimeter = Room("Altimètre", "avec les mesures de hauteur\n Altitude: 35000ft\n Vitesse verticale: 0ft/min")
        self.rooms.append(altimeter)
        radar = Room("Radar", "radar météo et navigation,\n Météo: Clair, Navigation: Sur route")
        self.rooms.append(radar)
        crew = Room("Crew", "zone de l'équipage,\n L'hôtesse semble triste, peut-être un café l'aiderait.")
        self.rooms.append(crew)
        business = Room("Business", "cabine business\n Il manque un passager.")
        self.rooms.append(business)
        economy = Room("Economy", "cabine economy\n Un passager semble malade.")
        self.rooms.append(economy)
        back_crew = Room("Back Crew", "zone arrière de l'équipage\n Tout va bien ici. Vous pouvez vous servir un café")
        self.rooms.append(back_crew)


        # Définition des sorties (exits) avec directions standard
        cockpit.exits = {"S": seat, "W": crew, "E": panel_center}
        seat.exits = {"N": cockpit, "W": panel_center, "S": radar, "E": crew}
        panel_center.exits = {"W": seat, "S": panel_top, "E": cockpit}
        panel_top.exits = {"N": panel_center, "S": panel_bottom, "W": seat}
        panel_bottom.exits = {"W": seat, "N": panel_top, "E": altimeter, "S": radar}
        altimeter.exits = {"W": panel_bottom, "S": seat, "E": cockpit}
        radar.exits = {"N": panel_bottom, "W": seat, "S": back_crew, "E": economy}
        crew.exits = {"E": cockpit, "S": business, "W": economy}
        business.exits = {"N": crew, "E": economy, "S": back_crew}
        economy.exits = {"W": crew, "S": back_crew, "E": business}
        back_crew.exits = {"N": economy, "W": business, "E": crew, "N": radar}


        # Items courts (ajout de messages éducatifs pour chaque checklist)
        seat.items = [Item("Casque", "Vous contactez la Tour :\n \033[92mAirESIEE 11² bonjour,\033[0m veuillez régler le \033[92mTranspondeur 8681\033[0m",
                   edu_message="Le casque et la phrase de contact permettent d'établir une communication claire avec la tour; la phrase type facilite l'identification et la coordination en aviation.")]
        panel_center.items = [
        Item(
        "QRH",
        "CHECKLIST ECAM — Phase Prévol\n\n"
        "1️⃣ Vérifier les voyants cabine:\n"
        "   - \033[92mSeatbelt : ON\033[0m\n"
        "   - \033[92mNo Smoking : AUTO\033[0m\n\n"
        "2️⃣ Vérifier pressurisation :\n"
        "   - \033[92mX BLEED : AUTO\033[0m\n\n"
        "3️⃣ Lire ECAM et appliquer actions recommandées en tapant par exemple : No Smoking : AUTO.\n",
        edu_message="La QRH/ECAM permet d'identifier rapidement les défaillances/irrégularités et d'appliquer des procédures pour y remédier. Le système ECAM, inventé par AIRBUS répertorie tout les états du système de vol (pneus, moteurs, hydraulique, freins)."
        )
        ]
        panel_bottom.items = [Item("InstrumentsCheck", "Vérification instruments : \033[92mVolet a 1\033[0m\n -- \033[92mThrottle set to idle\033[0m\n - \033[92mRadio tuned to tower\033[0m",
                        edu_message="Vérifier les instruments assure que les commandes de vol et communications sont conformes aux paramètres attendus avant manœuvres; c'est une routine de sécurité indispensable (imaginez les gaz a fond pendant tout le vol ==> consomation excessive de carburant ==> crash !). Les checklist sont essentielles pour arriver a cela et les répeter a l'oral a son partenaire de vol comme vous le faites est parfait.")]
        altimeter.items = [Item("FCUCheck", "Vous volez a une altitude de croisière de \033[92m35000 pieds\033[0m, \033[92mvitesse verticale 0 ft/min\033[0m",
                    edu_message="Le FCU donne les paramètres de vol (altitude/vitesse verticale) — surveiller ces valeurs est fondamental pour maintenir la trajectoire et la sécurité du vol. (ex: eviter de descendre trop bas aux alentour de l'hymalaya ou d'éviter les collisions avec d'autres avions)")]
        panel_top.items = [Item("AlarmsList", "\033[92mAucune alarme en cours\033[0m, \033[92mSurtension (38V)\033[0m \033[92mCarburant 3000 kg\033[0m",
                    edu_message="Lister les alarmes et états électriques permet d'anticiper et prioriser les actions en cas d'avarie; gérer l'énergie et carburant est essentiel en gestion de vol.")]
        radar.items = [Item("RadarScan", "Scan radar : \033[92mmétéo ok\033[0m, \033[92mnavigation ORLY\033[0m",
                     edu_message="Interpréter le radar météo et la navigation permet d'assurer la continuité de la route et d'éviter les zones dangereuses (turbulences, traffic aérien dense); c'est une compétence clé de navigation.")]
        crew.items = [Item("CrewChecklist", "Vérification équipage : \033[91mVous devez remonter le moral de l'hôtesse.\033[0m",
                   edu_message="La gestion de l'équipage et du service contribue à la sécurité et au confort des passagers; l'aspect humain est central dans le métier de pilote pour s'assurer que en cabine, rien ne déborde dans votre avion.")]
        business.items = [Item("PassengerList", "Liste passagers Business : - \033[92mM. Dupont\033[0m\n - \033[92mMme Durand\033[0m\n -\033[92mM. Courivaud\033[0m -\033[92mM. Martin\033[0m",
                       edu_message="Connaître les passagers (nom/présence) aide à la gestion des priorités et à assurer le service et la sécurité à bord, notamment lorsque les passagers sont des personalités, ont des antécédents ou vous ont été signalé par l'équipage.")]
        economy.items = [Item("PassengerComplaints", "Problèmes passagers : \033[91mUn passager s'est évanoui. Il a besoin d'aide médicale.\033[0m",
                       edu_message="Traiter rapidement un problème médical à bord implique coordination, communication et connaissance des procédures — la sécurité des passagers prime.")]
        back_crew.items = [Item("BackCrewChecklist", "\033[91mCafés prêts pour l'équipage\033[0m",
                      edu_message="Le soutien de l'équipage (service, pauses) participe à la performance de ceux ci et a comment ils vont travailler, ils sont des humains avant tout et un équipage fatigué ou mal servi peut faire des erreurs.")]

        # Ajouter des objets supplémentaires pour les quêtes
        back_crew.items.append(Item("Café", "Un café chaud et revigorant"))
        back_crew.items.append(Item("Eau", "Une bouteille d'eau fraîche"))
        back_crew.items.append(Item("TrousseMédicale", "Une trousse de premiers secours bien équipée"))

        for room in self.rooms:
            self.valid_directions.update(room.exits.keys())


        # Création du joueur
        self.player = Player(input("Entrez votre nom: "))
        self.player.current_room = cockpit

        # PNJ
        captain = Character("captain", cockpit,  "le commandant de bord", ["Tout va bien, copilote.", "Continuez comme ça."], False)
        hostess = Character("hostess", crew, "une hotesse de l'air", ["Bonjour, comment ça va?", "Tout est prêt dans la cabine."])
        passenger1 = Character("passenger1", business, "un passager", ["Je voudrais de l'eau.", "Tout est confortable."])
        passenger2 = Character("passenger2", economy, "un passager", ["Pouvez-vous m'aider?", "Merci."], False)
        passenger3 = Character("passenger3", back_crew,  "un passager", ["Quand atterrissons-nous?", "Je suis nerveux."])
        # Placement initial PNJ
        cockpit.characters[captain.name] = captain
        captain.current_room = cockpit

        crew.characters[hostess.name] = hostess
        hostess.current_room = crew

        business.characters[passenger1.name] = passenger1
        passenger1.current_room = business

        economy.characters[passenger2.name] = passenger2
        passenger2.current_room = economy

        back_crew.characters[passenger3.name] = passenger3
        passenger3.current_room = back_crew

    

    def play(self):
        print(f"\nBienvenue {self.player.name} dans Air ESIEE - Copilote A320,\n tapez help pour avoir la liste des commandes.\n")
        while not self.finished:
            cmd = input("> ")
            self.process_command(cmd)
        
        # Afficher le grade final
        self._display_final_grade()
    
    def _display_final_grade(self):
        """Affiche le grade final du joueur basé sur ses points."""
        points = self.player.score
        print(f"\n{'='*50}")
        print(f"RÉSULTATS FINAUX - {self.player.name}")
        print(f"{'='*50}")
        print(f"Points obtenus: {points}/100")
        
        if points >= 90:
            grade = "OR 🥇"
            print(f"Grade: {grade}")
            print("Vous avez piloté cet A320 avec excellence!")
        elif points >= 70:
            grade = "ARGENT 🥈"
            print(f"Grade: {grade}")
            print("Vous avez fait du très bon travail!")
        elif points >= 50:
            grade = "BRONZE 🥉"
            print(f"Grade: {grade}")
            print("Vous avez accompli votre mission.")
        else:
            print(f"Points insuffisants: {points}/50")
            print("Vous devez améliorer votre performance.")
        
        print(f"{'='*50}\n")


    def process_command(self, command_string):
        if not command_string.strip():
            return
        list_of_words = command_string.split()
        cmd_word = list_of_words[0]
        if cmd_word not in self.commands:
            # si commande inconnue, vérifier si l'utilisateur a tapé une phrase correspondant
            # à une des phrases vertes des checklists. Si oui, on attribue des points.
            handled = self._handle_phrase_input(command_string)
            if not handled:
                print(f"Commande '{cmd_word}' non reconnue. Tapez 'help'.")
            return
        else:
            cmd = self.commands[cmd_word]
            # Vérification si la commande est 'go' pour normaliser la direction
            if cmd_word == "go" and len(list_of_words) > 1:
                user_input = list_of_words[1]
                if user_input not in self.direction_aliases:
                    print(f"Direction '{user_input}' invalide !")
                    return
                # Remplacer par la direction standard
                list_of_words[1] = self.direction_aliases[user_input]
            # call the action and capture the result
            if cmd.number_of_parameters == -1:
                result = cmd.action(self, list_of_words, len(list_of_words) - 1)
            else:
                result = cmd.action(self, list_of_words, cmd.number_of_parameters)

            if cmd_word == "go" and result:
                if DEBUG: print(f"DEBUG: Commande 'go' valide, déplacement des personnages")
                self._move_all_characters()


    def _handle_phrase_input(self, command_string):
        """Vérifie si la commande saisie correspond à des phrases 'vertes' dans les items.

        Retourne True si au moins une phrase a été reconnue et traitée, False sinon.
        """
        normalized = command_string.lower()
        found_any = False

        # Inclure les items posés dans les salles ET ceux dans l'inventaire du joueur.
        inventory_items = list(getattr(self.player, "inventory", {}).values())

        for room in self.rooms:
            # room.items peut être une liste ou un dict
            items = None
            if isinstance(room.items, dict):
                items = list(room.items.values())
            else:
                items = room.items
            room_items = items or []
            for item in list(room_items) + inventory_items:
                # certains items peuvent ne pas avoir d'attribut green_phrases
                phrases = getattr(item, 'green_phrases', [])
                if not phrases:
                    continue
                # for each phrase, check if present in user input
                newly_found = []
                for phrase in phrases:
                    if phrase.lower() in normalized:
                        # check if already recorded for this player
                        already = phrase in self.player.item_progress.get(item.name, set())
                        if not already:
                            newly_found.append(phrase)
                # award points for newly found phrases
                for phrase in newly_found:
                    self.player.add_found_phrase(item.name, phrase)
                    self.player.award_points(3, reason=f"Identification de '{phrase}' ({item.name})")
                    found_any = True

                # if all phrases for this item have been found and item not yet completed -> award completeness
                if phrases:
                    got = self.player.item_progress.get(item.name, set())
                    if set(phrases).issubset(got) and item.name not in self.player.completed_items:
                        # award completeness points
                        self.player.completed_items.add(item.name)
                        self.player.award_points(2, reason=f"Checklist '{item.name}' complétée")
                        # print educational message
                        edu = getattr(item, 'edu_message', None)
                        if edu:
                            print(f"Explication: {edu}")
                        else:
                            print(f"Vous avez complété la checklist '{item.name}'. Cela améliore votre compréhension opérationnelle.")
                        found_any = True

        return found_any
    
    def _check_quests(self, character, room):
        """Vérifie et complète les quêtes associées aux personnages."""
        
        # Quête: Parler au captain avec un café
        if character.name == "captain":
            if "Café" in self.player.inventory and "captain_quest" not in self.player.completed_quests:
                self.player.completed_quests.add("captain_quest")
                self.player.award_points(6, reason="Quête complétée: Commandant satisfait avec un café")
                print(f"Le commandant vous sourit: 'Merci, excellent travail!'")
        
        # Quête: Parler à l'hôtesse avec un café
        if character.name == "hostess":
            if "Café" in self.player.inventory and "hostess_quest" not in self.player.completed_quests:
                self.player.completed_quests.add("hostess_quest")
                self.player.award_points(5, reason="Quête complétée: Hôtesse satisfaite avec un café")
                print(f"L'hôtesse semble beaucoup plus heureuse!")
        
        # Quête: Parler à passenger1 avec de l'eau
        if character.name == "passenger1":
            if "Eau" in self.player.inventory and "passenger1_quest" not in self.player.completed_quests:
                self.player.completed_quests.add("passenger1_quest")
                self.player.award_points(5, reason="Quête complétée: Passager Business servi avec de l'eau")
                print(f"Le passager vous remercie: 'Merci beaucoup, c\'est très gentil!'")
        
        # Quête: Parler à passenger2 avec la trousse médicale
        if character.name == "passenger2":
            if "Trousse médicale" in self.player.inventory and "passenger2_quest" not in self.player.completed_quests:
                self.player.completed_quests.add("passenger2_quest")
                self.player.award_points(7, reason="Quête complétée: Passager malade secouru avec trousse médicale")
                print(f"Le passager vous remercie: 'Merci pour votre aide, je me sens mieux maintenant!'")
        
        # Quête: Parler à passenger3 rapporte des points
        if character.name == "passenger3":
            if "passenger3_talk" not in self.player.completed_quests:
                self.player.completed_quests.add("passenger3_talk")
                self.player.award_points(8, reason="Vous avez rassuré passenger 3")
                print(f"Passenger 3 se sent rassuré.")
    
    def _move_all_characters(self):
        """Déplace tous les personnages (characters) du jeu de manière aléatoire."""
        if DEBUG: print(f"DEBUG: Début du déplacement de {sum(len(room.characters) for room in self.rooms)} personnages")
        for room in self.rooms:
            # Parcourir une copie de la liste car les characters se déplaceront
            for character in list(room.characters.values()):
                character.move()
        if DEBUG: print(f"DEBUG: Fin du déplacement de tous les personnages")
    
def main():
    game = Game()
    game.setup()
    
    Launch = input("Voulez vous l'interface graphique ? (Y=oui, N=non): ")
    if Launch.upper() == 'Y':
        try:
            # Try to initialize the GUI
            gui = GameGUI(game)
            gui.run()
        except (tk.TclError, ImportError) as e:
            # If Tkinter fails (no screen) or PIL is missing, fall back to console
            print("=" * 60)
            print("MODE CONSOLE ACTIVE")
            print(f"Raison : {e}")
            print("Lancement du mode textuel...")
            print("=" * 60)
            print()
            
            # Launch the text-only version
            game.play()
    else:
        # Launch the text-only version
        game.play()

if __name__ == "__main__":
    main()
