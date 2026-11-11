# Cron → Queue Migration Plan

Status: draft, not yet reviewed. Nothing in here should be executed until Phase 1
is signed off and the per-job checklists are filled in and approved.

Scope: 12 cron jobs on one VM → a queue-backed runner.
Hard constraints: no new paid services · no downtime > 5 min · no missed nightly jobs.
Deliverable: one migration checklist per job, reviewed by you before any change.

---

## 0. What this plan assumes, and the one thing it changes about your framing

Two jobs failed silently last month. A queue does not fix that by itself: a worker
that is down, or a job that dies without raising, is just as silent as a cron entry
that dies without raising. Retries help, but only for failures that are *detected*.

So this plan deliberately puts visibility first and treats the queue as a second,
optional step. If we migrate all 12 jobs onto a queue and still have no alert on
"job did not complete", you will still lose nightly jobs — with more moving parts.

The goal ("no more missed nightly jobs") is met by two things, in this order:

1. **Detection**: every job's outcome is recorded and a missed run raises an alert.
2. **Recovery**: a job that fails is retried, or is queued durably so a restart
   does not lose it.

A queue only supplies (2). We do (1) regardless of whether we migrate at all.

Second assumption worth stating: moving 12 jobs onto a broker + worker on the
*same single VM* adds a new single point of failure. If the worker process is not
running, all 12 jobs stop, and nothing in cron will tell you. That is a strictly
worse failure mode than today unless Phase 1 alerting covers the worker too. Every
checklist below therefore includes a worker-liveness item.

---

## 1. Inventory (blocked — I need your materials)

I do not have the crontab or the job scripts. Send them (or paste them) and I will
fill the per-job checklists from them rather than from guesses.

For each of the 12 jobs, capture:

| Field | Why it matters |
|---|---|
| Cron expression + timezone | fixed-time vs interval semantics differ in queues |
| What it actually does (1 line) | decides whether it belongs in a queue at all |
| Runtime (typical / worst seen) | jobs longer than their interval need overlap policy |
| Exit code semantics | does it exit non-zero on failure, or always 0? |
| Inputs (files, DBs, external APIs) | determines what a retry can safely repeat |
| Outputs / side effects | email sent, rows written, files uploaded, money moved |
| Idempotent? | if no, "retry" is a data-corruption button, not a safety net |
| Depends on another job finishing? | ordering constraints a queue can express, cron cannot |
| Who notices if it doesn't run? | if nobody, that is the bug to fix first |
| Cost of a duplicate run | same as above, from the other side |

Two questions drive most of the design:

- **Is the job idempotent?** If not, retries must be manual, and the queue's value
  drops to "durable scheduling + visible failure" only.
- **Does it need retry/ordering/long runtime?** If no, a queue is overhead.

---

## 2. Phase 1 — Make failures visible (do this first, no migration)

Applies to all 12 jobs whether or not they ever move.

- [ ] Every job writes a run record on completion: job name, start, end, exit code,
      host, and a one-line result. A table in the existing database is fine
      (`job_runs`); add an index on `(job_name, started_at)`. No new service.
- [ ] Jobs that currently swallow errors (`|| true`, `2>/dev/null`, catch-all
      `except: pass`, or scripts that `exit 0` on error) get that removed. List
      these explicitly in the inventory — these are probably your two silent
      failures.
- [ ] A nightly watchdog (one cron entry, ~15 lines) that reads `job_runs` and
      alerts if any expected job is missing a successful run in its window, or has
      a recorded failure. Alert goes somewhere a human reads: email to a mailbox
      you check, or a chat webhook. Not a log file.
- [ ] Alert on "job ran but produced nothing" for jobs whose output is a file or
      an email count — a 0-byte output is a failure that exited 0.
- [ ] Cron itself alerts on non-zero exit (`MAILTO=` set, or wrap each command).
- [ ] Worker/broker liveness alert (only if/when Phase 3 happens).
- [ ] **Verify the alerting works** by making one job fail on purpose, once, and
      confirming you got the alert. An untested alert is not an alert.

Exit criterion for this phase: you can answer "did last night's jobs all succeed,
and how do I know?" without logging into the VM.

This phase alone plausibly meets your stated goal. It is also the phase with the
best effort/benefit ratio and zero migration risk. I would not proceed to Phase 3
before it is done, because otherwise we cannot tell whether the queue improved
anything.

---

## 3. Phase 2 — Choose the queue (no paid services)

Pick based on what the VM already has, not on what is fashionable. In preference
order, all free and self-hosted:

1. **Already-installed Postgres** → table-based queue with `SELECT ... FOR UPDATE
   SKIP LOCKED`. No new process to babysit, jobs survive reboots and worker
   restarts, transactional with your data. Recommended default if Postgres exists.
2. **Already-installed Redis** → Redis + a small worker (RQ, or a ~100-line loop).
   Simpler code, but Redis needs a persistence policy you have actually set, or a
   restart drops queued jobs.
