# Define the Room class.
class Room:
    """
    Modélise une salle du jeu.

    Chaque salle possède un nom, une description narrative et des liaisons vers d'autres salles.

    Attributs
    ---------
    name : str
        Nom de la salle.
    description : str
        Texte décrivant la salle.
    exits : dict
        Dictionnaire des sorties disponibles depuis cette salle. Les clés correspondent aux directions
        et les valeurs sont les objets Room associés.

    Méthodes
    --------
    get_exit(direction) -> Room | None
        Renvoie la salle correspondant à la direction spécifiée ou None si elle n'existe pas.
    get_exit_string() -> str
        Fournit une chaîne listant toutes les sorties accessibles depuis la salle.
    get_long_description() -> str
        Produit une description complète de la salle incluant sa description et ses sorties.
    """

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
    
    def get_exit(self, direction):
        """
        Retourne la salle reliée dans une direction donnée.

        Parameters
        ----------
        direction : str
            La direction dans laquelle le joueur souhaite se rendre (ex : "nord", "est").

        Returns
        -------
        Room | None
            La salle reliée à cette direction, ou None si aucune sortie n'existe.
        """
        return self.exits.get(direction, None)
    
    def get_exit_string(self):
        """
        Génère une chaîne de caractères indiquant toutes les sorties possibles.

        Returns
        -------
        str
            Chaîne sous la forme "Sorties: nord, sud, est..." ou "Sorties:" si aucune sortie n'est définie.
        """
        exit_string = "Sorties: "
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    def get_long_description(self):
        """
        Fournit une description complète de la salle en combinant sa description et ses sorties.

        Utilise une f-string pour insérer dynamiquement la description et la liste des sorties.
        Exemple : f"Vous êtes {self.description}"

        Returns
        -------
        str
            Texte complet décrivant la salle et ses sorties.
        """
        return f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"