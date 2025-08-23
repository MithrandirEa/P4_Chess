""" prompts.py - CLI - Uniquement saisies, aucun logique métier."""

from __future__ import annotations
from typing import Dict, Optional


# ==============PROMPTS==================

def ask_yes_no(message: str) -> bool:
    """Demande une réponse oui/non à l'utilisateur."""
    while True:
        answer = input(f"{message} (y/n) : ").strip().lower()
        if answer in ('y','o', 'n'):
            return answer == 'o'
        print("Réponse invalide. Veuillez entrer 'o' pour oui ou 'n' pour non.")

def prompt_player_fields() -> Dict[str, Optional[str]]:
    print("=== Création d'un nouveau joueur ===")
    name = input("Nom complet : ").strip()
    birthdate = input("Date de naissance (YYYY-MM-DD) : ").strip()
    national_chess_id = input("ID national d'échecs : ").strip()
    address = input("Adresse (optionnelle) : ").strip()
    return {
        "name": name,
        "birthdate": birthdate,
        "national_chess_id": national_chess_id,
        "address": address or None,
    }
    
def promt_tournament_fields() -> Dict[str, Optional[str]]:
    print("=== Création d'un nouveau tournoi ===")
    name = input("Nom du tournoi : ").strip()
    location = input("Lieu : ").strip()
    start_date = input("Date de début (YYYY-MM-DD) : ").strip()
    end_date = input("Date de fin (YYYY-MM-DD) : ").strip()
    number_of_rounds = input("Nombre de rounds (par défaut 4) : ").strip()
    description = input("Description (optionnelle) : ").strip()
    return {
        "name": name,
        "location": location,
        "start_date": start_date,
        "end_date": end_date,
        "number_of_rounds": int(number_of_rounds) if number_of_rounds.isdigit() else 4,
        "description": description or None,
    }