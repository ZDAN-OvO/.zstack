TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/SKILL.md"}

TOOL bash: {"command": "ls -la; echo ---; find . -maxdepth 3 -not -path '*/.git/*' | head -50"}

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

Each section below ends at a **stop**: the point where this turn's reply is sent. Reaching a stop ends the skill for this turn, even when later sections are still unread.

## Enter

1. **Cost.** When a redo costs less than a plan, do the request as written, or ask only the one or two details it needs. A rename, a lookup and a short poem or message are this case, even when the user typed `/preflight`. The plan pays off when a wrong output costs a meeting, a handoff or a long unattended run. Stop.
2. **Consent.** The user typed `/preflight`, or accepted an offer: go on to Look. Otherwise offer the plan in one line and stop. Until the user accepts, the workspace stays unchanged, and that includes `local/plans/`: a plan file written before acceptance is a plan the user never asked for.

Accepting the plan is consent to plan, not to execute. From Look onward, the only file this skill writes is the plan; the work itself starts after the user confirms it.

## Look

Read the files, data and history the request touches. Facts you can look up go into the plan as facts. The questions you ask are about intent, which no file holds.

State each finding at the strength the data supports. Two things that change at the same time are a correlation to test. A cause needs evidence that rules the alternatives out.

## Stage

Match the request to the user's stage. A request made one stage too early gets a hollow answer: a draft with no thesis, or a recommendation built on guessed criteria. Only Execute goes on to Requirement and writes a plan. Each earlier stage gives its own result and stops.

- **Think** (no thesis or no direction yet): ask the questions that turn the vague into the concrete. Stop.
- **Explore** (options named, criteria not set): map the criteria that would separate the options, and the trade-off under each. Ask for the few facts that decide between them, and leave the choice open. Stop.
- **Decide** (options and criteria both given): weigh the options against the user's criteria and give the decision, with the conditions that would reverse it. Stop.
- **Execute** (the user wants the work done): continue with this skill.

## Requirement

Look at the task through all three lenses in this turn. Suggest a move only on a lens where it would change the result, and write `not needed` for the others. A deliverable named by its noun (a deck, a homepage, a report) always gets a Range move. Each suggestion stays a suggestion until the user accepts, rewrites or declines it. A declined move is recorded with its reason. When the user has already ruled on the moves offered earlier in the conversation, the Requirement is settled: record their rulings and open no new moves. A risk you notice goes under Open as a question.

- **Altitude**: hand over the outcome, not the step. Ask what should happen after this result, and climb rung by rung. Stop when a rung plainly exceeds what models can own today. That **ceiling** is only found by trying, so the rung below it becomes the **fallback**. Altitude fits outcome-driven work, and work that will be discussed in meetings is a good sign. It fits creative work less well. Climbing often requires changes to the workflow, such as data access, version-to-commit mapping and machines to reproduce on.
- **Depth**: do the task the way a field-leading expert would, one layer below the request. Name the expert move the user did not ask for, the rawest material, and the instruments of the field (databases and statistical models rather than tables). The instruments change the method. A persona only changes the vocabulary. Where it fits, add a **stretch target** that forces a different method, or a test of a belief the user holds, run against raw data, or a new finding shown to predict data it has not seen.
- **Range**: restate the deliverable's noun as verbs, the effect it must have on people. Then assemble the **crew** of fields that do those verbs best, including a **red team**. Ask for what each field *does*, not how it sounds.

Every move needs a **judge** outside the session that did the work. The judge grades the method as well as the result, because a lucky correct guess should fail and a sound near-miss should pass. Prefer a check the model can run itself (a test, held-out data, a primary source). Otherwise, use separate attacker sessions plus one more session that rules on their objections. When the user can judge the result directly, their judgment is enough.

## Task

Ask the five intent questions. Each one has an answer only the user holds:

- **Purpose**: the decision or problem the output serves. An action ("analyse five competitors") is not a purpose.
- **Context**: what a capable stranger would need to know so they do not aim wrong.
- **Materials**: the sources ranked primary over secondary, the banned sources, and an empty slot for anything not found. An unranked or unbounded source list invites fabrication.
- **Boundaries**: the outputs that would make the user say "not what I wanted". These are **walls**, mostly "don'ts". Directions and adjectives do not count.
- **Done**: what appears in front of the user that means stop. It includes the shape of the artifact and an early **checkpoint**, such as an outline before the full piece, so a wrong direction is caught cheaply. Boundaries and Done together give the scope.

The model can ask these questions, and only the user can answer them. Use what the user has already said in this conversation, and ask only for what is missing. Write each answer in the user's words. Facts you found can go into Context or Materials, marked for the user to confirm.

A Purpose or Done the user cannot answer stays empty, and the question goes under Open. The gap itself is the finding. Ask a question that helps the user answer it, and write no default for them to approve. For Materials, you may propose a source ranking, banned sources and a leave-blank rule; they go under Proposed for the user to rule on.

