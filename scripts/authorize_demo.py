#!/usr/bin/env python3
"""Authorization demo.

Shows that accept without human_flag is rejected.
With human_flag and a real candidate, it would succeed.
Residual seed: the human gate.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from refugia.authorize import Authorizer


def main() -> int:
    auth = Authorizer()
    # Attempt without flag
    result = auth.accept("example_claim", human_flag=False)
    print(json.dumps(result, indent=2))
    # Attempt with flag on non-candidate
    result = auth.accept("example_claim", human_flag=True)
    print(json.dumps(result, indent=2))
    print("\nhuman flag required; non-candidates rejected. Residual seed intact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
