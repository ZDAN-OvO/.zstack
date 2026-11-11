TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/SKILL.md"}

TOOL ls: {"path": "/tmp/pf-25-with_skill-cqp3jorq"}

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
2. **Consent.** The user typed `/preflight`, or accepted an offer: go on to Look. Otherwise offer the plan in one line and stop. The workspace stays unchanged until the user accepts.

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

Look at the task through three lenses. Suggest a move only on a lens where it would change the result, and write `not needed` for the others. Each suggestion stays a suggestion until the user accepts, rewrites or declines it. A declined move is recorded with its reason.

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

A slot the user cannot answer stays empty, and the question goes under Open. The gap itself is the finding. Ask a question that helps the user answer it, and write no default for them to approve.

## Write

Write `local/plans/<topic>.md` at the workspace root (the git root, or the current directory). `<topic>` is a short kebab-case English slug of the outcome. The plan may carry Open items; Ready tells the user what is still missing.

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
Proposed: <moves awaiting the user's ruling; omit when empty>
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


RESULT: .keep

TOOL bash: {"command": "timeout 8 curl -sS -o /dev/null -w '%{http_code}\\n' https://www.aliyun.com 2>&1; timeout 8 curl -sS -o /dev/null -w '%{http_code}\\n' https://www.baidu.com 2>&1"}

RESULT: 403
200


ASSISTANT: 网络能通（baidu 200），我可以去抓官网定价页 —— 但先说结论：**现在去写调研报告还早一步。**"下季买哪家"是个决策，而决定这个决策的标准你一个都还没给，我现在跑出来的只会是一张按标价排的表格，选错的概率很高。

## 卡在哪

你补的这句只解决了"目的"，没解决"比较什么"：

- **"买哪家"没有判定标准。** 国内这几家（通义灵码、Trae/字节、CodeBuddy、百度 Comate、Cursor 系国内代理、JetBrains AI 等）的价目单位根本不可比：有的按席位包月，有的按 token/请求额度，有的标价旁边写着"企业版请咨询"。同一个团队，按标价能算出三种排序。
- **"随便上网找"是个陷阱。** 定价页有 403、有 JS 渲染、有仅登录可见，还有大量二手博客转载的过期价格。不先定来源优先级，我就会拿一篇 2024 年的文章当依据。而且团队采购的真实成本从来不是标价，是**重度用户的实际月消耗**。

## 先定能分出高低的标准（按对采购的影响排序）

| 标准 | 为什么它决定选谁 |
|---|---|
| 计价单位与额度上限 | 包月低价常对重度用户设限；超限后的边际价可能反超旗舰 |
| 能力是否够用 | 只补全 vs 多文件 agent 改动，是两档东西。能力不达标的便宜不算便宜 |
| 合规硬约束 | 代码能否出内网/出境、是否必须私有化、要不要 SSO 与审计日志。这条不过，价格无意义 |
| 与现有链路集成 | IDE、GitLab/CI 接不上，省的钱全赔在切换上 |
| 迁移与锁定成本 | 配置、习惯、历史会话 |

而这些标准里，**合规和能力两条是硬门槛，价格只是门槛内的排序**。你如果只想要"哪家最便宜"，那答案大概率是错的那个。

## 我需要你回答四个问题（只有你知道）

1. **多少人、什么结构？** 总席位 + 其中多少是每天写几小时代码的重度用户。
2. **预算上限是多少，是"每人每月"还是"季度总额"？**
3. **合规有没有硬线？** 代码能不能出公司网络；能不能到境外；要不要私有化部署、SSO、审计。
4. **主力语言和 IDE 是什么，需不需要多文件自动改？** 这决定要不要为 agent 能力付溢价。

另外确认一件事：**判定"值"的标准是只用钱，还是钱 ÷ 团队实际产出提升？** 前者我给你一张比价表，后者需要你给一个能衡量的东西（比如人均合并 PR 数）。

你把这四条给我，我出的就不是价格表，而是**按你们约束筛过、统一折算成"每人每月实际成本"的候选集，附上会导致结论翻转的条件**。在那之前我不动手 —— 你要的是一份能拿去开会拍板的材料，不是一份搜出来的清单。

需要的话，下一步我可以把这份标准清单写成 `local/plans/ai-coding-tool-vendor-selection.md`，作为调研的执行依据。