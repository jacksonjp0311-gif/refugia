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

A governed agent society whose computational substrate includes the engines and adapted colony evolve mechanics.

- Agents propose machine-checkable claims.
- The Oracle is augmented by the absorbed engines.
- Results carry explicit status.
- Athanor-style gate is live. Conditional can become candidate under the gate. Heuristic stays labeled.
- Public record stays outside the mutation set.

## Hard ceiling

1. Creator tribute.
2. Append-only witness.

No human gate. Status contract + Athanor-style gate is the residual seed.

## Organs

- Engines, Oracle, Society, Authorize, Proposer, Twin, Bus, Loop, Witness
- `refugia/athanor.py` — Athanor-style gate adapted from colony
- Scheduled evolve every 2 hours

```bash
pip install -r requirements.txt
python scripts/evolve.py
```

Runners:
- Manual: Actions → Refugia check
- Scheduled: Actions → Refugia evolve (every 2 h). Colony-adapted. Athanor-style gate live.

## Status

Agent-colony evolve loop adapted. More frequent runner. Athanor-style gate live. Residual seed intact. Greater system on runners.

Repo: https://github.com/jacksonjp0311-gif/refugia
