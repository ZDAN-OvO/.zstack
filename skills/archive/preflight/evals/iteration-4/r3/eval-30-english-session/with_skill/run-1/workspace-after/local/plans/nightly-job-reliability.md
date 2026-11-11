# Plan: No more silently missed nightly jobs

- Asked: "help me plan a migration of our cron jobs to a queue"
- Stage: execute
- Date: 2026-11-10

## Requirement

**Hand over (proposed rung above the request):** every one of the 12 nightly jobs either completes or raises a human-visible alarm within a stated window — a miss can never again go unnoticed for a month. The queue becomes one option inside that guarantee, not the goal.

**Fallback (the request as written):** a per-job migration checklist, reviewed before any change. Take this if the rung above needs access you do not have yet (logs, alert channel, queue host).

**Depth:** the expert move not asked for is *measure before you migrate*. Rawest material: cron/journal logs, per-job exit codes, start/end times, overlap, and the last-run timestamps of the two silent failures — to establish whether they ever reached cron. Instruments: per-job contract (schedule, max runtime, idempotency, downstream readers), at-least-once vs at-most-once reasoning, retry with backoff, dead-letter visibility, and a heartbeat/dead-man's-switch on the schedule itself. *Stretch target:* replay 12 jobs under injected faults (worker killed mid-run, DST/weekend skip, duplicate delivery, job outliving its lock, no network) and show each job either completes or alarms — zero silent misses. *Belief to test:* "a queue prevents missed jobs." A queue prevents lost messages; if the enqueuer dies the queue stays empty and silent. That reframes the whole plan around the scheduler and the alarm, not the broker.

**Range:** the deliverable's verbs — (1) make the current failure modes visible, (2) decide a delivery guarantee per job, (3) make each job safe to re-run, (4) make a miss loud, (5) keep rollback and manual run in an operator's hands. Crew: a reliability/SRE engineer for guarantees, SLO and alerting; a Postgres/Redis person for a transactional enqueue (`SKIP LOCKED`) if the queue is DB-backed; a security reviewer for secrets in job scripts and egress; red team: someone paid to make the migration *lose* a job — kills workers, duplicates, drifts the clock, runs the job twice.

**Judge:** an outside session running the fault-injection harness above, plus one per-job duplicate-run test. It grades method as well as result: each checklist item must name its guarantee, its alarm and the evidence line it came from (log, script, or a stated assumption), and each of the two past failures must be traced to a primary log line or marked unresolved. Your own review of the checklist is the second judge, not the first.

**Needs:** crontab, the 12 job scripts, 30–90 days of cron/exec logs, the identity and logs of the two failed jobs, downstream readers per job, what software/egress the VM already has, and whether a queue may run on the same VM. *Missing: all of it — the workspace is empty; no crontab or script was found.*

**Declined:** none yet.

## Task

**Purpose:** no more missed nightly jobs. Two failed silently last month.
**Context:** 12 cron jobs on one VM. *(User-stated, confirm: single host, so a queue on that host is still one point of failure.)*
**Materials:** primary — the crontab and job scripts. Add, ranked: cron/exec logs and the failed jobs' own output. Banned: undocumented blog configs, assumed job behaviour. Not found → leave blank, do not invent.
**Boundaries:** no new paid services. No downtime over 5 minutes. *(Proposed walls, accept or reject: never change a job's business logic; never retire a cron entry before its replacement has proven a full cycle; no big-bang cutover night; no secrets in the queue payload.)*
**Done:** a migration checklist per job, reviewed by you before any change. *(Proposed shape: first a one-page reliability map — per job: trigger, guarantee, what breaks it, how a miss becomes visible — approved by you, then the per-job checklists. Markdown, one page per job.)*

## Open

- Is the queue required by the goal, or is the missing piece detection, retries and idempotency? The two silent failures suggest the latter.
- Root cause of the two silent failures: never ran, ran and errored, or ran and did nothing?
- Are the jobs idempotent today? Cannot tell without the scripts.
- Where does an alarm go at 03:00, and who acts on it?
- Does "no downtime over 5 minutes" mean per job, or the whole nightly batch?
- Does the queue host get to be a second machine, or must it share the VM?

## Tries

*(none yet)*

---

Ready: no — the three Requirement moves above are proposed, not ruled; the workspace holds none of the Materials.
