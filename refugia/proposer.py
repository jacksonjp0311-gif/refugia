"""Proposer role.

Posts well-formed, engine-supported claims to the bus under topic `propose`.
Does not verify. Does not decide. Residual seed begins with a clean proposal.
"""

from __future__ import annotations

from typing import Any

from .bus import Bus


def post_claim(
    bus: Bus,
    claim_id: str,
    engine: str,
    payload: dict,
    expected: Any = None,
    hypothesis: str = "",
) -> dict:
    msg = bus.post(
        role="proposer",
        topic="propose",
        payload={
            "claim_id": claim_id,
            "engine": engine,
            "payload": payload,
            "expected": expected,
            "hypothesis": hypothesis,
        },
    )
    return msg.to_dict()


def sample_claims() -> list[dict]:
    """Small set of engine-supported claims for manual exercise."""
    return [
        {
            "claim_id": "prop_factor_fermat",
            "engine": "factor",
            "payload": {"n": 2**128 + 1},
            "hypothesis": "factor of 2^128 + 1",
        },
        {
            "claim_id": "prop_classgroup_sample",
            "engine": "classgroup",
            "payload": {"coeffs": [1, 0, 14, -1], "name": "a"},
            "hypothesis": "class group of x^3 + 14x - 1 (conditional under GRH)",
        },
        {
            "claim_id": "prop_rank_11a",
            "engine": "rank",
            "payload": {"label": "11a", "proof": False},
            "hypothesis": "rank of 11a with proof=False (heuristic)",
        },
    ]
