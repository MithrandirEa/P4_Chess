# views/view_models.py
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Optional, Any
from type_validation import validate_cast  # déjà utilisé dans ton projet


class FormView(ABC):
    """Vue de formulaire générique pour la CLI."""

    def ask_str(self, label: str, default: Optional[str] = None) -> str:
        val = validate_cast(label, str, default=default or "")
        return str(val)

    def ask_optional_str(self, label: str) -> Optional[str]:
        val = validate_cast(label, str, default="")
        return val or None

    def ask_int(self, label: str, default: Optional[int] = None) -> int:
        val = validate_cast(label, int, default=default)
        return int(val)

    def ask_date_iso(self, label: str) -> Optional[str]:
        dt: Optional[datetime] = validate_cast(label, datetime)
        return dt.strftime("%Y-%m-%d") if dt else None

    # Hook pour validations spécifiques si besoin
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return data

    @abstractmethod
    def ask_fields(self) -> Dict[str, Optional[str]]:
        """Chaque sous-classe retourne un dict prêt à passer au controller."""
        ...


class TournamentView(FormView):
    def ask_fields(self) -> Dict[str, Optional[str]]:
        print("\n=== Création d’un nouveau tournoi ===")
        data: Dict[str, Optional[str]] = {
            "name": self.ask_str("Nom du tournoi : "),
            "location": self.ask_str("Lieu : ", default=""),
            "start_date": self.ask_date_iso("Date de début (YYYY-MM-DD) : "),
            "end_date": self.ask_date_iso("Date de fin (YYYY-MM-DD) : "),
            "number_of_rounds": str(
                self.ask_int("Nombre de rounds (par défaut 4) : ", default=4)
            ),
            "description": self.ask_optional_str("Description (optionnelle) : "),
        }
        return self.validate(data)


def select_tournament(controller):
    """Sélection d’un tournoi existant depuis le controller."""
    tournaments = controller.list_tournaments()
    if not tournaments:
        print("⚠ Aucun tournoi disponible.")
        return None

    print("\n=== Sélectionner un tournoi ===")
    for idx, t in enumerate(tournaments, start=1):
        print(f"{idx}. {t.name} ({t.start_date} → {t.end_date})")

    try:
        choice = int(input("Choisissez un tournoi (numéro) : ").strip())
        return tournaments[choice - 1] if 1 <= choice <= len(tournaments) else None
    except ValueError:
        print("⚠ Entrée invalide.")
        return None


class PlayerView(FormView):
    def ask_fields(self) -> Dict[str, Optional[str]]:
        print("\n=== Création d’un joueur ===")
        data: Dict[str, Optional[str]] = {
            "name": self.ask_str("Nom complet : "),
            "birthdate": self.ask_str("Date de naissance (YYYY-MM-DD) : "),
            "national_chess_id": self.ask_str("Identifiant fédéral : "),
            "address": self.ask_optional_str("Adresse (optionnelle) : "),
        }
        return self.validate(data)
