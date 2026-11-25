# Roles

Minimal roles for the residual seed society.

- **proposer** — posts claims to the bus under topic `propose`. Payload is a Claim dict. Does not verify or decide.
- **oracle** — verifies claims. Posts results under topic `verification`.
- **society** — applies keep/hold/revert. Posts decisions under topic `decision`. Keep becomes a candidate only.
- **twin** — runs treatment/control comparison. Posts under topic `twin`.
- **witness** — reads the append-only record. Does not write except its own notes.

**Authorization boundary**  
Durable acceptance is not performed by any role. Keep candidates are recorded. Acceptance requires an explicit human flag outside the roles.

Residual seed: every message and decision carries status where applicable. The human gate is part of the seed.
