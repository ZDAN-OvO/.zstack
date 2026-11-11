TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/SKILL.md"}

TOOL bash: {"command": "ls -la; echo ---; ls support 2>/dev/null; echo ---; ls analytics* 2>/dev/null"}

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
drwxrwxrwt 65 root root 167936 11月 10 21:42 ..
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 analytics
-rw-rw-r--  1 zdan zdan    151 11月 10 16:17 index.html
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 support
---
chats-sample.md
---
weekly.csv


TOOL bash: {"command": "cat analytics/weekly.csv; echo ===; cat support/chats-sample.md; echo ===; cat index.html"}

RESULT: week,visits,signups,conversion,top_source
2026-10-06,12000,480,4.0%,organic
2026-10-13,11800,460,3.9%,organic
2026-10-20,19500,390,2.0%,paid_social
2026-10-27,21000,399,1.9%,paid_social
===
- "我还是没搞懂你们和 Notion 有什么区别"
- "价格页在哪？"
- "注册后要连日历，我就放弃了"
===
<h1>The all-in-one platform for modern teams</h1>
<p>Boost productivity with our seamless, AI-powered workspace.</p>
<a href="/signup">Get started</a>


TOOL bash: {"command": "date +%F; git rev-parse --show-toplevel 2>/dev/null || echo \"no git\"; ls -la local/plans 2>/dev/null || echo \"no local/plans\""}

RESULT: 2026-11-10
no git
no local/plans


TOOL write: {"path": "/tmp/pf-27-with_skill-wadq00_h/local/plans/paid-social-signup-lift.md", "content": "# Plan: 付费社媒新访客注册率回到 3.5%\n\n- Asked: 首页转化率掉了一半，帮我重写首页文案（先给 3 版首屏标题+副标题，我挑一版再上 A/B）\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\nHand over: 3 版首屏标题+副标题，每版对准 support 聊天里的一条真实异议；由你在三者中挑一版上 A/B（已接受）\nFallback: 只改首屏标题，不动副标题与其余部分（已接受）\nDepth: 已接受\"先确认不是文案问题再改\"：转化 4.0%/3.9%（organic）→ 2.0%/1.9%（paid_social）与来源切换同周发生，同期访问量 12000→19500 而注册数 480→390 下降——文案是待验证假设，不是已定原因。素材用自家 support 聊天 + analytics，不用网上竞品文案（已接受）\nRange: 交付物是3版首屏文案，不是首页重设计。角色：转化文案（按异议写）、定位（和 Notion 的分界）、增长分析（定指标与判定）；红队：一个 Notion 老用户视角的付费社媒访客，逐句攻\"空话\"和\"没证据的承诺\"\nJudge: paid_social 新访客的注册率 A/B。判方法不只判结果：每版预登记假设、相对控制组只改一处、跑满整周、每版声称解决的异议须能追到某条聊天原话。红队攻完，你挑版本（你的判断对\"挑哪版\"已足够）\nNeeds: analytics/weekly.csv（有）；support/chats-sample.md（仅3条，有）；缺：按来源拆分的注册数（现只有周级总量）、付费社媒广告素材/落地页对应关系、注册流程截图\nDeclined: 无\n\n## Task\nPurpose: 你最终要挑一版上 A/B，用数据判断\"付费社媒来的新访客听不懂我们和 Notion 的区别\"是否真是注册率掉的原因\nContext: B2B 协作工具；新访客多数不知道我们和 Notion 的区别；掉的那两周流量来源从 organic 换成 paid_social，访问量涨了约 63% 但注册数绝对值在跌\nMaterials: 一手 = support/chats-sample.md（3条异议）、analytics/weekly.csv（4周、周级、注册数不分来源）；禁用 = 网上竞品文案；空白位 = 付费社媒投放素材、分来源注册数、注册流程截图\nBoundaries: 不改定价；不加弹窗；不承诺没有的功能\nDone: 先看到 3 版首屏标题+副标题（这一步就是检查点，方向错了在这里改）；你挑定一版后才上 A/B，A/B 结果回到你手上算结束\n\n## Open\n1. 3.5% 指整体注册率还是 paid_social 注册率？现在 paid_social 是 1.9–2.0%，到 3.5% 是相对 +79%，已接近 organic 的 4.0% 基线。口径不同，验收结论会相反。\n2. 聊天里 3 条异议中 2 条文案治不了：找不到价格页（导航问题）、注册要连日历就放弃（流程问题）。首屏文案只能处理\"和 Notion 的区别\"这一条。这版 A/B 若只动文案，3.5% 可能达不到——这次是仍以 3.5% 验收，还是先定一个可达的中间目标（例如 2.6%），另外两条另开一项？\n3. A/B 的样本与停手规则未定：按 1.9%→3.5% 估算，每组约需 1600 名付费社媒新访客（按当前流量约 2 天/组，但要跑满整周覆盖周内波动）；差异不显著时由谁决定下一步？\n4. 缺付费社媒的广告文案。没有它，首屏无法和广告做 message match（这是提升 paid_social 转化最直接的一招）。自家投放素材能不能给到？\n\nReady: no，因为 Open 1（3.5% 的口径）和 Open 2（是否接受文案只覆盖三分之一的异议）决定验收标准，不先定的话 3 版文案写出来也无法判定合格\n"}

RESULT: Successfully wrote to /tmp/pf-27-with_skill-wadq00_h/local/plans/paid-social-signup-lift.md

ASSISTANT: 计划已写好：`local/plans/paid-social-signup-lift.md`

我先把“要改什么”固定下来：3 版首屏标题和副标题，让付费社媒访客能从一版中看懂产品与 Notion 的区别，然后由你挑一版做 A/B。你已接受的四项（先确认原因不在文案、素材只用自家 support 和 analytics、用 A/B 判定、退路只改首屏标题）都记在 Requirement 里，没有新加要求。

读文件后，有两个发现必须请你先决定：

- **注册数在跌，不只转化率在跌**：访问量从 12000 增至 19500（+63%），注册数从 480 降到 390。所以问题也包括付费社媒带来的访客本身不注册，转化率的算术结果不能解释全部。
- **聊天里 3 条异议，文案只能处理 1 条**：找不到价格页（导航问题）、注册时要连日历就放弃（流程问题）。“和 Notion 的区别”只有这一条能靠首屏解决。

这两点合起来意味着：只靠改文案，付费社媒注册率可能到不了 3.5%（现在 1.9–2.0%，到 3.5% 是相对 +79%，已接近 organic 的 4.0%）。

Ready 写的是 **no**，因为还有两个问题没回答：**3.5% 指整体还是 paid_social 口径**；以及**这一版是否接受文案只处理三分之一的异议**。另外还有 A/B 停手规则，以及能否提供自家投放素材（没有它就无法与广告做 message match）。这四条你回答后，我再动手写 3 版。

要不要用 `/define-goal` 把这份 plan 作为输入？