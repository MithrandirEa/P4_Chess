from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from chessManager.models import Player
from chessManager.models import Round


@dataclass
class Tournament:
    """Modèle représentant un tournoi d'échecs.

    Gère les informations du tournoi, la liste des joueurs inscrits et les rondes.

    Attributes:
        name (str): Le nom du tournoi.
        location (str): Le lieu où se déroule le tournoi.
        start_date (str): La date de début (format JJ/MM/AAAA).
        end_date (str): La date de fin (format JJ/MM/AAAA).
        number_of_rounds (int): Le nombre de tours prévus (défaut à 4).
        description (Optional[str]): Description ou remarques sur le tournoi.
        players (List[Player]): Liste des joueurs inscrits.
        rounds (List[Round]): Liste des rondes du tournoi.
        current_round (Optional[Round]): La ronde actuellement en cours.
    """

    name: str
    location: str
    start_date: str
    end_date: str
    number_of_rounds: int
    description: Optional[str] = None

    players: List[Player] = field(default_factory=list)
    rounds: List[Round] = field(default_factory=list)
    current_round: Optional[Round] = None

    def __post_init__(self):
        """Initialise les rondes après la création de l'instance.

        Convertit number_of_rounds en int si nécessaire et prépare la liste
        des rondes si elle est vide.
        """
        self.number_of_rounds = int(self.number_of_rounds)  # Force la conversion en int
        if (
            not self.rounds
        ):  # éviter de recréer les rounds lors du chargement depuis JSON
            # Import local pour éviter les cycles si nécessaire,
            # bien que Round soit déjà importé en haut.
            from chessManager.models import Round
            self.rounds = [Round(name=f"Round {i + 1}") for i in range(self.number_of_rounds)]

    def add_player(self, player: Player):
        """Ajoute un joueur à la liste des participants.

        Args:
            player (Player): Le joueur à ajouter.
        """
        self.players.append(player)

    def player_list(self) -> List[Player]:
        """Retourne la liste des joueurs du tournoi.

        Returns:
            List[Player]: La liste des participants.
        """
        return self.players

    def get_round(self, number: int) -> Optional[Round]:
        """Récupère une ronde spécifique par son numéro.

        Args:
            number (int): Le numéro de la ronde (1-indexé).

        Returns:
            Optional[Round]: L'objet Round correspondant ou None si invalide.

        Raises:
            ValueError: Si le numéro de round est hors limites.
        """
        if 1 <= number <= self.number_of_rounds:
            return self.rounds[number - 1]
        raise ValueError(f"Numéro de round invalide : {number}")

    def get_current_round(self) -> Optional[Round]:
        """Identifie et retourne la ronde active.

        Une ronde est considérée comme active si elle n'a pas de date de fin.

        Returns:
            Optional[Round]: La première ronde non terminée trouvée, ou None.
        """
        for rnd in self.rounds:
            if rnd.end_datetime is None:
                self.current_round = rnd
                return rnd
        return None

    def is_finished(self) -> bool:
        """Vérifie si le tournoi est terminé.

        Returns:
            bool: True si toutes les rondes sont terminées, False sinon.
        """
        # Note: Supposant que le nombre de rounds correspond à la longueur de la liste
        if len(self.rounds) < self.number_of_rounds:
            return False
        return all(r.end_datetime is not None for r in self.rounds)

    # Ajout des méthodes de sérialisation
    def to_record(self) -> Dict[str, Any]:
        """Convertit le tournoi en dictionnaire sérialisable en JSON.

        Returns:
            Dict[str, Any]: Représentation dictionnaire du tournoi.
        """
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "description": self.description,
            "players": [p.to_record() for p in self.players],
            "rounds": [r.to_record() for r in self.rounds],
        }

    @staticmethod
    def from_record(data: Dict[str, Any]) -> Tournament:
        """Reconstruit une instance de Tournament à partir d'un dictionnaire.

        Args:
            data (Dict[str, Any]): Données du tournoi.

        Returns:
            Tournament: L'instance reconstruite.
        """
        tournament = Tournament(
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            number_of_rounds=data["number_of_rounds"],
            description=data.get("description"),
        )
        tournament.players = [Player.from_record(p) for p in data.get("players", [])]

        # Reconstruction des rondes avec les joueurs associés
        # Nécessite que Round.from_record gère correctement le lien avec les joueurs existants
        tournament.rounds = [
            Round.from_record(r, tournament.players) for r in data.get("rounds", [])
        ]
        return tournament
