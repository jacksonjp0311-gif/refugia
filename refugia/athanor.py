"""Athanor-style gate.

Adapted from agent-colony. Live gate can allow conditional results to become
candidates under the residual seed. Does not auto-promote heuristic without
explicit flag. Residual seed retained.
"""

from __future__ import annotations

import os
from typing import Optional

from .engines import CertifiedResult


def gate(result: CertifiedResult, promote_conditional: bool = False) -> str:
    """Return action recommendation under Athanor-style gate.

    live = honor status but allow conditional to candidate if flag set.
    """
    mode = os.environ.get("REFUGIA_ATHANOR_GATE", "live")
    if mode != "live":
        return "hold"
    if result.status == "proven":
        return "keep"
    if result.status == "conditional" and (promote_conditional or os.environ.get("REFUGIA_STATUS_PROMOTE") == "conditional"):
        return "candidate"
    if result.status == "heuristic":
        return "hold"
    return "revert"


def should_accept(result: CertifiedResult) -> bool:
    action = gate(result)
    return action in ("keep", "candidate")
