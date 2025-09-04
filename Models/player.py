from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Player:
    """Entité représentant un joueur d'échecs."""

    name: str
    birthdate: str
    national_chess_id: str
    address: Optional[str] = None
    tournament_score_value: float = 0.0  # Score dans le tournoi en cours
    
               
    def to_record(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "birthdate": self.birthdate,
            "national_chess_id": self.national_chess_id,
            "address": self.address,
        }

    @staticmethod
    def from_record(record: Dict[str, Any]) -> "Player":
        return Player(
            name=record.get("name", ""),
            birthdate=record.get("birthdate", ""),
            national_chess_id=record.get("national_chess_id", ""),
            address=record.get("address"),
                      
        )