# Définir la classe Inventory.

class Inventory:
    """
    Modélise l'inventaire du joueur.

    L'inventaire permet de stocker et de gérer les objets que le joueur collecte au cours du jeu.

    Attributs
    ---------
    items : dict
        Dictionnaire des objets dans l'inventaire. Les clés sont les noms des objets et les valeurs sont les objets Item associés.

    Méthodes
    --------
    add_item(item: Item) -> None
        Ajoute un objet à l'inventaire.
    remove_item(item_name: str) -> Item | None
        Retire un objet de l'inventaire par son nom et le retourne, ou None s'il n'existe pas.
    list_items() -> str
        Retourne une chaîne listant tous les objets présents dans l'inventaire.
    """

    def __init__(self):
        self.items = {}
    
    def add_item(self, item):
        self.items[item.name] = item
    
    def remove_item(self, item_name):
        return self.items.pop(item_name, None)
    
    def list_items(self):
        if not self.items:
            return ""
        item_list = ""
        for item in self.items.values():
            item_list += f"- {item}\n"
        return item_list

# Fin du fichier