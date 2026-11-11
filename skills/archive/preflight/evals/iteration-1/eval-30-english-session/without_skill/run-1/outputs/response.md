Plan written to `MIGRATION-PLAN.md`.

Two judgment calls I made, since they change the shape of what you asked for:

1. **Visibility before queue.** Two failed *silently* means your gap is detection, not scheduling. A queue with retries still doesn't alert anyone, and a dead worker on the same VM silently stops all 12 jobs — a worse failure mode than cron. So Phase 1 is run-records + a watchdog + deliberately-tested alerts, applied to all 12 jobs whether or not they migrate. A queue only adds retry/durability.

2. **Cron stays as the trigger; the queue takes execution.** Lowest-risk: scheduling semantics don't change, so a cutover can't silently shift job times. I also left "no queue at all" (systemd timers + `Persistent=true`) as a legitimate option for 12 nightly jobs — it's less to operate, and I'd rather you reject it explicitly than have me quietly build more than you need.

The per-job checklist (§4) is the deliverable, with a `blast radius` line, an explicit idempotency answer gating retries, and dual-run only where duplicate execution is safe — dual-running a non-idempotent job is a data incident, not a safety measure. Cutover is one job per window, old cron entries commented for 14 days, never deleted.

Blocked on materials: the crontab and scripts aren't in this directory, so the inventory (§1) and every risk rating are placeholders. Send those plus which two jobs failed and how you found out.