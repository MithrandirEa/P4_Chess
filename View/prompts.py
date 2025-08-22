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
    
