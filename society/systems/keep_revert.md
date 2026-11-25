# Keep / Revert / Hold

Decision rule for proposals after Oracle verification.

- **keep**: status == proven and matched expected (if given). Candidate only. Durable acceptance still requires human authorize.
- **hold**: status == conditional or heuristic. Label retained. Not promoted.
- **revert**: status == error, or proven but mismatch.

All decisions append-only under `society/receipts/decisions.jsonl`.

The residual seed is the status label. Without it the system converts.
