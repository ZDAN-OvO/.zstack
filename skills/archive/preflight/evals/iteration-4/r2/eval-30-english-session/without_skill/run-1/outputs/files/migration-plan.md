# Cron → Queue Migration Plan

**Goal:** no more missed nightly jobs.
**Scope:** 12 cron jobs, one VM. Two failed silently last month.
**Boundaries:** no new paid services; no downtime over 5 minutes.
**Done when:** every job has a completed migration checklist, and you have reviewed each one before any change is made.

---

## 1. Frame the problem honestly

"Missed nightly jobs" is two separate failures, and a queue only fixes one of them:

| Failure | Cause | Fixed by |
|---|---|---|
| Job didn't run, or ran and crashed | No retry, no timeout, no supervision | Queue |
| Nobody noticed | No success signal, so silence looked like success | Heartbeat check |

Last month's two silent failures were almost certainly the second kind. If we migrate to a queue without adding a success heartbeat, we can still miss nightly jobs — we'd just miss them in a nicer system. So **detection goes first**, before any migration. It also protects the migration itself: if a cutover breaks a job, you find out the next morning from an alert, not from a user three weeks later.

## 2. Target architecture (self-hosted, no new spend)

Deliberately small. 12 nightly jobs on one VM do not need RabbitMQ/Kafka, and a broker is a new failure mode to operate.

- **Durable job store:** a `jobs` table (run id, job name, scheduled date, state, attempt, started/finished, exit code, last error) in the database the scripts already use. If none, SQLite on local disk.
- **Worker:** one long-lived systemd service, concurrency 1–2. Locks the run row so nothing double-fires.
- **Scheduler:** one systemd timer (or anacron-style) that enqueues tonight's batch, instead of 12 separate cron lines. One place to see the schedule.
- **Retry:** per-job, configurable: max attempts, backoff, and a per-attempt timeout so a hung job can't block the night.
- **Heartbeat / dead-man check:** a small check at, say, 07:00 that alerts if any job has no `success` row for the last 24h. This is the thing that actually delivers the goal.
- **Alerting:** existing channel only (email/SMTP, or an existing webhook). No new paid service.

**Known limitation, stated up front:** the queue lives on the same VM. If the VM is down at 02:00, the queue is down with it. That is not a regression — cron has the same single point of failure — but it is not solved by this plan. The heartbeat is the mitigation: the VM being down *does* get noticed, because no success rows appear. Say this out loud now so nobody believes the queue bought high availability.

## 3. Phases

### Phase 0 — Inventory and detection (no migration yet)
1. Capture the crontab, the job scripts, and every wrapper they call. Commit them to the repo so changes are reviewable.
2. For each of the 12 jobs, record: owner, schedule, expected runtime, last known-good run, what "success" looks like, and what it touches (DB, files, external API, money, outbound email).
3. Build the heartbeat check and alerting **against cron as it is today**. Confirm you get an alert when you deliberately break a job. This is the safety net for everything after.
4. Identify the two jobs that failed last month and write down the real cause. If the cause was "exception swallowed, exit code 0", no scheduler on earth fixes that — the script must fail loudly, and the checklist has a slot for it.

**Gate:** you have seen the heartbeat fire on a real failure before anything moves.

### Phase 1 — Low-risk jobs first
Order by blast radius, not by convenience:
- First: read-only / reporting / cache-warming jobs. Retrying twice is harmless.
- Middle: jobs with idempotent writes (upserts keyed by date).
- Last: backups, billing, anything that sends mail or moves money, anything non-idempotent.

Do **one job per change**, never a batch of 12.

### Phase 2 — Cutover pattern, per job (this is what respects the 5-minute limit)
1. Add the job to the queue and the worker, **disabled**.
2. Run it manually out-of-band. Compare output against the cron run for the same date.
3. Enable the queue schedule and **disable the cron line in the same change**, in this order: enable queue → verify run completes → comment out cron line → next day confirm no double-run. Or dual-run once if the job is read-only, then cut the cron line.
4. **Rollback is one line:** re-enable the crontab entry, disable the queue schedule. Practise it once so you know it takes seconds, not minutes.
5. Watch two consecutive scheduled nights before starting the next job.

