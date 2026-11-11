Plan written to `local/plans/cron-to-queue-migration.md`.

Your brief answered the five Task slots, so the plan's substance came from it. Three things I found or think are worth your ruling:

- **The materials aren't here.** This workspace is empty and `crontab -l` returns "no crontab for zdan" — so the crontab, the 12 scripts and the failure logs still have to be provided. That's why Ready is no.
- **A migration doesn't fix your stated purpose.** You want to be told when a nightly job fails; moving cron to a queue doesn't give you that on its own. I proposed adding the alert check that would have caught last month's two failures — as a proposal, not folded in.
- **"Queue" is under-decided.** A self-hosted broker on that same VM has the same VM-level failure mode as cron. Per job, a retrying scheduler may already meet the goal.

Ruling needed on the three proposed moves (prove one job with its alert first; same-VM broker or not; treat the queue as one means), and the failure cause — which only the logs can settle.

`/define-goal` can take this plan as its source when you're ready.