#!/usr/bin/env python3
"""Manual society cycle.

Proposals enter the Oracle. Decisions respect status.
No auto-promotion. No durable acceptance. Residual seed intact.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from refugia.oracle import Claim
from refugia.society import Society


def main() -> int:
    society = Society()
    claims = [
        Claim(
            claim_id="factor_fermat",
            engine="factor",
            payload={"n": 2**128 + 1},
            hypothesis="factorization of 2^128+1",
        ),
        Claim(
            claim_id="classgroup_sample",
            engine="classgroup",
            payload={"coeffs": [1, 0, 14, -1], "name": "a"},
            expected="8",  # known class number example
            hypothesis="class number of x^3 + 14x - 1",
        ),
    ]
    decisions = society.cycle(claims)
    for d in decisions:
        print(json.dumps(d.to_dict(), indent=2))
        print(f"{d.claim_id}: {d.action} ({d.status}) — {d.reason}")
    print("\ncycle complete — residual seed intact, no auto-promotion, human authorize still required for durable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
