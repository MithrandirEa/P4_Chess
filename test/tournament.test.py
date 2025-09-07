def test_from_record_reconstructs_players_and_rounds():
    """Vérifie que from_record reconstruit correctement les joueurs et les rounds."""
    player1_data = {
        "name": "Magnus Carlsen",
        "birthdate": "1990-11-30",
        "national_chess_id": "NOR001",
        "address": "Oslo, Norway",
    }
    player2_data = {
        "name": "Hikaru Nakamura",
        "birthdate": "1987-12-09",
        "national_chess_id": "USA001",
        "address": "Sunrise, Florida",
    }
    round_data = {
        "number": 1,
        "start_datetime": "2023-10-26T10:00:00",
        "end_datetime": "2023-10-26T14:00:00",
        "matches": [([player1_data, 1.0], [player2_data, 0.0])],
    }
    tournament_data = {
        "name": "Test Tournament",
        "location": "Virtual",
        "start_date": "2023-01-01",
        "end_date": "2023-01-02",
        "number_of_rounds": 1,
        "description": "A test.",
        "players": [player1_data, player2_data],
        "rounds": [round_data],
    }

    tournament = Tournament.from_record(tournament_data)

    assert len(tournament.players) == 2
    assert isinstance(tournament.players[0], Player)
    assert tournament.players[0].name == "Magnus Carlsen"

    assert len(tournament.rounds) == 1
    assert isinstance(tournament.rounds[0], Round)
    assert tournament.rounds[0].number == 1

    reconstructed_match = tournament.rounds[0].matches[0]
    assert isinstance(reconstructed_match, Match)
    # Vérifie que les objets Player dans le match sont les mêmes que dans la liste du tournoi
    assert reconstructed_match.white_player is tournament.players[0]
    assert reconstructed_match.black_player is tournament.players[1]
    assert reconstructed_match.white_player_score == 1.0