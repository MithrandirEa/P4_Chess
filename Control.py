"""
Control.py — Couche Contrôleur : orchestre la View et le Model.
"""

from __future__ import annotations

import View as view
from models.player import Player
from models.round import Round
from models.match import Match
from models.stores import (
    list_players, add_player,
    list_rounds, create_round,
    add_match_to_round, set_match_result,
)

def flow_players() -> None:
    if view.ask_yes_no("Souhaitez-vous créer un nouveau joueur ?"):
        fields = view.prompt_player_fields()
        if not fields["name"] or not fields["birthdate"] or not fields["national_chess_id"]:
            print("Champs obligatoires manquants (nom, date de naissance, ID national).")
        else:
            ok = add_player(Player(**fields))
            view.show_player_added(ok, fields["name"])
    else:
        view.show_no_creation()
    view.show_players(list_players())


def flow_rounds() -> None:
    # 1) Créer un tour ?
    if view.ask_yes_no("Créer un nouveau tour ?"):
        r_fields = view.prompt_round_fields()
        if not r_fields["name"]:
            print("Le nom du tour est obligatoire.")
        else:
            r = create_round(**r_fields)
            view.show_round_created(r)

    # 2) Ajouter un match ?
    if view.ask_yes_no("Ajouter un match à un tour existant ?"):
        rounds = list_rounds()
        round_id = view.select_round(rounds)
        if round_id:
            m_fields = view.prompt_match_fields()
            created = add_match_to_round(
                round_id=round_id,
                white_id=m_fields["white_id"],
                black_id=m_fields["black_id"],
                board=m_fields["board"],
            )
            if created:
                view.show_match_added(created)
            else:
                print("Impossible d'ajouter le match (IDs joueurs invalides, identiques ou tour introuvable).")

    # 3) Mettre un résultat ?
    if view.ask_yes_no("Mettre à jour le résultat d'un match ?"):
        rounds = list_rounds()
        round_id = view.select_round(rounds)
        if round_id:
            # Affiche les matches du tour choisi
            for r in rounds:
                if r.round_id == round_id:
                    view.show_rounds([r])
                    break
            match_id = input("Saisir l'id du match : ").strip()
            result = input("Résultat (1-0, 0-1, 1/2-1/2) ou vide pour None : ").strip() or None
            ok = set_match_result(round_id, match_id, result)
            view.show_set_result(ok)

    # 4) État courant
    view.show_rounds(list_rounds())


def main_cli() -> None:
    print("=== Menu ===")
    print("1) Gérer les joueurs")
    print("2) Gérer les tours & matches")
    choice = input("Votre choix (1/2) : ").strip()
    if choice == "1":
        flow_players()
    elif choice == "2":
        flow_rounds()
    else:
        print("Choix non reconnu.")


if __name__ == "__main__":
    main_cli()
