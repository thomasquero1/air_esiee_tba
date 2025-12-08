from actor import Actor
import random

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
    
    def move(self):
        """Déplace le personnage vers une salle adjacente aléatoire avec une chance sur 2.
        
        Le personnage a 50% de chance de rester immobile et 50% de chance de se déplacer
        vers une salle adjacente choisie aléatoirement.
        """
        if not self.can_move:
            return False
        
        if random.random() < 0.5:
            # Obtenir les sorties disponibles
            if self.current_room.exits:
                next_room = random.choice(list(self.current_room.exits.values()))
                if next_room:
                    self.current_room = next_room
                    return True
        return False