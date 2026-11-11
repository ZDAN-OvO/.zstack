TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/SKILL.md"}

TOOL bash: {"command": "ls -la; crontab -l 2>/dev/null | head -50"}

RESULT: ---
name: preflight
description: >-
  Write a one-screen plan the user reads to check their own thinking before AI runs the work: could the requirement aim higher, deeper or wider, and can the user state the task's purpose, context, materials, boundaries and done? Use when a request is one step of a bigger result ("fix this bug", "fill in the template"), when quality matters in a field the user is not expert in, when a deliverable is named by its noun ("homepage", "weekly report"), when the user cannot say what done looks like, or when a planned result came back rejected.
---

# Preflight

A request is the user's guess at one step toward an outcome they have not stated. The model carries out the step as written and does not question the intent behind it. So two gaps go unseen until the output lands:

- **Requirement**: the request undershoots what the model could own today.
- **Task**: the intent is still unformed. The model mirrors vagueness back as a generic output.

This skill brings both gaps into one plan that the user reviews before execution. The user's thinking is the subject. Writing the goal and doing the work come after the plan.

## Enter

Offer the plan in one line, and go on only if the user accepts. When a redo costs less than a plan (a rename, a lookup), do the request as written. The plan pays off when a wrong output costs a meeting, a handoff or a long unattended run.

## Look

Read the files, data and history the request touches. Facts you can look up go into the plan as facts. The questions you ask are about intent, which no file holds.

## Stage

Match the request to the user's stage. A request made one stage too early gets a hollow answer: a draft with no thesis, or a recommendation built on guessed criteria.

- **Think**: ask questions that turn the vague into the concrete.
- **Explore**: map the options and their trade-offs.
- **Decide**: weigh the options against the user's decision logic.
- **Execute**: continue with this skill.

## Requirement

Suggest moves on three axes. The user accepts, rewrites or declines each one, and a declined move is recorded with its reason.

- **Altitude**: hand over the outcome, not the step. Ask what should happen after this result, and climb rung by rung. Stop when a rung plainly exceeds what models can own today. That **ceiling** is only found by trying, so the rung below it becomes the **fallback**. Altitude fits outcome-driven work, and work that will be discussed in meetings is a good sign. It fits creative work less well. Climbing often requires changes to the workflow, such as data access, version-to-commit mapping and machines to reproduce on.
- **Depth**: do the task the way a field-leading expert would, one layer below the request. Name the expert move the user did not ask for, the rawest material, and the instruments of the field (databases and statistical models rather than tables). The instruments change the method. A persona only changes the vocabulary. Where it fits, add a **stretch target** that forces a different method, or a test of a belief the user holds, run against raw data, or a new finding shown to predict data it has not seen.
- **Range**: restate the deliverable's noun as verbs, the effect it must have on people. Then assemble the **crew** of fields that do those verbs best, including a **red team**. Ask for what each field *does*, not how it sounds.

Every axis needs a **judge** outside the session that did the work. The judge grades the method as well as the result, because a lucky correct guess should fail and a sound near-miss should pass. Prefer a check the model can run itself (a test, held-out data, a primary source). Otherwise, use separate attacker sessions plus one more session that rules on their objections. When the user can judge the result directly, their judgment is enough.

## Task

Ask the five intent questions. Each one has an answer only the user holds:

- **Purpose**: the decision or problem the output serves. An action ("analyse five competitors") is not a purpose.
- **Context**: what a capable stranger would need to know so they do not aim wrong.
- **Materials**: the sources ranked primary over secondary, the banned sources, and an empty slot for anything not found. An unranked or unbounded source list invites fabrication.
- **Boundaries**: the outputs that would make the user say "not what I wanted". These are **walls**, mostly "don'ts". Directions and adjectives do not count.
- **Done**: what appears in front of the user that means stop. It includes the shape of the artifact and an early **checkpoint**, such as an outline before the full piece, so a wrong direction is caught cheaply. Boundaries and Done together give the scope.

