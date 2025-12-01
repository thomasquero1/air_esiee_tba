# item.py
import re

class Item:
    """
    Objet ou checklist dans un lieu.
    
    Attributes:
        name (str): Nom de l'objet
        description (str): Description détaillée
        weight (float): Poids de l'objet en kg
        use_count (int): Nombre de fois que l'objet a été utilisé
    """
    def __init__(self, name, description, weight = 0.0, edu_message=None):
        self.name = name
        self.description = description
        self.weight = weight
        self.use_count = 0
        # educational message to show when the checklist is fully completed
        self.edu_message = edu_message

        # extract green-highlighted phrases from the description (ANSI code \033[92m ... \033[0m)
        self.green_phrases = re.findall(r"\x1b\[92m(.*?)\x1b\[0m", description)
        # normalize phrases for matching
        self.green_phrases = [p.strip() for p in self.green_phrases if p.strip()]

    def use(self):
        """Utilise l'objet et affiche sa description détaillée."""
        self.use_count += 1
        print(f"\n[ACTION] Vous utilisez: {self.name}")
        print(f"Description: {self.description}")
        print(f"Nombre d'utilisations: {self.use_count}x\n")
    
    def __str__(self):
        count_display = f" (x{self.use_count})" if self.use_count > 0 else ""
        return f"{self.name} ({self.weight} kg): {self.description}{count_display}"