"""constant.py — Constantes de configuration de l'application."""

from pathlib import Path

# Fichier JSON contenant les joueurs (base de test)
DB_PLAYERS = Path("Data") / "FakePlayers.json"

# Fichier JSON contenant la DB des joueurs licenciés
DB_LICENSED_PLAYERS = Path("Data") / "LicensedPlayers.json"

# Fichier JSON contenant les tournois
DB_TOURNAMENTS = Path("Data") / "Tournaments.json"

# Encodage de lecture/écriture
DEFAULT_ENCODING = "utf-8"

# Résultats autorisés pour un match
VALID_RESULTS = {"0", "1", "0.5", None}
