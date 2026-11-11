TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/SKILL.md"}

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


TOOL bash: {"command": "ls -a; echo ---; ls local 2>/dev/null; echo ---; git rev-parse --show-toplevel 2>/dev/null"}

RESULT: .
..
.keep
---
---


Command exited with code 128

ASSISTANT: **阶段：探索**（你的目的清楚了：下季定一家买；但"哪几家在比"和"拿什么比"都还没定）。所以这一轮先给你能分开选项的标准和取舍，不替你选。

先说一个会影响结论的口径：我这个会话没有联网工具，能给的只有我知识里到某个时间点的价格，这类工具每季都调价。你说"随便上网找就行"= 来源无边界，而价格这种东西无边界来源的默认结局是把二手博客的数字写成事实。建议的规则（供你否掉）：**厂商官方定价页 > 官方文档/公告 > 第三方测评只做交叉验证不做价格依据**；每个价格标抓取日期；抓不到的留空，不估。

**能分开选项的四条标准**

1. **计费单位** — 席位/月（通义灵码、CodeGeeX、Copilot 类）vs 席位+按量（Cursor/Trae 类）vs 纯 Token（走 API 接入）。决定下季账单能不能预测。
   - 取舍：席位制便宜且可预测，代价是模型升级慢、有月度请求封顶；按量/Token 制灵活，但账单随团队用法放大，人一多就失控。
2. **套餐分界线在哪** — 个人版→专业版→企业版，企业版才给 SSO、审计日志、私有化/数据不入训。团队采购真正要比的是这一层，个人版价格基本是噪音。
   - 取舍：企业版解锁合规，常是个人版 3–5 倍，且要年付、有最低席位数。
3. **采购可行性** — 人民币结算与专票、数据是否境内、是否要企业认证。这条不是价格，是"能不能买"。
4. **隐性成本** — 支持的 IDE（只支持自家 IDE 就是全组迁移成本）、限流阈值、超额计费规则、培训。

**我需要你给三个事实**（只有你知道，决定我给你比哪几家）

- 席位规模：多少人买、全职写码 vs 偶尔用（偶尔用的人买席位制是浪费，全职的人用按量制会超支）
- 硬墙是哪些：能不能用海外服务？必须境内数据+专票吗？能年付吗？
- 预算口径：是"下季总预算 ≤ X"还是"人均 ≤ Y/月"？

这三条给完，我就进 Execute，写成一份带官方来源和抓取日期的比价计划给你过。你也可以直接说"就按席位制/就按我列的这四家"，我按你的约束收窄。

计划文件暂未写：探索阶段不落盘，等你确认口径。