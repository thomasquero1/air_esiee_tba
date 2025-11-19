# Define the Player class.
class Player:
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
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}
    
    def move(self, direction):
        """
        Déplace le joueur vers la salle située dans la direction spécifiée.

        Parameters
        ----------
        direction : str
            Direction dans laquelle le joueur souhaite se déplacer.

        Returns
        -------
        bool
            True si le joueur a été déplacé avec succès, False si le déplacement est impossible.
        """
        next_room = self.current_room.exits.get(direction)

        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        self.history.append(self.current_room)
        self.current_room = next_room
        print(self.current_room.get_long_description())
        print(self.get_history())
        return True

    def go_back(self):
        """
        Permet au joueur de revenir à la salle précédente.

        Returns
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

        Returns
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

        Returns
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