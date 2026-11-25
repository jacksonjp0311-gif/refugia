#!/usr/bin/env python3
"""Manual loop demo.

Posts a proposal to the bus. Runs the once loop. Prints decisions.
No auto-promotion. Residual seed intact.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from refugia.bus import Bus
from refugia.loop import run_once


def main() -> int:
    bus = Bus()
    bus.post(
        role="proposer",
        topic="propose",
        payload={
            "claim_id": "loop_factor",
            "engine": "factor",
            "payload": {"n": 2**128 + 1},
            "hypothesis": "Fermat factor via bus",
        },
    )
    print("proposal posted")
    decisions = run_once()
    for d in decisions:
        print(json.dumps(d.to_dict(), indent=2))
    print(f"\n{len(decisions)} decision(s). Residual seed intact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
