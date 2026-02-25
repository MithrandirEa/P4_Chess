from __future__ import annotations
from dataclasses import dataclass
from chessManager.models import Player


@dataclass
class Match:
    """Modèle représentant un match unique entre deux joueurs.

    Attributes:
        white_player (Player): Le joueur avec les pièces blanches.
        white_player_score (float): Le score du joueur blanc (0.0, 0.5 ou 1.0).
        black_player (Player): Le joueur avec les pièces noires.
        black_player_score (float): Le score du joueur noir (0.0, 0.5 ou 1.0).
    """

    white_player: Player
    white_player_score: float
    black_player: Player
    black_player_score: float

    def to_tuple(self) -> tuple[list, list]:
        """Convertit le match en un tuple de listes pour la sérialisation.

        Format: ([player1_dict, score1], [player2_dict, score2])

        Returns:
            tuple[list, list]: Le match sérialisé.
        """
        return (
            [self.white_player.to_record(), self.white_player_score],
            [self.black_player.to_record(), self.black_player_score],
        )

    @staticmethod
    def from_tuple(data: tuple[list, list], players: list[Player]) -> "Match":
        """Reconstruit un Match depuis un tuple et la liste des joueurs du tournoi.

        Tente de lier les joueurs du match aux instances existantes dans la liste `players`
        via leur nom. Si non trouvé, crée une nouvelle instance de Player (ce qui ne devrait
        idéalement pas arriver si la liste players est complète).

        Args:
            data (tuple[list, list]): Données du match (format exporté par to_tuple).
            players (list[Player]): Liste des objets Player du tournoi en cours.

        Returns:
            Match: L'instance de Match reconstituée.
        """
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
