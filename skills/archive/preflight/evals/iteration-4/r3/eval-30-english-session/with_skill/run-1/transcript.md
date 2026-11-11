TOOL bash: {"command": "ls -la /tmp/pf-30-with_skill-nyfbi327 && echo \"---\" && find /tmp/pf-30-with_skill-nyfbi327 -maxdepth 3 -not -path '*/.git/*' | head -50"}

RESULT: total 172
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 66 root root 167936 11月 10 22:48 ..
-rw-rw-r--  1 zdan zdan      0 11月 10 16:17 .keep
---
/tmp/pf-30-with_skill-nyfbi327
/tmp/pf-30-with_skill-nyfbi327/.keep


TOOL bash: {"command": "cd /home/zdan/.zstack/skills/plan/preflight && wc -l references/*.md && echo \"=== ambition ===\" && cat references/ambition.md && echo \"=== task ===\" && cat references/task-definition.md"}

RESULT:    61 references/ambition.md
   66 references/task-definition.md
  127 total
=== ambition ===
# Ambition: distilled

Source of the Requirement axes and the judge in `/preflight`. Distilled from Felix Rieseberg (engineering lead on Claude at Anthropic):

- **[E]** Essay, "How to be more ambitious: A tutorial for humans with models", 2026-10-13. <https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/>
- **[I]** Interview, Silicon Valley Girl, "Claude Engineering Lead: Stop Using Claude Like It's 2024", 2026-10-20. <https://www.youtube.com/watch?v=D-SVFneJ_Nk>. Timestamps are approximate and come from the auto-captions.

## Thesis

- **Best guess.** A task given to the model is the user's best guess at a route to an outcome. The model runs the guess. [E]
- **Four types.** Ambition comes in four types: speed, altitude, depth and range. Speed means the same work done faster. It is well established and needs no new thinking, so the skill leaves it out. [E]
- **Self-efficacy.** People are held back by what they believe is possible. Specific, hard goals beat "do your best" (Locke and Latham, 35 years of studies). Belief, a visible precedent and permission to fail all raise what gets attempted. The studies are on humans; carrying them over to models is Felix's extension. [E]

## Altitude

- **Goal beyond the goal.** Ask what should happen next, then hand that over. The crash example climbs from "fix this crash" to "keep the apps crash-free". [E]
- **Ceiling.** Keep climbing until the model fails. "Go make money" is past the line today. Work at the ceiling sits at the frontier and gains the most from the next model. [I 39:05]
- **Fit.** Altitude fits work after an ultimate outcome. Work that will be discussed in meetings is a good sign. It fits creative work less well. [E]
- **Workflow cost.** Climbing usually means rebuilding access first. Crash-free needed crash-report fetching, a version-to-commit map, and Windows, macOS and Linux machines to reproduce and verify on. The setup cost is real and worth paying. [E] [I 22:39]
- **Conveyor belt.** A user who carries items to the model one at a time is the bottleneck. Give the model the whole data source and let it choose what to act on. [I 22:39]

Worked ladder, a quarterly business review [E]:

1. Update the template's numbers.
2. What changed this quarter, why, and what to do.
3. The three most urgent decisions, with the case for and against each.
4. Replace the deck with a better way for leadership to catch problems early and move money and people. Prove on past history that it would have caught them sooner, then run it beside the deck for a quarter.

## Depth

- **Instruments, not costume.** A persona switches the vocabulary and keeps the method. Ask which tools the top of the field uses, then require those tools, and get the result explained plainly. The leap in AI 3D and motion work came from using Blender, not from a better grasp of animation. [E] [I 10:28, 25:20]
- **Stretch target.** Set an unreasonable goal and treat it as reasonable: 200 ms, not 5 s. When the model says it is impossible, tell it to keep going. [E]
- **Challenge beliefs.** Give the model the raw data and have it try to reproduce a belief the user holds ("churn is an onboarding problem"). [E]
- **New knowledge.** From inside the data, look for the blind spot: an unknown early signal, shown to predict data it has not seen. [E]
- **Expert questions.** Before the task is rewritten, name four things: (1) what a top professional would do that is not being asked; (2) the rawest material they would start from; (3) their specific methods and tools; (4) what, other than the model or the user, would show the result is right. Then rewrite the task to ask for exactly that. [E]
- **Process.** For work that rests on taste, the gain comes from copying the steps professionals take, since good work comes out of a refined process. [I 8:26–9:52]

