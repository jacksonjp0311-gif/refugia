"""Survival test for the colony utilization surface.

Status must never be stripped.
"""

from refugia.adapter import available_engines, oracle_query


def test_available_engines():
    engines = available_engines()
    assert "factor" in engines
    assert "classgroup" in engines


def test_oracle_query_status_retained():
    result = oracle_query("factor", {"n": 15})
    assert "status" in result
    assert result["status"] in ("proven", "conditional", "heuristic", "error")
    assert result["engine"] == "factor"
    # value present on success
    if result["status"] == "proven":
        assert result["value"] is not None


def test_unknown_engine_error():
    result = oracle_query("no_such_engine", {})
    assert result["status"] == "error"
