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
        
""" Prompts pour la création de joueurs """        
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

""" Prompt pour la création de tournois """    
def prompt_tournament_fields() -> Dict[str, Optional[str]]:
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
        "number_of_rounds": int(number_of_rounds) if number_of_rounds.isdigit() else 4, # Je ne comprends pas comment résoudre le problème de typage. Voir avec Patrick
        "description": description or None,
    }


# ===================== Menus & Sous-menus ====================

""" Prompt pour le menu principal """    
def prompt_main_menu() -> int:
    """Affiche le menu principal et retourne le choix de l'utilisateur."""
    print("\n=== Menu Principal ===")
    print("1. Créer un tournoi")
    print("2. Gerer un tournois")
    print("3. Afficher les rapports")
    print("0. Quitter")
    
    while True:
        try:
            choice = int(input("Sélectionnez une option (0-3) : ").strip())
            if choice in (0, 1, 2, 3):
                return choice
            else:
                print("Choix invalide. Veuillez entrer un nombre entre 0 et 3.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre.")
            
def prompt_select_tournament(tournaments) -> int:
    """ Affiche la liste des tournois et retourne l'indice choisi"""
    
    if not tournaments:
        print("\n Aucun tournoi disponible.")
        return -1
    
    print("\n=== Sélectionner un Tournoi ===")
    for idx, tournament in enumerate(tournaments, start=1):
        print(f"{idx}. {tournament.name} ({tournament.start_date} - {tournament.end_date})")
    print("0. Retour au menu principal")
    
    while True:
        try:
            choice = int(input(f"Sélectionnez un tournoi (0-{len(tournaments)}) : ").strip())
            if 0 <= choice <= len(tournaments):
                return choice - 1  # Retourne l'indice dans la liste
            else:
                print(f"Choix invalide. Veuillez entrer un nombre entre 0 et {len(tournaments)}.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre.")
            
    
            
""" Prompt pour le sous-menu de gestion des tournois """    
def prompt_tournament_management_menu() -> int:
    """Affiche le menu de gestion des tournois et retourne le choix de l'utilisateur."""
    print("\n=== Gestion des Tournois ===")
    print("1. Ajouter des joueurs au tournoi")
    print("2. Démarrer le tournoi")
    print("3. Enregistrer les résultats des matchs")
    print("4. Afficher le classement actuel")
    print("0. Retour au menu principal")
    
    while True:
        try:
            sub_choice = int(input("Sélectionnez une option (0-4) : ").strip())
            if sub_choice in (0, 1, 2, 3, 4):
                return sub_choice
            else:
                print("Choix invalide. Veuillez entrer un nombre entre 0 et 4.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre.")