import json
import random

from constant import DB_LICENSED_PLAYERS, DB_TOURNAMENTS, DEFAULT_ENCODING
from chessManager.models import Tournament, Player, Match
from chessManager.controllers import save_player
from chessManager.controllers import record_current_round_results


class TournamentController:
    def __init__(self):
        self.tournaments: list[Tournament] = []
        self.load_tournaments()

    def save_tournaments(self):
        """Sauvegarde tous les tournois en JSON, avec backup de sécurité."""
        if not self.tournaments:
            print("⚠️ Aucun tournoi à sauvegarder.")
            return

        # Sauvegarde backup
        import shutil

        backup_file = f"{DB_TOURNAMENTS}.bak"
        shutil.copy(DB_TOURNAMENTS, backup_file)

        # Sauvegarde principale
        with open(DB_TOURNAMENTS, "w", encoding=DEFAULT_ENCODING) as f:
            json.dump([t.to_record() for t in self.tournaments], f, indent=4)
        print("✅ État sauvegardé")

    def load_tournaments(self):
        try:
            with open(DB_TOURNAMENTS, "r", encoding=DEFAULT_ENCODING) as f:
                data = json.load(f)
                self.tournaments = [Tournament.from_record(d) for d in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tournaments = []

    def create_tournament(
        self, name, location, start_date, end_date, number_of_rounds, description=None
    ):
        tournament = Tournament(
            name, location, start_date, end_date, number_of_rounds, description
        )
        self.tournaments.append(tournament)
        self.save_tournaments()
        return tournament

    def list_tournaments(self):
        return self.tournaments

    @save_player(DB_LICENSED_PLAYERS)
    def add_player_to_tournament(self, tournament, player_data: dict):
        player = Player.from_record(player_data)
        tournament.add_player(player)
        self.save_tournaments()
        return player

    @save_player(DB_LICENSED_PLAYERS)
    def add_players_from_json(
        self, tournament, filepath: str
    ):  # Ajout de la vérification de doublons
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            players_list = data.get("players", data)
            added_count = 0
            existing_ids = {p.national_chess_id for p in tournament.players}
            for p in players_list:
                player = Player.from_record(p)
                if player.national_chess_id not in existing_ids:
                    tournament.add_player(player)
                    existing_ids.add(player.national_chess_id)
                    added_count += 1
            self.save_tournaments()
            print(f"✅ {added_count} joueurs importés depuis {filepath}.")
            return added_count
        except Exception as e:
            print(f"⚠️ Erreur import JSON : {e}")
            return 0

    def start_tournament(self, tournament):
        """Initialise le 1er round en appariant aléatoirement les joueurs (si vide)."""

        for player in tournament.players:
            player.tournament_score_value = 0.0

        first_round = tournament.get_round(1)

        if first_round.matches:
            print("Le premier round contient déjà des matchs.")
            return

        players = tournament.players[:]
        if len(players) < 2:
            print("Pas assez de joueurs.")
            return

        random.shuffle(players)
        matches = []
        for i in range(0, len(players) - 1, 2):
            p1, p2 = players[i], players[i + 1]
            match = Match(
                white_player=p1,
                white_player_score=0.0,
                black_player=p2,
                black_player_score=0.0,
            )
            matches.append(match)

        if len(players) % 2 == 1:
            print(f"{players[-1].name} n’a pas d’adversaire ce round.")
        # Ajouter dans le Round
        for m in matches:
            first_round.add_match(m)

        tournament.current_round = first_round
        self.save_tournaments()
        print(f"✅ Premier round initialisé avec {len(matches)} matchs.")

    def save_current_round_results(self, tournament):
        """Saisie des résultats du round en cours et sauvegarde."""
        if not isinstance(tournament, Tournament):
            raise TypeError(f"Expected Tournament, got {type(tournament)}")
        record_current_round_results(tournament)
        self.save_tournaments()
