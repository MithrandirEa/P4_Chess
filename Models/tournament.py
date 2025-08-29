from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from .player import Player
from .chessRound import Round


@dataclass
class Tournament:
    """Entité représentant un tournoi d’échecs."""

    name: str
    location: str
    start_date: str
    end_date: str
    number_of_rounds: int
    description: Optional[str] = None

    players: List[Player] = field(default_factory=list)
    rounds: List[Round] = field(default_factory=list)
    current_round: Optional[Round] = None
    

    def __post_init__(self):
        """Crée tous les rounds dès la création du tournoi."""
        self.number_of_rounds = int(self.number_of_rounds)  # Force la conversion en int
        if (
            not self.rounds
        ):  # éviter de recréer les rounds lors du chargement depuis JSON
            self.rounds = [Round(i + 1) for i in range(self.number_of_rounds)]

    def add_player(self, player: Player):
        """Ajoute un joueur au tournoi."""
        self.players.append(player)

    def player_list(self) -> List[Player]:
        """Retourne la liste des joueurs du tournoi."""
        return self.players

    def get_round(self, number: int) -> Optional[Round]:
        """Retourne la ronde par son numéro."""
        if 1 <= number <= self.number_of_rounds:
            return self.rounds[number - 1]
        raise ValueError("Numéro de round invalide.")

    def get_current_round(self) -> Optional[Round]:
        """Retourne la ronde en cours."""
        if self.rounds and self.rounds[-1].end_datetime is None:
            return self.current_round
        return None

    def is_finished(self) -> bool:
        """Indique si le tournoi est terminé."""
        return len(self.rounds) == self.number_of_rounds and all(
            r.end_datetime is not None for r in self.rounds
        )

    # Ajout des méthodes de sérialisation
    def to_record(self) -> Dict[str, Any]:
        """Convertit le tournoi en dictionnaire sérialisable en JSON."""
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "description": self.description,
            "players": [p.to_record() for p in self.players],
            "rounds": [r.to_record() for r in self.rounds],
        }

    @staticmethod
    def from_record(data: Dict[str, Any]) -> Tournament:
        """Reconstruit un tournoi depuis un dict JSON."""
        tournament = Tournament(
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            number_of_rounds=data["number_of_rounds"],
            description=data.get("description"),
        )
        tournament.players = [Player.from_record(p) for p in data.get("players", [])]
        tournament.rounds = [Round.from_record(r) for r in data.get("rounds", [])]
        return tournament
