from typing import Callable, Optional


class Menu:
    """Classe utilitaire pour créer et gérer des menus en ligne de commande.

    Attributes:
        title (str): Le titre du menu affiché en haut.
        options (dict): Dictionnaire mappant un numéro à un tuple (libellé, action).
    """

    def __init__(self, title: str):
        """Initialise un nouveau menu.

        Args:
            title (str): Le titre du menu.
        """
        self.title = title
        self.options = {}

    def add_option(self, number: int, label: str, action: Optional[Callable]):
        """Ajoute une option au menu.

        Args:
            number (int): Le numéro de l'option (touche à saisir).
            label (str): Le texte descriptif de l'option.
            action (Optional[Callable]): La fonction à exécuter si cette option est choisie.
                                       Si None, l'option sert à quitter la boucle du menu.
        """
        self.options[number] = (label, action)

    def display(self):
        """Affiche le menu et ses options triées par numéro."""
        print(f"\n=== {self.title} ===")
        for num, (label, _) in sorted(self.options.items()):
            if num == 0:  # Convention souvent utilisée pour Quitter/Retour
                continue
            print(f"{num}. {label}")

        # Afficher l'option 0 (souvent Quitter) à la fin si elle existe
        if 0 in self.options:
            print(f"0. {self.options[0][0]}")

    def run(self):
        """Lance la boucle principale du menu.

        Affiche le menu, attend une entrée utilisateur, et exécute l'action correspondante.
        La boucle s'arrête si l'action est None (convention pour Quitter/Retour).
        """
        while True:
            self.display()
            try:
                user_input = input("Votre choix : ").strip()
                if not user_input:
                    continue
                choice = int(user_input)
                if choice in self.options:
                    _, action = self.options[choice]
                    if action is None:  # Quitter ou Retour
                        break
                    action()
                else:
                    print("⚠️ Choix invalide.")
            except ValueError:
                print("⚠️ Entrée invalide.")