The model can ask these questions, and only the user can answer them. Write each answer in the user's words. Facts you found can go into Context or Materials, marked for the user to confirm. A slot the user cannot answer goes under Open. The gap itself is the finding, so it is never filled with a plausible guess.

## Write

Write `local/plans/<topic>.md` at the workspace root (the git root, or the current directory). `<topic>` is a short kebab-case English slug of the outcome. Ask before you overwrite a file from another task. Use the user's language and keep the plan to one screen:

```markdown
# Plan: <outcome in a few words>

- Asked: <the request as the user wrote it>
- Stage: execute
- Date: <YYYY-MM-DD>

## Requirement
Hand over: <accepted rung>
Fallback: <rung below>
Depth: <raw material; instruments; stretch target>
Range: <verbs; crew and what each does>
Judge: <the outside check, and what it grades>
Needs: <data, access, machines; mark what is missing>
Declined: <move, reason>

## Task
Purpose:
Context:
Materials:
Boundaries:
Done:

## Open
<what the user has not thought through yet; omit when empty>

Ready: <yes | no, because …>
```

`Ready` is yes when the user has ruled on every Requirement move and answered all five Task slots. The plan is done when the user has read it and confirmed the Ready line. Close with the path, and offer `/define-goal` with the plan as its source.

## After a try

When the user brings back a rejected result, find the cause and act on it:

- **Wrong method** (a missed diagnosis, a missing source): use more Depth on the same rung.
- **Too big**: take the Fallback.
- **Missed intent**: go back to the Task slot that let the miss through.

Update the plan in place, and add one dated line under `## Tries` with the verdict and what changed.

## References

- [references/ambition.md](references/ambition.md): the source of the Requirement axes and the judge, with a worked ladder and the expert questions. Read it when a Requirement move needs grounding.
- [references/task-definition.md](references/task-definition.md): the source of the stages and the five slots, with a worked brief. Read it when a Task question needs grounding.


RESULT: total 172
drwxrwxr-x   2 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 109 root root 167936 11月 10 18:03 ..
-rw-rw-r--   1 zdan zdan      0 11月 10 16:17 .keep


TOOL bash: {"command": "date +%F; ls /etc/cron* /var/spool/cron 2>/dev/null; crontab -l 2>&1 | head -5; systemctl --version 2>&1 | head -1"}

RESULT: 2026-11-10
/etc/crontab

/etc/cron.d:
anacron
e2scrub_all

/etc/cron.daily:
0anacron
apache2
apt-compat
aptitude
dpkg
google-chrome
logrotate
man-db
plocate

/etc/cron.hourly:

/etc/cron.monthly:
0anacron

/etc/cron.weekly:
0anacron
man-db

/etc/cron.yearly:

/var/spool/cron:
crontabs
no crontab for zdan
systemd 255 (255.4-1ubuntu8.18)


