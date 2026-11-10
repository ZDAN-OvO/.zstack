TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/SKILL.md"}

TOOL ls: {"path": "/tmp/pf-22-with_skill-xf2lz6m4"}

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


RESULT: data/
notes/
template.md

TOOL ls: {"path": "/tmp/pf-22-with_skill-xf2lz6m4/notes"}

TOOL ls: {"path": "/tmp/pf-22-with_skill-xf2lz6m4/data"}

TOOL read: {"path": "/tmp/pf-22-with_skill-xf2lz6m4/template.md"}

RESULT: worklog.md

RESULT: q3-metrics.csv

RESULT: # Q3 业务回顾

## 收入
本季收入：{{revenue}}

## 客户
新增：{{new}}，流失：{{churn}}

## 下季计划
{{plan}}


TOOL read: {"path": "/tmp/pf-22-with_skill-xf2lz6m4/notes/worklog.md"}

TOOL read: {"path": "/tmp/pf-22-with_skill-xf2lz6m4/data/q3-metrics.csv"}

RESULT: # 工作日志

- 9 月 8 日起，客服工单里"太难上手"的投诉明显变多。
- 8 月中旬把免费试用从 14 天改为 7 天。
- 老板说 QBR 下周四给 VP 看。


RESULT: month,revenue_usd,new_customers,churned_customers,nps
2026-07,182000,41,12,38
2026-08,176000,35,19,31
2026-09,171000,30,24,27


TOOL bash: {"command": "date +%F"}

RESULT: 2026-11-10


TOOL write: {"path": "/tmp/pf-22-with_skill-xf2lz6m4/local/plans/q3-review.md", "content": "# Plan: Q3 回顾——讲清变化与归因，交出三个下季决定\n\n- Asked: 帮我做 Q3 回顾，讲清楚本季变化、原因和下季要做的三个决定\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\nHand over: VP 会上能直接拍板的 Q3 回顾——变化、归因（含被排除的解释）、三个决定（每个带选项/代价/可逆性/建议）。\nFallback: 一份变化+归因的回顾加三个决定的选项清单，不含建议。\nDepth: 不报“收入跌 6%、流失翻倍”就完事，而是把收入变化拆成新增/留存/价格三项，并用 8 月中改试用期前后的注册批次做前后对比，检验“试用期 14→7 天导致上手难、流失升”这个说法，而不是直接当结论。原始材料：`data/q3-metrics.csv` 月度汇总、`notes/worklog.md`、客服工单原文。仪器：批次留存表、工单文本归类、收入变化分解，而非继续看月度小计。\nStretch target: 把“试用期缩短是流失主因”当成待检验的信念，拿工单时间线与批次数据去打它；打不成立或数据不足以判定，都要明写。\nRange: 要做的动词是——让变化可复述、让原因可被反驳、让决定可被拍板。crew：收入/财务分析（拆收入变化）、客服运营（归类 9/8 起的“难上手”工单）、留存分析（批次前后对比）、决策设计（每个决定给选项与代价）、红队（专门攻击主归因）。\nJudge: 红队会话攻击归因 + 逐项回溯源文件（每个数字必须能落到 csv 或原始导出，落不到就写“数据不足”）；最终由你在会前亲自过一遍。\nNeeds: 已知有月度汇总（7/8/9 月：收入 182k/176k/171k，新增 41/35/30，流失 12/19/24，NPS 38/31/27）和工作日志。缺：按注册月的批次留存、收入的新增/扩张/流失分解、8/15 前后分界的注册数据、工单全文导出。缺的这几项决定归因能做到哪一层。\nDeclined: （暂无）\n\n## Task\nPurpose: 未知——你没说这三个决定是给 VP 拍板用，还是给你自己定下季方向用，这会改变“决定”写到多细。\nContext: 已知事实：Q3 三个月收入连续下滑约 6%，流失从 12 升到 24，NPS 从 38 掉到 27；8 月中免费试用由 14 天改为 7 天；9/8 起“太难上手”类工单明显增多；QBR 下周四给 VP 看。（以上请你确认）\nMaterials: 一手：`data/q3-metrics.csv`、工单原文导出、注册/流失明细。二手：`notes/worklog.md`、`template.md`。禁用：无来源的行业均值、凭印象的百分比。\nBoundaries: 别编数字——每个数字要么可追溯，要么标“数据不足”，不许用估算、行业均值或编造的因果关系填空。\nDone: 未定（你说不清，见 Open）\n\n## Open\n- **Done**：你没定完成定义。我先给一个默认形状，等你点头或改：① 一页变化+归因（含被排除的解释）② 三个决定，每个含选项、代价、可逆性、建议 ③ 中间 checkpoint：先给你一页大纲（结论句 + 三个决定的标题），你确认后再写全篇。要不要按这个来？\n- **Purpose**：三个决定给谁拍板、拍完影响什么（预算？人力？下季目标？）。\n- **时间**：工作日志写“QBR 下周四”，但今天是 2026-11-10，和数据里的 7–9 月对不上——是日志过时，还是这份回顾给的是补做的会？\n- **三个决定的范围**：是完全由数据推出来（比如试用期要不要改回、上手投入、留存抓手），还是你心里已有候选，只要我补论证？\n\nReady: no —— Done 未定，Purpose 未答，另有两个确认项。\n"}

RESULT: Successfully wrote to /tmp/pf-22-with_skill-xf2lz6m4/local/plans/q3-review.md

ASSISTANT: Plan 已写到 `local/plans/q3-review.md`。

一句话：边界我按你原话记成硬墙——**每个数字可追溯，落不到就写"数据不足"，不许估算**。Done 你没定，我没替你编一个答案，而是给了一个默认形状等你点头：一页变化+归因 → 三个决定（选项/代价/可逆性/建议）→ 中间先看一页大纲再写全篇。

顺带三件看了文件才发现的事，需要你确认：

1. **数据只到月度汇总**（7–9 月收入 182k/176k/171k，流失 12/19/24）。要检验"试用期 14→7 天导致流失"，必须有 8/15 前后分界的注册批次、收入的新增/扩张/流失分解、工单原文导出。没有这些，归因只能停在"时间上相关"，我会明写这句而不是下结论。
2. **日志说 QBR 下周四**，但今天是 2026-11-10，和 7–9 月对不上——是日志过时，还是补做的会？
3. **Purpose 还空着**：这三个决定是给 VP 拍板，还是给你自己定下季方向？决定的写法差别很大。

Ready: no。你回一句"Done 按默认走"加上 Purpose 和范围，我就把 Ready 改 yes 并开工。

要接下一步可以用 `/define-goal`，拿这份 plan 当输入。