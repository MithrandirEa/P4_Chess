from typing import List, Optional
from chessManager.models import Tournament, Player, Match


def update_player_scores(tournament: Tournament, match: Match, score_white: float, score_black: float):
    """Met à jour les scores cumulés des joueurs dans le tournoi.

    Args:
        tournament (Tournament): Le tournoi en cours.
        match (Match): Le match dont les scores doivent être appliqués.
        score_white (float): Score du joueur blanc.
        score_black (float): Score du joueur noir.
    """
    for p in tournament.players:
        if p.national_chess_id == match.white_player.national_chess_id:
            p.tournament_score_value += score_white
        if p.national_chess_id == match.black_player.national_chess_id:
            p.tournament_score_value += score_black


def record_current_round_results(tournament: Tournament):
    """Interface interactive pour la saisie des résultats du round en cours.

    Parcourt les matchs du round actif, demande à l'utilisateur de saisir les scores,
    met à jour les objets Match et Player, et vérifie si le round peut être clôturé.

    Args:
        tournament (Tournament): L'instance du tournoi en cours.
    """

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
    """Demande un score à l'utilisateur et valide qu'il soit 0, 0.5 ou 1.

    Boucle tant que l'entrée n'est pas valide.

    Args:
        prompt (str): Le message à afficher à l'utilisateur.

    Returns:
        float: Le score validé (0.0, 0.5 ou 1.0).
    """
    while True:
        try:
            score = float(input(prompt).strip())
            if score in (0.0, 0.5, 1.0):
                return score
            else:
                print("⚠️ Score invalide.Les valeurs autorisées sont : 0, 0.5 ou 1.")
        except ValueError:
            print("⚠️ Entrée invalide. Veuillez entrer 0, 0.5 ou 1.")


def _already_played(tournament: Tournament, player1: Player, player2: Player) -> bool:
    """Vérifie si deux joueurs se sont déjà affrontés dans ce tournoi.

    Args:
        tournament (Tournament): Le tournoi à vérifier.
        player1 (Player): Le premier joueur.
        player2 (Player): Le deuxième joueur.

    Returns:
        bool: True si un match (dans n'importe quel sens) a déjà eu lieu, False sinon.
    """
    for rnd in tournament.rounds:  # rounds existants
        for m in rnd.matches:  # chaque match
            if (m.white_player is player1 and m.black_player is player2) or (
                m.white_player is player2 and m.black_player is player1
            ):
                return True
    return False


def prepare_next_round(tournament: Tournament) -> Optional[object]:
    """Prépare et génère les appariements pour le prochain round.

    Utilise le système suisse simplifié :
    1. Trie les joueurs par score (puis ordre alphabetique).
    2. Apparie les joueurs proches au classement qui n'ont pas encore joué ensemble (si possible).
    3. Gère le "bye" (joueur exempté) si nombre impair, lui donnant +1 point.

    Args:
        tournament (Tournament): Le tournoi concerné.

    Returns:
        Optional[object]: Le round préparé ou None si le tournoi est fini.
    """
    nxt = tournament.get_current_round()  # premier round sans end_datetime
    if nxt is None:
        print("Tournoi terminé.")
        return None
    if nxt.matches:  # déjà initialisé
        print(f"Round {nxt.round_number} déjà initialisé.")
        return nxt

    players: List[Player] = sorted(
        tournament.players, key=lambda p: (-p.tournament_score_value, p.name)
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
        if _already_played(tournament, a, b) and i + 2 < len(players):
            c = players[i + 2]
            if not _already_played(tournament, a, c):
                players[i + 1], players[i + 2] = players[i + 2], players[i + 1]
                b = players[i + 1]
            elif not _already_played(tournament, b, c):
                players[i], players[i + 2] = players[i + 2], players[i]
                a = players[i]
        nxt.add_match(
            Match(
                white_player=a,
                white_player_score=0.0,
                black_player=b,
                black_player_score=0.0,
            )
        )
        i += 2

    print(f"Round {nxt.round_number} initialisé avec {len(nxt.matches)} matchs.")
    return nxt


def reset_last_round_and_rescore(tournament: "Tournament"):
    """Réinitialise le dernier round et redemande la saisie des scores si le tournoi n'est pas fini."""
    if tournament.is_finished():
        print("⚠️ Le tournoi est déjà terminé, impossible de modifier les résultats.")
        return

    if not tournament.rounds:
        print("⚠️ Aucun round à réinitialiser.")
        return

    last_round = tournament.rounds[-1]
    print(f"\n=== Réinitialisation du Round {last_round.round_number} ===")

    # Remettre tous les scores à zéro
    for match in last_round.matches:
        match.white_player_score = 0.0
        match.black_player_score = 0.0

    for p in tournament.players:
        p.tournament_score_value = 0.0
        # recalcul des scores à partir des rounds précédents (sauf le dernier réinitialisé)
        for rnd in tournament.rounds[:-1]:
            for m in rnd.matches:
                if p.name == m.white_player.name:
                    p.tournament_score_value += m.white_player_score
                if p.name == m.black_player.name:
                    p.tournament_score_value += m.black_player_score

    print("♻️ Round réinitialisé. Vous pouvez ressaisir les résultats.")
    record_current_round_results(tournament)
