from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from chessManager.models import Match, Player


@dataclass
class Round:
    """Modèle représentant une ronde dans un tournoi d'échecs.

    Contient la liste des matchs, ainsi que les horodatages de début et de fin.

    Attributes:
        round_number (int): Le numéro de la ronde.
        matches (List[Match]): Liste des matchs prévus ou joués.
        start_datetime (datetime): Date et heure de début (défaut: maintenant).
        end_datetime (Optional[datetime]): Date et heure de fin (None tant que non terminé).
    """

    round_number: int
    matches: List[Match] = field(default_factory=list)
    start_datetime: datetime = field(default_factory=datetime.now)
    end_datetime: Optional[datetime] = None

    def add_match(self, match: Match):
        """Ajoute un match à la ronde.

        Args:
            match (Match): Le match à ajouter.
        """
        self.matches.append(match)

    def end_round(self):
        """Clôture la ronde en enregistrant la date et l'heure actuelles."""
        self.end_datetime = datetime.now()

    def to_record(self) -> dict:
        """Convertit la ronde et ses matchs en dictionnaire sérialisable.

        Returns:
            dict: Dictionnaire représentant la ronde.
        """
        return {
            "round_number": self.round_number,
            "start_datetime": self.start_datetime.isoformat(),
            "end_datetime": (
                self.end_datetime.isoformat() if self.end_datetime else None
            ),
            "matches": [m.to_tuple() for m in self.matches],
        }

    @staticmethod
    def from_record(data: dict, players: list[Player]) -> "Round":
        """Reconstruit une instance de Round depuis un dictionnaire.

        Args:
            data (dict): Données de la ronde.
            players (list[Player]): Liste des joueurs du tournoi (pour lier les matchs).

        Returns:
            Round: L'instance de Round reconstruite.
        """
        matches = [Match.from_tuple(tuple(t), players) for t in data["matches"]]
        start_dt = datetime.fromisoformat(data["start_datetime"])
        end_dt = (
            datetime.fromisoformat(data["end_datetime"])
            if data["end_datetime"]
            else None
        )
        return Round(
            round_number=data["round_number"],
            matches=matches,
            start_datetime=start_dt,
            end_datetime=end_dt,
        )
