"""Twin organ.

Treatment arm runs with the absorbed engines. Control arm runs without them
(or with a stub). Comparison is reported. No automatic promotion from twin result.
Residual seed remains the status label.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from .engines import CertifiedResult, query


@dataclass
class TwinReport:
    claim_id: str
    treatment: CertifiedResult
    control: CertifiedResult
    delta: str
    note: str = "twin comparison only; status of treatment retained"

    def to_dict(self) -> dict:
        d = asdict(self)
        d["treatment"] = self.treatment.to_dict()
        d["control"] = self.control.to_dict()
        return d


def control_stub(engine: str, payload: dict) -> CertifiedResult:
    """Control arm: no engines. Returns heuristic or error."""
    return CertifiedResult(
        value=None,
        status="heuristic",
        engine=engine,
        detail="control arm: engines not used",
    )


def twin(engine: str, payload: dict, claim_id: str = "") -> TwinReport:
    treatment = query(engine, payload)
    control = control_stub(engine, payload)
    if treatment.status == "error":
        delta = "treatment failed"
    elif control.status == "heuristic":
        delta = f"treatment {treatment.status} vs control heuristic"
    else:
        delta = "comparison incomplete"
    return TwinReport(
        claim_id=claim_id or engine,
        treatment=treatment,
        control=control,
        delta=delta,
    )
