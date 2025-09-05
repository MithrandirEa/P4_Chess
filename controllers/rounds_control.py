
# TODO: Ajouter une logique pour déclencher automatiquement à la clôture d'un round le système d'appairage général(Swiss system) pour les rounds suivants.


    
def record_current_round_results(tournament: "Tournament"):
    """Saisie des résultats du round en cours."""

    current_round = tournament.get_current_round()
    if not current_round:
        print("⚠️ Aucun round en cours.")
        return

    print(f"\n=== Résultats du Round {current_round.round_number} ===")
    if not current_round.matches:
        print("⚠️ Aucun match à saisir dans ce round.")
        return

    for idx, match in enumerate(current_round.matches, start=1):
        print(f"Match {idx}: {match.white_player} vs {match.black_player}")

        # Saisie seulement pour les blancs
        score_white = ask_score(f"Score {match.white_player} (0, 0.5, 1): ")
        score_black = 1 - score_white if score_white in (0, 1) else score_white

        # Mise à jour du match
        match.white_player_score = score_white
        match.black_player_score = score_black

        # Mise à jour des scores cumulés du tournoi
        for p in tournament.players:
            if p.national_chess_id == match.white_player.national_chess_id:
                p.tournament_score_value += score_white
            if p.national_chess_id == match.black_player.national_chess_id:
                p.tournament_score_value += score_black


    # ✅ Clôture du round uniquement si tous les scores sont valides
    all_matches_valid = all(
        m.white_player_score is not None and m.black_player_score is not None
        and m.white_player_score + m.black_player_score == 1
        for m in current_round.matches
    )

    if all_matches_valid:
        current_round.end_round()
        print(f"✅ Round {current_round.round_number} clôturé automatiquement.")
    else:
        print(f"⚠️ Round {current_round.round_number} non clôturé (scores incomplets ou invalides).")


def ask_score(prompt: str) -> float:
    """Demande et valide un score (0, 0.5 ou 1)."""
    while True:
        try:
            score = float(input(prompt).strip())
            if score in (0.0, 0.5, 1.0):
                return score
            else:
                print("⚠️ Score invalide. Les valeurs autorisées sont : 0, 0.5 ou 1.")
        except ValueError:
            print("⚠️ Entrée invalide. Veuillez entrer 0, 0.5 ou 1.")

