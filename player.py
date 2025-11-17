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
        
        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True
