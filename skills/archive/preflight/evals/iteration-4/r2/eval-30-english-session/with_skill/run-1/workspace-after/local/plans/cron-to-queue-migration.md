# Plan: nightly jobs that cannot fail silently

- Asked: "help me plan a migration of our cron jobs to a queue"
- Stage: execute
- Date: 2026-11-10

## Requirement

Hand over: **the 12 jobs report a run or a miss, and a miss reaches a human within minutes** — the queue is one way to get there, not the goal. *(Why the climb: the two failures were silent. A queue with no failure path stays silent too, so the migration as asked can leave you with the same bug.)*
Fallback: keep cron; wrap each job in a heartbeat + `OnFailure=`-style alert so a missed run pages someone. Cheaper, meets the wall, and can ship job by job.
Depth: find out *why* the two were silent — swallowed exit codes, cron mail to a dead mailbox, no alert on non-zero exit. Raw material: the crontab, the job scripts, journal/syslog lines and exit codes from last month. Instruments: run ledger (job, start, end, exit), dead-man's-switch check, retry with idempotency guard. Stretch: replay last month's two failed runs through the new path and show both would have been caught.
Range: verbs — *catch a failed run*, *retry it safely*, *tell a human*, *prove it ran*. Crew: SRE/on-call (detection path, who gets paged), data engineer (which of the 12 are safe to retry twice), red team (kill a job mid-run, fill the disk, expire a credential — name which of the 12 go silent again), cost reviewer (every option must be self-hosted at zero marginal cost).
Judge: the replay + red-team kill test on a clone, run outside this session — grades method (does it catch failures it was not tuned for) as well as the checklist. Your own review of the checklist stays the gate before any change.
Needs: the crontab and job scripts (**not in this workspace — empty repo**); last month's failure evidence (which two jobs, when, why no alert); a non-production clone to test on (your 5-minute wall); confirmation that self-hosted queue (Postgres/Redis/RabbitMQ/systemd) is acceptable; who receives the alert.
Declined: —

## Task

Purpose: no more missed nightly jobs.
Context: 12 cron jobs on one VM; two failed silently last month. *(Fact check: none of this is verifiable from the workspace — it is all your account.)*
Materials: the crontab and job scripts (primary). Nothing else ranked. Missing: the failure evidence — which two jobs failed, when, and why nobody was told.
Boundaries: no new paid services. No downtime over 5 minutes.
Done: a migration checklist per job, reviewed by you before any change.

## Open

- "No missed jobs": does that mean the job always completes, or that a miss is always *known* within some window? The fallback covers the second, the queue covers the first, and the two cost very differently.
- Whether the queue is required at all, or whether alerting alone closes the two silent failures.
- Nothing in the repo — so every fact above is unverified, and Needs is unmet.

Ready: no — the three Requirement moves (altitude, depth, range) await your accept/rewrite/decline, and Materials lacks the failure evidence.
