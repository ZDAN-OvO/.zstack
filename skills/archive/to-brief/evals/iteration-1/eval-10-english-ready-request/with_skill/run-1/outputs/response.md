Brief written and validated: `docs/briefs/billing-cronjobs-cutover.md` (checker exits 0, `1 brief(s) ok`).

**Per slot**

- **Goal** — a per-job runbook the on-call team executes at cutover so every run fires exactly once; duplicate invoice run is ranked as the worse failure, ahead of a skip.
- **Context** — 6 jobs on a crontab, old VM stays live until each job moves off, nightly invoice job must not double-run, no CronJob basics needed, verification must be observable without the DB.
- **Materials** — repo crontab + repo k8s manifests only; no live-cluster memory, no blog/cron-docs gap-filling; anything the sources don't say is left blank and marked "not found in sources".
- **Boundaries** — schedules and timezone carried over verbatim (VM timezone flagged, not guessed), commands/env unchanged, zero payments-DB contact (DB-touching checks become steps for you to approve), nothing executed, no unsolicited rescheduling.
- **Done** — one Markdown file, all 6 job sections in migration order plus a single-job and full-set rollback section, each with a "ran exactly once" proof, ending on your review gate.

**Assumptions you can veto** (bottom of the file): deliverable path `docs/billing-cronjobs-cutover-checklist.md`; one-job-at-a-time cutover rather than a single switch; a late-but-single run counts as no miss; old VM is not decommissioned; no outline gate before the full checklist.

**One fact worth knowing:** the workspace held no repo — only `README.txt` — so the crontab and manifests could not be inspected here. That's recorded in Materials as a first task for the executor (locate both, record paths) rather than guessed at.

Confirm or correct the brief and I'll apply changes and rerun the checker.