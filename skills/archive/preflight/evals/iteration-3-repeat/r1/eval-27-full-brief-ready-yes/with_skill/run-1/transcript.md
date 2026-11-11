TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/SKILL.md"}

TOOL bash: {"command": "ls -la /tmp/pf-27-with_skill-qpybu4xd"}

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
drwxrwxrwt 63 root root 167936 11月 10 21:28 ..
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 analytics
-rw-rw-r--  1 zdan zdan    151 11月 10 16:17 index.html
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 support


TOOL ls: {"path": "/tmp/pf-27-with_skill-qpybu4xd/analytics"}

TOOL ls: {"path": "/tmp/pf-27-with_skill-qpybu4xd/support"}

TOOL read: {"path": "/tmp/pf-27-with_skill-qpybu4xd/index.html"}

RESULT: weekly.csv

RESULT: chats-sample.md

RESULT: <h1>The all-in-one platform for modern teams</h1>
<p>Boost productivity with our seamless, AI-powered workspace.</p>
<a href="/signup">Get started</a>


TOOL read: {"path": "/tmp/pf-27-with_skill-qpybu4xd/analytics/weekly.csv"}

TOOL read: {"path": "/tmp/pf-27-with_skill-qpybu4xd/support/chats-sample.md"}

RESULT: week,visits,signups,conversion,top_source
2026-10-06,12000,480,4.0%,organic
2026-10-13,11800,460,3.9%,organic
2026-10-20,19500,390,2.0%,paid_social
2026-10-27,21000,399,1.9%,paid_social


RESULT: - "我还是没搞懂你们和 Notion 有什么区别"
- "价格页在哪？"
- "注册后要连日历，我就放弃了"


TOOL bash: {"command": "date +%F; ls -la /tmp/pf-27-with_skill-qpybu4xd/local 2>/dev/null || echo \"no local/\""}

RESULT: 2026-11-10
no local/


TOOL write: {"path": "/tmp/pf-27-with_skill-qpybu4xd/local/plans/paid-social-signup-rate.md", "content": "# Plan: 让付费社媒新访客的注册率回到 3.5%\n\n- Asked: 首页转化率掉了一半，帮我重写首页文案（你接受的四点：先确认是不是文案的问题、从 support 聊天和漏斗数据出发、用 A/B 判断、退路是只改首屏标题；落实为\"先给 3 版首屏标题+副标题，挑一版再上 A/B\"）\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\nHand over: 先按来源拆漏斗，判断下滑是不是文案造成的；再改首屏；用 A/B 判定（你上一轮已全部接受）\nFallback: 只改首屏标题（你指定的退路）\nDepth: 最原始素材是 support 聊天原话（三条分别是\"与 Notion 的区别\"\"价格页在哪\"\"注册后要连日历，放弃了\"）；仪器是按来源分层的注册率 + 双比例显著性检验与样本量估算（2.0%→3.5% 每臂约 1,500 访客，paid_social 一周 19,500 访客足够）；护栏指标加\"注册后连上日历完成率\"，避免只把注册数做高\nRange: not needed —— 交付面已被你收窄到首屏；扩到整页或注册流程会撞上\"不改定价、不加弹窗\"的边界，留到 A/B 之后\nJudge: A/B 测试，既判结果（3.5%）也判方法（随机分流、单变量、样本量、护栏指标不降）；3 版中挑哪版由你直接判断\nNeeds: weekly.csv 只有周级 top_source + 整体转化，缺\"按来源的注册数\"；缺 paid_social 的受众/素材是否同期变化；缺\"我们与 Notion 的差异\"这条产品事实（见 Open）\nDeclined: 无\n\n## Task\nPurpose: 让付费社媒来的新访客注册率回到 3.5%（现在 1.9–2.0%）\nContext: B2B 协作工具；新访客多不懂我们和 Notion 的区别。已核到的事实：10-20 那周来源从 organic 换成 paid_social，访问量翻倍（12,000→19,500）而注册数反而下降（480→390）；转化率与来源切换同时发生，目前只能算相关，需要分层再判。现首屏是通用套话（\"all-in-one platform… seamless, AI-powered\"），恰好没回答\"和 Notion 有什么不同\"。\nMaterials: 一手——support/chats-sample.md、analytics/weekly.csv、index.html 现文案、你口述的\"不懂与 Notion 的区别\"。禁用——网上竞品文案。空槽——与 Notion 的可对外差异（待你给）、按来源的注册数、paid_social 定向与素材。（输出语言按现站英文，要中文版你说一声）\nBoundaries: 不改定价；不加弹窗；不承诺没有的功能；不抄网上竞品文案；本轮只动首屏标题和副标题\nDone: 先交 3 版首屏标题+副标题，每版附一句定位理由和它对应聊天里的哪条；你挑 1 版；只改这一版上线 A/B，看注册率与\"连日历\"护栏；不达标就走只改标题的退路\n\n## Open\n- 3.5% 是 organic 的历史水平，paid_social 访客的意图可能天然更低；A/B 只能证明\"文案带来的增量\"。目标是绝对值 3.5%，还是\"相对提升 X%\"或分来源定目标？\n- 文案必须讲出\"我们和 Notion 的不同\"，但工作区里没有这条事实。请给 2–3 条能对外说的差异，否则只能写空洞卖点——那正是现在的问题。\n- 聊天里\"注册后要连日历就放弃\"指向注册流程，不是首屏。本轮不改流程，那首屏要不要明确写\"无需先连日历\"？这算一种承诺，需你确认。\n- paid_social 的受众或素材是否也在 10-20 那周换过？若是，转化下降还叠加了投放质量因素。\n\nReady: no —— 缺\"与 Notion 的差异\"这条产品事实，且 3.5% 的目标口径未定；这两项给了就能出 3 版\n"}

RESULT: Successfully wrote to /tmp/pf-27-with_skill-qpybu4xd/local/plans/paid-social-signup-rate.md

ASSISTANT: 计划已写好：`local/plans/paid-social-signup-rate.md`

要点（一屏内）：

- **两个事实**：10-20 那周来源从 organic 换成 paid_social，访问量 12,000→19,500，注册数却从 480 掉到 390。转化率与来源切换同时发生 → 只能算相关，A/B 前先按来源拆一版漏斗。样本量够（2.0%→3.5% 每臂约 1,500 访客，一周 19,500 访客可支撑）。
- **Requirement 已按你接受的四点定稿**：先诊断、以聊天+漏斗为素材、A/B 判定、退路只改标题。没有新开提案。
- **Depth 的额外一步（写进计划，不擅自改交付）**：护栏指标加"注册后连日历完成率"，否则只优化注册数会把问题往后推。
- **Ready: no**，只卡两件事：
  1. 与 Notion 的 2–3 条**可对外差异**——工作区没有这条事实，缺了只能写空洞卖点；
  2. 3.5% 是 organic 的水平，paid_social 意图可能天然更低——要绝对值 3.5%，还是相对提升/分来源目标？

这两项给我，我就出 3 版首屏标题+副标题（英文，每版附定位理由和对应哪条聊天）。要我直接用 `/define-goal` 把这份计划转成目标吗？