from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import uuid

from .match import Match


@dataclass
class Round:
    """Un tour (ronde) d’un tournoi. Contient une liste de matches."""

    name: str  # ex. "Ronde 1"
    number: Optional[int] = None
    date: Optional[str] = None  # ex. "2025-08-19"
    matches: List[Match] = field(default_factory=list)
    round_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_record(self) -> Dict[str, Any]:
        return {
            "round_id": self.round_id,
            "name": self.name,
            "number": self.number,
            "date": self.date,
            "matches": [m.to_record() for m in self.matches],
        }

    @staticmethod
    def from_record(rec: Dict[str, Any]) -> "Round":
        return Round(
            name=rec.get("name", ""),
            number=rec.get("number"),
            date=rec.get("date"),
            matches=[
                Match.from_record(m)
                for m in rec.get("matches", [])
                if isinstance(m, dict)
            ],
            round_id=rec.get("round_id", str(uuid.uuid4())),
        )
