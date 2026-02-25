import json
import os
from functools import wraps
from typing import Callable, Any


def save_player(path_file: str) -> Callable:
    """Décorateur pour sauvegarder automatiquement les joueurs d'un tournoi dans un fichier JSON.

    Ce décorateur intercepte l'exécution d'une fonction (supposée manipuler un tournoi)
    et sauvegarde la liste des joueurs de ce tournoi dans le fichier spécifié.

    Args:
        path_file (str): Le chemin du fichier JSON où sauvegarder les joueurs.

    Returns:
        Callable: La fonction décorée.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)

            # Ici on inspecte le tournoi passé en argument (supposé être le 2ème argument: args[1])
            # Attention: Cette implémentation dépend fortement de la signature de la fonction décorée.
            try:
                # args[0] est 'self' si méthode d'instance, args[1] est le tournoi
                tournament = args[1]
                players = tournament.players
            except IndexError:
                # Si la fonction n'a pas assez d'arguments, on ignore la sauvegarde
                return result
            except AttributeError:
                # Si l'objet récupéré n'a pas d'attribut 'players', on ignore
                return result

            # Charger JSON existant ou créer une structure vide
            if os.path.exists(path_file):
                try:
                    with open(path_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError):
                    data = {"players": []}
            else:
                data = {"players": []}

            # Utilisation d'un set pour éviter les doublons (basé sur l'ID national)
            existing_ids = {p["national_chess_id"] for p in data.get("players", [])}

            # Si "players" n'existe pas dans le dictionnaire, on le crée
            if "players" not in data:
                data["players"] = []

            for player in players:
                if player.national_chess_id not in existing_ids:
                    # On utilise __dict__ si to_record n'est pas disponible,
                    # mais il est préférable d'utiliser to_record() s'il existe sur Player
                    if hasattr(player, "to_record"):
                        data["players"].append(player.to_record())
                    else:
                        data["players"].append(player.__dict__)
                    existing_ids.add(player.national_chess_id)

            # Écriture dans le fichier
            with open(path_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return result

        return wrapper

    return decorator
