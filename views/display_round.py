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
    """Affiche la liste des matchs d'un round donné sous forme de tableau."""
    if not rnd.matches:
        print(f"⚠️ Aucun match pour le round {rnd.round_number}")
        return

    table = []
    for idx, match in enumerate(rnd.matches, start=1):
        table.append(
            [
                idx,
                match.white_player,  # Player → __str__ affiche juste le nom
                match.white_player_score,
                match.black_player,
                match.black_player_score,
            ]
        )

    headers = ["#", "Blancs", "Score Blancs", "Noirs", "Score Noirs"]
    print(f"\n=== Matchs du Round {rnd.round_number} ===")
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


def display_round_detail(tournament):

    display_tournament_rounds_list(tournament)

    for rnd in tournament.rounds:
        display_round_match_list(rnd)
