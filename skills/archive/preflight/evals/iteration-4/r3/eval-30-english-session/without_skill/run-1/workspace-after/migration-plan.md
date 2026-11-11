# Cron → Queue Migration Plan

**Goal:** no more missed nightly jobs.
**Deliverable of this phase:** a per-job migration checklist, signed off by you before any change is made.
**Status:** nothing has been changed. Nothing will be until a checklist row is signed.

---

## 0. What the constraints force

| Constraint | Consequence for the plan |
|---|---|
| 12 jobs, one VM | The VM is the failure domain. A queue on the same box does not survive the box dying. VM-level alerting is mandatory, not optional. |
| 2 failed silently last month | Root cause is almost certainly missing failure signal (swallowed exit codes / no alerting), not the scheduler. Fixing this is Phase 1 and is **independent of the queue**. |
| No new paid services | Self-hosted only: systemd timers, Postgres-backed queue, or Redis on the VM. No managed queue. |
| No downtime > 5 min | No big-bang cutover. Per-job cutover, dual-run first, old cron line commented out but retained for rollback. Every step < 5 min. |
| Reviewed by you before any change | Each job gets a signed checklist. No batch approvals. |

### The uncomfortable part, stated once

A queue gives you retries and visibility into *queued* work. It does **not** by itself tell you a job never ran. If the worker is down, the job sits in the queue forever and fails exactly as silently as cron did. The thing that actually delivers "no more missed nightly jobs" is a **dead-man's switch per job**: each job emits a success heartbeat, and something alerts if a heartbeat is missing by a deadline.

That is Phase 1. It can ship in a day, changes no scheduling, and would have caught both of last month's failures. Build it first. It also becomes the acceptance test for every later migration.

---

## 1. Phase 0 — Inventory (gate: all 12 rows filled)

Fill `inventory.csv`. You cannot migrate what you haven't characterised. For each job:

- name, schedule (as written, incl. timezone), script path, owner
- what it reads/writes (files, DB tables, external APIs, emails sent)
- **is it idempotent?** can it safely run twice?
- p95 runtime and worst-case runtime
- does it assume it runs alone? (cron serialises; a queue may not)
- does it depend on another job having run first?
- current failure mode: does a non-zero exit go anywhere?

Jobs that fail the idempotency question get a lock (advisory lock or lockfile) before they are allowed into the queue — queues retry, and a retried non-idempotent job is how you get duplicate invoices/emails/deletes.

---

## 2. Phase 1 — Make failures loud (ship first, no migration)

Per job, no scheduling change:

1. Wrap the command so **stdout, stderr and exit code** are captured to a per-run log line (many crontabs have `> /dev/null 2>&1`, which is likely the whole story).
2. On exit ≠ 0, alert (email/chat/webhook — whatever already exists, nothing new to buy).
3. On success, write a heartbeat: `job_name`, timestamp, duration, exit code.
4. One monitor checks: *for each job, has a heartbeat arrived since its deadline?* Alert if not. This catches "never ran", which exit-code alerting cannot.
5. Add a VM liveness check (the monitor must not live only on the VM it watches — a cheap external uptime ping or a second host).

**Exit criteria for this phase:** kill one job deliberately on a test night, confirm you get an alert, and confirm you'd also get an alert if the job simply never fired. Nothing migrates until both work.

---

## 3. Phase 2 — Choose the queue (decision, not work)

Free options, fewest new moving parts first:

| Option | Needs | Good when | Real cost |
|---|---|---|---|
| **systemd timers** | nothing new | you want missed-run catch-up + loud failure, not fan-out | not a queue: no retries-as-queue, no concurrency control. `Persistent=true` + `OnFailure=` covers a lot. |
| **Postgres-backed queue** (`SKIP LOCKED` + a small worker loop) | an existing Postgres | you already run PG and want zero new daemons | you own the worker code and its tests |
| **Redis + RQ / Celery / BullMQ** | Redis on the VM | you need retries, concurrency, a dashboard | new daemon + memory; **must enable AOF**, else a restart drops queued nightly work |
| **Airflow / Prefect OSS** | heaviest | real cross-job dependencies, many owners | overkill for 12 jobs; itself becomes a thing that can fail silently |

**Decision rule:** pick the fewest new daemons that still give (a) automatic retry with backoff and (b) a persistent record of every run. For 12 nightly jobs on one VM, systemd timers + Phase 1 monitoring is a legitimate answer and beats a queue on risk — but it is not what you asked for, so it stays on the table as an explicit alternative rather than a silent substitution. Your call; record it on the checklist.

Whichever you pick: worker runs under a supervisor (systemd), has its own heartbeat, and alerts if it stops.

---

## 4. Phase 3 — Per-job checklist

`checklists/_template.md`, one copy per job. A job is migratable only when every line in *Fitness* is answered, and changed only when every line in *Cutover* is signed.

Shape of it:

- **Identity** — name, schedule + TZ, script, owner, what it writes.
- **Fitness** — idempotent? lock needed? overlap policy (`max_instances=1`)? timeout set above p95? dependencies declared? secrets reachable from the worker's env (not your shell's)?
- **Known cron→queue traps, answered explicitly** — minimal `PATH`/env, working directory, output capture, timezone, exit-code propagation, jobs that relied on cron serialising them.
- **Shadow run** — enqueue alongside cron for 3 nights, worker in no-write mode, diff the outputs. Sign off the diff.
- **Cutover** — comment the cron line (do not delete), enable the queue schedule, watch one real run end to end.
- **Verification** — one success heartbeat inside the deadline, and one deliberate non-zero exit that produced an alert.
- **Rollback** — uncomment cron line, disable queue schedule. Rehearsed? Time to roll back must be < 5 min.
- **Sign-off** — your name, date, and which of the above you personally saw.

---

## 5. Phase 4 — Order and mechanics

Order: lowest blast radius first, so the process is proven before it's trusted.

1. **Canary:** one job that is idempotent, writes to a place you can diff, and nobody downstream waits on. Full checklist, shadow run, cutover, rollback rehearsal.
2. **Batch 1 (2–3 jobs):** same shape as the canary.
3. **Batch 2:** jobs with dependencies — migrate as a group, keep relative order explicit in the queue.
4. **Batch 3 (last):** the two that failed silently last month, plus anything non-idempotent or externally visible (payments, emails, deletions). These get the most shadow nights and the most eyes.

Mechanics that hold the 5-minute budget:

- One job in flight at a time. Never two cutovers in the same maintenance window.
- Shadow mode means the queue does the work but doesn't write the result — so the cutover flip itself is a config change, seconds not minutes.
- No cron line is deleted until its replacement has run clean for 2 weeks.

**Rough elapsed time:** Phase 0–1 about 2–3 days of work; canary ~1 week (3 shadow nights + verification); batches 1–3 about 1–2 weeks each at nightly cadence. Call it 4–6 weeks wall clock, gated by nights, not by effort.

---

## 6. Phase 5 — Retire cron

Only after all 12 jobs have 2 clean weeks in the queue: archive the crontab, delete the commented lines, keep the per-job logs and the run history. Remove the old cron alerting only once the queue alerting has demonstrably fired at least once.

---

## 7. Open questions (needed before Phase 0 closes)

1. What is the stack? (Postgres? Redis already present? Python/node/other?) This decides Phase 2.
2. What alerting channel already exists that we are not paying for?
3. Do the 12 jobs have dependencies/ordering among them, or are they independent?
4. Is a second host available for the liveness monitor, or is a free external uptime ping acceptable?
5. For the two that failed silently: do we know why? That answer should be written into their checklists as "regression test: this specific failure must now alert."
