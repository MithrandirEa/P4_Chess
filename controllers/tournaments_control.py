import json
import random

from constant import DB_TOURNAMENTS, DEFAULT_ENCODING

from models import Tournament, Player, Round, Match


class TournamentController:
    def __init__(self):
        self.tournaments: list[Tournament] = []
        self.load_tournaments()

    def save_tournaments(self):
        with open(DB_TOURNAMENTS, "w", encoding=DEFAULT_ENCODING) as f:
            json.dump([t.to_record() for t in self.tournaments], f, indent=4)

    def load_tournaments(self):
        try:
            with open(DB_TOURNAMENTS, "r", encoding=DEFAULT_ENCODING) as f:
                data = json.load(f)
                self.tournaments = [Tournament.from_record(d) for d in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tournaments = []

    def create_tournament(self, name, location, start_date, end_date, number_of_rounds, description=None):
        tournament = Tournament(name, location, start_date, end_date, number_of_rounds, description)
        self.tournaments.append(tournament)
        self.save_tournaments()
        return tournament

    def list_tournaments(self):
        return self.tournaments

    def add_player_to_tournament(self, tournament, player_data: dict):
        player = Player.from_record(player_data)
        tournament.add_player(player)
        self.save_tournaments()
        return player

    def add_players_from_json(self, tournament, filepath: str): # Ajout de la vérification d'existance
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
        """Create the first round with random pairing of players."""
        if tournament.rounds and any(
            all(m.white_player_score != 0 or m.black_player_score != 0 for m in r.matches)
            for r in tournament.rounds
        ):
            print("⚠️ Le tournoi a déjà commencé.")
            return

        players = tournament.players[:]
        if len(players) < 2:
            print("⚠️ Pas assez de joueurs pour démarrer un round.")
            return

        random.shuffle(players)
        matches = []
        for i in range(0, len(players) - 1, 2):
            white = players[i]
            black = players[i + 1]
            match = Match(
                white_player=white,
                white_player_score=0,
                black_player=black,
                black_player_score=0
            )
            matches.append(match)
        # Si nombre impair, le dernier joueur ne joue pas ce round
        if len(players) % 2 == 1:
            print(f"⚠️ Le joueur {players[-1].name} n'a pas d'adversaire ce round.")

        round1 = Round(
            round_number=1,
            matches=matches
        )
        tournament.rounds.append(round1)
        tournament.current_round = round1
        print("✅ Premier round créé et joueurs appariés.")

    def write_current_round_result(self, tournament):
        round = tournament.get_current_round()
        if not round:
            print("⚠️ Aucun round en cours.")
            return
        print(f"Round en cours : {round.name}")
        for match in round.matches:
            print(f"Match {match.match_id} : {match.white_id} vs {match.black_id} (résultat actuel : {match.result})")
            result = input("Résultat (1 (win), 0 (lose), 0.5 (draw) ou vide pour laisser inchangé) : ").strip()
            if result:
                controllers.set_match_result(tournament, round, match, result)
        print("✅ Résultats mis à jour.")