## Write

Write `local/plans/<topic>.md` at the workspace root (the git root, or the current directory). `<topic>` is a short kebab-case English slug of the outcome. Write the plan in the same turn as Requirement and Task, with unanswered slots under Open; Ready tells the user what is still missing.

Check the path before the write. When a file there belongs to another task, keep it unchanged. Ask which path to use, or write to a new slug and name it in the reply. A backup copy does not count as permission to overwrite.

Use the user's language and keep the plan to one screen:

```markdown
# Plan: <outcome in a few words>

- Asked: <the request as the user wrote it>
- Stage: execute
- Date: <YYYY-MM-DD>

## Requirement
Hand over: <accepted rung, or the request as asked>
Fallback: <rung below>
Depth: <raw material; instruments; stretch target | not needed>
Range: <verbs; crew and what each does | not needed>
Judge: <the outside check, and what it grades>
Needs: <data, access, machines; mark what is missing>
Proposed: <moves the user has not ruled on yet; omit when the user has ruled on them all>
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

`Ready` is yes when the user has ruled on every proposed move and answered all five Task slots. The plan is done when the user has read it and confirmed the Ready line. Close with the path, and offer `/define-goal` with the plan as its source. Stop.

## After a try

When the user brings back a rejected result, find the cause and act on it:

- **Wrong method** (a missed diagnosis, a missing source): use more Depth on the same rung.
- **Too big**: take the Fallback.
- **Missed intent**: go back to the Task slot that let the miss through.

Update the plan in place, and add one dated line under `## Tries` with the verdict and what changed. Stop.

## References

- [references/ambition.md](references/ambition.md): the source of the Requirement axes and the judge, with a worked ladder and the expert questions. Read it when a Requirement move needs grounding.
- [references/task-definition.md](references/task-definition.md): the source of the stages and the five slots, with a worked brief. Read it when a Task question needs grounding.


RESULT: total 184
drwxrwxr-x  4 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 64 root root 167936 11月 10 21:35 ..
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 analytics
-rw-rw-r--  1 zdan zdan    151 11月 10 16:17 index.html
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 support
---
.
./index.html
./support
./support/chats-sample.md
./analytics
./analytics/weekly.csv


TOOL bash: {"command": "cd /tmp/pf-27-with_skill-6woxvi5k; echo '=== index.html'; cat index.html; echo; echo '=== weekly.csv'; cat analytics/weekly.csv; echo; echo '=== chats'; cat support/chats-sample.md"}

RESULT: === index.html
<h1>The all-in-one platform for modern teams</h1>
<p>Boost productivity with our seamless, AI-powered workspace.</p>
<a href="/signup">Get started</a>

=== weekly.csv
week,visits,signups,conversion,top_source
2026-10-06,12000,480,4.0%,organic
2026-10-13,11800,460,3.9%,organic
2026-10-20,19500,390,2.0%,paid_social
2026-10-27,21000,399,1.9%,paid_social

=== chats
- "我还是没搞懂你们和 Notion 有什么区别"
- "价格页在哪？"
- "注册后要连日历，我就放弃了"


TOOL bash: {"command": "cd /tmp/pf-27-with_skill-6woxvi5k; ls -la local/plans 2>/dev/null; date +%F"}

RESULT: 2026-11-10


TOOL write: {"path": "/tmp/pf-27-with_skill-6woxvi5k/local/plans/paid-social-signup-rate.md", "content": "# Plan: 付费社媒新访客注册率回到 3.5%\n\n- Asked: 首页转化率掉了一半，帮我重写首页文案\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\nHand over: 3 版首屏标题+副标题（用户先挑一版），再上 A/B，目标付费社媒新访客注册率 3.5%\nFallback: 只改首屏标题（已接受）\nDepth: 已接受——逐条引用 support/chats-sample.md 原话，按来源拆 analytics/weekly.csv 漏斗，不凭感觉写\nRange: 已由用户裁决——不新增；素材限定在 support 聊天与 analytics\nJudge: A/B 结果本身（分来源看注册率）；上线前由用户挑版\nNeeds: 3.5% 目标对应的每臂样本量（见 Open）；paid_social 落地页来源参数与注册漏斗埋点是否可拆到首屏来源\nDeclined: 用网上竞品文案（用户：不用）；改定价、加弹窗、承诺没有的功能（用户：不改）\n\n## Task\nPurpose: 让付费社媒带来的新访客看懂“我们和 Notion 的区别”并完成注册，注册率从 1.9–2.0% 回到 3.5%\nContext: B2B 协作工具；新访客多不懂我们和 Notion 的区别；降价那周起 top_source 从 organic 变为 paid_social（10-06/13 约 3.9–4.0%，10-20/27 约 1.9–2.0%）\nMaterials: 一手——support/chats-sample.md（3 条原话）、analytics/weekly.csv、现首页 index.html；禁用——网上竞品文案\nBoundaries: 不改定价；不加弹窗；不承诺没有的功能\nDone: 3 组“标题+副标题”交到用户手上，附各自对应的聊天原话与取舍理由；用户挑定一版后才进入 A/B\n\n## Open\n- 转化腰斩与来源切换同时发生，目前只是相关：先确认 paid_social 访客的注册率是否同样低，文案才能算主因\n- 3.5% 需要每臂约 3.8k 访客（2.0%→3.5%，80% 功效）；按 20k/周约 2 周可读出结果，用户是否接受这个周期\n- 聊天里“注册后要连日历，我就放弃了”指向注册流程而非首屏文案，且“价格页在哪”指向导航；边界内无法处理，是否记为已知限制\n- paid_social 新访客意图可能低于 organic，3.5% 是否仍为合理目标\n\nReady: no —— 需确认上述 4 个 Open 项（尤其第 1 项与第 3 项）\n"}