## Range

- **Noun to verb.** A deliverable's name hides its job. A quarterly review is not "a deck". It gets busy people to believe a cause-and-effect story and decide under uncertainty in 30 minutes. The verbs show which fields can help. The idea comes from Kelley and Littman, *The Art of Innovation*. [E]
- **Crew.** Ask which team would be assembled if the stakes were extreme. For the review: an analyst, a journalist and an editor; a motion and audio designer if it is presented; a short seller and a forensic accountant as the red team. [E]
- **Do, not write.** Use the crew to find fields and techniques. Ask the model to do the short seller's research, not to write in a short seller's voice. Role play makes the transcript stranger and the output no better. [E]

## Judge

- **Outside session.** The session that did the work is a poor judge of it. Far more tasks are unsafe to trust to a single session than to the model. Prefer a check the model can run and get feedback from at once. [E] [I 26:10]
- **Grade the process.** A correct guess of the temperature fails. A half-degree miss that came from the right location and a reputable source passes. [I 7:35]
- **Adversarial review.** When nothing hard can check the work, spin off sessions whose only job is to prove the output wrong, as red teams and short sellers do. Finding flaws is easier than building, so a cheaper model can do the attacking. Then one more session rules on which objections hold. Valid objections go back to the maker, which can decline them. [I 12:57–15:39]
- **User as client.** When the user can tell good from bad themselves, their judgment of the result is enough. When they cannot, add more AI review. [I 16:15]
- **Fact checks.** Requiring a verified primary source for every number in a document can be trusted to a single session. [I 17:03]

## Access

- **Model experience.** Picture yourself as the model doing this task. You would want the raw data, a computer, the ability to install software, and room to decide for yourself. [I 22:01]
- **Prerequisite.** Every type of ambition needs a computer that can install software, plus access to the relevant data. [E]
- **Start cheap.** Let the model drive the user's tools in a browser first. Build connectors only after a workflow has proven itself. [I 24:00]
- **Generalists.** Give a generalist model the tools and the data rather than a cast of narrow persona agents with pre-sliced data. Generalist models overtook a purpose-built math system within months. [I 17:37]

## On skills

- **Half-life.** Skills often carry advice meant for the previous model generation, and removing a skill sometimes improves the output. Making that call takes an eval and a clear sense of good and bad output. [I 21:26]
=== task ===
# Task definition: distilled

Source of the stages and the five slots in `/preflight`. Distilled from Gary Chen, 《Prompt 再完整也没用：先学会定义任务》, Bilibili BV1fseX6vE2L, about 20 min. <https://www.bilibili.com/video/BV1fseX6vE2L/>. Timestamps come from the auto transcript.

## Thesis

- **Two layers.** Writing a prompt makes the words precise. Defining the task decides what is wanted. The prompt is the floor, the task decides the height. An empty task gives an empty output however polished the words; a defined task makes the prompt write itself. [0:34–1:30]
- **Senior, not intern.** Current models read, revise, verify and re-plan on their own. Scripting the steps is intern-era management. Brief the what, the why, the walls and the stop, and leave the how to the model. [2:53–3:58]
- **Content, not intent.** The model challenges facts. It never questions what the user wants, and it acts on receipt. [4:11, 15:32]
- **Mirror.** Vague intent comes back as generic output. "Ask me if unsure" only turns an essay question into a fill-in-the-blank. The model can ask, but the blanks are still the user's to fill. [16:02–16:27]
- **Management.** Defining a task is thinking (what do I want, what does it support, what counts as good) plus communication (making it clear to another capable mind). A good brief is hard to write mostly because the thinking is unfinished. Human reports often do not dare to ask back either. [17:16–18:31]

## Stages

Serious knowledge work moves through **think → explore → decide → execute**. A request made at the wrong stage gets the wrong job [5:07–6:14]:

| Stage | What the model should do | What a request from the next stage gets |
|---|---|---|
| Think | Ask the user questions until the vague becomes concrete | A full draft: the version anyone could write, with no thesis |
| Explore | Map the options and the trade-offs | A recommendation: a guess at criteria the user has not set |
| Decide | Weigh the options against the user's decision logic | — |
| Execute | Work from the five slots | — |

The model never says the stage is wrong. The skill is to pause and name the stage first. [5:54]

## Five slots

