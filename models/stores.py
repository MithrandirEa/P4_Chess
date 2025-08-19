from __future__ import annotations

import json
import os
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from constant import DB_PLAYERS, DB_ROUNDS, DEFAULT_ENCODING, VALID_RESULTS
from .player import Player
from .match import Match
from .round import Round


# ------------ utilitaires JSON ------------
def _ensure_store_exists(path: Path, root_key: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        _atomic_write_json(path, {"count": 0, root_key: []})

def _atomic_write_json(path: Path, data: Dict[str, Any]) -> None:
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding=DEFAULT_ENCODING) as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.flush()
        os.fsync(f.fileno())
    tmp_path.replace(path)

# ------------ joueurs ------------
def _normalize_players(players_raw: Any) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if not isinstance(players_raw, list):
        return out
    for r in players_raw:
        if not isinstance(r, dict):
            continue
        out.append({
            "name": r.get("name", ""),
            "birthdate": r.get("birthdate", ""),
            "national_chess_id": r.get("national_chess_id", ""),
            "address": r.get("address"),
        })
    return out

def _read_players_store() -> Dict[str, Any]:
    _ensure_store_exists(DB_PLAYERS, "players")
    with DB_PLAYERS.open("r", encoding=DEFAULT_ENCODING) as f:
        raw = json.load(f)

    if isinstance(raw, dict) and "players" in raw:
        players = _normalize_players(raw.get("players", []))
        data = dict(raw)
        data["players"] = players
        data["count"] = len(players)
        return data

    if isinstance(raw, list):
        players = _normalize_players(raw)
        return {"players": players, "count": len(players)}

    return {"players": [], "count": 0}

def _write_players_store(data: Dict[str, Any]) -> None:
    _atomic_write_json(DB_PLAYERS, data)

# ------------ rounds & matches ------------
def _read_rounds_store() -> Dict[str, Any]:
    _ensure_store_exists(DB_ROUNDS, "rounds")
    with DB_ROUNDS.open("r", encoding=DEFAULT_ENCODING) as f:
        raw = json.load(f)

    if isinstance(raw, dict) and "rounds" in raw:
        rounds_norm = []
        for r in raw.get("rounds", []):
            if not isinstance(r, dict):
                continue
            matches = []
            for m in r.get("matches", []):
                if not isinstance(m, dict):
                    continue
                matches.append({
                    "match_id": m.get("match_id", str(uuid.uuid4())),
                    "white_id": m.get("white_id", ""),
                    "black_id": m.get("black_id", ""),
                    "board": m.get("board"),
                    "result": m.get("result"),
                })
            rounds_norm.append({
                "round_id": r.get("round_id", str(uuid.uuid4())),
                "name": r.get("name", ""),
                "number": r.get("number"),
                "date": r.get("date"),
                "matches": matches,
            })
        data = dict(raw)
        data["rounds"] = rounds_norm
        data["count"] = len(rounds_norm)
        return data

    if isinstance(raw, list):
        rounds_norm = []
        for r in raw:
            if not isinstance(r, dict):
                continue
            matches = []
            for m in r.get("matches", []):
                if not isinstance(m, dict):
                    continue
                matches.append({
                    "match_id": m.get("match_id", str(uuid.uuid4())),
                    "white_id": m.get("white_id", ""),
                    "black_id": m.get("black_id", ""),
                    "board": m.get("board"),
                    "result": m.get("result"),
                })
            rounds_norm.append({
                "round_id": r.get("round_id", str(uuid.uuid4())),
                "name": r.get("name", ""),
                "number": r.get("number"),
                "date": r.get("date"),
                "matches": matches,
            })
        return {"rounds": rounds_norm, "count": len(rounds_norm)}

    return {"rounds": [], "count": 0}

def _write_rounds_store(data: Dict[str, Any]) -> None:
    _atomic_write_json(DB_ROUNDS, data)

# ------------ services exposés (API modèle) ------------
def list_players() -> List[Player]:
    data = _read_players_store()
    return [
        Player.from_record(rec)
        for rec in data.get("players", [])
        if isinstance(rec, dict) and rec.get("national_chess_id")
    ]

def add_player(player: Player) -> bool:
    data = _read_players_store()
    players: List[Dict[str, Any]] = data.get("players", [])
    if any((isinstance(rec, dict) and rec.get("national_chess_id") == player.national_chess_id) for rec in players):
        return False
    players.append(player.to_record())
    data["players"] = players
    data["count"] = len(players)
    _write_players_store(data)
    return True

def list_rounds() -> List[Round]:
    data = _read_rounds_store()
    return [Round.from_record(r) for r in data.get("rounds", [])]

def create_round(name: str, number: Optional[int] = None, date: Optional[str] = None) -> Round:
    data = _read_rounds_store()
    new_round = Round(name=name, number=number, date=date, matches=[])
    rounds = data.get("rounds", [])
    rounds.append(new_round.to_record())
    data["rounds"] = rounds
    data["count"] = len(rounds)
    _write_rounds_store(data)
    return new_round

def _players_id_set() -> set[str]:
    return {p.national_chess_id for p in list_players()}

def add_match_to_round(round_id: str, white_id: str, black_id: str,
                       board: Optional[int] = None) -> Optional[Match]:
    if not white_id or not black_id or white_id == black_id:
        return None
    ids_ok = _players_id_set()
    if white_id not in ids_ok or black_id not in ids_ok:
        return None

    data = _read_rounds_store()
    rounds = data.get("rounds", [])
    for r in rounds:
        if r.get("round_id") == round_id:
            m = Match(white_id=white_id, black_id=black_id, board=board)
            r.setdefault("matches", []).append(m.to_record())
            _write_rounds_store(data)
            return m
    return None

def set_match_result(round_id: str, match_id: str, result: Optional[str]) -> bool:
    if result not in VALID_RESULTS:
        return False

    data = _read_rounds_store()
    rounds = data.get("rounds", [])
    for r in rounds:
        if r.get("round_id") == round_id:
            for m in r.get("matches", []):
                if m.get("match_id") == match_id:
                    m["result"] = result
                    _write_rounds_store(data)
                    return True
    return False

def list_matches_for_round(round_id: str) -> List[Match]:
    data = _read_rounds_store()
    for r in data.get("rounds", []):
        if r.get("round_id") == round_id:
            return [Match.from_record(m) for m in r.get("matches", []) if isinstance(m, dict)]
    return []
