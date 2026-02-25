from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Player:
    """Modèle représentant un joueur d'échecs.

    Cette classe contient les informations personnelles du joueur ainsi que son score
    dans le tournoi actuel.

    Attributes:
        name (str): Le nom complet du joueur.
        birthdate (str): La date de naissance au format JJ/MM/AAAA.
        national_chess_id (str): L'identifiant national d'échecs (ex: AB12345).
        address (Optional[str]): L'adresse postale ou électronique du joueur.
        tournament_score_value (float): Le score actuel du joueur dans le tournoi (défaut à 0.0).
    """

    name: str
    birthdate: str
    national_chess_id: str
    address: Optional[str] = None
    tournament_score_value: float = 0.0

    def to_record(self) -> Dict[str, Any]:
        """Convertit l'instance du joueur en dictionnaire pour la sérialisation.

        Returns:
            Dict[str, Any]: Un dictionnaire contenant les attributs du joueur.
        """
        return {
            "name": self.name,
            "birthdate": self.birthdate,
            "national_chess_id": self.national_chess_id,
            "address": self.address,
            "tournament_score_value": self.tournament_score_value,
        }

    @staticmethod
    def from_record(record: Dict[str, Any]) -> "Player":
        """Crée une instance de Player à partir d'un dictionnaire.

        Args:
            record (Dict[str, Any]): Le dictionnaire contenant les données du joueur.

        Returns:
            Player: Une nouvelle instance de Player initialisée avec les données fournies.
        """
        return Player(
            name=record.get("name", ""),
            birthdate=record.get("birthdate", ""),
            national_chess_id=record.get("national_chess_id", ""),
            address=record.get("address", None),
            tournament_score_value=record.get("tournament_score_value", 0.0),
        )

    def __str__(self) -> str:
        """Retourne une représentation textuelle du joueur (son nom).

        Returns:
            str: Le nom du joueur.
        """
        return self.name
