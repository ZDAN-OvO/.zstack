# Brief — Billing cron migration checklist (VM crontab → Kubernetes CronJobs)

**Status:** draft for user review. Produces a document only; nothing is executed against any VM, cluster, or database.

## Objective

Produce a migration checklist that the on-call team can follow next sprint to move **6 billing cron jobs** from the old VM's crontab to Kubernetes CronJobs, such that **no scheduled run is missed** and the **nightly invoice job never runs twice** during or after the cutover.

The deliverable is the checklist itself, reviewed by the requester **before** anyone executes it. Writing the checklist is in scope; performing the migration is not.

## Deliverable

One Markdown file: `docs/billing-cron-k8s-migration.md`, containing:

1. **Source register** — where the crontab and the k8s manifests were read from (path + commit SHA or equivalent), and the exact lines used.
2. **Job inventory table** — all 6 jobs: crontab name, expression, run-as user, command, target CronJob, target namespace.
3. **One checklist section per job** (6 total), each with pre-checks, cutover steps, post-run verification, and a per-job rollback.
4. **Cutover sequence** — the order jobs are moved and why, plus the definition of the cutover window.
5. **Rollback section** — global decision point plus per-job revert steps.
6. **Open items** — anything the sources could not answer.

Checklists must be actionable as written: imperative steps, explicit commands or UI actions, one observable verification per step, named owner role per step.

## Inputs and source-of-truth rules

**Permitted sources, exclusively:**

- The crontab file in the repo.
- The Kubernetes manifests in the repo.

**Rules:**

- Every job in the checklist must trace to a crontab line. Every CronJob must trace to a manifest. Cite `file:line` for both.
- If the crontab contains a different number of billing jobs than 6, **stop and report** — do not trim or pad the list.
- If the manifests contain no CronJob definitions, or cover fewer jobs than the crontab, report the gap per job rather than authoring new manifests.
- Never infer a schedule, image, secret name, or command that is not written in the sources. Mark it `UNKNOWN — see Open items`.
- Do not read or use anything outside the repo for job definitions (no cluster state, no prior runbooks, no memory of how "it usually works").

## Hard constraints

| # | Constraint |
|---|---|
| C1 | **Schedules do not change.** Each k8s `schedule` must be the literal crontab expression, or a conversion whose equivalence is demonstrated in one line. Any conversion that cannot be shown equivalent is a stop condition, not a judgement call. |
| C2 | **No payments DB contact.** No connections, queries, migrations, credential changes, or schema edits — read-only queries included. Verification must come from logs, scheduler output, and Kubernetes Job status. If a check genuinely requires DB access, list it as an open item for the requester. |
| C3 | **Invoice job runs at most once per fire time**, across the whole transition. Requires an explicit single-owner handoff and a stated duplicate-run guard; "the CronJob has `concurrencyPolicy: Forbid`" alone is not a guard against the VM copy also running. |
| C4 | **No missed run** for any of the 6 jobs. For each job, the checklist must show the expected fire times spanning the cutover and demonstrate that each one is claimed by exactly one scheduler. |
| C5 | Read-only with respect to infrastructure while writing the brief. No `kubectl apply`, no crontab edits, no VM access. |

## Facts to establish from the sources before writing steps

Record each as fact + citation, or as `UNKNOWN`:

- Cron expression, run-as user, command, and working directory / env for each job.
- Timezone semantics: what timezone the crontab is interpreted in, versus the CronJob's (`timeZone` field availability depends on cluster version — if that is not visible in the manifests, it is an open item, not an assumption).
- Anything the crontab does that a CronJob does not do natively: `%` escaping, `MAILTO`, `PATH`, shell built-ins, output redirection, overlapping-run behaviour, retry-on-failure behaviour.
- For each target manifest: image, namespace, `concurrencyPolicy`, `startingDeadlineSeconds`, `backoffLimit`, `activeDeadlineSeconds`, `suspend`, history limits, secret/config references.
- Which job is the nightly invoice job, and its fire time relative to the planned cutover window.

## Required content per job section

Use this skeleton for all 6:

```markdown
### <job name>

| | |
|---|---|
| Crontab source | `path:line` — `<expression>` as `<user>` |
| Command | `<exact command>` |
| Target CronJob | `<namespace>/<name>` — `manifests/path:line` |
| Schedule mapping | literal copy / conversion — `<justification>` |
| Fire times in window | `<list>` |
| Owner before / after | VM crontab / CronJob `<name>` |

**Pre-checks**
- [ ] … (each with a pass/fail observation)

**Cutover**
- [ ] … (ordered; each step names who acts and what proves it happened)

**First-run verification**
- [ ] … (expected run count at each fire time in the window; where to look)

**Rollback for this job**
- [ ] … (restore VM ownership, suspend the CronJob, prove the revert)
```

## Cutover and rollback requirements

- Define the cutover window explicitly (start, end, and the fire times that fall inside it).
- Choose and justify the sequence — per-job stagger versus batch, and where the invoice job sits in the order. State the reasoning in terms of C3 and C4.
- State, for the transition itself, which side owns each job at each moment, and what happens to a fire time that lands mid-handoff.
- Rollback must be triggerable per job without reverting the others, must name who may call it, and must restore the pre-migration state observably (VM entry active, CronJob suspended, no double-ownership gap that misses a run).
- Rollback must not depend on actions ruled out by C2.

## Done criteria

The brief is done when all of the following hold, and the checklist states each one as a checkable item:

1. Exactly 6 jobs are covered, each traced to a crontab line and a manifest.
2. No schedule differs from the crontab, and any conversion is shown equivalent.
3. Every job has a stated single-owner handoff covering every fire time in the cutover window.
4. The invoice job has an explicit duplicate-run guard beyond `concurrencyPolicy`.
5. Each of the 6 sections has a rollback that stands alone.
6. No step requires touching the payments DB.
7. Open items are enumerated, and none of them is silently filled with an assumption.
8. The document is delivered for requester review — **execution is blocked until that review happens.**

## Out of scope

- Executing any step, or dry-running against a real cluster or VM.
- Changing schedules, job commands, images, or manifest structure.
- Payments DB access, credential changes, secret rotation.
- Authoring new CronJob manifests where the repo has none.
- Migration tooling, monitoring/alerting setup, or post-migration decommissioning of the VM.

## Stop conditions

Return to the requester instead of proceeding if: the job count is not 6; the crontab or manifests cannot be located; a schedule cannot be shown equivalent under C1; the invoice job has no available duplicate-run guard; or a required verification would need DB access.

## Notes for the executing agent

- The team has run CronJobs before. Skip CronJob fundamentals; spend the space on this migration's boundary risks.
- Prefer fewer, verifiable steps over exhaustive prose. Every checkbox needs an observable outcome.
- Keep the two invariants (C3, C4) visible in each job section rather than only in the introduction — the reader executes section by section.
