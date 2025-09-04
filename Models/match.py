from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Any
from models import Player


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
            [self.white_player, self.white_player_score],
            [self.black_player, self.black_player_score],
        )

    @staticmethod
    def from_tuple(data: tuple[list, list]) -> "Match":
        """Reconstruit un Match depuis un tuple de deux listes [nom, score]."""
        p1, p2 = data
        return Match(
            white_player=p1[0],  # nom du joueur (str)
            white_player_score=p1[1],  # score (float)
            black_player=p2[0],
            black_player_score=p2[1],
        )
