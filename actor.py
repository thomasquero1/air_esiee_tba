class Actor:
    """Classe mère représentant un acteur dans le jeu.
    
    Attributs
    ---------
    name : str
        Nom de l'acteur.
    current_room : Room | None
        Salle dans laquelle se trouve actuellement l'acteur.
    """
    def __init__(self, name, current_room):
        self.name = name
        self.current_room = current_room
        