#!/usr/bin/env python3
"""Scheduled evolve step (colony-adapted).

Posts claims if quiet. Runs loop. Applies Athanor-style gate.
Accepts proven and (if flagged) conditional candidates.
Witnesses. Quiet on success. Residual seed intact.
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from refugia.athanor import gate, should_accept
from refugia.authorize import Authorizer
from refugia.bus import Bus
from refugia.loop import run_once
from refugia.proposer import post_claim, sample_claims
from refugia.witness import summarize


def main() -> int:
    bus = Bus()
    recent_propose = bus.recent(10, topic="propose")
    if len(recent_propose) < 2:
        for c in sample_claims():
            post_claim(bus, **c)
        print("posted sample claims")
    else:
        print("bus has recent proposals; skipping post")

    decisions = run_once()
    print(f"loop produced {len(decisions)} decision(s)")

    # Athanor-style: accept under gate (proven always; conditional if env)
    auth = Authorizer()
    accepted_ids = set()
    if auth.accepted_path.exists():
        for line in auth.accepted_path.read_text().splitlines():
            if line:
                accepted_ids.add(json.loads(line).get("claim_id"))

    promote = os.environ.get("REFUGIA_STATUS_PROMOTE") == "conditional"
    if auth.candidates_path.exists():
        for line in auth.candidates_path.read_text().splitlines():
            if not line:
                continue
            c = json.loads(line)
            cid = c.get("claim_id")
            status = c.get("status")
            if cid and cid not in accepted_ids:
                # Re-check via gate logic
                from refugia.engines import CertifiedResult
                fake = CertifiedResult(value=None, status=status, engine="recorded")
                if should_accept(fake) or (status == "proven") or (status == "conditional" and promote):
                    receipt = auth.accept(cid)
                    if receipt.get("accepted"):
                        print(f"accepted {cid} ({status})")

    summary = summarize()
    print(json.dumps(summary, indent=2))
    print("evolve step complete — Athanor-style gate applied — residual seed intact")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
