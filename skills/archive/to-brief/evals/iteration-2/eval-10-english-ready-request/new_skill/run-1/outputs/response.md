Brief written and validated (checker exit 0, `1 brief(s) ok`).

**Path:** `/tmp/to-brief-eval/10-english-ready-request/with_skill/ws/docs/briefs/billing-cron-migration-checklist.md`

**Slots**
- **Stage** — execute; you're commissioning an artifact, so the brief commissions that.
- **Goal** — clear: an executable cutover checklist for all 6 jobs next sprint, where "no missed run" and "invoice never runs twice" are checkable at each step rather than assumed. Audience is experienced CronJob operators, so content carries billing-specific risk points, not scheduler basics.
- **Context** — clear: 6 jobs, one VM crontab, one sprint, nightly invoice with an overlap window as the failure mode to design out, you review and on-call executes.
- **Materials** — thin, so defaulted with the rule stated: crontab + manifests only; no runbook/wiki/ticket may fill a field; anything absent is marked "not found", never reconstructed; effective time traced from the manifests' `timeZone` rather than assumed.
- **Boundaries** — clear: schedules unchanged (flag, don't redesign), payments DB untouched (no schema, migration, credentials, new access), no edits to crontab/manifests/cluster while writing, no invented names or timings, no safety-for-speed trade on the invoice job.
- **Done** — clear: one Markdown checklist, 6 job sections + rollback section, checkboxed steps with observable proof, each job's rollback line in place, submitted for your sign-off before anything executes.

**Assumptions you can veto** (in the file): the repo's crontab and manifests aren't in this workspace — only `README.txt` — so the brief pins their role and the missing-data rule rather than inventing job contents; "don't touch the payments DB" is read as no schema/migration/credential/new-access changes, not a ban on citing a secret the jobs already use; "don't change schedules" is read as preserving effective wall-clock time.

One question before I'd call it final:

❓ **Q1** — **Where are the crontab and manifests?** This workspace has no repo (`README.txt` only). Two readings: (a) point me at the paths or paste the files so the 6 job sections and their commands are real, or (b) keep the checklist written against marked gaps that you or on-call fill from the repo. Everything else in the brief is already closed by your request.

➡️ (a) — the whole point is a per-job checklist, and 6 sections built on invented job names would be the exact failure the Materials rule bans. If the files can't be supplied in this session, I'd still take (a) but leave the brief as-is and hand you the gap list.

Confirm or correct the file above and I'll rerun the checker; no execution or repo changes happen before your sign-off.