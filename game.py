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
from PIL import Image, ImageDraw, ImageFont
import threading
import time


class _StdoutRedirector:
    """Redirige stdout vers un widget Text de Tkinter."""
    def __init__(self, text_widget):
        self.text_widget = text_widget
    
    def write(self, string):
        if string:
            self.text_widget.insert(tk.END, string)
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
        self.root.geometry("1400x900")
        self.root.configure(bg="#1a1a1a")
        
        # Rediriger stdout
        self.output_buffer = io.StringIO()
        self.old_stdout = sys.stdout
        
        # Créer les frames
        self.create_widgets()
        self.room_images = self.generate_room_images()
        self.current_fade = 0
        self.displaying = False
        
    def create_widgets(self):
        """Crée les widgets principaux."""
        # Frame gauche - Affichage
        left_frame = tk.Frame(self.root, bg="#0a0a0a", width=900)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Canvas pour l'image de la salle
        self.canvas = tk.Canvas(left_frame, bg="#000000", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.photo_image = None
        
        # Frame droite - Texte et contrôles
        right_frame = tk.Frame(self.root, bg="#1a1a1a", width=500)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Zone de texte
        text_label = tk.Label(right_frame, text="Jeu", bg="#1a1a1a", fg="#00ff00", 
                             font=("Courier", 10, "bold"))
        text_label.pack(anchor=tk.W, pady=5)
        
        self.text_output = tk.Text(right_frame, height=25, width=60, 
                                   bg="#0a0a0a", fg="#00ff00", 
                                   font=("Courier", 9), wrap=tk.WORD)
        self.text_output.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(right_frame, command=self.text_output.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_output.config(yscrollcommand=scrollbar.set)
        
        # Frame pour entrée de commande
        input_frame = tk.Frame(right_frame, bg="#1a1a1a")
        input_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(input_frame, text="> ", bg="#1a1a1a", fg="#00ff00", 
                font=("Courier", 10, "bold")).pack(side=tk.LEFT)
        
        self.command_input = tk.Entry(input_frame, bg="#0a0a0a", fg="#00ff00", 
                                     font=("Courier", 10), insertbackground="#00ff00")
        self.command_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.command_input.bind("<Return>", self.on_command_enter)
        
        # Rediriger stdout
        sys.stdout = _StdoutRedirector(self.text_output)
    
    def generate_room_images(self):
        """Génère les images pour chaque salle."""
        images = {}
        
        room_designs = {
            "Cockpit": self.create_cockpit_image,
            "Siège": self.create_seat_image,
            "Panneau central": self.create_panel_center_image,
            "Panneau haut": self.create_panel_top_image,
            "Panneau bas": self.create_panel_bottom_image,
            "Altimètre": self.create_altimeter_image,
            "Radar": self.create_radar_image,
            "Crew": self.create_crew_image,
            "Business": self.create_business_image,
            "Economy": self.create_economy_image,
            "Back Crew": self.create_back_crew_image,
        }
        
        for room_name, create_func in room_designs.items():
            images[room_name] = create_func()
        
        return images
    
    def create_cockpit_image(self):
        """Crée l'image du cockpit."""
        img = Image.new("RGB", (880, 660), color="#001a33")
        draw = ImageDraw.Draw(img)
        
        # Cadre cockpit
        draw.rectangle([50, 50, 830, 610], outline="#00ff00", width=3)
        
        # Sièges
        draw.rectangle([100, 100, 250, 200], fill="#333333", outline="#00ff00", width=2)
        draw.text((110, 150), "COMMANDANT", fill="#00ff00")
        
        draw.rectangle([280, 100, 430, 200], fill="#555555", outline="#ffff00", width=2)
        draw.text((295, 150), "COPILOTE", fill="#ffff00")
        
        # Tableau de bord
        draw.rectangle([100, 250, 830, 600], fill="#1a1a1a", outline="#00ff00", width=2)
        draw.text((300, 280), "SYSTEMES AVIONIQUES", fill="#00ff00")
        draw.text((150, 350), "ALT: 35000ft", fill="#00ff00")
        draw.text((400, 350), "SPD: 450kt", fill="#00ff00")
        draw.text((150, 400), "HDG: 090", fill="#00ff00")
        draw.text((400, 400), "VS: 0 ft/min", fill="#00ff00")
        
        return img
    
    def create_seat_image(self):
        """Crée l'image du siège."""
        img = Image.new("RGB", (880, 660), color="#2a2a2a")
        draw = ImageDraw.Draw(img)
        
        draw.rectangle([50, 50, 830, 610], outline="#0080ff", width=3)
        draw.text((300, 100), "POSITION COPILOTE", fill="#0080ff")
        
        # Siège
        draw.ellipse([300, 250, 580, 500], fill="#444444", outline="#0080ff", width=2)
        draw.rectangle([350, 500, 530, 550], fill="#333333", outline="#0080ff", width=2)
        
        draw.text((200, 580), "Café chaud nearby...", fill="#00ff00")
        
        return img
    
    def create_panel_center_image(self):
        """Crée l'image du panneau central."""
        img = Image.new("RGB", (880, 660), color="#1a1a1a")
        draw = ImageDraw.Draw(img)
        
        draw.rectangle([50, 50, 830, 610], outline="#ff8800", width=3)
        draw.text((250, 80), "PANNEAU CENTRAL - ECAM", fill="#ff8800")
        
        # Affichage ECAM
        draw.rectangle([100, 150, 780, 400], fill="#0a0a0a", outline="#ff8800", width=2)
        draw.text((150, 170), "ECAM STATUS:", fill="#ff8800")
        draw.text((150, 200), "Seatbelt: OFF", fill="#ff0000")
        draw.text((150, 230), "No Smoking: ON", fill="#ff0000")
        draw.text((150, 260), "X-Bleed: OFF", fill="#ff0000")
        draw.text((150, 310), "Pressurization: AUTO", fill="#00ff00")
        
        draw.rectangle([100, 450, 780, 580], fill="#0a0a0a", outline="#ff8800", width=2)
        draw.text((150, 470), "QRH disponible - Use pour voir checklist", fill="#ffff00")
        
        return img
    
    def create_panel_top_image(self):
        """Crée l'image du panneau supérieur."""
        img = Image.new("RGB", (880, 660), color="#1a0a1a")
        draw = ImageDraw.Draw(img)
        
        draw.rectangle([50, 50, 830, 610], outline="#ff00ff", width=3)
        draw.text((200, 80), "PANNEAU HAUT - ECLAIRAGE & ELECTRICITE", fill="#ff00ff")
        
        # Batteries
        draw.rectangle([100, 150, 400, 250], fill="#0a0a0a", outline="#ff00ff", width=2)
        draw.text((120, 170), "BATTERIES", fill="#ff00ff")
        draw.text((120, 210), "Tension: 28.5V", fill="#00ff00")
        
        # Carburant
        draw.rectangle([450, 150, 750, 250], fill="#0a0a0a", outline="#ff00ff", width=2)
        draw.text((470, 170), "CARBURANT", fill="#ff00ff")
        draw.text((470, 210), "Reste: 3000 kg", fill="#00ff00")
        
        # Lights
        draw.rectangle([100, 300, 750, 500], fill="#0a0a0a", outline="#ff00ff", width=2)
        draw.text((120, 320), "LIGHTS", fill="#ff00ff")
        draw.text((120, 360), "Landing Light: ON", fill="#00ff00")
        draw.text((120, 390), "Taxi Light: ON", fill="#00ff00")
        draw.text((120, 420), "Cabin Light: AUTO", fill="#00ff00")
        
        return img
    
    def create_panel_bottom_image(self):
        """Crée l'image du panneau inférieur."""
        img = Image.new("RGB", (880, 660), color="#0a1a1a")
        draw = ImageDraw.Draw(img)
        
        draw.rectangle([50, 50, 830, 610], outline="#00ff88", width=3)
        draw.text((150, 80), "PANNEAU BAS - GAZ & COMMUNICATIONS", fill="#00ff88")
        
        # Manettes de gaz
        draw.rectangle([100, 180, 400, 400], fill="#0a0a0a", outline="#00ff88", width=2)
        draw.text((120, 200), "THROTTLE (GAZ)", fill="#00ff88")
        draw.text((120, 260), "Moteur 1: IDLE", fill="#00ff00")
        draw.text((120, 290), "Moteur 2: IDLE", fill="#00ff00")
        draw.text((120, 340), "Volets: 1", fill="#00ff00")
        
        # Communications
        draw.rectangle([450, 180, 750, 400], fill="#0a0a0a", outline="#00ff88", width=2)
        draw.text((470, 200), "COMMUNICATIONS", fill="#00ff88")
        draw.text((470, 260), "Radio: 121.5 MHz", fill="#00ff00")
        draw.text((470, 290), "Status: Tower", fill="#00ff00")
        draw.text((470, 340), "Transponder: 8681", fill="#00ff00")
        
        return img
    
    def create_altimeter_image(self):
        """Crée l'image de l'altimètre."""
        img = Image.new("RGB", (880, 660), color="#001a00")
        draw = ImageDraw.Draw(img)
        
        draw.rectangle([50, 50, 830, 610], outline="#00ff00", width=3)
        draw.text((250, 80), "ALTIMETRE & VARIOMETRE", fill="#00ff00")
        
        # Altimètre
        draw.ellipse([150, 180, 450, 480], outline="#00ff00", width=3)
        draw.text((250, 300), "35000 ft", fill="#00ff00")
        
        # Variomètre
        draw.ellipse([500, 180, 800, 480], outline="#00ff00", width=3)
        draw.text((620, 300), "VS: 0 ft/min", fill="#00ff00")
        
        return img
    
    def create_radar_image(self):
        """Crée l'image du radar."""
        img = Image.new("RGB", (880, 660), color="#1a1a1a")
        draw = ImageDraw.Draw(img)
        
        draw.rectangle([50, 50, 830, 610], outline="#00ffff", width=3)
        draw.text((250, 80), "RADAR METEO & NAVIGATION", fill="#00ffff")
        
        # Radar
        draw.ellipse([200, 200, 500, 500], outline="#00ffff", width=2)
        draw.text((280, 350), "CLEAR", fill="#00ff00")
        
        # Navigation
        draw.rectangle([550, 200, 800, 500], fill="#0a0a0a", outline="#00ffff", width=2)
        draw.text((570, 230), "NAVIGATION", fill="#00ffff")
        draw.text((570, 280), "Route: ORLY", fill="#00ff00")
        draw.text((570, 310), "Distance: 150nm", fill="#00ff00")
        draw.text((570, 340), "ETA: 12:30", fill="#00ff00")
        
        return img
    
    def create_crew_image(self):
        """Crée l'image de la zone équipage."""
        img = Image.new("RGB", (880, 660), color="#2a1a1a")
        draw = ImageDraw.Draw(img)
        
        draw.rectangle([50, 50, 830, 610], outline="#ff6600", width=3)
        draw.text((250, 80), "ZONE EQUIPAGE", fill="#ff6600")
        
        # Hôtesse
        draw.ellipse([300, 200, 450, 350], fill="#ffaa00", outline="#ff6600", width=2)
        draw.text((310, 270), "Hôtesse", fill="#000000")
        
        draw.text((200, 420), "L'hôtesse semble triste...", fill="#ff6600")
        draw.text((200, 460), "Peut-être un café l'aiderait?", fill="#ffff00")
        
        return img
    
    def create_business_image(self):
        """Crée l'image de la cabine business."""
        img = Image.new("RGB", (880, 660), color="#1a1a1a")
        draw = ImageDraw.Draw(img)
        
        draw.rectangle([50, 50, 830, 610], outline="#cccccc", width=3)
        draw.text((250, 80), "CABINE BUSINESS", fill="#cccccc")
        
        # Passagers
        for i in range(3):
            draw.rectangle([100 + i*200, 200, 180 + i*200, 300], 
                          fill="#666666", outline="#cccccc", width=2)
            draw.text((105 + i*200, 240), f"P{i+1}", fill="#ffffff")
        
        draw.text((150, 420), "Passager 1 en Business", fill="#cccccc")
        draw.text((150, 460), "Demande de l'eau", fill="#ffff00")
        
        return img
    
    def create_economy_image(self):
        """Crée l'image de la cabine économique."""
        img = Image.new("RGB", (880, 660), color="#1a1a1a")
        draw = ImageDraw.Draw(img)
        
        draw.rectangle([50, 50, 830, 610], outline="#888888", width=3)
        draw.text((250, 80), "CABINE ECONOMY", fill="#888888")
        
        # Sièges
        for row in range(2):
            for col in range(4):
                x = 100 + col*170
                y = 150 + row*150
                draw.rectangle([x, y, x+140, y+120], fill="#333333", outline="#888888", width=1)
        
        draw.text((150, 450), "Un passager semble malade...", fill="#888888")
        draw.text((150, 490), "Besoin d'aide médicale", fill="#ff0000")
        
        return img
    
    def create_back_crew_image(self):
        """Crée l'image de la zone arrière équipage."""
        img = Image.new("RGB", (880, 660), color="#1a1a0a")
        draw = ImageDraw.Draw(img)
        
        draw.rectangle([50, 50, 830, 610], outline="#ffff00", width=3)
        draw.text((200, 80), "ZONE ARRIERE EQUIPAGE", fill="#ffff00")
        
        # Caféière
        draw.rectangle([150, 200, 350, 350], fill="#8B4513", outline="#ffff00", width=2)
        draw.text((160, 270), "CAFE", fill="#ffff00")
        
        # Provisions
        draw.rectangle([450, 200, 650, 350], fill="#666666", outline="#ffff00", width=2)
        draw.text((460, 270), "PROVISIONS", fill="#ffff00")
        
        # Passagers
        draw.ellipse([100, 420, 250, 550], fill="#ffcc00", outline="#ffff00", width=2)
        draw.text((130, 480), "Passager 3", fill="#000000")
        
        draw.text((350, 450), "Nerveux", fill="#ffff00")
        draw.text((350, 490), "Quand atterrissons-nous?", fill="#ff8800")
        
        return img
    
    def display_room(self, fade_transition=True):
        """Affiche la salle actuelle."""
        if self.displaying:
            return
        
        self.displaying = True
        room = self.game.player.current_room
        
        if fade_transition and self.photo_image:
            # Transition fondu en noir
            self.animate_fade_out(room)
        else:
            self.show_room_image(room)
        
        # Afficher la description
        print(room.get_long_description())
        self.displaying = False
    
    def animate_fade_out(self, next_room):
        """Anime le fondu en noir."""
        img = self.room_images[next_room.name]
        
        for alpha in range(0, 256, 20):
            fade_img = Image.new("RGBA", img.size, (0, 0, 0, alpha))
            if self.photo_image:
                composite = Image.new("RGB", img.size)
                composite.paste(self.photo_image, (0, 0))
                composite = Image.alpha_composite(
                    Image.new("RGBA", img.size, (255, 255, 255, 255)),
                    Image.new("RGBA", composite.size, (0, 0, 0, 0))
                )
            time.sleep(0.01)
        
        self.show_room_image(next_room)
    
    def show_room_image(self, room):
        """Affiche l'image de la salle."""
        img = self.room_images[room.name]
        
        # Redimensionner si nécessaire
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width > 1:
            img = img.resize((canvas_width - 20, canvas_height - 20))
        
        self.photo_image = tk.PhotoImage(file=None)
        self.photo_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, image=self.photo_image, anchor=tk.NW)
        
        # Ajouter les boutons pour les PNJ
        self.add_character_buttons(room)
    
    def add_character_buttons(self, room):
        """Ajoute des boutons pour chaque PNJ."""
        self.canvas.delete("npc_button")
        
        char_positions = {
            "captain": (200, 150),
            "hostess": (350, 280),
            "passenger1": (250, 260),
            "passenger2": (450, 350),
            "passenger3": (150, 480),
        }
        
        for char_name, character in room.characters.items():
            if char_name in char_positions:
                x, y = char_positions[char_name]
                self.canvas.create_oval(
                    x-20, y-20, x+20, y+20,
                    fill="#ffff00", outline="#ff8800", width=2, tags="npc_button"
                )
                self.canvas.create_text(
                    x, y, text=char_name[:3].upper(), 
                    fill="#000000", font=("Arial", 8, "bold"), tags="npc_button"
                )
                self.canvas.tag_bind("npc_button", "<Button-1>", 
                                   lambda e, cn=char_name: self.on_npc_click(cn))
    
    def on_canvas_click(self, event):
        """Gère les clics sur le canvas."""
        pass
    
    def on_npc_click(self, char_name):
        """Gère les clics sur les PNJ."""
        self.command_input.delete(0, tk.END)
        self.command_input.insert(0, f"talk {char_name}")
        self.on_command_enter(None)
    
    def on_command_enter(self, event):
        """Gère la saisie de commande."""
        command = self.command_input.get()
        self.command_input.delete(0, tk.END)
        
        if command.strip():
            print(f"> {command}")
            self.game.process_command(command)
            
            # Mettre à jour l'affichage
            if command.split()[0] == "go":
                self.display_room(fade_transition=True)
            elif command.split()[0] == "look":
                self.display_room(fade_transition=False)
    
    def run(self):
        """Lance l'application GUI."""
        try:
            from PIL import ImageTk
            globals()['ImageTk'] = ImageTk
        except ImportError:
            messagebox.showerror("Erreur", "Pillow est requis. Installez avec: pip install Pillow")
            return
        
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
        altimeter = Room("Altimètre", "avec les mesures de hauteur\n Altitude: 35000ft\n Vertical Speed: 0ft/min")
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
        seat.items = [Item("Casque", "Vous contactez la Tour :\n \033[92mAirESIEE 11² bonjour, Transpondeur 8681\033[0m",
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
        altimeter.items = [Item("FCUCheck", "Vous volez a une altitude de croisière de \033[92m35000 pieds\033[0m, \033[92mvitesse vertical 0 ft/min\033[0m",
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
        back_crew.items.append(Item("Trousse médicale", "Une trousse de premiers secours bien équipée"))

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

        for room in self.rooms:
            # room.items peut être une liste ou un dict
            items = None
            if isinstance(room.items, dict):
                items = list(room.items.values())
            else:
                items = room.items
            if not items:
                continue
            for item in items:
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
    
    # Check if graphical display is available
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

if __name__ == "__main__":
    main()
