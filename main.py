from controller.tournaments_control import TournamentController
from view import prompts
from controller import tournaments_control
from view.prompts import (
    prompt_main_menu,
    prompt_tournament_fields,
    prompt_tournament_management_menu,
    prompt_select_tournament,
)  


def main():
    controller = TournamentController()

    while True:
        choice = prompt_main_menu()

        if choice == 0:
            print("Au revoir 👋")
            break

        elif choice == 1:
            # Demande les infos du tournois
            fields = prompts.prompt_tournament_fields()
            
            # Crée le tournoi via le controller
            tournament = controller.create_tournament(**fields)
            print(f"✅ Tournoi '{tournament.name}' créé.")
                    
        elif choice == 2:
            # Liste d'abord les tournois et demande d'en choisir un
            idx = prompts.prompt_select_tournament(controller.list_tournaments())
            if idx == -1:
                continue # retour au menu principal

                        # Ensuite appelle le sous-menu de gestion des tournois
            sub_choice = prompt_tournament_management_menu()
            if sub_choice == 1:
                print(">> Ajouter des joueurs au tournoi (à implémenter)")
            elif sub_choice == 2:
                print(">> Démarrer le tournoi (à implémenter)")
            elif sub_choice == 3:
                print(">> Enregistrer les résultats (à implémenter)")
            elif sub_choice == 4:
                print(">> Afficher le classement (à implémenter)")
            elif sub_choice == 0:
                print("Retour au menu principal")
                
            

        elif choice == 3:
            print(">> Affichage des rapports")

if __name__ == "__main__":
    main()

