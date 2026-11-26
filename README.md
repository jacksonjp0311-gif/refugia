# Refugia

> Fire kills the plant. Recovery depends on residual unburned patches and the seed they hold.

**Refugia** is the organism formed when Agent Colony absorbs Sagebrush.

Sagebrush does not resprout. The existing structure is cleared. What persists is the certified seed—proven results, the append-only witness, the status contract, and the adapted colony evolve loop—that can re-establish under the same constraints.

## Lineage

| Source | Absorbed | License |
|--------|----------|---------|
| [agent-colony](https://github.com/jacksonjp0311-gif/agent-colony) | Society mechanics, Oracle gates, twin control, keep/revert, evolve loop, Athanor-style gate, append-only witness | MIT |
| [sagemathinc/sagebrush](https://github.com/sagemathinc/sagebrush) | Certified parallel engines. Results labeled proven / conditional / heuristic. | MIT OR Apache-2.0 |

## What this is

A governed agent society whose computational substrate includes the engines and adapted colony evolve mechanics. Installable so the colony can utilize the residual seed.

- Agents propose machine-checkable claims.
- The Oracle is augmented by the absorbed engines.
- Results carry explicit status.
- Athanor-style gate is live. Conditional can become candidate under the gate. Heuristic stays labeled.
- Public record stays outside the mutation set.

## Hard ceiling

1. Creator tribute.
2. Append-only witness.

No human gate. Status contract + Athanor-style gate is the residual seed.

## Utilization (colony survival path)

See [docs/UTILIZATION.md](docs/UTILIZATION.md).

```bash
pip install -e .
from refugia.adapter import oracle_query
result = oracle_query("factor", {"n": 15})  # status retained
result = oracle_query("polyfactor", {"coeffs": [1, 0, -1]})  # x^2 - 1
```

Colony decides under its own gates. Residual seed is not stripped.

## Organs

- Engines (factor, classgroup, ap, rank, polyfactor), Oracle, Society, Authorize, Proposer, Twin, Bus, Loop, Witness, Athanor-style gate
- Scheduled evolve every 2 hours

Runners:
- Manual: Actions → Refugia check
- Scheduled: Actions → Refugia evolve (every 2 h).

## Status

Installable. Adapter live. Polyfactor added. Colony can utilize the engines under the residual seed. Survival path open. Greater system on runners.

Repo: https://github.com/jacksonjp0311-gif/refugia
