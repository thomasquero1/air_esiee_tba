# item.py
import re

class Item:
    """
    Objet ou checklist dans un lieu.
    
    Attributs :
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
        # message pédagogique affiché lorsque la checklist est entièrement complétée
        self.edu_message = edu_message

        # extraire les phrases surlignées en vert depuis la description (code ANSI \033[92m ... \033[0m)
        self.green_phrases = re.findall(r"\x1b\[92m(.*?)\x1b\[0m", description)
        # normaliser les phrases pour la comparaison
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

# Fin du fichier