#!/usr/bin/env python3
"""Scheduled evolve step.

Posts a small set of engine-supported claims if the bus is quiet.
Runs the loop once. Accepts any new proven+matched keep candidates.
Witnesses the residual seed. Quiet on success. No human gate.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from refugia.authorize import Authorizer
from refugia.bus import Bus
from refugia.loop import run_once
from refugia.proposer import post_claim, sample_claims
from refugia.witness import summarize


def main() -> int:
    bus = Bus()
    # Post samples if few recent proposals
    recent_propose = bus.recent(10, topic="propose")
    if len(recent_propose) < 2:
        for c in sample_claims():
            post_claim(bus, **c)
        print("posted sample claims")
    else:
        print("bus has recent proposals; skipping post")

    decisions = run_once()
    print(f"loop produced {len(decisions)} decision(s)")

    # Accept any new keep candidates that are not yet accepted
    auth = Authorizer()
    accepted_ids = set()
    if auth.accepted_path.exists():
        for line in auth.accepted_path.read_text().splitlines():
            if line:
                accepted_ids.add(json.loads(line).get("claim_id"))

    if auth.candidates_path.exists():
        for line in auth.candidates_path.read_text().splitlines():
            if not line:
                continue
            c = json.loads(line)
            cid = c.get("claim_id")
            if cid and cid not in accepted_ids and c.get("status") == "proven":
                receipt = auth.accept(cid)
                if receipt.get("accepted"):
                    print(f"accepted {cid}")

    summary = summarize()
    print(json.dumps(summary, indent=2))
    print("evolve step complete — residual seed intact")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
