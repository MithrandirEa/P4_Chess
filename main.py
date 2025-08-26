from controller.tournaments_control import TournamentController
from view import prompts
from controller import tournaments_control
from view.prompts import prompt_main_menu


def main():
    controller = TournamentController()

    while True:
        choice = prompt_main_menu()

        if choice == 0:
            print("Au revoir 👋")
            break

        elif choice == 1:
            print(">> Création d’un tournoi")
            # Demande les infos du tournois
            fields = prompts.prompt_tournament_fields()
            
            # Crée le tournoi via le controller
            tournament = controller.create_tournament(**fields)
            print(f"✅ Tournoi '{tournament.name}' créé.")
            
        elif choice == 2:
            print(">> Gestion d’un tournoi")

        elif choice == 3:
            print(">> Affichage des rapports")

if __name__ == "__main__":
    main()

