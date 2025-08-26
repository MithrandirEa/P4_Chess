from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from .match import Match


@dataclass
class Round:
    """Entité représentant une ronde dans un tournoi d'échecs."""

    round_number: int
    matches: List[Match] = field(default_factory=list)
    start_datetime: datetime = field(default_factory=datetime.now)
    end_datetime: Optional[datetime] = None

    def add_match(self, match: Match):
        """Ajoute un match au round."""
        self.matches.append(match)

    def end_round(self):
        """Marque la fin du round en enregistrant la date et l'heure de fin."""
        self.end_datetime = datetime.now()

    def to_record(self) -> dict:
        """Convertit le round et ses matches en dictionnaire sérialisable"""
        return {
            "round_number": self.round_number,
            "start_datetime": self.start_datetime.isoformat(),
            "end_datetime": self.end_datetime.isoformat() if self.end_datetime else None,
            "matches": [m.to_tuple() for m in self.matches]
        }

    @staticmethod
    def from_record(data: dict) -> "Round":
        """Reconstruit un Round depuis un dictionnaire."""
        matches = [Match.from_tuple(t) for t in data["matches"]]
        start_dt = datetime.fromisoformat(data["start_datetime"])
        end_dt = datetime.fromisoformat(data["end_datetime"]) if data["end_datetime"] else None
        return Round(round_number=data["round_number"],
                     matches=matches,
                     start_datetime=start_dt,
                     end_datetime=end_dt)
