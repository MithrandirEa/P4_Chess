"""display.py - CLI - Affichage des rapports."""
import json

from tabulate import tabulate
from pathlib import Path
from constant import DB_TOURNAMENTS, DEFAULT_ENCODING

 
def display_tournament_list():
    """Affiche la liste des tournois sous forme de tableau."""
    if not DB_TOURNAMENTS.exists():
        print("⚠️ Aucun tournoi enregistré.")
        return

    with open(DB_TOURNAMENTS, "r", encoding=DEFAULT_ENCODING) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Fichier de tournois corrompu ou vide.")
            return

    if not data:
        print("⚠️ Aucun tournoi disponible.")
        return

    # Préparer les données pour tabulate
    table = []
    for idx, t in enumerate(data, start=1):
        table.append([
            idx,
            t.get("name", ""),
            t.get("location", ""),
            t.get("start_date", ""),
            t.get("end_date", ""),
            t.get("number_of_rounds", 0),
            len(t.get("players", [])),
        ])

    headers = ["#", "Nom", "Lieu", "Début", "Fin", "Rounds", "Nb Joueurs"]

    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
