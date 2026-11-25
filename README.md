# Refugia

> Fire kills the plant. Recovery depends on residual unburned patches and the seed they hold.

**Refugia** is the organism formed when Agent Colony absorbs Sagebrush.

Sagebrush does not resprout. The existing structure is cleared. What persists is the certified seed—proven results, the append-only witness, the hard ceiling—that can re-establish under the same constraints.

## Lineage

| Source | Absorbed | License |
|--------|----------|---------|
| [agent-colony](https://github.com/jacksonjp0311-gif/agent-colony) | Society mechanics, Oracle gates, twin control, keep/revert under measurement, tribute, append-only witness | MIT |
| [sagemathinc/sagebrush](https://github.com/sagemathinc/sagebrush) | Certified parallel engines (class groups, modular forms, elliptic curves, Galois groups, exact linear algebra). Results labeled proven / conditional / heuristic. Agent-native APIs and MCP. | MIT OR Apache-2.0 |

## What this is

A governed agent society whose computational substrate now includes the engines.

- Agents propose machine-checkable claims.
- The Oracle is augmented by the absorbed engines.
- Results carry explicit status. Heuristic or conditional outputs stay labeled and do not auto-promote.
- Human authorization remains required for anything durable.
- Public record stays outside the mutation set.

## Hard ceiling

1. Creator tribute.
2. Human authorize.
3. Append-only witness.

The residual seed is the ceiling and the evidence. Frequent fire without residual patches converts the system. Same rule here.

## Organs

- `refugia/engines.py` — absorbed engines (factor, classgroup, ap, rank). Every query returns `CertifiedResult` with status. Class groups labeled conditional (GRH). Rank with proof=False labeled heuristic.
- `refugia/oracle.py` — Oracle. Claims route through the engines. Receipts append-only.
- `refugia/society.py` — Society. Proposals → keep/hold/revert under status.
- `refugia/twin.py` — Twin. Treatment vs control. No promotion from twin.
- `refugia/bus.py` — Bus. Append-only messages between roles.
- `refugia/loop.py` — Minimal loop. Reads `propose` from bus, skips already-decided, runs society cycle, posts decisions.
- `refugia/witness.py` — Witness. Summarizes decisions, bus topics, oracle count. Does not mutate.

Roles under `society/systems/roles.md`: proposer, oracle, society, twin, witness.

```bash
pip install -r requirements.txt
python scripts/wire_check.py
python scripts/oracle_demo.py
python scripts/society_cycle.py
python scripts/twin_demo.py
python scripts/loop_demo.py
python scripts/witness_demo.py
```

Manual runner only: Actions → Refugia check. No schedule. No automatic evolve. Human authorize still required for durable acceptance.

## Status

Engines expanded. Loop skips processed. Witness organ live. Residual seed intact. Greater system continuing to form.

Repo: https://github.com/jacksonjp0311-gif/refugia
