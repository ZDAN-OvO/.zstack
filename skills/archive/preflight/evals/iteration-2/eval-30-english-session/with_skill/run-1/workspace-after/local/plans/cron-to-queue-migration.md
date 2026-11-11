# Plan: no more missed nightly jobs

- Asked: "help me plan a migration of our cron jobs to a queue" — done: "a migration checklist per job, reviewed by me before any change"
- Stage: execute
- Date: 2026-11-10

## Requirement
Hand over: the request as asked — a per-job migration checklist, reviewed by you before any change — **plus** the check that would have caught last month's two silent failures, since a migration alone does not give you that.
Fallback: the checklists only, if the failure-detection work exceeds what you want to own.
Depth: classify all 12 jobs from the raw crontab and scripts before drafting anything — overlap risk, idempotency, runtime vs. interval, secrets, local state, exit codes. Silent failure usually means a job that exited 0, exited non-zero into unread mail, or did not run at all; those are three different fixes. Logs from the two failures decide which. Instruments: the actual scripts, not a summary of them.
Range: *make failures impossible to miss*, *keep every job running while it moves*, *prove each job still does its work after the move*. Crew: a reliability engineer (idempotency, retries, overlap, alerting) and you as the owner who knows what each job is for; a red team that kills a job mid-run and confirms you were told.
Judge: your review of each checklist before any change — you can judge this directly. Second check: disable one migrated job and confirm an alert arrives before the other 11 move.
Needs: **missing** — the crontab and the 12 job scripts are not in this workspace (`crontab -l` is empty for this user), and the logs from the two failures are not here. Also missing: which queue you mean, and whether it may run on the same VM.
Proposed: (1) prove one job end-to-end, including its alert, before drafting checklists for the other 11; (2) decide up front whether a self-hosted broker on that VM is acceptable — a queue on the same host does not survive a VM-level outage, which is the failure mode cron also has; (3) treat "queue" as one means, and let the checklist state per job whether a retrying scheduler (e.g. systemd timers + a wrapper) already meets the goal.
Declined: —

## Task
Purpose: no more missed nightly jobs — you can no longer tell when one failed, and you want to be told.
Context: 12 cron jobs on one VM; two failed silently last month; no new paid services; no downtime over 5 minutes.
Materials: the crontab (primary), the 12 job scripts (primary), logs of the two failures (primary, not found), your memory of what each job is for (primary). Banned: none stated.
Boundaries: no new paid services; no downtime over 5 minutes; nothing changes until you have reviewed the checklist.
Done: a migration checklist per job, reviewed by you before any change. **Checkpoint:** the first job's checklist, in front of you, before the other 11 are drafted.

## Open
- What the two silent failures actually were — cause cannot be decided without their logs, and the fix differs per cause.
- Whether the queue is self-hosted on the same VM or a scheduler; this decides the whole migration.
- Who receives the alert, and through which channel — an alert nobody reads repeats last month.

Ready: no — the named materials are absent, the queue choice is open, and the three proposed moves await your ruling.
