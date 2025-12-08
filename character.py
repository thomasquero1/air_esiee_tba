from actor import Actor
import random
from config import DEBUG

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
            if DEBUG: print(f"DEBUG: {self.name} ne peut pas se déplacer (can_move=False)")
            return False
        
        if random.random() < 0.5:
            if DEBUG: print(f"DEBUG: {self.name} a gagné le test 50% - tentative de déplacement")
            # Obtenir les sorties disponibles
            if self.current_room.exits:
                next_room = random.choice(list(self.current_room.exits.values()))
                if next_room:
                    old_room = self.current_room.name
                    self.current_room = next_room
                    if DEBUG: print(f"DEBUG: {self.name} s'est déplacé de {old_room} vers {next_room.name}")
                    return True
        else:
            if DEBUG: print(f"DEBUG: {self.name} a échoué le test 50% - reste immobile")
        return False
    
    def next_msg(self):
        """Retourne le message suivant du personnage de manière cyclique."""
        if not self.msgs:
            return "..."
        msg = self.msgs.pop(0)
        self.msgs.append(msg)
        return msg