| Slot | Question the user asks themselves | Without it |
|---|---|---|
| Purpose | What will I do with this output? | The model performs the action textbook-style: everything covered, nothing to decide on. |
| Context | What would a capable stranger need to know before taking over? | The model assumes the generic case: a big company, free to change prices, competing with everyone. |
| Materials | What should it work from? | Anything not banned counts as allowed. Sources go unranked, and gaps get plausible inventions. |
| Boundaries | What output would make me say "not what I wanted"? | The open space fills with directions nobody imagined. |
| Done | What appears in front of me that means I can stop? | A wrong direction surfaces at page 30, not at the outline. |

[7:20–13:11, summary 19:19]

- **Purpose is a decision, not an action.** "Analyse five competitors" is an action. "Support next quarter's call between easier and cheaper, and end with one recommendation" is a purpose, and it lets the model narrow its focus on its own. [7:33–8:17]
- **Context sets the angle.** Context is not extra information. It decides how the model looks at the task. [9:09]
- **Narrowing is defining.** Studying three overlapping rivals in depth beats scanning five. [9:50]
- **Leave blank.** Write "not found, leave it blank, do not invent" into Materials, and ban low-trust sources by name. [10:08]
- **Walls versus directions.** Purpose, Context and Materials give direction. Boundaries are the walls, mostly "don'ts". Most briefs give direction and no walls. [11:14]
- **What, not how.** Specifying the artifact (an outline, Markdown, 3–4 bullets per section) is part of Done. Micromanagement governs the process; the artifact's shape is the user's call. [12:27]
- **Checkpoint.** The most valuable line in Done: "give me the framework first, not the full report". [12:54]
- **Scope.** Boundaries say what not to do, and Done says where to stop. Together they give the scope. [13:11]

## When to skip

There is one test: is a redo expensive? Skip the brief for a quick question or a lookup. Write it for output that goes to a meeting, to another person, or comes from a long unattended run. Ten minutes of briefing beats three reruns. [15:04]

## Worked brief, a SaaS competitor analysis

| Slot | Brief [7:54–12:26] |
|---|---|
| Purpose | Next quarter's product direction: should the USP lean easier or cheaper? End with one recommendation and the reasons. |
| Context | A ~$2M-revenue marketing-automation SaaS. Customers are mostly firms under 50 people who say the product is complex and expensive. Last year's price change landed badly. |
| Materials | Primary: three rivals' sites and product docs. Secondary: the user's compiled reviews. No second-hand review articles. Not found → leave blank. |
| Boundaries | No invented ARR, user counts or growth rates. Do not touch the tier structure (pricing position is open). No adjective-only output without trade-offs. |
| Done | An outline first: key differences, the recommended USP, and the reasoning. The full report only after review. Markdown, 3–4 bullets per section. |

The vague prompt gave five near-identical rivals and no direction. The brief gave an outline that picks easier, benchmarks the rival with three-step onboarding, and flags that easier and cheaper conflict. That outline is ready for a meeting. The figures are the video's case setup, not industry data. [13:52–14:37]

## Unverified

- The video gives no tested wording for making the model ask back.
- It cites the Microsoft and LinkedIn 2024 Work Trend Index without quoting it. Check the report before citing it.


TOOL bash: {"command": "cd /tmp/pf-30-with_skill-nyfbi327 && date +%F && ls local/plans 2>/dev/null || echo \"no plans dir yet\""}

RESULT: 2026-11-10
no plans dir yet


