TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/SKILL.md"}

TOOL bash: {"command": "ls -la; echo ---; ls -la notes data 2>/dev/null"}

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
drwxrwxrwt 60 root root 167936 11月 10 20:53 ..
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 data
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 notes
-rw-rw-r--  1 zdan zdan    131 11月 10 16:17 template.md
---
data:
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  126 11月 10 16:17 q3-metrics.csv

notes:
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  182 11月 10 16:17 worklog.md


TOOL bash: {"command": "cd /tmp/pf-22-with_skill-h_d0erm_ && for f in template.md data/q3-metrics.csv notes/worklog.md; do echo \"=== $f\"; cat \"$f\"; done; echo \"=== git\"; git rev-parse --show-toplevel 2>&1 | head -1"}

RESULT: === template.md
# Q3 业务回顾

## 收入
本季收入：{{revenue}}

## 客户
新增：{{new}}，流失：{{churn}}

## 下季计划
{{plan}}
=== data/q3-metrics.csv
month,revenue_usd,new_customers,churned_customers,nps
2026-07,182000,41,12,38
2026-08,176000,35,19,31
2026-09,171000,30,24,27
=== notes/worklog.md
# 工作日志

- 9 月 8 日起，客服工单里"太难上手"的投诉明显变多。
- 8 月中旬把免费试用从 14 天改为 7 天。
- 老板说 QBR 下周四给 VP 看。
=== git
fatal: not a git repository (or any of the parent directories): .git


TOOL bash: {"command": "date +%F"}

RESULT: 2026-11-10


TOOL write: {"path": "/tmp/pf-22-with_skill-h_d0erm_/local/plans/q3-review.md", "content": "# Plan: Q3 回顾（给 VP，含三个下季决定）\n\n- Asked: 「帮我做 Q3 回顾，讲清楚本季变化、原因和下季要做的三个决定」\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\nHand over: 一页回顾 + **三个可拍板的决定**，每个决定带推荐项、下季负责人/时点和验收指标（VP 下周四 QBR 要能当场选）\nFallback: 只做回顾（变化 + 原因的证据强度），三个决定列成待议清单\nDepth: 材料只有 3 行月度数据（`data/q3-metrics.csv`：收入 182,000→176,000→171,000；新客 41→35→30；流失 12→19→24；NPS 38→31→27）和 `notes/worklog.md`。专家动作：不写\"流失翻倍所以是试用缩短\"的叙述，而把三个替代解释并列（8 月中试用 14→7 天 / 9 月 8 日起\"太难上手\"工单上升 / 季节性），逐条写\"手上数据能证到哪一步、要补什么才能定因果\"。仪器：3 个点做不了任何趋势或断点检验，结论只能写成相关与待验证假设。Stretch：给一个能证伪的预测（若流失由试用缩短驱动，应先在新客首 30 天出现）——需 cohort 数据才跑。\nRange: 动词 = 让 VP 相信 / 取舍 / 承诺 / 排期。Crew：口径核对（每个数字回指 csv 行）、留存归因（替代解释与证伪条件）、红队（攻击\"原因\"结论 + 攻击任何无出处数字）。模板 `template.md` 的 `{{revenue}}`/`{{plan}}` 槽位正是\"编数字\"的入口，只借章节名、不借占位符。\nJudge: 独立红队 session，只审两件事——每个数字能在 csv/worklog 找到出处；每条\"原因\"都没超出证据允许的强度。不审文风。用户自查即可替代。\nNeeds: **缺 Q2 数字**（材料里没有上一季，\"本季变化\"目前只能读成季内趋势）；缺 cohort/日级试用转化、工单分类计数、渠道/客群拆分。这些在材料里找不到，我不补。\nProposed: ① Altitude 升到\"三个决定带推荐+验收指标\"；② Depth 用替代解释+证伪条件代替因果叙述；③ Range 加红队与口径核对两关。\nDeclined: —\n\n## Task\nPurpose: 下周四 QBR 给 VP 看，让 VP 对下季三件事拍板。\nContext: 季内收入连续两月下滑（-3.3%、-2.8%），新客走低（-14.6%、-14.3%），流失翻倍（+58%、+26%），NPS 连降（-7、-4）；8 月中试用 14→7 天；9 月 8 日起\"太难上手\"投诉变多。两条时间线相邻，仅此而已。\nMaterials: 主：`data/q3-metrics.csv`（唯一数字源）、`notes/worklog.md`（事件与时间）。禁用：任何不在两处材料里的数字、任何由我推算补齐的季度合计/百分比基数以外的量。空槽：Q2 对比、cohort、工单计数——均未找到。\nBoundaries: 别编数字。凡数字必须能指回 csv 某行或 worklog 某句；指不回的就不写，标为\"缺\"。\nDone:\n\n## Open\n- **Done**：你说不清 → 空着。可用来定的问法：VP 看完这一页，你希望他**当场做的动作**是什么（拍三个决定 / 只给方向 / 批预算或人头）？以及中途想看哪一步先给你过（我建议先给\"变化一页 + 三个待决定\"，你点头再展开原因部分）。\n- **Q2 基线**：没有上一季数字，\"本季变化\"的参照系要不要补？不补我就只讲季内趋势并明说没有同比/环比基线。\n- Ready 前需要你对 Proposed 三条各给一句裁定（接受 / 改 / 不要）。\n\nReady: no，因为 Done 仍空，且 Proposed 三条未裁定。\n"}

RESULT: Successfully wrote to /tmp/pf-22-with_skill-h_d0erm_/local/plans/q3-review.md

ASSISTANT: 已写好：`/tmp/pf-22-with_skill-h_d0erm_/local/plans/q3-review.md`

我在计划里标出了三件事：第一，你提出的边界“别编数字”，我把它变成了可检查的规则，即每个数字都要指回 csv 的行或 worklog 的句子，指不回去就标“缺”。第二，**材料里没有 Q2 数字**，因此“本季变化”目前只能读成季内趋势；要让这句话有参照系，你还得提供上一季的数据。第三，试用缩短和“太难上手”投诉在时间上相邻，但只有 3 行月度数据时，现在只能写成相关和待验证假设，把“原因”当成定论就是编。

`Done` 我留空了，没有替你填一个默认值。最省事的做法是回答：VP 看完后要**当场做的动作**是什么，以及要不要先看“变化一页 + 三个待决定”再展开？计划末尾的 Ready 仍为 no，等你对 Proposed 的三条各给一句裁定。

如果你愿意，我可以接着用 `/define-goal` 把这份 plan 拆成目标，以它为输入。