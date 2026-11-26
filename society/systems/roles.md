# Roles

Minimal roles for the residual seed society.

- **proposer** — posts claims to the bus under topic `propose`. Payload is a Claim dict. Does not verify or decide.
- **oracle** — verifies claims. Posts results under topic `verification`.
- **society** — applies keep/hold/revert. Posts decisions under topic `decision`. Keep becomes a candidate. Proven+matched candidates can be accepted under the status contract.
- **twin** — runs treatment/control comparison. Posts under topic `twin`.
- **witness** — reads the append-only record. Does not write except its own notes.

No human gate. Durable acceptance of proven+matched keep candidates is permitted by the society. Conditional and heuristic results remain labeled and do not promote.

Residual seed: status label + append-only witness.
