# actions.py
from item import Item

MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:
    """Fonctions de callback pour commandes."""

    @staticmethod
    def go(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False
        return game.player.move(list_of_words[1])

    @staticmethod
    def back(game, list_of_words, number_of_parameters):
        if len(list_of_words) != 1:
            print(MSG0.format(command_word="back"))
            return False
        return game.player.undo()

    @staticmethod
    def look(game, list_of_words, number_of_parameters):
        print(game.player.current_room.get_long_description())
        return True

    @staticmethod
    def take(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False
        item_name = list_of_words[1]
        room = game.player.current_room
        for item in room.items:
            if item.name.lower() == item_name.lower():
                game.player.inventory.append(item)
                room.items.remove(item)
                print(f"Vous prenez {item.name}.")
                return True
        print(f"Aucun objet nommé {item_name} ici.")
        return False

    @staticmethod
    def use(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False
        item_name = list_of_words[1]
        for item in game.player.inventory:
            if item.name.lower() == item_name.lower():
                item.use()
                return True
        print(f"Vous ne possédez aucun objet nommé {item_name}.")
        return False

    @staticmethod
    def inventory(game, list_of_words, number_of_parameters):
        if game.player.inventory:
            print("Votre inventaire: " + ", ".join([i.name for i in game.player.inventory]))
        else:
            print("Inventaire vide.")
        return True

    @staticmethod
    def help(game, list_of_words, number_of_parameters):
        print("\nCommandes disponibles:")
        for cmd in game.commands.values():
            print(f"- {cmd.command_word} {cmd.help_string}")
        return True

    @staticmethod
    def quit(game, list_of_words, number_of_parameters):
        print(f"\nMerci {game.player.name} d'avoir joué. Au revoir.")
        game.finished = True
        return True

    @staticmethod
    def history(game, list_of_words, number_of_parameters):
        """
        Affiche l'historique des salles visitées par le joueur.


        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.


        Returns:
            bool: True si la commande a été exécutée avec succès, False sinon.


        Examples:


        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> history(game, ["history"], 0)
        True
        >>> history(game, ["history", "N"], 0)
        False
        >>> history(game, ["history", "N", "E"], 0)
        False


        """


        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False


        print(game.player.get_history())
        return True

