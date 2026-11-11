Plan written to `/tmp/pf-30-without_skill-msjg14_a/migration-plan.md`.

The short version:

1. **Detection before migration.** The two silent failures were a monitoring gap, not a scheduling gap. Build a success heartbeat (alert if no `success` row in 24h) against cron *as it exists now*, and prove it fires by deliberately breaking a job. That net then protects every cutover.
2. **Minimal on-VM stack.** `jobs` table + one systemd worker + one systemd timer enqueuing the nightly batch, per-job retries/timeouts. No broker — 12 nightly jobs don't justify one, and it's just another thing to operate. Explicitly noted: same VM means the VM dying still kills the queue; the heartbeat is what makes that visible.
3. **One job per change, ordered by blast radius.** Read-only first, backups/billing last. Cutover = enable queue schedule, verify, disable cron line, with rollback as a one-line revert — that's how the 5-minute limit is respected. Two clean nights per job before the next.
4. **The checklist** (section 4) is the deliverable, with a sign-off line, covering exit-code sanity, idempotency/retry safety, timezone mismatch (a common silent-failure cause), and positive proof the job actually did its work.

Three things I'd expect you to argue with, flagged in section 5: retries on non-idempotent jobs should be zero with alert-on-first-failure; a few one-liner jobs are better as systemd timers than queue entries; and the real constraint is the two-night observation per job, so honest duration is ~2–3 weeks, not days.

Assumptions in section 7 need confirming before Phase 0 — especially that a free alert channel already exists, since "no new paid services" makes that load-bearing.

I couldn't read the actual crontab or scripts from here, so the inventory (Phase 0) and each checklist's section A still need filling from those files.