3. **Nothing installed** → SQLite-backed queue on the same disk. Single-writer, fine
   for 12 nightly jobs, no new daemon. Adequate here.
4. **No queue at all** → systemd timers with `Restart=on-failure` and `Persistent=true`
   (catches missed runs after downtime), plus Phase 1 alerting. For 12 jobs on one
   VM this is a legitimate answer and less to operate. Do not rule it out.

Do **not** introduce a broker *and* a separate worker *and* a scheduler if cron can
remain the trigger. Keeping cron as the trigger (`* * * * * enqueue-due-jobs`) is
the lowest-risk design: scheduling semantics stay identical, and the queue only
takes over execution, retries, and visibility.

Record the decision and the reason in this file before touching any job.

---

## 4. Phase 3 — Per-job checklist (the deliverable)

One copy of this per job, completed and reviewed by you *before* that job is
changed. Filename: `jobs/<job-name>.md`. Copy the template verbatim; do not skip
items, write "n/a — because …" instead.

```
### Job: <name>
Owner:                     
Cron spec + TZ:            
What it does (1 line):     
Runtime typical / worst:   
Exit code on failure:      # non-zero? always 0? unknown?
Writes / side effects:     
Idempotent?                # yes / no / only if <condition>
Retry allowed?             # yes / no (manual only, reasons:)
Overlap policy:            # skip / queue / allow concurrent (reasons:)
Ordering deps:             # must run after <job>, before <job>
Success signal:            # what "it worked" looks like, beyond exit 0
Alert if missed by:        # time, and who gets it
Max acceptable delay:      # how late is still OK

PRE-CHANGE
[ ] Job appears in inventory with all fields above filled
[ ] Job currently succeeds when run by hand, on demand
[ ] Current behaviour captured: one recorded run (log + output + timing) as baseline
[ ] Failure path tested once on the old setup, alert observed
[ ] Kill switch identified: exact command to disable this job only
[ ] Rollback rehearsal: re-enable old cron entry, confirm it still works untouched
[ ] Blast radius written down: what breaks for users if this job is late or runs twice

CUTOVER (this job only, no other job touched in the same window)
[ ] New path deployed but NOT yet scheduled
[ ] Manual run via new path: output matches baseline
[ ] Duplicate-run test: run it twice via new path, confirm no double side effects
[ ] New path scheduled; old cron entry commented out in the same commit, not deleted
[ ] Old cron entry kept commented for 14 days, with the date and the reason

POST-CUTOVER
[ ] First scheduled run completes, run record present, success signal matches
[ ] Missed-run alert verified for this job (skip a run deliberately, once)
[ ] Failure alert verified for this job (force a failure, once)
[ ] Noted in this file: date, who, what was observed
[ ] Reviewed by you: signature/date

AFTER 14 DAYS
[ ] Old cron entry deleted
[ ] Job removed from any "still on cron" list
```

"Blast radius written down" is the item I would not let anyone skip. For a nightly
billing export it is "invoices are a day late"; for a cleanup script it may be
"nothing, it runs again tomorrow". Those two jobs deserve different amounts of care,
and the checklist should say so rather than treating all 12 identically.

---

## 5. Cutover order and downtime

Order: lowest blast radius first, the two previously-silent jobs last-but-one
(they need the most attention), and any job with external side effects last.

One job per change window. Never two jobs in the same window, even if they look
trivial — if something breaks you need one variable, not two.

Downtime budget: nightly batch jobs are not user-facing, so "no downtime > 5 min"
should be met trivially by running both paths for one night where the job is
idempotent or read-only. Where a job is neither, cut over between runs (after
completion, before next window) and do not dual-run — dual-running a
non-idempotent job is not a safety measure, it is a data incident. Say which
category each job is in, in its checklist.

Cron entries are commented out, never deleted, for 14 days. That is the whole
rollback plan and it costs nothing.

---

## 6. What I need from you to finish this

1. The crontab, and the scripts (or at least their entry points and their error
   handling).
2. Which two jobs failed last month, and how you found out — that tells me what
   "silent" means concretely here.
3. Whether Postgres or Redis is already on the VM, and whether it is backed up.
4. Who should receive alerts, and through which channel you actually read.
5. For each job: is a duplicate run harmless? Where you don't know, mark unknown —
   I will treat unknown as "not safe to retry".
6. Which job, if it silently missed a night, would cost the most? That one sets the
   standard for the rest.

---

## 7. Definition of done

- 12 completed per-job checklists in `jobs/`, each reviewed and dated by you.
- Phase 1 alerting live and *tested by deliberate failure*, per job.
- Each job cut over in its own window, old entry commented for 14 days.
- After 14 days: all 12 jobs on the new path, old entries deleted, and a single
  place that answers "did everything run last night?" in under a minute.

Note on what I have not done: this is a plan, not an audit. Every judgement above
about which jobs are risky is a placeholder until I see the actual crontab and
scripts. The two silent failures may well be a five-line fix in a wrapper script,
in which case most of Phase 3 is unnecessary work — worth checking before
committing to it.
