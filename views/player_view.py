from typing import Dict, Optional


class PlayerView:  # TODO: Grouper TournamentView et PlayerView dans le même script - créer un objet FormView dont hériterons TournamentView et PlayerView
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
