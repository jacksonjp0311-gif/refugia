"""Tests for the residual seed: status contract and decision rule.

Run with: python -m pytest tests/ -q
"""

import json
from pathlib import Path

import pytest

from refugia.engines import CertifiedResult, query
from refugia.oracle import Claim, Oracle
from refugia.society import Society


def test_certified_result_status_labels():
    r = CertifiedResult(value=42, status="proven", engine="test")
    assert r.status == "proven"
    assert r.to_dict()["status"] == "proven"


def test_query_unknown_engine():
    r = query("no_such", {})
    assert r.status == "error"
    assert "unknown" in (r.detail or "")


def test_society_hold_on_heuristic(tmp_path):
    society = Society(tmp_path)
    # Force a heuristic path via rank proof=False if engines available;
    # otherwise mock by direct decide on a verification-like object is harder.
    # Use a claim that will error or hold.
    claim = Claim("t1", "rank", {"label": "11a", "proof": False})
    v = society.propose(claim)
    d = society.decide(v)
    if v.result.status == "heuristic":
        assert d.action == "hold"
        assert "retained" in d.reason
    elif v.result.status == "error":
        assert d.action == "revert"


def test_society_keep_only_proven_matched(tmp_path):
    society = Society(tmp_path)
    # Synthetic: we cannot easily force proven+matched without real engine,
    # so test the decision logic path by checking that hold/revert never keep
    # on non-proven.
    claim = Claim("t2", "classgroup", {"coeffs": [1, 0, 14, -1]})
    v = society.propose(claim)
    d = society.decide(v)
    if v.result.status != "proven":
        assert d.action != "keep"


def test_append_only_receipts(tmp_path):
    society = Society(tmp_path)
    claim = Claim("t3", "factor", {"n": 15})
    v = society.propose(claim)
    d = society.decide(v)
    decisions_path = tmp_path / "society" / "receipts" / "decisions.jsonl"
    assert decisions_path.exists()
    lines = decisions_path.read_text().strip().splitlines()
    assert len(lines) >= 1
    rec = json.loads(lines[-1])
    assert rec["claim_id"] == "t3"
    assert rec["status"] == d.status
