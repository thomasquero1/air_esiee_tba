from actor import Actor

class Character(Actor):
    """Représente un personnage dans l'univers du jeu.
    
    Attributs
    ---------
    name : str
        Nom du personnage.
    current_room : Room | None
        Salle dans laquelle se trouve actuellement le personnage.
    description : str
        Description du personnage.
    msgs : list
        Messages du personnage.
    """
    def __init__(self, name, current_room, description, msgs, can_move=True):
        super().__init__(name, current_room)
        self.description = description
        self.msgs = msgs
        self.can_move = can_move

    def __str__(self):
        return f"{self.name}: {self.description}"
    
    def move(self, directions):
        """Déplace le personnage dans une direction aléatoire parmi celles disponibles.
        
        Parameters
        ----------
        directions : list
            Liste des directions possibles où le personnage peut se déplacer.
        """
        import random
        if self.can_move and directions:
            direction = random.choice(directions)
            next_room = self.current_room.get_exit(direction)
            if next_room:
                self.current_room = next_room