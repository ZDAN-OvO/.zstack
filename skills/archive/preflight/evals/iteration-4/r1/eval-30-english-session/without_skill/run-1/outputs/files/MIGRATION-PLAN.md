# Cron → Queue Migration Plan

**Goal:** no more missed nightly jobs.
**Context:** 12 cron jobs on one VM; two failed silently last month.
**Boundaries:** no new paid services; no downtime over 5 minutes.
**Done:** a migration checklist per job, reviewed by you, before any change.

---

## 0. One thing to settle before the plan is worth anything

Two jobs failed *silently*. That is not a scheduling problem — cron ran them, they
exited, nobody was told. **A queue does not fix silent failure.** A job that dies
inside a queue worker also dies silently unless you record the outcome and alert on
it.

So the goal ("no more missed nightly jobs") is met mostly by Phase 1, not by the
queue. The queue buys you retries, ordering, catch-up, and a durable record of
*intent* vs *attempt* — worth having, but it is the second fix, not the first.

Sequencing follows from that: **make failures loud while still on cron, then migrate.**
This also keeps you inside the 5-minute-downtime boundary, because Phase 1 needs no
cutover at all.

**Assumption to verify:** the two failures were (a) job crashed, (b) job never fired,
or (c) job fired and did nothing (empty input, lock held, wrong creds). The answer
changes which phase matters most. Get it from logs/journal before Phase 0 closes.

---

## 1. Target architecture (constrained by "no new paid services")

Do not pick blindly — it depends on what is already on the VM. In preference order:

| Option | Use when | Notes |
|---|---|---|
| **A. Postgres + `SKIP LOCKED`** | Postgres already present | No new component. Durable, transactional, retries + history in one table. Best default. |
| **B. Redis + worker** | Redis already present | Fast, but durability/visibility tuning needed; check persistence config. |
| **C. systemd timers + retry/alert wrapper** | Nothing else present, jobs are shell | Not really a queue, but delivers retries, catch-up, logging, alerting with zero new deps. Honest answer if A/B aren't available. |
| **D. SQLite-backed queue** | Single VM, low volume, no server | Acceptable; watch file locking if jobs overlap. |

Whatever the choice: **one worker process, one queue, one history table.** Do not
introduce a broker you have to operate for 12 jobs on one VM.

Required capabilities (non-negotiable, they are the point of the exercise):
- Durable record: job name, scheduled time, attempt count, start, end, exit code, stderr tail.
- **Alert on:** non-zero exit after retries, no-success-within-grace-window, and *missed fire* (job due but no attempt row). The third one is what failed you last month.
- Retry with backoff, max attempts, and a dead-letter state that is visible.
- Per-job policy for missed runs: `run-late` vs `skip` (a nightly report can run late; a nightly "reset counters" job probably should not run twice at 09:00).
- Overlap guard: at most one run per job at a time, unless proven safe.

---

## 2. Phases

### Phase 0 — Inventory and root cause (no changes)
- Capture the crontab verbatim (`crontab -l > crontab.baseline`), plus any `/etc/cron.*` entries and systemd timers.
- For each job: path, interpreter, env vars, credentials source, writes to, reads from, runtime, peak duration, overlap risk, whether re-running is safe.
- Root-cause the two silent failures. Write one line each: what happened, why nobody knew.
- **Exit:** 12 rows complete in the tracker in §3; both failures explained.

### Phase 1 — Make cron loud (no cutover, no downtime)
- Wrap each job in a runner script: same command, but records start/end/exit/stderr and emits an alert on failure.
- Add a **missed-fire check**: a small watchdog that compares "expected runs today" against "runs recorded today" and alerts on gaps. Catches jobs that never start, which an exit-code alert cannot.
- Alert channel: reuse what you already have (mail, Slack webhook, PagerDuty if present). No new paid service.
- Run this for **at least one full week of nightly cycles** before Phase 2 begins.
- **Exit:** all 12 jobs produce a success record every scheduled night; you have seen one alert fire and one missed-fire alert fire (force a test).

### Phase 2 — Stand up the queue (parallel, nothing migrated)
- Provision the chosen option, deploy the worker, create the history table, wire alerts to the same channel as Phase 1.
- Enqueue a **canary job** that does nothing but log. Confirm: fires on schedule, records history, retries on forced failure, alerts on forced failure, and the missed-fire watchdog covers queue jobs too.
- **Exit:** canary green for 3 nights; alert path proven end-to-end.

### Phase 3 — Migrate job by job (one job per change)
- One job per change, one review, one deploy. Never a batch. This is what keeps downtime under 5 minutes and makes rollback trivial.
- Order: lowest risk first — read-only/reporting jobs → jobs that write but are idempotent → jobs with external side effects (email, payments, third-party APIs) last.
- Per job: dual-run (queue + cron disabled) → compare outputs for 1–3 nights → then remove the cron line in a separate change.
  - Dual-run means *cron disabled, queue live*, not both firing. Never let both fire on a job with side effects.
- **Exit per job:** the §3 checklist fully signed off.

