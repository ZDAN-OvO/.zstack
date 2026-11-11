# Plan: nightly cron jobs that cannot fail silently

- Asked: "help me plan a migration of our cron jobs to a queue"
- Stage: execute
- Date: 2026-11-10

## Requirement

Hand over (proposed, not yet ruled): rung 3 of the ladder, not the rung asked for. Not "a checklist per job", but *every job whose run is missing, failed or late produces an alert within N minutes, and a missed run can be replayed on purpose* — with the per-job checklist as one artifact inside that. A queue does not detect silent failure; it only moves the run somewhere else. Detection is the part that fixes what bit you.
Fallback: rung 1 as written — 12 per-job migration checklists, no monitoring or backfill design. Take this if rung 3 is too big for one pass.
Depth: the expert move you did not ask for is *classify before you choose a queue*. All 12 jobs get tagged: idempotent vs not, runtime, needs a lock, has downstream consumers, safe to replay, and — the key one — *is a missed run even visible today?* Two failed silently, so the answer for at least two is "no"; if the rest are `2>/dev/null` with no mail agent, the true count is higher than two. Instruments: the crontab as raw text, cron/journal logs for the failure dates, exit codes, and self-hosted-only queue options (systemd timers + `OnFailure=`, Redis/Celery or RQ on the VM, or Postgres `SKIP LOCKED`/pgmq if you already run Postgres) — chosen because "no new paid services" removes SQS/Cloud Tasks.
Stretch target: prove the detection actually works by disabling one job in a canary and confirming the alert fires, before touching the other 11. This tests the belief that "moving to a queue stops silent failures" against held-out behaviour rather than against the migration's own output.
Range: the deliverable's verbs are *enumerate, classify, map, prove, sequence, roll back*. Crew: reliability engineer (alert thresholds, "missed" definition, runbook, on-call path), backend/data engineer (idempotency keys, replay/backfill, retries and poison messages), the queue implementer (deployment within the 5-minute window), and a red team whose job is to assume every job is non-idempotent and that the queue loses or duplicates runs during cutover.
Judge: your review of the checklists (your stated Done) plus one test the work can run itself — canary job stops, alert arrives, missed run is replayed correctly, with the script and log output attached. Grades method as well as result: a checklist with no detection test per job fails even if the queue is deployed.
Needs: crontab and the 12 scripts (absent here — this workspace holds only `.keep`, so nothing can be verified from files yet); cron/journal logs around the two failures; whether mail or any alerting is configured; owner per job; your definition of the nightly window; VM specs and whether Postgres/Redis are already present. Missing: all of it.
Declined: none yet — no Requirement move has been accepted or refused. "No new paid services" is recorded as a wall, which eliminates managed queues from the option set rather than as a declined move.

## Task

Purpose: "no more missed nightly jobs."
Context: "12 cron jobs on one VM, two failed silently last month." Found, for you to confirm: this workspace has no crontab and no job scripts, so the plan below is structure, not evidence. Also worth knowing before you pick a queue — if the two failures were silent, the cause is likely absent exit-code capture or alerting, which a queue inherits unless it is designed in.
Materials: 1) the crontab and the 12 job scripts (primary), 2) cron/journal logs covering the two failures, 3) any existing runbook or ownership notes. Banned: none stated. Empty slot: the two incident records / logs — not supplied.
Boundaries: "no new paid services"; "no downtime over 5 minutes". Walls, both of them.
Done: "a migration checklist per job, reviewed by me before any change." Checkpoint, in your words' spirit: one canary job fully cut over and reviewed before the other 11, so a wrong approach costs one job, not twelve.

## Open

- Which queue, given free/self-hosted only — and whether Postgres or Redis already exists on the VM.
- Root cause of the two silent failures: still unknown, and it decides whether the queue is the fix or the alarm is.
- Whether any of the 12 can be re-run safely after a missed slot, or whether a late run is worse than no run.
- What "nightly" means per job (fixed time vs "before 06:00"), since queue delivery is not time-based by default.
- Whether the 5-minute downtime limit is total or per job, and whether a maintenance window exists.
- Who owns each job and who receives the alert — an alert with no owner is another silent failure.

Ready: no — Requirement moves (altitude, depth, range, judge) are unruled, and Materials lists the crontab and scripts but none are in this workspace.

Plan written to `local/plans/cron-to-queue-migration.md`. Once you have ruled on the Requirement lines and dropped the crontab and scripts in, `/define-goal` can take this plan as its source.
