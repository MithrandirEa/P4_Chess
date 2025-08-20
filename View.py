"""
View.py — Couche Vue (CLI). Uniquement saisies/affichages, aucune logique métier.
"""

from __future__ import annotations
from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.player import Player
    from models.round import Round
    from models.match import Match


# =========== PROMPTS ===========
def ask_yes_no(message: str) -> bool:
    answer = input(f"{message} (y/n) : ").strip().lower()
    return answer in {"y", "o", "yes", "oui"}


def prompt_player_fields() -> Dict[str, str]:
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


def prompt_round_fields() -> Dict[str, str]:
    print("=== Création d'un nouveau tour ===")
    name = input("Nom du tour (ex. 'Ronde 1') : ").strip()
    number_raw = input("Numéro (optionnel) : ").strip()
    date = input("Date (YYYY-MM-DD, optionnelle) : ").strip()
    number = int(number_raw) if number_raw.isdigit() else None
    return {"name": name, "number": number, "date": date or None}


def prompt_match_fields() -> Dict[str, str]:
    print("=== Ajout d'un match ===")
    white_id = input("ID national des blancs : ").strip()
    black_id = input("ID national des noirs : ").strip()
    board_raw = input("N° de table (optionnel) : ").strip()
    board = int(board_raw) if board_raw.isdigit() else None
    return {"white_id": white_id, "black_id": black_id, "board": board}


def select_round(rounds: List["Round"]) -> Optional[str]:
    if not rounds:
        print("Aucun tour disponible.")
        return None
    print("\n=== Sélection du tour ===")
    for idx, r in enumerate(rounds, start=1):
        print(f"{idx}. {r.name} (id={r.round_id}) — number={r.number} date={r.date}")
    raw = input("Votre choix (numéro) : ").strip()
    if not raw.isdigit():
        return None
    i = int(raw)
    if 1 <= i <= len(rounds):
        return rounds[i - 1].round_id
    return None


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


def show_round_created(r: "Round") -> None:
    print(f"Tour créé : {r.name} (id={r.round_id}, number={r.number}, date={r.date})")


def show_match_added(m: "Match") -> None:
    print(
        f"Match ajouté : {m.white_id} vs {m.black_id} (id={m.match_id}, table={m.board})"
    )


def show_rounds(rounds: List["Round"]) -> None:
    if not rounds:
        print("Aucun tour enregistré.")
        return
    print("\n=== Tours & matches ===")
    for r in rounds:
        print(f"- {r.name} (id={r.round_id}, number={r.number}, date={r.date})")
        if not r.matches:
            print("    (aucun match)")
        else:
            for m in r.matches:
                res = m.result or "—"
                print(
                    f"    · [{m.match_id}] table={m.board}  {m.white_id} vs {m.black_id}  -> {res}"
                )


def show_set_result(ok: bool) -> None:
    print(
        "Résultat mis à jour."
        if ok
        else "Échec de la mise à jour (IDs/valeur invalides)."
    )
