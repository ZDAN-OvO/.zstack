Plan written: `/tmp/pf-30-with_skill-nyfbi327/local/plans/nightly-job-reliability.md`

Two things before it can run:

1. **The workspace is empty** — no crontab, no job scripts, no logs. Materials are listed but none are reachable, so every per-job claim would be invented. Needs a path to those files (copy the crontab and scripts in, or paste the two failed jobs' logs).
2. **The queue may be the wrong instrument.** Your goal is "no missed nightly jobs"; a queue prevents lost *messages*, not missed *schedules* — if the enqueuer dies, the queue is simply empty and silent, which is the same failure that burned you last month. Worth deciding whether the real missing piece is detection + retry + idempotency, with the queue as one option.

The plan records that as the rung above your request, with your per-job checklist as the fallback — so it's useful either way.

Ready is **no**: rule on the three Requirement moves (hand-over, depth, range) and fill the Open gaps. When you have, `Ready` becomes yes and `/define-goal` can take this plan as its source.