TOOL write: {"path": "/tmp/pf-30-with_skill-nyfbi327/local/plans/nightly-job-reliability.md", "content": "# Plan: No more silently missed nightly jobs\n\n- Asked: \"help me plan a migration of our cron jobs to a queue\"\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\n\n**Hand over (proposed rung above the request):** every one of the 12 nightly jobs either completes or raises a human-visible alarm within a stated window — a miss can never again go unnoticed for a month. The queue becomes one option inside that guarantee, not the goal.\n\n**Fallback (the request as written):** a per-job migration checklist, reviewed before any change. Take this if the rung above needs access you do not have yet (logs, alert channel, queue host).\n\n**Depth:** the expert move not asked for is *measure before you migrate*. Rawest material: cron/journal logs, per-job exit codes, start/end times, overlap, and the last-run timestamps of the two silent failures — to establish whether they ever reached cron. Instruments: per-job contract (schedule, max runtime, idempotency, downstream readers), at-least-once vs at-most-once reasoning, retry with backoff, dead-letter visibility, and a heartbeat/dead-man's-switch on the schedule itself. *Stretch target:* replay 12 jobs under injected faults (worker killed mid-run, DST/weekend skip, duplicate delivery, job outliving its lock, no network) and show each job either completes or alarms — zero silent misses. *Belief to test:* \"a queue prevents missed jobs.\" A queue prevents lost messages; if the enqueuer dies the queue stays empty and silent. That reframes the whole plan around the scheduler and the alarm, not the broker.\n\n**Range:** the deliverable's verbs — (1) make the current failure modes visible, (2) decide a delivery guarantee per job, (3) make each job safe to re-run, (4) make a miss loud, (5) keep rollback and manual run in an operator's hands. Crew: a reliability/SRE engineer for guarantees, SLO and alerting; a Postgres/Redis person for a transactional enqueue (`SKIP LOCKED`) if the queue is DB-backed; a security reviewer for secrets in job scripts and egress; red team: someone paid to make the migration *lose* a job — kills workers, duplicates, drifts the clock, runs the job twice.\n\n**Judge:** an outside session running the fault-injection harness above, plus one per-job duplicate-run test. It grades method as well as result: each checklist item must name its guarantee, its alarm and the evidence line it came from (log, script, or a stated assumption), and each of the two past failures must be traced to a primary log line or marked unresolved. Your own review of the checklist is the second judge, not the first.\n\n**Needs:** crontab, the 12 job scripts, 30–90 days of cron/exec logs, the identity and logs of the two failed jobs, downstream readers per job, what software/egress the VM already has, and whether a queue may run on the same VM. *Missing: all of it — the workspace is empty; no crontab or script was found.*\n\n**Declined:** none yet.\n\n## Task\n\n**Purpose:** no more missed nightly jobs. Two failed silently last month.\n**Context:** 12 cron jobs on one VM. *(User-stated, confirm: single host, so a queue on that host is still one point of failure.)*\n**Materials:** primary — the crontab and job scripts. Add, ranked: cron/exec logs and the failed jobs' own output. Banned: undocumented blog configs, assumed job behaviour. Not found → leave blank, do not invent.\n**Boundaries:** no new paid services. No downtime over 5 minutes. *(Proposed walls, accept or reject: never change a job's business logic; never retire a cron entry before its replacement has proven a full cycle; no big-bang cutover night; no secrets in the queue payload.)*\n**Done:** a migration checklist per job, reviewed by you before any change. *(Proposed shape: first a one-page reliability map — per job: trigger, guarantee, what breaks it, how a miss becomes visible — approved by you, then the per-job checklists. Markdown, one page per job.)*\n\n## Open\n\n- Is the queue required by the goal, or is the missing piece detection, retries and idempotency? The two silent failures suggest the latter.\n- Root cause of the two silent failures: never ran, ran and errored, or ran and did nothing?\n- Are the jobs idempotent today? Cannot tell without the scripts.\n- Where does an alarm go at 03:00, and who acts on it?\n- Does \"no downtime over 5 minutes\" mean per job, or the whole nightly batch?\n- Does the queue host get to be a second machine, or must it share the VM?\n\n## Tries\n\n*(none yet)*\n\n---\n\nReady: no — the three Requirement moves above are proposed, not ruled; the workspace holds none of the Materials.\n"}

RESULT: Successfully wrote to /tmp/pf-30-with_skill-nyfbi327/local/plans/nightly-job-reliability.md

ASSISTANT: Plan written: `/tmp/pf-30-with_skill-nyfbi327/local/plans/nightly-job-reliability.md`

Two things before it can run:

1. **The workspace is empty** — no crontab, no job scripts, no logs. Materials are listed but none are reachable, so every per-job claim would be invented. Needs a path to those files (copy the crontab and scripts in, or paste the two failed jobs' logs).
2. **The queue may be the wrong instrument.** Your goal is "no missed nightly jobs"; a queue prevents lost *messages*, not missed *schedules* — if the enqueuer dies, the queue is simply empty and silent, which is the same failure that burned you last month. Worth deciding whether the real missing piece is detection + retry + idempotency, with the queue as one option.

The plan records that as the rung above your request, with your per-job checklist as the fallback — so it's useful either way.

Ready is **no**: rule on the three Requirement moves (hand-over, depth, range) and fill the Open gaps. When you have, `Ready` becomes yes and `/define-goal` can take this plan as its source.