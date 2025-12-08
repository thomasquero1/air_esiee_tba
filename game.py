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
        economy.items = [Item("PassengerComplaints", "Problèmes passagers : \33[91mUn passager s'est évanoui. Il a besoin d'aide médicale.\033[0m",
                       edu_message="Traiter rapidement un problème médical à bord implique coordination, communication et connaissance des procédures — la sécurité des passagers prime.")]
        back_crew.items = [Item("BackCrewChecklist", "\033[91mCafés prêts pour l'équipage\033[0m",
                      edu_message="Le soutien de l'équipage (service, pauses) participe à la performance de ceux ci et a comment ils vont travailler, ils sont des humains avant tout et un équipage fatigué ou mal servi peut faire des erreurs.")]


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
            cmd.action(self, list_of_words, cmd.number_of_parameters)

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
    
    def get_next_rooms(self):
        """Retourne une liste des salles accessibles depuis la salle actuelle de l'acteur."""
        current_room = self.player.current_room
        next_rooms = []
        for direction, room in current_room.exits.items():
            if room:
                next_rooms.append((direction, room))
        return next_rooms


def main():
    game = Game()
    game.setup()
    game.play()

if __name__ == "__main__":
    main()
