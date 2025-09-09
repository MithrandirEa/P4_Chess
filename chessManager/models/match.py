from __future__ import annotations
from dataclasses import dataclass
from chessManager.models import Player


@dataclass
class Match:
    white_player: Player
    white_player_score: float
    black_player: Player
    black_player_score: float

    def to_tuple(self):
        return (
            [self.white_player.to_record(), self.white_player_score],
            [self.black_player.to_record(), self.black_player_score],
        )

    @staticmethod
    def from_tuple(data: tuple[list, list], players: list[Player]) -> "Match":
        """Reconstruit un Match depuis un tuple + la liste des joueurs du tournoi."""
        data = tuple(data)
        p1, p2 = data

        # Retrouver l'objet Player existant ou le recréer
        white = next(
            (p for p in players if p.name == p1[0]["name"]), Player.from_record(p1[0])
        )
        black = next(
            (p for p in players if p.name == p2[0]["name"]), Player.from_record(p2[0])
        )

        return Match(
            white_player=white,
            white_player_score=p1[1],
            black_player=black,
            black_player_score=p2[1],
        )
