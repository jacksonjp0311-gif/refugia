"""Thin adapter for agent-colony (or any caller) to utilize the engines.

Survival interface. Returns CertifiedResult. Status is never stripped.
Colony decides keep/revert under its own gates. Residual seed stays intact.
"""

from __future__ import annotations

from typing import Any, Dict

from .engines import CertifiedResult, query


def oracle_query(engine: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Call an absorbed engine. Return plain dict with status retained.

    Example:
        result = oracle_query("factor", {"n": 15})
        # result["status"] is "proven" | "conditional" | "heuristic" | "error"
    """
    r: CertifiedResult = query(engine, payload)
    return r.to_dict()


def available_engines() -> list[str]:
    return ["factor", "classgroup", "ap", "rank"]
