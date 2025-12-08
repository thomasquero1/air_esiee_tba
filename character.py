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
    def __init__(self, name, current_room, description, msgs):
        super().__init__(name, current_room)
        self.description = description
        self.msgs = msgs

    def __str__(self):
        return f"{self.name}: {self.description}"