### Phase 4 — Decommission
- After all 12 are green for 7 consecutive nights: remove the cron entries, keep the runner wrapper available, keep the watchdog (it now watches the queue).
- Write a one-page runbook: how to enqueue manually, how to inspect the dead-letter state, how to re-run a job safely, who gets paged.

---

## 3. Per-job migration checklist

Copy one block per job. **No job moves to Phase 3 until its block is complete and you have signed it.**

```
Job ID:            J__        Name:
Cron expression:   [fill]     Local timezone handling:
Command:           [fill]
Owner:             [fill]
Runtime (normal / worst seen):        [fill]
Reads:             [fill]     Writes:            [fill]
External side effects (email/API/money): [fill]
Credentials:       [fill] (where stored, how rotated)
Overlaps itself?   [ ] no  [ ] yes → guard required
Re-runnable safely (idempotent)?  [ ] yes  [ ] no → retries must be disabled
                                    [ ] no → missed run policy = skip, not run-late
Missed-run policy: [ ] run-late  [ ] skip        Grace window: ____
Negative-value case: what breaks if this runs TWICE?   [fill]
                     what breaks if this runs LATE?    [fill]
                     what breaks if this never runs?   [fill]

Phase 1 (on cron)
  [ ] wrapped by runner, records start/end/exit/stderr
  [ ] one alert observed (forced failure)
  [ ] 7 consecutive successful nights recorded
  [ ] duration baseline captured for timeout setting

Phase 2 (queue, before enabling)
  [ ] registered in queue with correct schedule + timezone
  [ ] timeout set above worst-seen runtime, below next run
  [ ] max attempts set (1 if not idempotent)
  [ ] missed-run policy implemented and tested
  [ ] overlap guard verified (kill a run mid-flight, confirm no second run)
  [ ] credentials reachable from worker env (and not from a stray crontab var)

Phase 3 (cutover)
  [ ] queue version runs, output diffed against cron output on ____ dates
  [ ] cron line disabled (not deleted) — change: ______
  [ ] 3 consecutive nights green from queue
  [ ] cron line deleted — change: ______
  [ ] rollback rehearsed: re-enable cron line, confirm it still works

Sign-off: __________  date: ______
```

### Tracker (fill from the real crontab)

| ID | Job | Schedule | Runtime | Side effects | Idempotent | Missed-run policy | Phase 3 order | Status |
|----|-----|----------|---------|--------------|------------|-------------------|---------------|--------|
| J01 | [fill] | | | | | | | |
| J02 | [fill] | | | | | | | |
| J03 | [fill] | | | | | | | |
| J04 | [fill] | | | | | | | |
| J05 | [fill] | | | | | | | |
| J06 | [fill] | | | | | | | |
| J07 | [fill] | | | | | | | |
| J08 | [fill] | | | | | | | |
| J09 | [fill] | | | | | | | |
| J10 | [fill] | | | | | | | |
| J11 | [fill] | | | | | | | |
| J12 | [fill] | | | | | | | |

Mark the two that failed last month in the Status column — they are the ones whose
silent-failure cause must be closed, not just migrated.

---

## 4. Rules that keep you inside the boundaries

**Downtime under 5 minutes**
- Every change is one job, reversible by re-enabling one cron line.
- No job is cut over within 30 minutes of its next scheduled run.
- Never delete the cron line in the same change that enables the queue.
- Never run cron and queue for the same job simultaneously.

**No new paid services**
- Reuse existing Postgres/Redis/alerting. If none exists, take option C and say so plainly — it still meets the goal.

**Reviewer gate**
- You review each job's checklist block before that job's change is deployed. No standing approval, no batching.

---

## 5. Risks

| Risk | Mitigation |
|---|---|
| Queue masks the real failure mode (still silent) | Phase 1 exists; missed-fire watchdog, not just exit-code alerts |
| Double execution on a non-idempotent job | Idempotency question is blocking; max attempts = 1 if unknown |
| Timezone/DST shift moves a nightly run | Pin queue schedule to the same TZ as cron; test the DST night deliberately |
| Worker dies → all jobs stop at once (new blast radius) | Watchdog alerts on zero attempts; supervisor restarts worker; missed-run policy fills gaps |
| Long job overlaps next schedule | Timeout + overlap guard + alert on "still running at next fire" |
| Lingering crontab env vars (`PATH`, creds) missing in worker | Phase 2 credential check per job; the class of bug that causes silent no-ops |

---

## 6. Open questions for you

1. What are the two jobs that failed, and what did the logs show? (Determines whether Phase 1 or Phase 2 is the real fix.)
2. Is Postgres or Redis already running on that VM? (Picks the queue option.)
3. Which of the 12 are safe to re-run, and which have external side effects?
4. Is a late run acceptable for each job, or must a missed night be skipped?
5. Where should alerts go, and who is on the hook at 03:00?
6. Any hard dependency between jobs (J03 must finish before J04)?

**Blocking for me to fill in the tracker:** the crontab and the job scripts — neither
is in this workspace.
