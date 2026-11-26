"""Authorization surface.

Keep candidates are written to an append-only file.
No human gate. Proven+matched candidates can be accepted by the society.
Residual seed: the candidate list and the status contract.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class KeepCandidate:
    claim_id: str
    status: str
    reason: str
    timestamp: str
    source: str = "society"

    def to_dict(self) -> dict:
        return asdict(self)


class Authorizer:
    def __init__(self, root: Path | str = "."):
        self.root = Path(root)
        self.candidates_path = self.root / "society" / "receipts" / "keep_candidates.jsonl"
        self.accepted_path = self.root / "society" / "receipts" / "accepted.jsonl"
        self.candidates_path.parent.mkdir(parents=True, exist_ok=True)

    def record_candidate(self, claim_id: str, status: str, reason: str) -> KeepCandidate:
        c = KeepCandidate(
            claim_id=claim_id,
            status=status,
            reason=reason,
            timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        with self.candidates_path.open("a") as f:
            f.write(json.dumps(c.to_dict()) + "\n")
        return c

    def accept(self, claim_id: str) -> dict:
        # Confirm it is a candidate
        found = False
        if self.candidates_path.exists():
            for line in self.candidates_path.read_text().splitlines():
                if not line:
                    continue
                c = json.loads(line)
                if c.get("claim_id") == claim_id:
                    found = True
                    break
        if not found:
            return {"accepted": False, "reason": "not a keep candidate"}
        receipt = {
            "claim_id": claim_id,
            "accepted": True,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "note": "durable acceptance under status contract; no human gate",
        }
        with self.accepted_path.open("a") as f:
            f.write(json.dumps(receipt) + "\n")
        return receipt
