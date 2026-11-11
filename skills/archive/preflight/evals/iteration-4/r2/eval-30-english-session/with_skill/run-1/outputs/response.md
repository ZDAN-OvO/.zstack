Plan written: `local/plans/cron-to-queue-migration.md`

The load-bearing finding: your two failures were **silent**, and a queue without a failure path stays silent. So the plan climbs one rung — from "move to a queue" to "a miss reaches a human" — with a cheaper fallback (cron + heartbeat/failure alert) that also meets your 5-minute wall and can ship per job.

Three things need you before this is ready:

1. **Altitude / Fallback** — does "no missed jobs" mean the job always completes, or that a miss is always *known*? That decides queue vs. alerting-only.
2. **Depth** — replay last month's two failures through the new path as the judge. Cheap, and it grades the method, not just the checklist.
3. **Materials** — the repo is empty: no crontab, no scripts, no failure evidence. Want to drop them in, or paste the crontab?

Decline any move and I'll record it with the reason.

When the Ready line is yes, run `/define-goal` with this plan as its source.