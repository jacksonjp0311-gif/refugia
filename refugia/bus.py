"""Message bus.

Roles post messages. Bus is append-only. No mutation of prior messages.
Residual seed: the record itself.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass
class Message:
    role: str
    topic: str
    payload: dict
    timestamp: str
    reply_to: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


class Bus:
    def __init__(self, path: Path | str = "society/receipts/bus.jsonl"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def post(self, role: str, topic: str, payload: dict, reply_to: Optional[str] = None) -> Message:
        m = Message(
            role=role,
            topic=topic,
            payload=payload,
            timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            reply_to=reply_to,
        )
        with self.path.open("a") as f:
            f.write(json.dumps(m.to_dict(), default=str) + "\n")
        return m

    def recent(self, n: int = 20, topic: Optional[str] = None) -> list[dict]:
        if not self.path.exists():
            return []
        lines = self.path.read_text().strip().splitlines()
        msgs = [json.loads(line) for line in lines]
        if topic:
            msgs = [m for m in msgs if m.get("topic") == topic]
        return msgs[-n:]
