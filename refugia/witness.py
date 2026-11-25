"""Witness organ.

Reads the append-only record. Produces a summary. Does not mutate.
Residual seed made visible.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def summarize(root: Path | str = ".") -> dict:
    root = Path(root)
    summary = {"decisions": {}, "bus_topics": {}, "oracle_count": 0}

    decisions_path = root / "society" / "receipts" / "decisions.jsonl"
    if decisions_path.exists():
        actions = []
        statuses = []
        for line in decisions_path.read_text().strip().splitlines():
            if not line:
                continue
            d = json.loads(line)
            actions.append(d.get("action"))
            statuses.append(d.get("status"))
        summary["decisions"] = {
            "total": len(actions),
            "by_action": dict(Counter(actions)),
            "by_status": dict(Counter(statuses)),
        }

    bus_path = root / "society" / "receipts" / "bus.jsonl"
    if bus_path.exists():
        topics = []
        for line in bus_path.read_text().strip().splitlines():
            if not line:
                continue
            m = json.loads(line)
            topics.append(m.get("topic"))
        summary["bus_topics"] = dict(Counter(topics))

    oracle_path = root / "society" / "receipts" / "oracle.jsonl"
    if oracle_path.exists():
        summary["oracle_count"] = sum(1 for line in oracle_path.read_text().splitlines() if line.strip())

    return summary
