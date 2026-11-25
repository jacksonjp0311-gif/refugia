"""Society organ.

Proposals enter. Oracle verifies. Keep only when status is proven and matched.
Conditional and heuristic stay labeled and do not promote.
Append-only decisions. Human authorize still required for durable acceptance.
Residual seed: status + receipt + ceiling.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .oracle import Claim, Oracle, Verification


@dataclass
class Decision:
    claim_id: str
    action: str  # "keep" | "revert" | "hold"
    status: str
    reason: str
    timestamp: str

    def to_dict(self) -> dict:
        return asdict(self)


class Society:
    def __init__(self, root: Path | str = "."):
        self.root = Path(root)
        self.oracle = Oracle(self.root / "society" / "receipts" / "oracle.jsonl")
        self.decisions_path = self.root / "society" / "receipts" / "decisions.jsonl"
        self.decisions_path.parent.mkdir(parents=True, exist_ok=True)

    def propose(self, claim: Claim) -> Verification:
        return self.oracle.verify(claim)

    def decide(self, verification: Verification) -> Decision:
        status = verification.result.status
        matched = verification.matched
        if status == "error":
            action = "revert"
            reason = "engine error"
        elif status in ("heuristic", "conditional"):
            action = "hold"
            reason = f"status {status} retained; not promoted"
        elif status == "proven" and matched is True:
            action = "keep"
            reason = "proven and matched"
        elif status == "proven" and matched is False:
            action = "revert"
            reason = "proven but mismatch"
        else:
            action = "hold"
            reason = "no expected value or inconclusive"
        d = Decision(
            claim_id=verification.claim_id,
            action=action,
            status=status,
            reason=reason,
            timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        self._append_decision(d)
        return d

    def _append_decision(self, d: Decision) -> None:
        with self.decisions_path.open("a") as f:
            f.write(json.dumps(d.to_dict()) + "\n")

    def cycle(self, claims: list[Claim]) -> list[Decision]:
        decisions = []
        for c in claims:
            v = self.propose(c)
            d = self.decide(v)
            decisions.append(d)
        return decisions
