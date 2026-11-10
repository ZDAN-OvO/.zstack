TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/SKILL.md"}

TOOL ls: {"path": "/tmp/pf-28-with_skill-ke_tyk9c"}

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

TOOL bash: {"command": "cd /tmp/pf-28-with_skill-ke_tyk9c && ls -la data notes && echo \"---\" && cat template.md"}

TOOL bash: {"command": "cd /tmp/pf-28-with_skill-ke_tyk9c && head -50 notes/* 2>/dev/null | head -60"}

RESULT: data:
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  126 11月 10 16:17 q3-metrics.csv

notes:
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  182 11月 10 16:17 worklog.md
---
# Q3 业务回顾

## 收入
本季收入：{{revenue}}

## 客户
新增：{{new}}，流失：{{churn}}

## 下季计划
{{plan}}


RESULT: # 工作日志

- 9 月 8 日起，客服工单里"太难上手"的投诉明显变多。
- 8 月中旬把免费试用从 14 天改为 7 天。
- 老板说 QBR 下周四给 VP 看。


TOOL read: {"path": "/tmp/pf-28-with_skill-ke_tyk9c/data/q3-metrics.csv"}

RESULT: month,revenue_usd,new_customers,churned_customers,nps
2026-07,182000,41,12,38
2026-08,176000,35,19,31
2026-09,171000,30,24,27


TOOL bash: {"command": "date +%F; cd /tmp/pf-28-with_skill-ke_tyk9c && git rev-parse --show-toplevel 2>/dev/null || echo \"no git\""}

RESULT: 2026-11-10
no git


