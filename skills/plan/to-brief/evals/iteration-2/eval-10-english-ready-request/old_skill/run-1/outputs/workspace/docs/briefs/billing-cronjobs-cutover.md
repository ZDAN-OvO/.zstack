# Brief: Cut 6 billing cron jobs over from the old VM to Kubernetes CronJobs with no missed run and no duplicate invoice run

- Stage: execute
- Source: "I need a migration checklist so our on-call team can move the billing cron jobs from the old VM to Kubernetes CronJobs next sprint without a missed run. Context: 6 jobs, the nightly invoice job must not run twice, the team has run CronJobs before. Use the crontab in the repo and our k8s manifests only. Don't change job schedules or touch the payments DB. Done is a Markdown checklist per job plus a rollback step, reviewed by me before anyone executes it."

## Goal

- Give the on-call team a per-job runbook they follow at cutover, so every scheduled run in the window fires exactly once and the nightly invoice job never fires twice.
- The failure this must prevent is a duplicate invoice run, ahead of a skipped run; either one means the checklist failed.
- Written for an operator executing under time pressure mid-window, not for a design review.

## Context

- 6 billing cron jobs currently run from a crontab on the old VM; that VM stays the live scheduler until the checklist moves a job off it.
- The nightly invoice job must not run twice — double invoicing is the costly failure mode.
- The on-call team has run Kubernetes CronJobs before, so CronJob / Job / suspend / concurrencyPolicy mechanics need no explanation.
- Cutover is planned for next sprint, in a window the team controls, not an emergency.
- Verification has to be observable without the payments DB: CronJob and Job status, pod logs, and the jobs' own outputs.

## Materials

- Primary and only sources: the crontab in the repo (job names, cron expressions, commands, any env or wrapper it references) and the Kubernetes manifests in the repo.
- Cluster, namespace, image, and secret facts only as the manifests state them; nothing from memory of the live cluster.
- Neither the crontab nor the manifests were present in this workspace, so the executor locates both in the repo first and records the paths used at the top of the checklist.
- Anything the sources do not state (a schedule, a command line, the VM timezone, a manifest field) is left blank and marked "not found in sources"; never inferred, reconstructed, or filled from general cron or Kubernetes knowledge.

## Boundaries

- Do not change job schedules: cron expressions carry over verbatim, and the VM timezone counts as part of the schedule — if the sources do not state it, mark it unresolved instead of choosing one.
- Do not change job commands, arguments, entrypoints, or env values; a job that cannot run unchanged on Kubernetes becomes a blocker recorded on its own entry.
- Do not touch the payments DB: no writes, migrations, backfills, or reconciliation runs, and a check that would need to query it is written as a step for you to approve rather than something the checklist does.
- Do not execute anything — no kubectl apply, no crontab edit, no suspend or resume. The deliverable is the file; running it is the team's job after your review.
- Do not propose optimising, merging, or rescheduling the jobs even where the cron setup looks wrong; record the observation and leave the schedule alone.

## Done

- One Markdown file containing a section per job (all 6, ordered by migration sequence) plus one rollback section.
- Each job section states its cron expression and the file it came from, the pre-cutover state, the cutover steps, and the specific check proving the next run happened exactly once.
- The rollback section covers reverting a single job and reverting the full set, including what gets re-enabled and how to confirm the VM is scheduling again.
- The file carries a review gate as its last line: you approve it before anyone executes it, and nothing in it has been applied.

## Assumptions

- Deliverable path: `docs/billing-cronjobs-cutover-checklist.md`. Veto if you want it elsewhere.
- Cutover is one job at a time rather than a single switch, because each job needs its own "ran exactly once" check. Veto if you planned all 6 at once.
- "Without a missed run" means every scheduled run in the window fires once; a late run that still fires once passes.
- The old VM is not decommissioned by this checklist and its crontab stays intact until rollback is no longer needed.
- No outline gate before the full checklist: the review of the finished file is the single checkpoint.
