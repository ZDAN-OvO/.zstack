Wrote `MIGRATION-PLAN.md`.

The plan's main move: **silent failure isn't a scheduling problem, so a queue alone doesn't meet your goal.** Two jobs died and nobody knew — a worker would swallow them the same way. So Phase 1 wraps each cron job in a runner that records success/exit and alerts on *missed fire*, not just non-zero exit. That phase needs no cutover, so it's free against your 5-minute boundary, and it starts protecting you immediately while migration runs in the background.

Shape of it:
- **Phase 0** inventory + root-cause the two failures (no changes)
- **Phase 1** make cron loud, 7 nights of proof — this is the phase that actually closes the goal
- **Phase 2** stand up queue with a canary, nothing migrated
- **Phase 3** one job per change, risk-ordered, dual-run with cron *disabled* (never both firing)
- **Phase 4** decommission after 7 green nights + runbook

Deliverable is the per-job checklist block (idempotency, overlap, run-late vs skip, "what breaks if it runs twice / late / never") plus the 12-row tracker.

Two things to flag:
1. **No crontab or job scripts in the workspace** — the tracker is `[fill]` placeholders. Paste them and I'll populate it and order Phase 3.
2. Queue choice depends on what's already on the VM (Postgres → `SKIP LOCKED`; Redis → worker; neither → systemd+retry wrapper). I haven't picked, because picking blind is how you end up operating a broker for 12 jobs.

The riskiest unknown is `idempotent` in the tracker: any job that can't safely re-run gets max-attempts=1 and skip-on-miss, and that decision needs your input, not mine.