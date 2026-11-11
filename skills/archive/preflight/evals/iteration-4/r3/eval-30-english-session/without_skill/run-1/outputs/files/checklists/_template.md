# Migration checklist: `<JOB NAME>`

Copy this file to `checklists/<job-name>.md`. One job per file. Nothing changes until
the Sign-off section is filled in by the reviewer.

---

## Identity

| Field | Value |
|---|---|
| Job name | |
| Current schedule (as written in crontab) | |
| Timezone | |
| Script / entrypoint | |
| Owner (who gets woken) | |
| What it reads | |
| What it writes (files, tables, APIs) | |
| External side effects (emails, payments, deletes, webhooks) | |

---

## Fitness for a queue

Answer every line. "Unknown" is a blocking answer, not a pass.

- [ ] **Idempotent?** Running it twice produces the same end state. If no → lock added
      (advisory lock / lockfile) and re-verified.
- [ ] **Overlap policy** set (`max_instances=1` or equivalent). Justification:
- [ ] **Timeout** set, and it is above p95 runtime with margin.
- [ ] p95 runtime / worst-case runtime recorded:
- [ ] **Dependencies** declared (other jobs, services, files, network):
- [ ] **Ordering** with other jobs is explicit in the queue, not implied by crontab order.
- [ ] **Secrets/env** reachable from the worker's environment — not only from an
      interactive shell or a `.bashrc`.
- [ ] **Log destination** decided; output retained per run.

### cron → queue traps, answered explicitly

Each of these is a real cause of "it worked under cron":

- [ ] `PATH` and env are set explicitly in the worker (cron's env was minimal and
      different — do not assume your shell's env).
- [ ] Working directory (`chdir`) set explicitly.
- [ ] stdout/stderr captured; exit code propagated to the queue, not swallowed by
      `> /dev/null 2>&1` or `|| true`.
- [ ] Timezone set explicitly on the scheduler (cron used the system's).
- [ ] Jobs that relied on cron serialising them are now protected by a lock or by
      a single-worker concurrency limit.
- [ ] Any job that assumed "only one copy runs at 02:00" verified under the queue.

---

## Shadow run

- [ ] Worker configured to do the work but **not** apply writes (dry-run / staging target).
- [ ] Queued schedule enabled **alongside** the existing cron line.
- [ ] Shadow nights completed: ___ of 3
- [ ] Outputs diffed, run by run. Diff summary:
- [ ] Any divergence explained:
- [ ] Reviewer has seen the diffs: (name / date)

---

## Cutover

- [ ] Window agreed: (date / start / end). Single job only.
- [ ] Rollback rehearsed **before** cutover. Time to roll back: ___ (must be < 5 min)
- [ ] Cron line commented out (not deleted), with the date and this job's name:
      `# MIGRATED-TO-QUEUE 20YY-MM-DD <job-name> — rollback: uncomment`
- [ ] Queue schedule enabled with the same TZ and time.
- [ ] First real run observed end to end.

---

## Verification (all must be witnessed by the reviewer)

- [ ] Success heartbeat arrived inside the deadline.
- [ ] A **deliberate** non-zero exit produced an alert.
- [ ] A **skipped/missed** run produced an alert (job absent, not failed) — this is the
      failure that bit us last month.
- [ ] Duplicate-run test: two concurrent executions did not corrupt anything.
- [ ] Run appears in the run history with correct duration and exit code.

---

## Sign-off

| | |
|---|---|
| Reviewer | |
| Date | |
| Which verification steps I personally saw | |
| Notes / exceptions | |

---

## Remaining in cron until

- [ ] 2 clean weeks in the queue completed (date: ____)
- [ ] Commented cron line deleted, crontab archived
