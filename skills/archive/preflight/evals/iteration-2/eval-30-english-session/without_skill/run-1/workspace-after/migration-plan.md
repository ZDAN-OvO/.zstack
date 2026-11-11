# Cron → Queue Migration Plan

**Goal:** zero missed nightly jobs.
**Constraints:** 12 jobs on one VM · no new paid services · ≤5 min downtime · nothing changes without your review.
**Deliverable:** one checklist per job, reviewed and signed off before that job is touched.

---

## 0. The thing that has to be said first

A queue does not fix "missed nightly jobs." It fixes *retries* and *durability of enqueued work*. The two failures last month were **silent**, which means the actual defect is detection, not scheduling.

Worse: a naive migration makes silence *more* likely. Today 2 of 12 jobs fail quietly. After migration, one dead worker or one full disk means **12 of 12 fail quietly**. So the ordering below is deliberate — instrumentation first, queue second. If we did it the other way we would be widening the blast radius of the exact problem we're solving.

Second honesty check: all 12 jobs live on one VM. A queue on that same VM does not survive the VM dying, and it does not catch up jobs missed while it was down. At least one part of this plan (boot-time catch-up) is what actually delivers the goal, and it does not require a queue at all. It's still worth doing the migration — but for operability, not as the fix.

---

## 1. Phase 0 — Inventory and forensics (no changes to any job)

Blocking. Nothing else starts until this is done.

1. `crontab -l > crontab.backup.$(date +%F)` for every user with a crontab, plus `/etc/cron.d/*`, `/etc/cron.{daily,hourly}`, and any systemd timers already in play. Commit to git. This is the rollback artifact.
2. For each of the 12 jobs, fill the **Job Card** in §4.
3. **Identify the two silent failures.** Pull the evidence before it rotates:
   - `journalctl -u cron --since '2 months ago'`, `/var/log/syslog*`, `/var/log/cron*`
   - each script's own log/output destination
   - `last reboot`, `dmesg`, `apt` history, disk-full events in the window
4. Root-cause each into one of:
   - **Didn't fire** (host down/asleep, cron daemon, DST, bad schedule, crontab edited)
   - **Fired, failed, nobody told** (no alerting / alert went to a mailbox nobody reads)
   - **Fired, exited 0, did nothing** (script lies about success — most common and most dangerous)
5. Write the one-line finding per job. These findings set the migration order in §6 and may change the tech choice in §2.

**Exit criterion:** every job has a Job Card; both silent failures have a named root cause; the crontab is in git.

---

## 2. Phase 1 — Choose the queue (constrained to what you already run)

Pick in this order; stop at the first that's true.

| If you already have… | Use | Notes for this goal |
|---|---|---|
| PostgreSQL | **Postgres table + `FOR UPDATE SKIP LOCKED`** | Best fit. Enqueue in the same transaction as the job's own writes; job state is queryable with SQL; no new service, no new cost, survives restarts. Needs a tiny worker loop, but it's ~100 lines and fully inspectable. |
| Redis (already installed, with AOF on) | Redis + a small worker | Fine, lighter. Require `appendonly yes` and `appendfsync everysec`, or a restart eats queued jobs. |
| Nothing, and you don't want a broker | **systemd timers** | Not a queue, but delivers most of the goal: `Persistent=true` runs missed jobs on boot, `OnFailure=` alerts, journald logging for free. Consider this as the *fallback* target for jobs too fragile to migrate. |
| An already-paid cloud queue | Use it | "No new paid services" permits this, but it adds a network dependency to nightly batch jobs — only if it's genuinely already in use. |

**Do not** stand up RabbitMQ/Celery/Redis *and* a scheduler on a single small VM just to migrate 12 cron jobs. That's three new failure modes and a Python dependency tree for something Postgres or systemd does natively.

Regardless of choice, two things are non-negotiable and are installed in Phase 2:

- **Broker/queue durability on disk** (Postgres: it's a database. Redis: AOF. systemd: it isn't needed).
- **Worker supervised by systemd** with `Restart=always`, `RestartSec=5`, and a startup check that fails loudly if the broker is unreachable.

---

## 3. Phase 2 — Build the safety net before migrating anything

This is the phase that actually stops silent failures. Do it while all 12 jobs are still on cron.

1. **Honest exit codes.** Audit every script: does it `exit 0` after a failed `curl`, a `set -e`-less pipe, a partial write? Add `set -euo pipefail` and explicit failure exits. A job that can't fail loudly cannot be monitored, in cron or in a queue.
2. **Positive proof of work.** Exit 0 is not success. Each job must emit a verifiable signal: rows written, output file non-empty and fresh, report delivered. The Job Card records what "success" *means* per job.
3. **Heartbeat / dead-man's switch.** Every job pings a local endpoint on verified success. Anything that hasn't pinged within `expected_duration + grace` alerts. Self-hosted, no cost. This one mechanism catches "didn't fire," "died mid-run," and "exited 0 and did nothing" — the three ways a night goes missing.
4. **Alert routing that a human sees.** One destination (chat channel, not an unread mailbox). Test it by deliberately failing a non-critical job once.
5. **Boot catch-up.** Missed-window jobs must run on boot (`Persistent=true`, or a startup check that enqueues any job whose last success predates its window). Without this, a reboot at 02:55 still loses the night — queue or no queue.

