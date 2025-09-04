from datetime import datetime

from typing import Dict, Optional
from type_validation import validate_cast


class TournamentView:  # TODO: Grouper TournamentView et PlayerView dans le même script - créer un objet FormView dont hériterons TournamentView et PlayerView
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
            "name": name,
            "location": location,
            "start_date": start_date.strftime("%Y-%m-%d") if start_date else None,
            "end_date": end_date.strftime("%Y-%m-%d") if end_date else None,
            "number_of_rounds": (
                str(number_of_rounds) if number_of_rounds is not None else None
            ),
            "description": description or None,
        }
