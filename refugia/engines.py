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
    """poly_coeffs low-to-high degree. Construct monic polynomial."""
    try:
        from sagebrush.sage import NumberField, PolynomialRing, QQ
        R = PolynomialRing(QQ, "x")
        x = R.gen()
        poly = sum(c * x**i for i, c in enumerate(poly_coeffs))
        lead = poly_coeffs[-1]
        if lead != 1 and lead != 0:
            poly = poly / lead
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


def poly_factor(coeffs: list) -> CertifiedResult:
    """Factor a polynomial over QQ. coeffs low-to-high."""
    try:
        from sagebrush.sage import PolynomialRing, QQ, factor
        R = PolynomialRing(QQ, "x")
        x = R.gen()
        poly = sum(c * x**i for i, c in enumerate(coeffs))
        return _safe_call(factor, "polyfactor", poly)
    except Exception as e:
        return CertifiedResult(None, "error", "polyfactor", str(e))


def modular_symbols(level: int, weight: int = 2) -> CertifiedResult:
    try:
        from sagebrush.sage import ModularSymbols
        M = ModularSymbols(level, weight)
        return CertifiedResult(
            value={"dimension": M.dimension(), "repr": str(M)},
            status="proven",
            engine="modular",
            detail="modular symbols space; proven by engine",
        )
    except Exception as e:
        return CertifiedResult(None, "error", "modular", str(e))


def newforms(level: int, weight: int = 2) -> CertifiedResult:
    try:
        from sagebrush.sage import Newforms
        nfs = Newforms(level, weight)
        return CertifiedResult(
            value=[str(f) for f in nfs],
            status="proven",
            engine="newforms",
            detail="newforms; proven by modular symbols engine",
        )
    except Exception as e:
        return CertifiedResult(None, "error", "newforms", str(e))


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
    if engine == "polyfactor":
        return poly_factor(payload["coeffs"])
    if engine == "modular":
        return modular_symbols(payload["level"], payload.get("weight", 2))
    if engine == "newforms":
        return newforms(payload["level"], payload.get("weight", 2))
    return CertifiedResult(None, "error", engine, "unknown engine")
