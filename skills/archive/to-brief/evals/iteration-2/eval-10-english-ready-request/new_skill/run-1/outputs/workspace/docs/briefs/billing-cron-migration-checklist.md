# Brief: A per-job checklist the on-call team runs to move 6 billing cron jobs from the old VM to Kubernetes CronJobs next sprint with no missed run and no duplicate invoice run

- Stage: execute
- Source: "I need a migration checklist so our on-call team can move the billing cron jobs from the old VM to Kubernetes CronJobs next sprint without a missed run. Context: 6 jobs, the nightly invoice job must not run twice, the team has run CronJobs before. Use the crontab in the repo and our k8s manifests only. Don't change job schedules or touch the payments DB. Done is a Markdown checklist per job plus a rollback step, reviewed by me before anyone executes it."

## Goal
- Give the on-call team a checklist they can execute without re-deciding anything: cut over all 6 billing cron jobs from the old VM crontab to Kubernetes CronJobs during next sprint.
- The checklist must make the two failure conditions checkable, not assumed: no job misses a run during the handoff, and the nightly invoice job never executes twice.
- Write for operators who already know CronJobs, so the content carries the billing-specific risk points (overlap window, effective time, secrets/config, ordering of the invoice job) instead of scheduler basics.

## Context
- Six jobs are scheduled today by one crontab on one old VM; all six move in the same sprint, so the checklist is read once, under time pressure, by whoever is on call.
- The invoice job runs nightly and must produce exactly one run per night across the cutover; an overlap window where old and new schedules are both live is the failure mode to design out.
- The team has run CronJobs before; the checklist states decisions and verification points, not how a CronJob manifest works.
- The requester reviews the checklist and signs off before any step is executed; execution is done by on-call, not by the person writing it.

## Materials
- Only two inputs: the repo's crontab (job names, cron expressions, command lines, environment) and the repo's k8s manifests (namespaces, images, existing CronJob conventions, secret and config references).
- No other source may fill a field: no runbooks, wikis, tickets, dashboards, or another service's manifests, even when they look equivalent.
- Every per-job field in the checklist (name, schedule, image, namespace, command, secret/config refs) is copied from those two files; anything absent there is written as "not found - confirm before execute", never reconstructed from memory or analogy.
- Effective time must be traced from the sources, not assumed: compare the crontab's timezone with the manifests' CronJob `timeZone` (or cluster default) and record which offset applies; if it cannot be determined, flag it as unresolved rather than rewriting the expression.

## Boundaries
- Do not propose changing any job's schedule: same cron expression, same effective wall-clock time, same frequency. If an expression cannot be carried over as-is, flag it for the requester instead of redesigning it.
- Do not touch the payments DB: no schema changes, no migrations, no data fixes, no new credentials or connection-string edits, no new DB access beyond what the existing jobs already have.
- Do not modify the crontab, the manifests, or the cluster while producing the checklist; the deliverable is a document humans execute after review.
- Invent no job names, schedules, namespaces, images, owners or timings, and no "probably runs in a few minutes" assumptions - unknown values are marked, and unverifiable timing is an explicit gate.
- Never trade safety for speed on the invoice job: the stop-old / start-new ordering needs a verified completion or explicit decision, not an overlap nobody checked.

## Done
- One Markdown checklist: a section per job (6 sections) plus one rollback section, every step a checkbox with the command or console action and the observable result that proves the step worked.
- Each job section covers pre-check, the cutover steps, the proof that the job is scheduled and has run (or will run) exactly once, and that job's rollback line.
- The rollback section restores each job to the VM in reverse order - re-enable the crontab entry, disable the CronJob - and includes the case where the invoice job already ran twice.
- Ends by submitting the file to the requester for sign-off; no execution and no cluster changes beforehand.
- Any "not found" fields are collected at the end so the reviewer can close them in one pass before approving.

## Assumptions
- Materials: the crontab and k8s manifests are not in this workspace (only README.txt is), so the brief fixes their identity and the missing-data rule instead of inventing job contents; the checklist will carry marked gaps until the paths are supplied.
- Boundaries reading: "don't touch the payments DB" means no schema, migration, credential or new-access changes; it does not forbid naming an existing secret/config reference the jobs already use. If it forbids even mentioning DB connection details, this bullet tightens.
- Boundaries reading: "don't change schedules" means preserving effective wall-clock time, so a local-time crontab landing on a UTC CronJob schedule gets a `timeZone` note (or an unresolved flag), not a rewritten expression.
- Output shape: checklist is plain Markdown, no scripts; commands are quoted as they exist in the two sources, not rewritten into wrapper tooling.
