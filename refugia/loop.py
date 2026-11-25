"""Minimal propose-from-bus loop.

Reads proposals from the bus. Runs them through society. Posts decisions back.
Manual only. No automatic scheduling. Residual seed intact.
"""

from __future__ import annotations

import json
from pathlib import Path

from .bus import Bus
from .oracle import Claim
from .society import Society


def run_once(root: Path | str = ".") -> list:
    bus = Bus(Path(root) / "society" / "receipts" / "bus.jsonl")
    society = Society(root)
    proposals = bus.recent(50, topic="propose")
    decisions = []
    for msg in proposals:
        try:
            payload = msg.get("payload", {})
            claim = Claim(
                claim_id=payload.get("claim_id", "unknown"),
                engine=payload["engine"],
                payload=payload.get("payload", {}),
                expected=payload.get("expected"),
                hypothesis=payload.get("hypothesis", ""),
            )
            v = society.propose(claim)
            d = society.decide(v)
            bus.post(
                role="society",
                topic="decision",
                payload=d.to_dict(),
                reply_to=msg.get("timestamp"),
            )
            decisions.append(d)
        except Exception as e:
            bus.post(
                role="society",
                topic="error",
                payload={"error": str(e), "source": msg},
            )
    return decisions
