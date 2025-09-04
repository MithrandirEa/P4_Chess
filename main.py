from controllers.tournaments_control import TournamentController
from views.menu import Menu
from views.tournament_view import TournamentView
from views.player_view import PlayerView
from views.display import display_tournament_list

def manage_tournament(
    controller: TournamentController,
):  # Fonction de gestion des tournois
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
    manage_menu.add_option(
        1,
        "Ajouter un joueur",
        lambda: controller.add_player_to_tournament(
            tournament, PlayerView().ask_player_fields()
        ),
    )
    manage_menu.add_option(
        2,
        "Importer joueurs JSON",
        lambda: controller.add_players_from_json(tournament, "Data/FakePlayers.json"),
    )  #TODO: Prévoir saisie ou sélection dans navigateur

    manage_menu.add_option(
        3, "Afficher les joueurs", lambda: [print(p.name) for p in tournament.players]
    )

    manage_menu.add_option(
        4, "Initier un tournois", lambda: controller.start_tournament(tournament)
    )
    manage_menu.add_option(
        5,
        "Saisir les résultats du round en cours",
        lambda: controller.record_current_round_results(tournament),
    )
    manage_menu.add_option(0, "Retour", None)
    manage_menu.run()


#TODO: Compléter la fonction
def display_report():
    reports_menu = Menu("Afficher les rapports")
    reports_menu.add_option(
        1,
        "Liste des joueurs de la FFE (ordre alphabétique)",
        lambda: print("⚠️ À implémenter"),
    )
    reports_menu.add_option(
        2, "Liste de tous les tournois", lambda: display_tournament_list()  )
    reports_menu.add_option(
        3,
        "Liste des joueurs d'un tournois (ordre alphabétique)",
        lambda: print("⚠️ À implémenter"),
    )
    reports_menu.add_option(
        4,
        "Liste des rounds et matchs d'un tournois",
        lambda: lambda: print("⚠️ À implémenter"),
    )
    reports_menu.add_option(0, "Retour", None)
    reports_menu.run()


def main():
    controller = TournamentController()
    tview = TournamentView()

    main_menu = Menu("Menu Principal")
    main_menu.add_option(
        1,
        "Créer un tournoi",
        lambda: controller.create_tournament(**tview.ask_tournament_fields()),
    )
    main_menu.add_option(2, "Gérer un tournoi", lambda: manage_tournament(controller))
    main_menu.add_option(3, "Afficher les rapports", lambda: display_report())
    # TODO: Ajouter l'option pour afficher les resultats du tournois. cf. display.py. Se renseigner sur l'affichage de tableau en CLI
    main_menu.add_option(0, "Quitter", None)

    main_menu.run()


if __name__ == "__main__":
    main()