TOOL write: {"path": "/tmp/pf-30-with_skill-9voo7x8n/local/plans/nightly-jobs-queue-migration.md", "content": "# Plan: nightly jobs stop going missing\n\n- Asked: \"help me plan a migration of our cron jobs to a queue … Write the plan.\"\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\nHand over: not \"12 cron jobs → queue\". The outcome is *every nightly job either runs or is loudly known not to have run*. Queue is one means; detection is the other half. Plan covers both, one checklist per job, each with a signal that proves it ran.\nFallback: the checklist as asked — 12 per-job cutover steps, queue mechanics only, no detection design. Take this if detection is someone else's ticket.\nDepth: rawest material is last month's evidence — `journalctl`/cron mail for the two silent failures, their exit codes, and job runtimes (runtimes set visibility timeouts). Expert move you didn't ask for: a queue alone still fails silently (worker dies mid-message, message lost, poison retry loop) — so each job needs a visibility timeout, a dead-letter queue, and a heartbeat/dead-man's-switch check-in that pages on *absence*, not on error. Stretch target: deliberately break one job in staging and confirm the alert fires — this tests the belief \"queueing them means we stop missing them.\"\nRange: verbs behind the noun \"checklist\" → *prove* (each job ran), *catch* (each failure), *undo* (rollback < 5 min), *own* (a human per job). Crew: an SRE for queue semantics, idempotency and retries (the \"one VM, systemd 255\" fact means systemd timers are a free fallback — no paid service); a data engineer for any job that writes to a DB (re-run safety); a red team for \"2am: worker OOMs mid-job, what does the operator see?\".\nJudge: outside the session that writes it. Primary check: the 2am failure drill above, run against staging, graded on whether absence produced a page. Second: a separate session red-teams each checklist item against the real crontab and logs; a third rules on its objections. A lucky-passing drill (alert fired for the wrong reason) fails.\nNeeds: the actual crontab and 12 job scripts — **not present here** (this machine has only stock `/etc/cron.daily`; no user crontab). Logs from the two failures. Confirm: is the queue already chosen (Redis/RabbitMQ/SQS/…)? Anything paid is excluded, so it must be self-hosted.\nDeclined: —\n\n## Task\nPurpose: no more missed nightly jobs — so a job that didn't run is noticed the same night, not a month later.\nContext: 12 cron jobs on one VM; two failed silently last month and nobody knew. No new paid services. No downtime over 5 minutes.\nMaterials: the crontab (primary, missing here); the 12 job scripts (primary, missing here); last month's logs for the two failures (primary, missing — go get these first); the queue's own docs once chosen (secondary). Banned: none stated.\nBoundaries: anything requiring a paid service; any cutover window over 5 minutes; changing job *logic*, not just how it's scheduled.\nDone: one migration checklist per job (12), each reviewed by you before any change. Early checkpoint: the checklist for **one** job first — the worst-behaved of the twelve — for you to approve before the other eleven are written.\n\n## Open\n- Which queue, and is self-hosted Redis/RabbitMQ acceptable, or is the existing systemd timer enough for the 9 harmless jobs? (\"queue\" may be the wrong instrument for all 12 — worth ruling on.)\n- Do the two failures have logs at all? If not, detection design comes before any migration, and the checklist order changes.\n- Who owns each job after migration — a name per job, or the whole set?\n- 5-minute downtime: for the queue deployment, or per job cutover?\n\nReady: no — the three Requirement moves need your accept / rewrite / decline, and Open #1 changes the shape of all 12 checklists.\n"}

RESULT: Successfully wrote to /tmp/pf-30-with_skill-9voo7x8n/local/plans/nightly-jobs-queue-migration.md

ASSISTANT: Written: `local/plans/nightly-jobs-queue-migration.md`

Your five Task slots transferred intact. Three things I'd push back on before any checklist gets written:

1. **"Migrate to a queue" may be the wrong framing.** The two jobs failed *silently* — that's a detection failure, not a scheduling one. A queue still loses messages (worker dies mid-message, poison retries). The rung above your request: every job either runs or is loudly known not to have run. That means a dead-letter queue plus a heartbeat check that pages on *absence*. Fallback if you decline: the checklist exactly as asked.
2. **The two failures' logs are the rawest material and they're not here.** This box has only stock `/etc/cron.daily` — no user crontab, no job scripts. Without last month's exit codes and runtimes you can't set retry or timeout policy, so the plan's Needs section is a to-do for you.
3. **Not all 12 need a queue.** You're on systemd 255; timers give you dependency ordering and journald logging for free, and "no new paid services" rules out managed queues anyway.

Checkpoint I built in: you approve the checklist for the *worst-behaved single job* before I write the other eleven.

Ready is **no** — the three moves in Requirement need accept/rewrite/decline, and the queue choice reshapes all twelve checklists. Once you've ruled, run `/define-goal` with this plan as its source.