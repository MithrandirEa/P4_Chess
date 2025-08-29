from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Any
from .player import Player


@dataclass
class Match:
    """Entité représentant une partie d'échecs."""

    white_player: Player
    white_player_score: float
    black_player: Player
    black_player_score: float

    def to_tuple(self) -> Tuple[List[Any], List[Any]]:
        """Retourne la représentation sous forme de tuple sérialisable."""
        return (
            [self.white_player.to_record(), self.white_player_score],
            [self.black_player.to_record(), self.black_player_score],
        )

    @staticmethod
    def from_tuple(data: Tuple[List[Any], List[Any]]) -> "Match":
        """Reconstruit une instance de Match à partir d'un tuple sérialisé."""
        p1, p2 = data
        white = Player.from_record(p1[0])
        black = Player.from_record(p2[0])
        return Match(white, p1[1], black, p2[1])
