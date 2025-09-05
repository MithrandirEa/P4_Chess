import json
import os
from functools import wraps


def save_player(path_file):
    """Fonction décoratrice pour sauvegarder les joueurs dans un fichier JSON qui servira de base de données."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Ici on inspecte le tournoi passé en argument
            # et on sauvegarde tous les joueurs qu'il contient
            try:
                tournament = args[1]  # self, tournament, filepath
                players = tournament.players
            except Exception:
                return result

            # Charger JSON existant
            if os.path.exists(path_file):
                try:
                    with open(path_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError):
                    data = {"players": []}
            else:
                data = {"players": []}

            existing_ids = {p["national_chess_id"] for p in data["players"]}

            for player in players:
                if player.national_chess_id not in existing_ids:
                    data["players"].append(player.__dict__)
                    existing_ids.add(player.national_chess_id)

            with open(path_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return result

        return wrapper

    return decorator
