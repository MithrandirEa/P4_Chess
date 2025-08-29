# main.py
from controller.tournaments_control import TournamentController
from view.prompt_model import Menu
from view.tournament_view import TournamentView

def main():
    controller = TournamentController()
    view = TournamentView()

    # Création du menu principal
    main_menu = Menu("Menu Principal")
    main_menu.add_option(1, "Créer un tournoi", lambda: controller.create_tournament(**view.ask_tournament_fields()))
    main_menu.add_option(2, "Gérer un tournoi", lambda: print("⚠️ À implémenter"))
    main_menu.add_option(3, "Afficher les rapports", lambda: print("⚠️ À implémenter"))
    main_menu.add_option(0, "Quitter", None)

    main_menu.run()

if __name__ == "__main__":
    main()
