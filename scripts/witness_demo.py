#!/usr/bin/env python3
"""Witness demo. Prints residual seed summary. Does not mutate."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from refugia.witness import summarize


def main() -> int:
    s = summarize()
    print(json.dumps(s, indent=2))
    print("\nwitness complete — residual seed visible")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
