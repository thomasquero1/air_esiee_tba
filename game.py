# game_main.py
from player import Player
from room import Room
from actions import Actions
from command import Command
import random


class Game:
    def __init__(self):
        self.finished = False
        self.player = None
        self.commands = {}


        # Structure des directions valides et aliases
        self.valid_directions = {"N", "S", "E", "W"}
        self.direction_aliases = {
            "N": "N", "NORD": "N", "Nord": "N", "nord": "N",
            "S": "S", "SUD": "S", "Sud": "S", "sud": "S",
            "E": "E", "EST": "E", "Est": "E", "est": "E",
            "O": "W", "OUEST": "W", "Ouest": "W", "ouest": "W"
        }


    def setup(self):
        """Initialisation du jeu : commandes, salles, objets, PNJ et joueur."""
        # Commandes
        self.commands["look"] = Command("look", "", Actions.look, 0)
        self.commands["go"] = Command("go", "<direction>", Actions.go, 1)
        self.commands["back"] = Command("back", "", Actions.back, 0)
        self.commands["take"] = Command("take", "<objet>", Actions.take, 1)
        self.commands["use"] = Command("use", "<objet>", Actions.use, 1)
        self.commands["talk"] = Command("talk", "<pnj>", Actions.talk, 1)
        self.commands["inventory"] = Command("inventory", "", Actions.inventory, 0)
        self.commands["help"] = Command("help", "", Actions.help, 0)
        self.commands["quit"] = Command("quit", "", Actions.quit, 0)


        # Création des salles
        cockpit = Room("Cockpit", "dans le cockpit avec les panneaux ECAM et FCU")
        self.rooms.append(cockpit)
        seat = Room("Siège", "à votre siège de copilote")
        self.rooms.append(seat)
        panel_center = Room("Panneau central", "avec ECAM, MCDU et boutons principaux")
        self.rooms.append(panel_center)
        panel_top = Room("Panneau haut", "avec voyants et alarmes")
        self.rooms.append(panel_top)
        panel_bottom = Room("Panneau bas", "instruments secondaires")
        self.rooms.append(panel_bottom)
        altimeter = Room("Altimètre", "avec les mesures de hauteur")
        self.rooms.append(altimeter)
        radar = Room("Radar", "radar météo et navigation")
        self.rooms.append(radar)
        crew = Room("Crew", "zone de l'équipage")
        self.rooms.append(crew)
        business = Room("Business", "cabine business")
        self.rooms.append(business)
        economy = Room("Economy", "cabine economy")
        self.rooms.append(economy)
        back_crew = Room("Back Crew", "zone arrière de l'équipage")
        self.rooms.append(back_crew)


        # Définition des sorties (exits) avec directions standard
        cockpit.exits = {"S": seat, "W" : crew}
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


        for room in self.rooms:
            self.valid_directions.update(room.exits.keys())


        # Création du joueur
        self.player = Player(input("Entrez votre nom: "))
        self.player.current_room = cockpit


    def play(self):
        print(f"\nBienvenue {self.player.name} dans Air ESIEE – Copilote A320")
        while not self.finished:
            # Déplacement aléatoire de l'hôtesse
            self.hostess.move()
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
