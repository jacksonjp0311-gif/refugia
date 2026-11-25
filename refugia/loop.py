"""Minimal propose-from-bus loop.

Reads proposals from the bus. Runs them through society. Posts decisions back.
Skips claims that already have a decision. Manual only. Residual seed intact.
"""

from __future__ import annotations

import json
from pathlib import Path

from .bus import Bus
from .oracle import Claim
from .society import Society


def _already_decided(bus: Bus, claim_id: str) -> bool:
    for m in bus.recent(200, topic="decision"):
        if m.get("payload", {}).get("claim_id") == claim_id:
            return True
    return False


def run_once(root: Path | str = ".") -> list:
    bus = Bus(Path(root) / "society" / "receipts" / "bus.jsonl")
    society = Society(root)
    proposals = bus.recent(50, topic="propose")
    decisions = []
    for msg in proposals:
        try:
            payload = msg.get("payload", {})
            claim_id = payload.get("claim_id", "unknown")
            if _already_decided(bus, claim_id):
                continue
            claim = Claim(
                claim_id=claim_id,
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
                payload={"error": str(e), "source": str(msg)[:200]},
            )
    return decisions
