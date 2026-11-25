"""Oracle organ for Refugia.

Claims are machine-checkable. Verification goes through the absorbed engines.
Status labels are retained. Heuristic or conditional results do not auto-promote.
Append-only receipt of every verification. Residual seed intact.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from .engines import CertifiedResult, query


@dataclass
class Claim:
    claim_id: str
    engine: str
    payload: dict
    expected: Optional[Any] = None
    hypothesis: str = ""


@dataclass
class Verification:
    claim_id: str
    result: CertifiedResult
    matched: Optional[bool]
    timestamp: str
    note: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d["result"] = self.result.to_dict()
        return d


class Oracle:
    def __init__(self, receipts_path: Path | str = "society/receipts/oracle.jsonl"):
        self.receipts_path = Path(receipts_path)
        self.receipts_path.parent.mkdir(parents=True, exist_ok=True)

    def verify(self, claim: Claim) -> Verification:
        result = query(claim.engine, claim.payload)
        matched = None
        if claim.expected is not None and result.status != "error":
            matched = str(result.value) == str(claim.expected)
        note = ""
        if result.status in ("heuristic", "conditional"):
            note = "status retained; not auto-promoted"
        elif result.status == "error":
            note = "engine error; claim not verified"
        v = Verification(
            claim_id=claim.claim_id,
            result=result,
            matched=matched,
            timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            note=note,
        )
        self._append(v)
        return v

    def _append(self, v: Verification) -> None:
        with self.receipts_path.open("a") as f:
            f.write(json.dumps(v.to_dict(), default=str) + "\n")

    def recent(self, n: int = 10) -> list[dict]:
        if not self.receipts_path.exists():
            return []
        lines = self.receipts_path.read_text().strip().splitlines()
        return [json.loads(line) for line in lines[-n:]]
