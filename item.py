# Define the Item Class.

class Item:
    """
    Modélise un objet manipulable dans le jeu.

    Chaque objet possède un nom, une description et un poids.

    Attributs
    ---------
    name : str
        Nom de l'objet.
    description : str
        Description narrative de l'objet.
    weight : float | int
        Poids de l'objet (en kg).

    Méthodes
    --------
    __init__(name, description, weight)
        Initialise un nouvel objet avec nom, description et poids.
    __str__() -> str
        Retourne une représentation textuelle de l'objet.
    """

    def __init__(self, name, description, weight):
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        return f"{self.name} : {self.description} ({self.weight} kg)"
        