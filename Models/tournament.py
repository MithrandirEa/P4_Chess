from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from .player import Player
from .chessRound import Round   


@dataclass
class Tournament:
    """Entité représentant un tournoi d'échecs."""

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
        """Crée tous les rounds dès la création du tournoi."""
        self.rounds = [Round(i +1) for i in range(self.number_of_rounds)] 
    
    def add_player(self, player: Player):
        """Ajoute un joueur au tournoi."""
        self.players.append(player)
        
    def player_list(self) -> List[Player]:
        """Retourne la liste des joueurs du tournoi."""
        return self.players
        
    def get_round(self, number: int) -> Optional [Round]:
        """Retourne la ronde par son numéro."""
        if 1<= number <= self.number_of_rounds:
            return self.rounds[number -1]
        raise ValueError("Numéro de round invalide.")
        
    def get_current_round(self) -> Optional[Round]:
        """Retourne la ronde en cours."""
        if self.rounds and self.rounds[-1].end_datetime is None:
            return self.current_round
        
    def is_finished(self) -> bool:
        """Indique si le tournoi est terminé."""
        return len(self.rounds) == self.number_of_rounds and all(r.end_datetime is not None for r in self.rounds)