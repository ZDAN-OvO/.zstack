Written: `local/plans/nightly-jobs-queue-migration.md`

Your five Task slots transferred intact. Three things I'd push back on before any checklist gets written:

1. **"Migrate to a queue" may be the wrong framing.** The two jobs failed *silently* — that's a detection failure, not a scheduling one. A queue still loses messages (worker dies mid-message, poison retries). The rung above your request: every job either runs or is loudly known not to have run. That means a dead-letter queue plus a heartbeat check that pages on *absence*. Fallback if you decline: the checklist exactly as asked.
2. **The two failures' logs are the rawest material and they're not here.** This box has only stock `/etc/cron.daily` — no user crontab, no job scripts. Without last month's exit codes and runtimes you can't set retry or timeout policy, so the plan's Needs section is a to-do for you.
3. **Not all 12 need a queue.** You're on systemd 255; timers give you dependency ordering and journald logging for free, and "no new paid services" rules out managed queues anyway.

Checkpoint I built in: you approve the checklist for the *worst-behaved single job* before I write the other eleven.

Ready is **no** — the three moves in Requirement need accept/rewrite/decline, and the queue choice reshapes all twelve checklists. Once you've ruled, run `/define-goal` with this plan as its source.