from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import uuid

@dataclass
class Match:
    """Un match entre deux joueurs, référencés par leur national_chess_id."""
    white_id: str
    black_id: str
    board: Optional[int] = None
    result: Optional[str] = None   # "1-0" | "0-1" | "1/2-1/2" | None
    match_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_record(self) -> Dict[str, Any]:
        return {
            "match_id": self.match_id,
            "white_id": self.white_id,
            "black_id": self.black_id,
            "board": self.board,
            "result": self.result,
        }

    @staticmethod
    def from_record(rec: Dict[str, Any]) -> "Match":
        return Match(
            white_id=rec.get("white_id", ""),
            black_id=rec.get("black_id", ""),
            board=rec.get("board"),
            result=rec.get("result"),
            match_id=rec.get("match_id", str(uuid.uuid4())),
        )
