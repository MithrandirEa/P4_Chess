from tabulate import tabulate


def display_tournament_rounds_list(tournament):
    """Affiche la liste des rounds d'un tournoi sous forme de tableau."""
    rounds = tournament.rounds
    if not rounds:
        print("⚠️ Aucun round dans ce tournoi.")
        return

    # Préparer les données pour tabulate
    table = []
    for idx, r in enumerate(rounds, start=1):
        table.append(
            [
                idx,
                r.round_number,
                r.start_datetime,
                r.end_datetime if r.end_datetime else "En cours",
                len(r.matches),  # nombre de matchs au lieu d'afficher l'objet brut
            ]
        )

    headers = ["#", "Round", "Début", "Fin", "Nb Matches"]
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
    display_round_match_list(rounds[-1])  # Affiche les matchs du dernier round


def display_round_match_list(rnd):
    """Affiche la liste des matchs d'un round donné sous forme de tableau.

    Args:
        rnd (Round): L'objet ronde contenant les matchs à afficher.
    """
    if not rnd.matches:
        print(f"⚠️ Aucun match pour le round {rnd.round_number}")
        return

    table = []
    # On ajoute des entêtes pour clarifier l'affichage
    headers = ["#", "Blancs", "Res Blancs", "Noirs", "Res Noirs"]

    for idx, match in enumerate(rnd.matches, start=1):
        white_name = str(match.white_player)
        black_name = str(match.black_player)

        # Gestion de l'affichage des scores (peut être None si non joué)
        w_score = match.white_player_score if match.white_player_score is not None else "-"
        b_score = match.black_player_score if match.black_player_score is not None else "-"

        table.append([idx, white_name, w_score, black_name, b_score])

    print(f"\n=== Matchs du Round {rnd.round_number} ===")
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


def display_round_detail(tournament):
    """Affiche le détail complet des rondes et des matchs d'un tournoi.

    Args:
        tournament (Tournament): Le tournoi à afficher.
    """
    if not tournament.rounds:
        print("Aucune ronde générée pour ce tournoi.")
        return

    print(f"\nDétails du tournoi : {tournament.name}")
    # display_tournament_rounds_list(tournament) # Optionnel si redondant

    for rnd in tournament.rounds:
        display_round_match_list(rnd)
