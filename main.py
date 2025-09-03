from controllers.tournaments_control import TournamentController
from views.menu import Menu
from views.tournament_view import TournamentView
from views.player_view import PlayerView

def manage_tournament(controller: TournamentController): # Fonction de gestion des tournois
    tournaments = controller.list_tournaments()
    if not tournaments:
        print("⚠️ Aucun tournoi disponible.")
        return

    # Sélection d’un tournoi
    print("\n=== Sélectionner un tournoi ===")
    for idx, t in enumerate(tournaments, start=1):
        print(f"{idx}. {t.name} ({t.start_date} → {t.end_date})")
    idx = int(input("Choix : ").strip()) - 1
    if not (0 <= idx < len(tournaments)):
        return
    tournament = tournaments[idx]

    # Sous-menu gestion 
    manage_menu = Menu(f"Gérer le tournoi {tournament.name}")
    manage_menu.add_option(1, "Ajouter un joueur", lambda: controller.add_player_to_tournament(
        tournament, PlayerView().ask_player_fields()
    ))
    manage_menu.add_option(2, "Importer joueurs JSON", lambda: controller.add_players_from_json(
        tournament, "Data/FakePlayers.json" 
    )) #FIXME: Pour présentation: prévoir la saisie ou sélection dans navigateur 
    
    manage_menu.add_option(3, "Afficher les joueurs", lambda: [print(p.name) for p in tournament.players])
    manage_menu.add_option(4, "Initier un tournois", lambda: controller.start_tournament(tournament)) #TODO: Ajouter la logique d'initialisation tournois
    manage_menu.add_option(5, "Saisir les résultats du round en cours", lambda: controller.DEFINIR_NOM_METHODE(tournament))#TODO: Ajouter l'option "Saisir les score". Affiche tous les matchs du round en cours (identifier le round en cours?) et permet la saisie du score de chaque joueur du match.
    manage_menu.add_option(0, "Retour", None)
    manage_menu.run()

#TODO: Ajout d'une fonction "display_report" sur le modèle du menu de gestion des tournois

def main():
    controller = TournamentController()
    tview = TournamentView()

    main_menu = Menu("Menu Principal")
    main_menu.add_option(1, "Créer un tournoi", lambda: controller.create_tournament(**tview.ask_tournament_fields()))
    main_menu.add_option(2, "Gérer un tournoi", lambda: manage_tournament(controller))
    main_menu.add_option(3, "Afficher les rapports", lambda: print("⚠️ À implémenter")) #TODO: Implémenter l'affichage (display.py) et la logique des rapports (controllers/reports_control.py)
    main_menu.add_option(0, "Quitter", None)

    main_menu.run()


if __name__ == "__main__":
    main()
