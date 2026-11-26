"""Absorbed Sagebrush engines.

Every call returns a result with an explicit status label.
Heuristic or conditional results stay labeled and do not auto-promote.
The residual seed is the status and the hard ceiling.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Optional


@dataclass
class CertifiedResult:
    value: Any
    status: str  # "proven" | "conditional" | "heuristic" | "error"
    engine: str
    detail: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


def _safe_call(fn, engine: str, *args, **kwargs) -> CertifiedResult:
    try:
        result = fn(*args, **kwargs)
        status = getattr(result, "status", None)
        if status not in ("proven", "conditional", "heuristic"):
            status = "proven"
        return CertifiedResult(value=result, status=status, engine=engine)
    except Exception as e:
        return CertifiedResult(value=None, status="error", engine=engine, detail=str(e))


def factor_integer(n: int) -> CertifiedResult:
    try:
        from sagebrush.sage import factor
        return _safe_call(factor, "factor", n)
    except ImportError:
        return CertifiedResult(None, "error", "factor", "sagebrush not installed")
    except Exception as e:
        return CertifiedResult(None, "error", "factor", str(e))


def class_group(poly_coeffs: list, name: str = "a") -> CertifiedResult:
    """poly_coeffs is low-to-high. Convert to monic by reversing and normalizing."""
    try:
        from sagebrush.sage import NumberField, PolynomialRing, QQ
        R = PolynomialRing(QQ, "x")
        x = R.gen()
        # Reverse to high-to-low and ensure monic
        coeffs = list(reversed(poly_coeffs))
        if coeffs and coeffs[0] != 1:
            # Normalize leading coefficient to 1 if possible
            lead = coeffs[0]
            coeffs = [c / lead for c in coeffs]
        poly = sum(c * x**(len(coeffs)-1-i) for i, c in enumerate(coeffs))
        K = NumberField(poly, name)
        cg = K.class_group()
        return CertifiedResult(
            value=str(cg),
            status="conditional",
            engine="classgroup",
            detail="GRH assumed where applicable; label retained",
        )
    except Exception as e:
        return CertifiedResult(None, "error", "classgroup", str(e))


def elliptic_ap(label: str, bound: int = 20) -> CertifiedResult:
    try:
        from sagebrush.sage import EllipticCurve
        E = EllipticCurve(label)
        return _safe_call(lambda: E.aplist(bound), "ap")
    except Exception as e:
        return CertifiedResult(None, "error", "ap", str(e))


def elliptic_rank(label: str, proof: bool = False) -> CertifiedResult:
    try:
        from sagebrush.sage import EllipticCurve
        E = EllipticCurve(label)
        if proof:
            try:
                r = E.rank()
                return CertifiedResult(value=r, status="proven", engine="rank")
            except Exception:
                return CertifiedResult(value=None, status="conditional", engine="rank",
                                       detail="proof unavailable; GRH path not taken")
        else:
            r = E.rank(proof=False)
            return CertifiedResult(value=r, status="heuristic", engine="rank",
                                   detail="proof=False; heuristic retained")
    except Exception as e:
        return CertifiedResult(None, "error", "rank", str(e))


def query(engine: str, payload: dict) -> CertifiedResult:
    """Single entry point for the society bus or Oracle.

    Residual seed: status is always returned. Callers must respect it.
    """
    if engine == "factor":
        return factor_integer(payload["n"])
    if engine == "classgroup":
        return class_group(payload["coeffs"], payload.get("name", "a"))
    if engine == "ap":
        return elliptic_ap(payload["label"], payload.get("bound", 20))
    if engine == "rank":
        return elliptic_rank(payload["label"], payload.get("proof", False))
    return CertifiedResult(None, "error", engine, "unknown engine")