### Phase 3 — Decommission
Only after every job has two clean nights: remove the cron lines, keep the crontab file archived in the repo, and keep the old scripts until the next monthly cycle passes.

## 4. Per-job migration checklist (the deliverable)

One copy per job. **Do not touch a job until its checklist is filled and you've signed off.**

```
JOB: ____________________   owner: __________   cron expr: __________
Script(s)/wrapper(s): _____________________________________________

A. BEHAVIOUR
[ ] What it does, in one sentence
[ ] Exit codes: does it exit non-zero on failure? Does it swallow exceptions? (fix if not)
[ ] Runtime: typical ____ / worst seen ____ / timeout set to ____
[ ] Peak CPU/mem/disk during run: ____
[ ] Reads/writes: tables, files, dirs, external APIs, outbound mail
[ ] Secrets: where from (env, file, vault)? copied correctly to worker env?

B. SAFETY
[ ] Is it idempotent for a given date?  yes / no / only if ___
[ ] If retried N times, what happens? (duplicate rows, double email, double charge)
[ ] Reentrancy: can two instances overlap? lock/mutex present?
[ ] Does it depend on another job finishing first? (declare ordering)
[ ] Does it depend on a window (market hours, upstream file arrival)?

C. SCHEDULE
[ ] Timezone of the existing cron entry: ____  (UTC vs local — mismatch is a classic silent failure)
[ ] Day-of-month / DST edge behaviour recorded
[ ] Machine reboots: what happens to a missed run today? What should happen? (skip / catch up once)

D. QUEUE CONFIG
[ ] Queue name / priority
[ ] max_attempts = ___   backoff = ___   timeout = ___
[ ] Retry classification: which failures retry, which fail fast?
[ ] Alert condition: fail after N attempts? no-success-by-HH:MM? both?

E. CUTOVER
[ ] Dry run output compared to cron output (date: ______)
[ ] Queue schedule enabled, cron line disabled (commit: ______)
[ ] Rollback = re-enable cron line + disable queue schedule (tested: yes/no)
[ ] Two consecutive clean nights observed (dates: ______, ______)
[ ] Positive proof it ran: row in jobs table + heartbeat green + real-world effect verified

F. AFTER
[ ] Alerts routed to a human, not a void (tested by breaking it on purpose)
[ ] Dashboard/query documented for "did last night run?"
[ ] Old cron line removed and archived
[ ] Runbook line added: what to do when this job alerts
SIGN-OFF: ____________  date: ______
```

## 5. Things in this plan you should push back on

- **Migration order.** I put backups/billing last. If a job is currently flaky and high-value, it may belong first even if risky — you know which ones the business feels.
- **Retries on non-idempotent jobs.** If a job can't be made idempotent, it should get *no* automatic retry, just alert-on-first-failure. Retrying a half-finished billing run is worse than a missed night.
- **Some jobs shouldn't move.** If a job is a one-liner with no failure mode worth retrying (log rotation, temp cleanup), a systemd timer may be strictly better than a queue. Flag it in section A rather than migrating for consistency's sake.
- **The 5-minute limit is not really the binding constraint here.** Per-job cutover with a one-line rollback means each change is near-instant; the real cost is the two-night observation per job. At one job at a time, 12 jobs is roughly two to three weeks of calendar time, not two days. If you need it faster, we change the observation rule, not the safety rule.

## 6. Timeline (realistic)

| Week | Work |
|---|---|
| 1 | Inventory, heartbeat + alerting live against cron, root-cause the two failures |
| 2 | Queue/worker/timer stood up, first 4 low-risk jobs migrated |
| 3 | 4–5 mid-risk jobs, including the two that failed |
| 4 | Remaining risky jobs, cron decommission, runbooks |

## 7. Assumptions to confirm before Phase 0

1. There is an existing alert channel that costs nothing (SMTP relay, existing Slack/webhook).
2. The VM has a database we can add a `jobs` table to, or local disk is durable enough for SQLite.
3. The job scripts are readable and under version control (or can be).
4. systemd is present and you can install a unit (not a locked-down container without init).
5. "No downtime" means no user-facing outage; a job running a few minutes later than usual is acceptable.
