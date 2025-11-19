# game_main.py
from player import Player
from room import Room
from actions import Actions
from command import Command
import random
from item import Item


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
        self.commands["inventory"] = Command("inventory", "", Actions.inventory, 0)
        self.commands["help"] = Command("help", "", Actions.help, 0)
        self.commands["quit"] = Command("quit", "", Actions.quit, 0)
        self.commands["history"] = Command("history", "", Actions.history, 0)
        self.commands["inventory"] = Command("inventory", "", Actions.inventory, 0)
        self.commands["drop"] = Command("drop", "<objet>", Actions.drop, 1)


        # Création des salles
        cockpit = Room("Cockpit", "dans le cockpit debout")
        self.rooms.append(cockpit)
        seat = Room("Siège", "à votre siège de copilote, parlez a votre commandant avec un café dans votre inventaire")
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
        seat.exits = {"N": cockpit, "E": panel_center, "S": radar}
        panel_center.exits = {"W": seat, "S": panel_top}
        panel_top.exits = {"N": panel_center, "S": panel_bottom, "E":seat}
        panel_bottom.exits = {"W": seat, "S": panel_top, "E": altimeter, "N": cockpit}
        altimeter.exits = {"W": panel_bottom, "S": seat, "E": cockpit}
        radar.exits = {"N": altimeter, "E": seat, "S": panel_bottom}
        crew.exits = {"W": cockpit, "S": business, "E": economy}
        business.exits = {"N": crew, "E": economy, "S": back_crew}
        economy.exits = {"W": crew, "S": back_crew, "E": business}
        back_crew.exits = {"N": economy, "W": business, "E": crew}


        # Items courts
        seat.items = [Item("Casque", "Vous contactez la Tour :\n AirESIEE 11² bonjour, Transpondeur 8681")]
        panel_center.items = [
        Item(
        "QRH",
        "CHECKLIST ECAM — Phase Prévol\n\n"
        "1️⃣ Vérifier les voyants cabine:\n"
        "   - Seatbelt 🔔 : ON\n"
        "   - No Smoking 🚭 : AUTO\n\n"
        "2️⃣ Vérifier pressurisation :\n"
        "   - X BLEED : AUTO\n\n"
        "3️⃣ Lire ECAM et appliquer actions recommandées.\n"
        "\nUtilisez la commande : `ecam check`"
        )
        ]
        panel_bottom.items = [Item("InstrumentsCheck", "Vérification instruments")]
        altimeter.items = [Item("FCUCheck", "Vous volez a une altitude de croisière de 35000 pieds, vitesse vertical 0 ft/min")]
        panel_top.items = [Item("AlarmsList", "Aucune alarme en cours, Surtension (38   V) Carburant 3000 kg")]
        radar.items = [Item("RadarScan", "Scan radar")]
        crew.items = [Item("CrewChecklist", "Vérification équipage : Vous devez remonter le moral de l'hôtesse.")]
        business.items = [Item("PassengerList", "Liste passagers Business : - M. Dupont\n - Mme Durand\n -M. Courivaud -M. Martin")]
        economy.items = [Item("PassengerComplaints", "Problèmes passagers : Un passager s'est évanoui. Il a besoin d'aide médicale.")]
        back_crew.items = [Item("BackCrewChecklist", "Cafés prêts pour l'équipage")]


        for room in self.rooms:
            self.valid_directions.update(room.exits.keys())


        # Création du joueur
        self.player = Player(input("Entrez votre nom: "))
        self.player.current_room = cockpit


    def play(self):
        print(f"\nBienvenue {self.player.name} dans Air ESIEE - Copilote A320,\n tapez help pour avoir la liste des commandes.\n")
        while not self.finished:
            cmd = input("> ")
            self.process_command(cmd)


    def process_command(self, command_string):
        if not command_string.strip():
            return
        list_of_words = command_string.split()
        cmd_word = list_of_words[0]
        if cmd_word not in self.commands:
            print(f"Commande '{cmd_word}' non reconnue. Tapez 'help'.")
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
            cmd.action(self, list_of_words, cmd.number_of_parameters)


def main():
    game = Game()
    game.setup()
    game.play()

if __name__ == "__main__":
    main()
