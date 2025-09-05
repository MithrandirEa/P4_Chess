from typing import List, Optional
from models import Tournament, Player, Match

def update_player_scores(tournament, match, score_white, score_black):
    for p in tournament.players:
        if p.national_chess_id == match.white_player.national_chess_id:
            p.tournament_score_value += score_white
        if p.national_chess_id == match.black_player.national_chess_id:
            p.tournament_score_value += score_black

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

        update_player_scores(tournament, match, score_white, score_black)

    # ✅ Clôture du round uniquement si tous les scores sont valides
    all_matches_valid = all(
        m.white_player_score is not None and m.black_player_score is not None
        for m in current_round.matches
    )
    if all_matches_valid:
        current_round.end_round()
        print("✅ Round clôturé.")
        prepare_next_round(tournament)
    else:
        print(
            f"⚠️ Round {current_round.round_number} non clôturé (scores incomplets ou invalides)."
        )

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

def _already_played(t, a, b) -> bool:
    for rnd in t.rounds:                                  # rounds existants
        for m in rnd.matches:                             # chaque match
            if (m.white_player is a and m.black_player is b) \
               or (m.white_player is b and m.black_player is a):
                return True
    return False


def prepare_next_round(t: Tournament) -> Optional[object]:
    """Crée les matchs du prochain round non clôturé."""
    nxt = t.get_current_round()  # premier round sans end_datetime
    if nxt is None:
        print("Tournoi terminé.")
        return None
    if nxt.matches:              # déjà initialisé
        print(f"Round {nxt.round_number} déjà initialisé.")
        return nxt

    players: List[Player] = sorted(
        t.players, key=lambda p: (-p.tournament_score_value, p.name)
    )

    # Bye si impair
    if len(players) % 2 == 1:
        bye = players.pop()
        bye.tournament_score_value += 1.0
        print(f"Bye pour {bye.name} (+1.0)")

    i = 0
    while i < len(players):
        a, b = players[i], players[i + 1]
        # micro-swap si déjà joués
        if _already_played(t, a, b) and i + 2 < len(players):
            c = players[i + 2]
            if not _already_played(t, a, c):
                players[i + 1], players[i + 2] = players[i + 2], players[i + 1]
                b = players[i + 1]
            elif not _already_played(t, b, c):
                players[i], players[i + 2] = players[i + 2], players[i]
                a = players[i]
        nxt.add_match(Match(
            white_player=a, white_player_score=0.0,
            black_player=b, black_player_score=0.0
        ))
        i += 2

    print(f"Round {nxt.round_number} initialisé avec {len(nxt.matches)} matchs.")
    return nxt
