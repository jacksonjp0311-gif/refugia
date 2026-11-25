#!/usr/bin/env python3
"""Proposer demo. Posts sample claims to the bus. Does not run the loop."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from refugia.bus import Bus
from refugia.proposer import post_claim, sample_claims


def main() -> int:
    bus = Bus()
    for c in sample_claims():
        msg = post_claim(bus, **c)
        print(json.dumps({"posted": msg["payload"]["claim_id"], "ts": msg["timestamp"]}, indent=2))
    print("\nproposals posted — residual seed begins clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
