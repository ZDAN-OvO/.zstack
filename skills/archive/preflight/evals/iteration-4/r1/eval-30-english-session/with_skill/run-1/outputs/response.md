Plan written to `local/plans/cron-to-queue-migration.md`.

Two things I found rather than assumed: this workspace is empty (only `.keep` — no crontab, no scripts, so nothing here is verifiable yet), and "no new paid services" silently removes SQS/Cloud Tasks/Cloud Scheduler from the option set, leaving systemd timers, self-hosted Redis+Celery/RQ, or Postgres `SKIP LOCKED`/pgmq.

The main pushback is the altitude one: a queue does not stop silent failures — it relocates the run. Your two failures were almost certainly invisible for a reason (exit codes dropped, no mail agent, no alert path), and a queue inherits that reason unless detection is designed in. So the plan proposes handing over "every missed/failed/late run alerts and can be replayed", with the per-job checklist as an artifact inside it, and a canary that deliberately kills one job to prove the alert fires. Fallback is the checklist-only version as asked.

Ready is **no** — the Requirement moves are unruled. Answer these and I'll tighten it:

1. Accept the climb (detection + backfill) or take the fallback (checklists only)?
2. Do you know *why* the two jobs failed silently, or is that still open?
3. Can any of the 12 be re-run after a missed slot, or is a late run worse than none?

Drop the crontab and scripts here when you can — without them the classification is a template, not a plan.