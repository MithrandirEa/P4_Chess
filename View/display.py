"""display.py - CLI - Uniquement affichages, aucune logique métier."""

from __future__ import annotations
from typing import List
from models import Player

# =========== AFFICHAGES ===========

def show_player_added(ok: bool, name: str) -> None:
    if ok:
        print(f"Joueur « {name} » ajouté avec succès.")
    else:
        print("Ce joueur existe déjà (ID national en double).")


def show_no_creation() -> None:
    print("Aucun élément créé.")


def show_players(players: List["Player"]) -> None:
    if not players:
        print("Aucun joueur enregistré.")
        return
    print("\n=== Liste des joueurs ===")
    for p in players:
        addr = p.address or "-"
        print(f"- {p.name} | {p.birthdate} | {p.national_chess_id} | {addr}")
