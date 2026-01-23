from actor import Actor
from config import DEBUG

# Définir la classe Player.
class Player(Actor):
    """
    Représente un joueur dans l'univers du jeu.

    Le joueur possède un nom et se situe dans une salle donnée à chaque instant.

    Attributs
    ---------
    name : str
        Nom du joueur.
    current_room : Room | None
        Salle dans laquelle se trouve actuellement le joueur.

    Méthodes
    --------
    move(direction) -> bool
        Déplace le joueur dans la direction indiquée si possible.
        Retourne True si le déplacement a été effectué, False sinon.
    """

    def __init__(self, name):
        super().__init__(name, current_room=None)
        self.history = []
        self.inventory = {}
        # score pour l'identification des mots-clés verts et la complétude
        self.score = 0
        # suivi des phrases vertes trouvées par item : { item_name: set(phrases) }
        self.item_progress = {}
        # ensemble des items entièrement complétés
        self.completed_items = set()
        # ensemble des quêtes complétées
        self.completed_quests = set()
    
    def move(self, direction):
        """
        Déplace le joueur vers la salle située dans la direction spécifiée.

        Paramètres
        ----------
        direction : str
            Direction dans laquelle le joueur souhaite se déplacer.

        Retourne
        -------
        bool
            True si le joueur a été déplacé avec succès, False si le déplacement est impossible.
        """
        if DEBUG: print(f"DEBUG: {self.name} tente de se déplacer vers {direction} depuis {self.current_room.name}")
        next_room = self.current_room.exits.get(direction)

        if next_room is None:
            if DEBUG: print(f"DEBUG: Pas de sortie {direction} disponible")
            print("\nAucune porte dans cette direction !\n")
            return False
        # Empêcher l'accès au cockpit depuis d'autres salles
        if next_room.name == "Cockpit" and self.current_room.name != "Cockpit":
            if DEBUG: print(f"DEBUG: Accès au cockpit refusé depuis {self.current_room.name}")
            print("\nAccès refusé : personne ne peut entrer dans le cockpit.\n")
            return False

        self.history.append(self.current_room)
        self.current_room = next_room
        if DEBUG: print(f"DEBUG: {self.name} s'est déplacé vers {next_room.name}")
        print(self.current_room.get_long_description())
        print(self.get_history())
        return True

    def go_back(self):
        """
        Permet au joueur de revenir à la salle précédente.

        Retourne
        -------
        bool
            True si le joueur a pu revenir en arrière, False si l'historique est vide.
        """
        if not self.history:
            print("\nAucune salle précédente dans l'historique !\n")
            return False
        
        self.current_room = self.history.pop()
        print(self.current_room.get_long_description())
        print(self.get_history())
        return True
    
    def get_history(self):
        """
        Retourne l'historique des salles visitées par le joueur.

        Retourne
        -------
        chaine de caractères: lines
            Liste des salles visitées.
        """
        if not self.history:
            return "\nAucune salle visitée pour le moment.\n"

        lines = ["Historique des salles visitées :"]
        for room in self.history:
            lines.append(f"\t- {room.name}\n")
        return "\n".join(lines)
        
    def get_inventory(self):
        """
        Retourne l'inventaire des objets possédés par le joueur.

        Retourne
        -------
        chaine de caractères: lines
            Liste des objets dans l'inventaire.
        """
        if not self.inventory:
            return "\nL'inventaire est vide.\n"

        lines = ["Inventaire des objets :"]
        for item_name, item in self.inventory.items():
            lines.append(f"\t- {str(item)}\n")
        return "\n".join(lines)

    def award_points(self, points, reason=None):
        """Ajoute des points au joueur et affiche un court message."""
        self.score += points
        if reason:
            print(f"[+{points} pts] {reason} (Total: {self.score} pts)")
        else:
            print(f"[+{points} pts] (Total: {self.score} pts)")

    def add_found_phrase(self, item_name, phrase):
        """Enregistre que le joueur a trouvé une phrase pour un item donné."""
        s = self.item_progress.get(item_name)
        if s is None:
            s = set()
            self.item_progress[item_name] = s
        s.add(phrase)

# Fin du fichier