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
        """Initialise le 1er round en appariant aléatoirement les joueurs (si vide)."""
        #TODO: Ajouter la réinitialisation à 0 de l'attribut tournament_score_value de chaque joueur.
        #TODO: Ajouter la gestion de la parité de joueurs.
        
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
            p1, p2 = players[i], players[i+1]
            match = Match(
                white_player=p1.name,
                white_player_score=0.0,
                black_player=p2.name,
                black_player_score=0.0
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
        
    def record_current_round_results(self, tournament):
        """Permet de saisir les scores des matchs du round en cours."""
        #TODO: Ajouter une demande de validation à chaque saisie
        #TODO: Ajouter la vérification que la somme des scores de chaque match est bien égale à 1 (1-0, 0-1, 0.5-0.5)
        #TODO: Ajouter la mise à jour des scores des joueurs (attribut tournament_score_value) à la méthoderecord_current_round_results
        current_round = tournament.get_current_round()
        if not current_round:
            print("⚠️ Aucun round en cours.")
            return

        print(f"\n=== Saisie des résultats du Round {current_round.round_number} ===")

        for idx, match in enumerate(current_round.matches, start=1):
            print(f"\nMatch {idx}: {match.white_player} vs {match.black_player}")

            # Saisie score joueur blanc
            while True:
                try:
                    score_white = float(input(f"Score {match.white_player} : ").strip())
                    if score_white in (0.0, 0.5, 1.0):
                        match.white_player_score = score_white
                        break
                    else:
                        print("⚠️ Score invalide. Autorisés : 0, 0.5, 1.")
                except ValueError:
                    print("⚠️ Entrez un nombre (0, 0.5, 1).")

            # Saisie score joueur noir
            while True:
                try:
                    score_black = float(input(f"Score {match.black_player} : ").strip())
                    if score_black in (0.0, 0.5, 1.0):
                        match.black_player_score = score_black
                        break
                    else:
                        print("⚠️ Score invalide. Autorisés : 0, 0.5, 1.")
                except ValueError:
                    print("⚠️ Entrez un nombre (0, 0.5, 1).")

        # Marquer le round comme terminé
        current_round.end_round()
        self.save_tournaments()
        print(f"\n✅ Résultats du Round {current_round.round_number} enregistrés.")
#TODO: Ajouter une logique pour déclencher automatiquement à la clôture d'un round le système d'appairage général(Swiss system) pour les rounds suivants.

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