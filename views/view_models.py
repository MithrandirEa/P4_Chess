from datetime import datetime
from typing import Dict, Optional
from type_validation import validate_cast

class FormView:
    pass

class TournamentView:
    def ask_tournament_fields(self) -> Dict[str, Optional[str]]:
        print("\n=== Création d’un nouveau tournoi ===")
        name = validate_cast("Nom du tournoi : ", str)
        location = validate_cast("Lieu : ", str, default="")
        start_date = validate_cast("Date de début (YYYY-MM-DD) : ", datetime)
        end_date = validate_cast("Date de fin (YYYY-MM-DD) : ", datetime)
        number_of_rounds = validate_cast(
            "Nombre de rounds (par défaut 4) : ", int, default=4
        )
        description = validate_cast("Description (optionnelle) : ", str, default="")

        return {
# FIXME:gérer les problèmes de type
            "name": name,
            "location": location,
            "start_date": start_date.strftime("%Y-%m-%d") if start_date else None,
            "end_date": end_date.strftime("%Y-%m-%d") if end_date else None,
            "number_of_rounds": (
                str(number_of_rounds) if number_of_rounds is not None else None
            ),
            "description": description or None,
        }
        
def select_tournament(controller):
    """Permet à l'utilisateur de sélectionner un tournoi existant"""
    tournaments = controller.list_tournaments()

    if not tournaments:
        print("⚠ Aucun tournoi disponible.")
        return None

    print("\n=== Sélectionner un tournoi ===")
    for idx, t in enumerate(tournaments, start=1):
        print(f"{idx}. {t.name} ({t.start_date} → {t.end_date})")

    try:
        choice = int(input("Choisissez un tournoi (numéro) : ").strip())
        if 1 <= choice <= len(tournaments):
            return tournaments[choice - 1]
        else:
            print("⚠ Choix invalide.")
            return None
    except ValueError:
        print("⚠ Entrée invalide.")
        return None

        

class PlayerView:
    def ask_player_fields(self) -> Dict[str, Optional[str]]:
        print("\n=== Création d’un joueur ===")
        name = input("Nom complet : ").strip()
        birthdate = input("Date de naissance (YYYY-MM-DD) : ").strip()
        national_chess_id = input("Identifiant fédéral : ").strip()
        address = input("Adresse (optionnelle) : ").strip()

        return {
            "name": name,
            "birthdate": birthdate,
            "national_chess_id": national_chess_id,
            "address": address or None,
        }
