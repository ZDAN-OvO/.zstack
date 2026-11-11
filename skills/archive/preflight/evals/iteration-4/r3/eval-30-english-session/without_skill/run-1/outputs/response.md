Plan written to three files:

- `migration-plan.md` — the plan
- `checklists/_template.md` — the per-job checklist (copy one per job)
- `inventory.csv` — Phase 0 fill-in

**The plan in short**

| Phase | What | Why it's in this order |
|---|---|---|
| 0 | Inventory all 12 jobs: idempotency, runtime, deps, what "failure" looks like today | can't migrate what isn't characterised |
| 1 | Make failures loud — per-run exit code + log, and a **heartbeat dead-man's switch** per job | ships in a day, changes no scheduling, would have caught both of last month's silent failures |
| 2 | Pick the queue (systemd timers / Postgres `SKIP LOCKED` / Redis+RQ) | free-only, drives off your existing stack |
| 3 | One checklist per job | your sign-off gate |
| 4 | Canary → batch 1 → dependency batch → the two that already failed, last | proves the process before trusting it on the risky jobs |
| 5 | Retire cron after 2 clean weeks per job | rollback stays available |

**Three things you should push back on before signing**

1. **A queue alone won't meet your goal.** If the worker is down, the job sits in the queue and fails as silently as cron did. The heartbeat/dead-man's switch is the load-bearing piece — it's Phase 1 precisely because it's the actual fix and doesn't need the migration.
2. **The VM is still a single point of failure.** A queue on the same box doesn't survive the box. The liveness monitor must not live only on the VM it watches.
3. **For 12 nightly jobs, systemd timers + Phase 1 may beat a queue on risk** (`Persistent=true` catches missed runs, `OnFailure=` makes them loud). It's on the table as an explicit alternative, not a silent substitution. Your call — record it.

**Open questions blocking Phase 0:** what stack you run (Postgres? Redis?), what alerting channel already exists, whether the 12 jobs have ordering between them, whether a second host is available for the monitor, and *why* the two failed silently — that answer becomes a regression test on their checklists.

I don't have your crontab or scripts, so the inventory and checklists are blank templates. Send those and I'll fill in Phase 0 for all 12.