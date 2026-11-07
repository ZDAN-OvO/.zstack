Wrote the brief to `docs/briefs/billing-cron-k8s-migration.md` (125 lines).

**What it specifies:** one deliverable Markdown file with a source register, a 6-job inventory table, one checklist section per job (pre-checks → cutover → first-run verification → per-job rollback), a justified cutover order, and a rollback decision point. The two invariants are carried into every job section rather than stated once: at-most-once for the invoice job (with a single-owner handoff and a duplicate-run guard that goes beyond `concurrencyPolicy`, since `Forbid` does not stop the VM copy from also firing) and no-missed-run (every fire time in the window must be shown to be claimed by exactly one scheduler). Constraints are numbered C1–C5 so they can be cited as stop conditions: literal schedule preservation, zero payments-DB contact (including reads — verification via logs and Job status), and read-only while writing.

**Two things shaped the brief.** The workspace contains only `README.txt` ("Scratch workspace for marketing and ops tasks") — no repo, no crontab, no manifests. So the brief defines the sources as exclusive and tells the executing agent to stop and report on any gap rather than fill it, and it requires a source register with commit SHAs. Also, "no missed run" and "must not run twice" conflict precisely at the cutover boundary; the brief requires that conflict to be resolved explicitly per job with a stated ownership instant, not left implicit.

**Questions I could not resolve, and did not invent answers to:**

1. **Where are the repo, crontab, and manifests?** The workspace is empty. A path, or permission to search elsewhere, is required before this brief can be executed.
2. **Which timezone does the VM crontab run in?** CronJobs default to UTC unless `timeZone` is set (needs cluster ≥ 1.27). If the two differ, every schedule shifts — that is a C1 stop condition, not a detail.
3. **How should "don't touch the payments DB" be read?** I took the strict reading: no connections at all, including read-only verification. If read-only queries are acceptable, some verification steps get materially cheaper.
4. **Which job is the nightly invoice job, and what is the cutover window?** Both drive the ordering and the fire-time ledger.
5. **What is the duplicate-run guard if none exists today?** If the invoice job has no idempotency key or lock, the brief's C3 cannot be satisfied from the permitted sources and the migration needs a different design.

Is the file location and this level of constraint-numbering what you wanted, or should the brief be lighter-weight for a checklist an on-call engineer reads at 2 a.m.?