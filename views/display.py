#TODO: REFACTORING - Décorateur ?

"""display.py - CLI - Affichage des rapports."""
import json

from tabulate import tabulate
from pathlib import Path
from constant import DB_LICENSED_PLAYERS, DB_TOURNAMENTS, DEFAULT_ENCODING
 
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
    
def display_tournament_players_list(tournament):
    """Affiche la liste des joueurs d'un tournoi sous forme de tableau."""
    players = tournament.players
    if not players:
        print("⚠️ Aucun joueur dans ce tournoi.")
        return

    # Préparer les données pour tabulate
    table = []
    for idx, p in enumerate(players, start=1):
        table.append([
            idx,
            p.name,
            p.birthdate,
            p.national_chess_id,
            p.address or "",
            p.tournament_score_value,
        ])
    headers = ["name", "birthdate", "national_chess_id", "address", "stournament_score_value"]
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

def display_chessplayers_list():
    """Affiche la liste des joueurs d'échecs sous forme de tableau."""
    players_file = Path(DB_LICENSED_PLAYERS)
    if not players_file.exists():
        print("⚠️ Aucun joueur enregistré.")
        return

    with open(players_file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            players = data.get("players", [])
        except json.JSONDecodeError:
            print("⚠️ Fichier de joueurs corrompu ou vide.")
            return

    if not players:
        print("⚠️ Aucun joueur disponible.")
        return

    # Préparer les données pour tabulate
    table = []
    for idx, p in enumerate(players, start=1):
        table.append([
            idx,
            p.get("name", ""),
            p.get("birthdate", ""),
            p.get("national_chess_id", ""),
            p.get("address", ""),
        ])
    headers = ["name", "birthdate", "national_chess_id", "address"]
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))