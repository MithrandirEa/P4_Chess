class Menu:
    def __init__(self, title: str):
        self.title = title
        self.options = {}

    def add_option(self, number: int, label: str, action):
        self.options[number] = (label, action)

    def display(self):
        print(f"\n=== {self.title} ===")
        for num, (label, _) in sorted(self.options.items()):
            print(f"{num}. {label}")

    def run(self):
        while True:
            self.display()
            try:
                choice = int(input("Votre choix : ").strip())
                if choice in self.options:
                    label, action = self.options[choice]
                    if action is None:  # Quitter ou Retour
                        break
                    action()
                else:
                    print("⚠️ Choix invalide.")
            except ValueError:
                print("⚠️ Entrée invalide.")
