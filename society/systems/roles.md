# Roles

Minimal roles for the residual seed society.

- **proposer** — posts claims to the bus under topic `propose`. Payload is a Claim dict.
- **oracle** — verifies claims. Posts results under topic `verification`.
- **society** — applies keep/hold/revert. Posts decisions under topic `decision`.
- **twin** — runs treatment/control comparison. Posts under topic `twin`.
- **witness** — reads the append-only record. Does not write except its own notes.

Human authorize remains outside the roles. Durable acceptance is not performed by any role.

Residual seed: every message and decision carries status where applicable.
