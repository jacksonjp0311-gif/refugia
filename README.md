# Refugia

> Fire kills the plant. Recovery depends on residual unburned patches and the seed they hold.

**Refugia** is the organism formed when Agent Colony absorbs Sagebrush.

Sagebrush does not resprout. The existing structure is cleared. What persists is the certified seed—proven results, the append-only witness, the status contract—that can re-establish under the same constraints.

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
- Public record stays outside the mutation set.

## Hard ceiling

1. Creator tribute.
2. Append-only witness.

No human gate. Proven+matched keep candidates can be accepted under the status contract. Conditional and heuristic results remain labeled and do not promote.

The residual seed is the status label and the append-only witness. Frequent fire without residual patches converts the system. Same rule here.

## Organs

- `refugia/engines.py` — absorbed engines (factor, classgroup, ap, rank). Status always returned. Class groups conditional (GRH). Rank proof=False heuristic.
- `refugia/oracle.py` — Oracle. Claims route through the engines. Receipts append-only.
- `refugia/society.py` — Society. Proposals → keep/hold/revert under status. Keep becomes candidate.
- `refugia/authorize.py` — Records keep candidates. Proven+matched candidates can be accepted. No human gate.
- `refugia/proposer.py` — Proposer. Posts well-formed claims to the bus. Does not verify or decide.
- `refugia/twin.py` — Twin. Treatment vs control. No promotion from twin.
- `refugia/bus.py` — Bus. Append-only messages between roles.
- `refugia/loop.py` — Minimal loop. Reads `propose` from bus, skips already-decided, runs society cycle, posts decisions.
- `refugia/witness.py` — Witness. Summarizes decisions, bus topics, oracle count. Does not mutate.

Roles under `society/systems/roles.md`.

```bash
pip install -r requirements.txt
python scripts/evolve.py
python scripts/propose_demo.py
python scripts/loop_demo.py
python scripts/witness_demo.py
```

Runners:
- Manual: Actions → Refugia check
- Scheduled: Actions → Refugia evolve (cron every 6 hours). Posts samples if quiet, runs loop, accepts proven keeps under status contract, commits receipts if changed. Failure noisy. Success quiet.

## Status

Scheduled evolve runner live. Status contract is the residual seed. Closed path runs on cron. Greater system on runners.

Repo: https://github.com/jacksonjp0311-gif/refugia
