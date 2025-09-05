from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Any
from models import Player


@dataclass
class Match:
    white_player: Player
    white_player_score: float
    black_player: Player
    black_player_score: float

    def to_tuple(self) -> Tuple[List[Any], List[Any]]:
        return (
            [self.white_player.name, self.white_player_score],
            [self.black_player.name, self.black_player_score],
        )

    @staticmethod
    def from_tuple(data: tuple[list, list], players: list[Player]) -> "Match":
        """Reconstruit un Match depuis un tuple + la liste des joueurs du tournoi."""
        p1, p2 = data
        # retrouver les objets Player correspondants
        white = next((p for p in players if p.name == p1[0]), Player(name=p1[0], birthdate="", national_chess_id=""))
        black = next((p for p in players if p.name == p2[0]), Player(name=p2[0], birthdate="", national_chess_id=""))
        return Match(
            white_player=white,
            white_player_score=p1[1],
            black_player=black,
            black_player_score=p2[1]
        )