**Exit criterion:** you can lose a job on purpose and get paged within N minutes. Until this is true, migration is not allowed to start. If a job fails during this phase, you have already won.

---

## 4. The per-job checklist (your review artifact)

One copy per job, committed as `jobs/<name>.md`. This is the thing you sign off. **No checkbox, no change.**

### A. Identity
- [ ] Job name, one-line purpose, business owner
- [ ] Current schedule (cron expression) → proposed schedule; timezone confirmed explicit
- [ ] Runtime: typical ___, worst observed ___, timeout set to ___
- [ ] Why it runs nightly (what breaks downstream if a night is lost)

### B. Semantics
- [ ] Inputs, outputs, side effects (files, DB tables, emails, external APIs)
- [ ] **Idempotent?** Can it safely run twice? If no, what lock/guard is added
- [ ] Concurrency: must never overlap with itself / with job ___
- [ ] Ordering: depends on ___ completing first
- [ ] **Catch-up policy:** if the window is missed — run late, run once, or skip? (decide explicitly, per job)
- [ ] Retry policy: max attempts ___, backoff ___, retryable failures vs. fail-fast ones

### C. Failure
- [ ] Known failure modes, and the one that bit us last month (from Phase 0)
- [ ] Exit code semantics — nonzero on every real failure?
- [ ] **Success signal:** what proves it worked (this feeds the heartbeat)
- [ ] Alert destination and threshold
- [ ] Expected manual recovery procedure, timed

### D. Migration
- [ ] Shadow-run result: new path and cron path compared on ___ night(s), outputs matched
- [ ] Cutover date/time, chosen so a bad night doesn't hit a business deadline
- [ ] **Rollback:** exact command to revert to cron, tested, under 5 minutes
- [ ] Cron line kept commented for 30 days after cutover
- [ ] Reviewer sign-off: __________ date ______

---

## 5. Cutover procedure (same for every job, aim for zero downtime)

1. **Shadow.** New scheduler runs the job with writes redirected to a scratch target, or dry-run mode. Compare against that night's cron output. Two nights for anything with money or customers in it.
2. **Dual-run.** Both run for one cycle. Safe only if the job is idempotent and locked — this is why §4.B is a gate.
3. **Cutover.** Comment the cron line (do not delete), enable the queue schedule. Typically seconds; schedule it outside the job's own run time.
4. **Rollback test.** Immediately after cutover, exercise the rollback path once. An untested rollback is not a rollback.
5. **Observe two cycles.** Green heartbeat + matched output, then mark the job done. Delete the cron line only at day 30.

**One job per night, maximum.** Never two jobs on the same night. That keeps every change inside the 5-minute window and keeps the blast radius at exactly one job.

---

## 6. Order of migration

Risk-ascending, not schedule-ascending:

1. **Canary:** lowest-stakes, idempotent, no external side effects. Proves the plumbing.
2. **The two that failed last month.** They're already broken, they're now instrumented, and fixing them visibly is the point of the project.
3. **Remaining simple jobs**, one per night.
4. **Last:** anything with external API calls, money movement, customer-visible output, or no idempotency. These may reasonably end up staying on cron/systemd timers with the Phase-2 safety net — that is a successful outcome, not a failure.

---

## 7. Boundaries, enforced

- **No paid services:** everything above runs on what's installed. The only real cost is the queue table's disk, which needs monitoring.
- **≤5 min downtime:** guaranteed by per-job cutover + tested rollback. No big-bang switchover. The 5-minute limit is a ceiling; the target is zero.
- **Review gate:** you approve each Job Card before that job moves. Phase 0 and Phase 2 produce findings, not changes.

---

## 8. Definition of done

- [ ] All 12 Job Cards complete and signed off
- [ ] Both historical silent failures root-caused and now alerting
- [ ] Every job has a heartbeat with a proven alert path
- [ ] Missed-window catch-up verified by a real reboot test
- [ ] 11+ jobs migrated, or explicitly and consciously retained with the safety net (documented why)
- [ ] Cron entries removed only after 30 green days
- [ ] Runbook: one page — how to see queue state, retry a job, and roll a job back to cron

---

## 9. What I need from you before Phase 0 starts

1. Access to `crontab -l`, the 12 scripts, and last month's logs (or the scripts' own log paths).
2. Which two jobs failed, and how you found out — the discovery path matters more than the failure.
3. Is there a window where a lost night is genuinely unacceptable (billing, payroll, customer report)? That sets the freeze on cutover nights.
4. Do you already run Postgres or Redis on this VM? Answer decides §2 and the whole shape of the work.
5. Who gets paged, and at 3am do they actually look?

Estimated shape: Phase 0 ≈ half a day, Phase 2 ≈ 1–2 days, then ~1 job/night. The queue itself is the small part.
