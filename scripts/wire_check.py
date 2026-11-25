#!/usr/bin/env python3
"""Manual wiring verification.

Installs nothing. Expects sagebrush already present.
Prints certified results. Does not promote. Does not evolve.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from refugia.engines import query


def main() -> int:
    checks = [
        ("factor", {"n": 2**128 + 1}),
        ("classgroup", {"coeffs": [1, 0, 14, -1], "name": "a"}),  # x^3 + 14x - 1
    ]
    ok = True
    for engine, payload in checks:
        result = query(engine, payload)
        print(json.dumps(result.to_dict(), default=str, indent=2))
        if result.status == "error":
            ok = False
            print(f"::warning::engine {engine} returned error", file=sys.stderr)
        else:
            print(f"status retained: {result.status} (not auto-promoted)")
    print("wiring check complete — residual seed intact" if ok else "wiring check incomplete")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
