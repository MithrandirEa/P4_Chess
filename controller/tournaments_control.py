""" tournaments_control.py - Contrôleur des tournois."""

from __future__ import annotations
from typing import List, Optional
from models import Tournament, Round, Match, Player
from view import prompts

class TournamentController:
    """Contrôleur pour gérer les tournois."""
    
    def __init__(self):
        self.tournaments: List[Tournament] = []
        
    def create_tournament(self, name: str, location: str, start_date: str,
                          end_date: str, number_of_rounds: int,
                          description: Optional[str] = None) -> Tournament:
        """Crée un nouveau tournoi et l'ajoute à la liste des tournois."""
        tournament = Tournament(
            name=name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            number_of_rounds=number_of_rounds,
            description=description
        )
        self.tournaments.append(tournament)
        return tournament
    
    def list_tournaments(self) -> List[Tournament]:
        """Retourne la liste des tournois existants."""
        return self.tournaments
    
controller = TournamentController()

# Création d'un tournoi
def create




