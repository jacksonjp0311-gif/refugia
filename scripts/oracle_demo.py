#!/usr/bin/env python3
"""Oracle demo. Manual only.

Verifies sample claims. Prints status. Does not promote. Does not evolve.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from refugia.oracle import Claim, Oracle


def main() -> int:
    oracle = Oracle()
    claims = [
        Claim(
            claim_id="factor_2^128+1",
            engine="factor",
            payload={"n": 2**128 + 1},
            hypothesis="factor of Fermat number",
        ),
        Claim(
            claim_id="classgroup_x3+14x-1",
            engine="classgroup",
            payload={"coeffs": [1, 0, 14, -1], "name": "a"},
            hypothesis="class number of Q(adjoined root of x^3 + 14x - 1)",
        ),
    ]
    for c in claims:
        v = oracle.verify(c)
        print(json.dumps(v.to_dict(), default=str, indent=2))
        print(f"status: {v.result.status} | matched: {v.matched} | {v.note}")
    print("\nRecent receipts:")
    for r in oracle.recent():
        print(f"  {r['claim_id']} → {r['result']['status']}")
    print("\nresidual seed intact — no auto-promotion")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
