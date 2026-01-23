# Ce fichier contient la classe Command.

class Command:
    """
    Cette classe représente une commande. Une commande est composée d'un mot-clé,
    d'une chaîne d'aide, d'une action et d'un nombre de paramètres.

    Attributs :
        command_word (str) : Mot-clé de la commande.
        help_string (str) : Chaîne d'aide.
        action (function) : Action à exécuter lorsque la commande est appelée.
        number_of_parameters (int) : Nombre de paramètres attendus.

    Méthodes :
        __init__(self, command_word, help_string, action, number_of_parameters) : Constructeur.
        __str__(self) : Représentation textuelle de la commande.

    Exemples :

    >>> from actions import go
    >>> command = Command("go", "Permet de se déplacer dans une direction.", go, 1)
    >>> command.command_word
    'go'
    >>> command.help_string
    'Permet de se déplacer dans une direction.'
    >>> type(command.action)
    <class 'function'>
    >>> command.number_of_parameters
    1

    """

    # Constructeur.
    def __init__(self, command_word, help_string, action, number_of_parameters):
        self.command_word = command_word
        self.help_string = help_string
        self.action = action
        self.number_of_parameters = number_of_parameters
    
    # Représentation textuelle de la commande.
    def __str__(self):
        return  self.command_word \
                + self.help_string
    