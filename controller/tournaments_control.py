"""tournaments_control.py - Contrôleur des tournois."""

from __future__ import annotations
from pathlib import Path
from typing import List, Optional

import random
import json

from utils.constant import DB_TOURNAMENTS, DEFAULT_ENCODING
from models import Tournament, Round, Match, Player


class TournamentController:
    """Contrôleur pour gérer les tournois."""

    def __init__(self, storage_path=DB_TOURNAMENTS):
        self.storage_path = Path(storage_path)
        self.tournaments: List[Tournament] = []
        self.load_tournaments()  # Charge les tournois existants au démarrage

    def create_tournament(
        self,
        name: str,
        location: str,
        start_date: str,
        end_date: str,
        number_of_rounds: int,
        description: Optional[str] = None,
    ) -> Tournament:
        """Crée un nouveau tournoi et l'ajoute à la liste des tournois."""
        tournament = Tournament(
            name=name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            number_of_rounds=number_of_rounds,
            description=description,
        )
        self.tournaments.append(tournament)
        self.save_tournaments()
        return tournament
    
    def add_player_to_tournament(self, tournament, player_data: dict):
        """Ajoute un joueur à un tournoi et sauvegarde."""
        player = Player.from_record(player_data)
        tournament.add_player(player)
        self.save_tournaments()
        return player

    def add_players_from_json(self, tournament, filepath: str):
        """Ajoute plusieurs joueurs depuis un fichier JSON."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            # si le fichier contient une clé "players", on la prend
            players_list = data.get("players", data)  

            for player_data in players_list:
                player = Player.from_record(player_data)
                tournament.add_player(player)

            self.save_tournaments()
            return len(players_list)
            
        except FileNotFoundError:
            print(f"Fichier {filepath} introuvable.")
            return 0
        except json.JSONDecodeError:
            print("Erreur : le fichier JSON est mal formé.")
            return 0


    def save_tournaments(self):
        """Sauvegarde la liste des tournois dans un fichier JSON."""
        with open(DB_TOURNAMENTS, "w", encoding=DEFAULT_ENCODING) as f:
            json.dump([t.to_record() for t in self.tournaments], f, indent=4)

    def load_tournaments(self):
        """Charge la liste des tournois depuis un fichier JSON."""
        try:
            with open(DB_TOURNAMENTS, "r", encoding=DEFAULT_ENCODING) as f:
                tournaments_data = json.load(f)
                self.tournaments = [
                    Tournament.from_record(data) for data in tournaments_data
                ]
        except FileNotFoundError:
            self.tournaments = []
        except json.JSONDecodeError:
            self.tournaments = []

    def list_tournaments(self) -> List[Tournament]:
        """Retourne la liste des tournois existants."""
        return self.tournaments


def first_round_shuffle(players: List[Player]) -> Round:
    """Mélange les joueurs et crée les matchs du premier round."""

    # Copie pour ne pas modifier la liste originale
    shuffled_players = players[:]
    random.shuffle(shuffled_players)

    # Création du Round 1
    round1 = Round(round_number=1)

    # Parcours deux par deux
    for i in range(0, len(shuffled_players), 2):
        if i + 1 < len(shuffled_players):
            p1 = shuffled_players[i]
            p2 = shuffled_players[i + 1]
            match = Match(
                white_player=p1,
                white_player_score=0.0,
                black_player=p2,
                black_player_score=0.0,
            )
            round1.add_match(match)

    return round1
