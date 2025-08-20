"""constant.py — Constantes de configuration de l'application."""

from pathlib import Path

# Fichier JSON contenant les joueurs (ta base existante)
DB_PLAYERS = Path("Data") / "FakePlayers.json"

# Fichier JSON pour les tours & matches
DB_ROUNDS = Path("Data") / "Rounds.json"

# Encodage de lecture/écriture
DEFAULT_ENCODING = "utf-8"

# Résultats autorisés pour un match
VALID_RESULTS = {"1-0", "0-1", "1/2-1/2", None}
