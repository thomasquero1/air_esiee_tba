# Définir la classe Room.
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
    ## Modification du constructeur pour qu'il inclus le le préfixe "dans " à la description à la ligne 30.
    def __init__(self, name, description):
        self.name = name
        self.description = "dans " + description
        self.exits = {}
        self.items = {}
        self.characters = {}
    
    def get_exit(self, direction):
        """
        Retourne la salle reliée dans une direction donnée.

        Paramètres
        ----------
        direction : str
            La direction dans laquelle le joueur souhaite se rendre (ex : "nord", "est").

        Retourne
        -------
        Room | None
            La salle reliée à cette direction, ou None si aucune sortie n'existe.
        """
        return self.exits.get(direction, None)
    
    def get_exit_string(self):
        """
        Génère une chaîne de caractères indiquant toutes les sorties possibles.

        Retourne
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

        Retourne
        -------
        str
            Texte complet décrivant la salle et ses sorties.
        """
        desc = f"\nVous êtes {self.description}\n{self.get_exit_string()}"
        if self.items:
            desc += "\nObjets ici: " + ", ".join([item.name for item in self.items])
        if self.characters:
            desc += "\nPersonnages ici: " + ", ".join([char.name for char in self.characters.values()])
        return desc

    
    def get_inventory(self):
        """
        Retourne l'inventaire des objets présents dans la salle.

        Retourne
        -------
        dict
            Dictionnaire des objets dans la salle, où les clés sont les noms des objets et les valeurs sont les objets Item.
        """
        if not self.inventory:
            return "\nLa pièce n'a aucun objet récupérable\n"

        lines = ["La pièce contient :"]
        for item_name, item in self.inventory.items():
            lines.append(f"\t- {str(item)}\n")
        return "\n".join(lines)