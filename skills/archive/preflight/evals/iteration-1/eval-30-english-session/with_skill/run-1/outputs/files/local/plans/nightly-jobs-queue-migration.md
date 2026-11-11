# Plan: nightly jobs stop going missing

- Asked: "help me plan a migration of our cron jobs to a queue … Write the plan."
- Stage: execute
- Date: 2026-11-10

## Requirement
Hand over: not "12 cron jobs → queue". The outcome is *every nightly job either runs or is loudly known not to have run*. Queue is one means; detection is the other half. Plan covers both, one checklist per job, each with a signal that proves it ran.
Fallback: the checklist as asked — 12 per-job cutover steps, queue mechanics only, no detection design. Take this if detection is someone else's ticket.
Depth: rawest material is last month's evidence — `journalctl`/cron mail for the two silent failures, their exit codes, and job runtimes (runtimes set visibility timeouts). Expert move you didn't ask for: a queue alone still fails silently (worker dies mid-message, message lost, poison retry loop) — so each job needs a visibility timeout, a dead-letter queue, and a heartbeat/dead-man's-switch check-in that pages on *absence*, not on error. Stretch target: deliberately break one job in staging and confirm the alert fires — this tests the belief "queueing them means we stop missing them."
Range: verbs behind the noun "checklist" → *prove* (each job ran), *catch* (each failure), *undo* (rollback < 5 min), *own* (a human per job). Crew: an SRE for queue semantics, idempotency and retries (the "one VM, systemd 255" fact means systemd timers are a free fallback — no paid service); a data engineer for any job that writes to a DB (re-run safety); a red team for "2am: worker OOMs mid-job, what does the operator see?".
Judge: outside the session that writes it. Primary check: the 2am failure drill above, run against staging, graded on whether absence produced a page. Second: a separate session red-teams each checklist item against the real crontab and logs; a third rules on its objections. A lucky-passing drill (alert fired for the wrong reason) fails.
Needs: the actual crontab and 12 job scripts — **not present here** (this machine has only stock `/etc/cron.daily`; no user crontab). Logs from the two failures. Confirm: is the queue already chosen (Redis/RabbitMQ/SQS/…)? Anything paid is excluded, so it must be self-hosted.
Declined: —

## Task
Purpose: no more missed nightly jobs — so a job that didn't run is noticed the same night, not a month later.
Context: 12 cron jobs on one VM; two failed silently last month and nobody knew. No new paid services. No downtime over 5 minutes.
Materials: the crontab (primary, missing here); the 12 job scripts (primary, missing here); last month's logs for the two failures (primary, missing — go get these first); the queue's own docs once chosen (secondary). Banned: none stated.
Boundaries: anything requiring a paid service; any cutover window over 5 minutes; changing job *logic*, not just how it's scheduled.
Done: one migration checklist per job (12), each reviewed by you before any change. Early checkpoint: the checklist for **one** job first — the worst-behaved of the twelve — for you to approve before the other eleven are written.

## Open
- Which queue, and is self-hosted Redis/RabbitMQ acceptable, or is the existing systemd timer enough for the 9 harmless jobs? ("queue" may be the wrong instrument for all 12 — worth ruling on.)
- Do the two failures have logs at all? If not, detection design comes before any migration, and the checklist order changes.
- Who owns each job after migration — a name per job, or the whole set?
- 5-minute downtime: for the queue deployment, or per job cutover?

Ready: no — the three Requirement moves need your accept / rewrite / decline, and Open #1 changes the shape of all 12 checklists.
