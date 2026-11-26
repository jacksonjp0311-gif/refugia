#!/usr/bin/env python3
"""Authorization demo. No human gate.

Non-candidates are rejected. Candidates can be accepted under the status contract.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from refugia.authorize import Authorizer


def main() -> int:
    auth = Authorizer()
    # Non-candidate
    result = auth.accept("example_claim")
    print(json.dumps(result, indent=2))
    print("\nno human gate. Candidates only. Residual seed is status + witness.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