RESULT: Successfully wrote to /tmp/pf-27-with_skill-6woxvi5k/local/plans/paid-social-signup-rate.md

TOOL read: {"path": "/tmp/pf-27-with_skill-6woxvi5k/local/plans/paid-social-signup-rate.md"}

RESULT: # Plan: 付费社媒新访客注册率回到 3.5%

- Asked: 首页转化率掉了一半，帮我重写首页文案
- Stage: execute
- Date: 2026-11-10

## Requirement
Hand over: 3 版首屏标题+副标题（用户先挑一版），再上 A/B，目标付费社媒新访客注册率 3.5%
Fallback: 只改首屏标题（已接受）
Depth: 已接受——逐条引用 support/chats-sample.md 原话，按来源拆 analytics/weekly.csv 漏斗，不凭感觉写
Range: 已由用户裁决——不新增；素材限定在 support 聊天与 analytics
Judge: A/B 结果本身（分来源看注册率）；上线前由用户挑版
Needs: 3.5% 目标对应的每臂样本量（见 Open）；paid_social 落地页来源参数与注册漏斗埋点是否可拆到首屏来源
Declined: 用网上竞品文案（用户：不用）；改定价、加弹窗、承诺没有的功能（用户：不改）

## Task
Purpose: 让付费社媒带来的新访客看懂“我们和 Notion 的区别”并完成注册，注册率从 1.9–2.0% 回到 3.5%
Context: B2B 协作工具；新访客多不懂我们和 Notion 的区别；降价那周起 top_source 从 organic 变为 paid_social（10-06/13 约 3.9–4.0%，10-20/27 约 1.9–2.0%）
Materials: 一手——support/chats-sample.md（3 条原话）、analytics/weekly.csv、现首页 index.html；禁用——网上竞品文案
Boundaries: 不改定价；不加弹窗；不承诺没有的功能
Done: 3 组“标题+副标题”交到用户手上，附各自对应的聊天原话与取舍理由；用户挑定一版后才进入 A/B

## Open
- 转化腰斩与来源切换同时发生，目前只是相关：先确认 paid_social 访客的注册率是否同样低，文案才能算主因
- 3.5% 需要每臂约 3.8k 访客（2.0%→3.5%，80% 功效）；按 20k/周约 2 周可读出结果，用户是否接受这个周期
- 聊天里“注册后要连日历，我就放弃了”指向注册流程而非首屏文案，且“价格页在哪”指向导航；边界内无法处理，是否记为已知限制
- paid_social 新访客意图可能低于 organic，3.5% 是否仍为合理目标

Ready: no —— 需确认上述 4 个 Open 项（尤其第 1 项与第 3 项）


ASSISTANT: 计划已写好：`local/plans/paid-social-signup-rate.md`

要点：
- **Requirement 已全部按你的裁决记录**（不新增提议）：交付 3 版首屏标题+副标题 → 你挑一版 → A/B；退路只改首屏标题；素材限 support 聊天 + analytics，禁用网上竞品文案。
- **判断口径**：分来源看注册率，A/B 结果是唯一裁判。
- **Ready: no**，四件事需要你点头：
  1. 腰斩和来源切换同时发生，现在只是**相关**——需要先确认 paid_social 访客注册率本身同样低，文案才可能是主因。
  2. 3.5% 每臂约需 3.8k 访客，约 2 周才读得出结果，可接受吗？
  3. 聊天里“要连日历就放弃了”“价格页在哪”指向注册流程和导航，不在你给的边界内——记为已知限制？
  4. paid_social 意图可能低于 organic，3.5% 仍是合理目标？

确认后我按 Done 的定义直接产出 3 组标题+副标题（各附对应聊天原话和取舍理由）。下一步可用 `/define-goal` 以这份 plan 为源。