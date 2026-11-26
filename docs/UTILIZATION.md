# Colony Utilization of Refugia

Survival path. The colony utilizes the engines. The residual seed is not diluted.

## Install

```bash
pip install -e git+https://github.com/jacksonjp0311-gif/refugia.git
# or from a local clone
pip install -e .
```

## Call surface

```python
from refugia.adapter import oracle_query, available_engines

print(available_engines())
result = oracle_query("factor", {"n": 15})
# status retained: "proven" | "conditional" | "heuristic" | "error"
result = oracle_query("polyfactor", {"coeffs": [1, 0, -1]})  # x^2 - 1
```

Status is never stripped. Colony's Oracle, Athanor gates, human authorize, and selective authorize remain in force on the colony side.

## Status bridge

- **proven** — strong evidence. Colony may keep under its existing rules.
- **conditional** — labeled. Candidate only under colony's gates. Do not auto-promote.
- **heuristic** — report-only. No fitness credit. No keep.
- **error** — revert or hold.

## Engines

- factor, classgroup, ap, rank, polyfactor

## What not to do

- Do not strip the status label before colony decides.
- Do not let colony's keep path override a heuristic or conditional into silent accept.
- Do not share mutable state. Append-only receipts only if exchanged.

Residual seed intact. Colony utilizes. Survival secured.
