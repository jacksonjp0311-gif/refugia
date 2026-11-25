#!/usr/bin/env python3
"""Twin + bus demo. Manual only.

Treatment uses engines. Control does not. Comparison reported.
Messages posted to append-only bus. No promotion.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from refugia.twin import twin
from refugia.bus import Bus


def main() -> int:
    bus = Bus()
    report = twin("factor", {"n": 2**128 + 1}, claim_id="twin_factor")
    print(json.dumps(report.to_dict(), default=str, indent=2))
    bus.post(
        role="oracle",
        topic="twin",
        payload={"claim_id": report.claim_id, "delta": report.delta, "treatment_status": report.treatment.status},
    )
    bus.post(
        role="society",
        topic="note",
        payload={"message": "twin comparison recorded; status retained"},
    )
    print("\nRecent bus:")
    for m in bus.recent(5):
        print(f"  [{m['role']}] {m['topic']}: {m['payload']}")
    print("\nresidual seed intact — twin does not promote")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