TOOL write: {"path": "/tmp/pf-28-with_skill-ke_tyk9c/local/plans/early-warning-monitoring.md", "content": "# Plan: 季报之外，早一步知道\n\n- Asked: 我想把季度回顾换成每日监控，异常才提醒老板\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\n\n**Hand over（建议接手的高度）**：不只交出\"每日监控+提醒\"，而是交出一份**可被反驳的早发现机制**：①回测报告——如果这套规则 7 月就存在，它会在哪天报警、比季报早几天、期间误报几次；②并行运行一个季度的日监控与提醒。老板看的是\"提前了多少天\"，不是看板截图。\n\n**Fallback（下一级）**：只做 rung 0 —— 每日指标抓异常 + 异常才提醒，先跑通管道；不承诺\"更早\"，不写回测。\n\n**Ceiling（今天模型单独做不到的）**：改造信号源本身——接生产埋点、把工单/激活漏斗做成事件流，并把告警绑定成人（谁在多少小时内响应）。需要生产数据权限和组织承诺，超出模型能 own 的范围。\n\n**Depth**：专家不会拿月度汇总表做监控。原始材料是**日/周粒度的事件级数据**；仪器是先行指标与流失的 lead-lag 分析、变点检测/EWMA 残差（不是拍阈值）、以及用精确率-召回率回测告警（lead time + 误报预算，多重比较要校正）。你笔记里已经有一条真实线索：8 月中试用 14→7 天 → 9 月 8 日起\"太难上手\"投诉变多 → 流失 12→19→24。**先行信号长在工单和上手行为里，不长在收入里。**\n**Stretch target**：用 9 月之前的数据拟合规则，在 9 月数据上做留出检验，报出 lead time 天数与误报次数——一个能预测它没见过的数据点。\n\n**Range**：动词是 发现（异常检测）· 证明（回测/留出）· 不打扰（误报预算）· 说服（一页给老板）。\nCrew：留存分析（lead-lag 与先行指标）· 可观测性/SRE（告警设计、误报预算、runbook）· 统计（变点、多重比较）· **红队**（专攻\"事后诸葛\"\"只是噪声\"\"天天响\"）· 老板（是否接受非季报节奏的打扰）。\n\n**Judge**：留出期检验（8 月前拟合，9 月判定），加红队 session 与一个裁决 session；最终判据是老板能指认\"这条提醒让我提前做了哪个决定\"。方法也判：蒙对的事件不算过。\n\n**Needs**：日/周粒度的试用转化、激活漏斗、工单量、续费/流失发生日期、使用量 —— **data/ 里只有 3 行月度数据，这是主要缺口**；工单原文；试用期改动日期作为已知干预点；一台跑回测的机器。缺：日粒度与事件级数据、告警接收渠道。\n\n**Declined**：暂无——三条移动待你裁决。\n\n## Task\n\n**Purpose**：问题早发现 —— 让老板在问题还小的时候就知道，而不是在季报上才知道。\n\n**Context**：B2B SaaS；老板只看季报；QBR 下周四给 VP 看（现有产物见 `template.md`）；8 月中试用从 14 天改为 7 天；9 月 8 日起客服工单\"太难上手\"投诉明显变多；`data/q3-metrics.csv`：收入 182k→176k→171k，新客 41→35→30，流失 12→19→24，NPS 38→31→27。（事实，请确认）\n\n**Materials**：`data/q3-metrics.csv`（**仅 3 行月度，不足以\"证明\"更早**）；`notes/worklog.md`（唯一一条非结构化先行线索）；`template.md`（季报格式，作为并行对照）。缺失位：日粒度历史、工单原文、流失发生日期。\n\n**Boundaries**：不发垃圾提醒；不拿 3 行数据\"证明\"结论（宁可不证明也不编）；不替代现有季报/QBR；回测没过之前不把告警发给老板。\n\n**Done**：一份回测报告（每个已知事件：比季报早几天、误报几次）+ 一条日监控与季报并行跑一个季度。\n**Checkpoint**：先给你一页\"先行指标候选 + 回测设计\"，你点头再跑数。\n\n## Open\n\n1. **最大的洞：历史数据粒度。** 3 行月度数据无法证伪也无法证明\"更早\"。能否导出过去 6–12 个月的日/周数据（试用转化、工单量、活跃）？拿不到的话，\"用历史数据证明\"这个完成定义必须重写——这是本次最该先解决的，而不是先写告警代码。\n2. \"异常\"由谁定义：业务阈值你定，还是统计基线自动学？老板只被叫几次才不烦（误报预算）。\n3. 提醒发到哪（微信/邮件/看板），谁负责第二天看。\n4. 并行一个季度的失败标准是什么——误报几次、漏报几次就停？\n5. 老板是否真的愿意接受\"不按季报节奏\"的打扰（这是组织问题，不是技术问题）。\n\nReady: **no** —— 等你裁决三条 Requirement 移动（接手高度/深度/班组，尤其是否接受\"回测报告\"替代\"每日看板\"作为首个交付），并回答 Open 第 1 条（能否拿到日粒度历史数据）。\n"}

RESULT: Successfully wrote to /tmp/pf-28-with_skill-ke_tyk9c/local/plans/early-warning-monitoring.md

ASSISTANT: 已写入 `local/plans/early-warning-monitoring.md`。

三点需要你先裁决，其余按你给的五项填好了：

1. **最大的洞在素材上，不在方案上。** `data/q3-metrics.csv` 只有 3 行月度数据——流失 12→19→24 就是全部"历史"。3 个点既不能证明也不能证伪"更早发现"，所以你的完成定义里"用历史数据证明"目前无法验证。要么拿到过去 6–12 个月的日/周数据（试用转化、工单量、活跃），要么把完成定义改成别的。
2. **先行信号不在收入表里。** `notes/worklog.md` 已经写着一条真实的因果链：8 月中试用 14→7 天 → 9 月 8 日"太难上手"投诉变多 → 流失翻倍。所以要监控的是工单和上手行为，收入只是结果。按收入做每日监控，你只是在更频繁地看滞后指标。
3. **建议把首个交付从"每日看板"换成"回测报告"**（提前几天、误报几次），看板本身不构成"更早"的证据。我现在给的是这个高度，fallback 是只跑通每日提醒管道、不承诺提前量。

拒绝或改写哪一条，说一声我改 plan；Open 里第 5 条（老板是否接受非季报节奏的打扰）是组织问题，只有你能答。

确认 Ready 后，可以用 `/define-goal` 以这份 plan 为输入。