TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/SKILL.md"}

TOOL bash: {"command": "ls -la /tmp/pf-28-with_skill-navzqgbd && ls -la /tmp/pf-28-with_skill-navzqgbd/data 2>/dev/null"}

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


RESULT: total 184
drwxrwxr-x  4 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 59 root root 167936 11月 10 20:54 ..
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 data
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 notes
-rw-rw-r--  1 zdan zdan    131 11月 10 16:17 template.md
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  126 11月 10 16:17 q3-metrics.csv


TOOL bash: {"command": "cd /tmp/pf-28-with_skill-navzqgbd && echo \"=== template.md ===\" && cat template.md && echo \"=== notes ===\" && ls -la notes && for f in notes/*; do echo \"--- $f ---\"; cat \"$f\"; done && echo \"=== data/q3-metrics.csv ===\" && cat data/q3-metrics.csv && echo && echo \"=== git ===\" && git status 2>&1 | head -5"}

RESULT: === template.md ===
# Q3 业务回顾

## 收入
本季收入：{{revenue}}

## 客户
新增：{{new}}，流失：{{churn}}

## 下季计划
{{plan}}
=== notes ===
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  182 11月 10 16:17 worklog.md
--- notes/worklog.md ---
# 工作日志

- 9 月 8 日起，客服工单里"太难上手"的投诉明显变多。
- 8 月中旬把免费试用从 14 天改为 7 天。
- 老板说 QBR 下周四给 VP 看。
=== data/q3-metrics.csv ===
month,revenue_usd,new_customers,churned_customers,nps
2026-07,182000,41,12,38
2026-08,176000,35,19,31
2026-09,171000,30,24,27

=== git ===
fatal: not a git repository (or any of the parent directories): .git


TOOL bash: {"command": "cd /tmp/pf-28-with_skill-navzqgbd && ls -d local/plans 2>/dev/null; ls -la local 2>/dev/null"}

RESULT: (no output)

Command exited with code 2

TOOL write: {"path": "/tmp/pf-28-with_skill-navzqgbd/local/plans/daily-anomaly-early-warning.md", "content": "# Plan: 用领先指标做每日预警，替代季度后才看见问题\n\n- Asked: \"我想把季度回顾换成每日监控，异常才提醒老板\"\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\nHand over: 不是\"每日看板\"，而是一套**可回测的领先指标预警**：在结果指标（收入/流失）恶化前数周发出可解释、可行动的一条提醒，并与季报并行一个季度做验证。\nFallback: 保留季报，先加一份每周领先指标摘要（试用转化、上手投诉、激活率），不做到日级。\nDepth: 原始材料要事件级/日级数据（注册、试用、工单含时间与文本、产品使用事件、改配置的时间点），不是月度 CSV；方法用因果驱动链（试用天数→激活→\"太难上手\"工单→流失）+ 变点/EWMA 控制图与季节性，而不是拍阈值；stretch target：用滚动起点回测证明它在 9 月流失抬升前 N 周就会触发，且优于季报的发现日期；同时检验\"每日=更早\"这个信念。\nRange: 动词是 detect / explain / rank / notify。crew：可观测性工程师（告警设计与噪声预算）、统计师（变点检测、回测防前视）、留存分析师（驱动链建模）、红队（专门把它搞成噪音或让它漏掉 9 月那次）、老板（接收方，提醒必须一行能懂能决策）。\nJudge: 滚动起点回测（阈值只用训练窗口定，禁止前视），同时评方法分与结果分——蒙对不算过，方法对但差一点算过；外加老板\"会不会照它行动\"的接受度测试。\nNeeds: **日级/事件级历史数据（缺失）**——现在 `data/q3-metrics.csv` 只有 2026-07/08/09 三行月度汇总；还缺工单时间戳与文本、试用转化、产品使用事件、8 月中旬试用期改动的配置记录。\nProposed:\n- (Altitude) 把目标从\"每日监控指标\"抬到\"领先指标预警 + 回测领先时间\"，因 3 个月度点无法支撑\"更早发现\"的证明。\n- (Depth) 监控驱动链而非结果指标；用变点/控制图 + 噪声预算，替掉固定阈值。\n- (Range) 加噪声预算责任人、红队与\"一行可行动提醒\"格式。\nDeclined: 无\n\n## Task\nPurpose: 问题早发现——在收入/流失已经掉了之前就看见，而不是季度复盘时才解释。\nContext: B 端 SaaS，老板只看季报，QBR 下周四要给 VP 看；`notes/worklog.md` 记 8 月中旬试用 14→7 天、9 月 8 日起\"太难上手\"投诉变多；同期流失 12→19→24、NPS 38→31→27、收入逐月降。这些是同时发生，属于待验证的相关性，还不能当因果。\nMaterials: 主：`data/q3-metrics.csv`（3 行月度汇总）、`notes/worklog.md`（定性的时间线索）、`template.md`（现有季报结构）。缺：任何日级数据。禁：编造历史日级序列。\nBoundaries: 不发垃圾提醒（待定死：连续跑一个季度里，可接受频率与误报率是多少？）\nDone: 用历史数据证明它比季报更早发现问题，再与季报并行跑一个季度。\n\n## Open\n- \"不发垃圾提醒\"需要一个数字（如每周 ≤1 条、或每条提醒的准确率下限），否则无法验收，也无法回测。\n- 只有 3 个月度点，**回测做不了**。要么补日级历史，要么把\"证明更早\"降级为\"并行一季度的对照记录\"——请选一条。\n- 并行一季度的结束判据：什么结果会让你真的砍掉季报？\n- 提醒给谁、他要在几分钟内做什么动作？\n\nReady: no — 4 个 proposed 未被裁决，且日级素材缺失、噪声预算无数字。\n"}

RESULT: Successfully wrote to /tmp/pf-28-with_skill-navzqgbd/local/plans/daily-anomaly-early-warning.md

ASSISTANT: 计划已写到 `local/plans/daily-anomaly-early-warning.md`。

有三件事需要你先裁决或补上:

1. **数据不足以支撑你的"完成"标准。** `data/q3-metrics.csv` 只有 2026-07/08/09 三行月度汇总,没有日级序列。三行数据无法回测,所以"用历史数据证明它更早发现问题"目前做不到。要么补日级/事件级历史(注册、试用、工单时间戳与文本、使用事件、8 月中旬改试用期的配置记录),要么把证明方式降级为"并行一季度的对照记录"。请选一条。
2. **"不发垃圾提醒"需要一个数字**:每周至多几条,或每条提醒的准确率下限。没有数字就无法验收,也无法回测。
3. **建议把目标抬高一级**:从"每日看指标"到"领先指标预警,并给出回测的领先时间"。因为收入/流失是滞后且带噪音的结果指标,日级盯它只会既吵又晚;真正的线索在 `notes/worklog.md` 里那条链——试用期缩短 → "太难上手"工单增加 → 流失抬升。注意这三件事是同时发生,是相关性,还不能当因果。

Ready 目前是 no,原因在计划末行。确认后我可以用 `/define-goal` 以这份 plan 为输入继续。