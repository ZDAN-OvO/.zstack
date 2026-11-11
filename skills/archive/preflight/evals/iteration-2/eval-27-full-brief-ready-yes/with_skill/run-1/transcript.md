TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/SKILL.md"}

TOOL ls: {"path": "/tmp/pf-27-with_skill-1x4flbgw"}

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


RESULT: analytics/
index.html
support/

TOOL bash: {"command": "cd /tmp/pf-27-with_skill-1x4flbgw && ls -R analytics support | head -50 && echo \"---\" && wc -l index.html"}

TOOL read: {"path": "/tmp/pf-27-with_skill-1x4flbgw/support/chats-sample.md"}

RESULT: analytics:
weekly.csv

support:
chats-sample.md
---
3 index.html


RESULT: - "我还是没搞懂你们和 Notion 有什么区别"
- "价格页在哪？"
- "注册后要连日历，我就放弃了"


TOOL read: {"path": "/tmp/pf-27-with_skill-1x4flbgw/analytics/weekly.csv"}

TOOL read: {"path": "/tmp/pf-27-with_skill-1x4flbgw/index.html"}

RESULT: week,visits,signups,conversion,top_source
2026-10-06,12000,480,4.0%,organic
2026-10-13,11800,460,3.9%,organic
2026-10-20,19500,390,2.0%,paid_social
2026-10-27,21000,399,1.9%,paid_social


RESULT: <h1>The all-in-one platform for modern teams</h1>
<p>Boost productivity with our seamless, AI-powered workspace.</p>
<a href="/signup">Get started</a>


TOOL bash: {"command": "date +%F; cd /tmp/pf-27-with_skill-1x4flbgw && ls -a; git rev-parse --show-toplevel 2>/dev/null || echo \"no git\""}

RESULT: 2026-11-10
.
..
analytics
index.html
support
no git


TOOL write: {"path": "/tmp/pf-27-with_skill-1x4flbgw/local/plans/paid-social-homepage-copy.md", "content": "# Plan: 把 paid_social 新访客的注册率拉回 3.5%\n\n- Asked: 首页转化率掉了一半，帮我重写首页文案\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\nHand over: 交付 3 版首屏（标题+副标题），每版都能让不懂我们的陌生人说出\"我们和 Notion 的区别\"，选 1 版上 A/B，使 paid_social 新访客注册率回到 3.5%\nFallback: 只交 3 版标题+副标题，注册率的归因留给 A/B 之后\nCeiling: 注册后\"要连日历就放弃\"的流失（support 第 3 条）在注册流程里，改它属于产品/工程，文案只能设定预期、不能拥有这段流失\nDepth: 原始素材=聊天原文与投放流量周表，不做摘要；仪器=按来源分层的周漏斗、5 秒陌生人对齐测试（编码表：说出差异化/说错/说不出）、注册事件口径；stretch target=不看品牌名的 5 秒测试中 ≥70% 的人能正确复述差异化，并用它预测 A/B 走向\nRange: 动词=5 秒内分辨我们与 Notion、敢点注册、对注册后步骤有正确预期；crew=转化文案（写差异化）、B2B 产品营销（选对比锚点与证据）、用户研究（读原始聊天、跑 5 秒测试）、增长实验设计（定效应量/分流/停止规则）、红队（扮\"今天就要用 Notion 的人\"攻击每版的差异化和承诺）\nJudge: A/B 是终审；预筛用 session 外的 5 秒测试 + 1 轮红队 + 1 份裁决 → 由你挑版（你知情，只能算半个裁决者），评分同时看方法：是否单变量（只动首屏）、是否守住三条边界、是否预注册效应量与停止规则\nNeeds: 有=周流量表、3 条聊天原文、现有首屏；缺=聊天记录的来源标签（organic/paid 未知）、注册后激活数据、A/B 分流工具与注册事件口径、自家 paid_social 广告素材与承诺\nProposed:\n1. Altitude — 把\"3 版标题+副标题\"扩成\"3 版完整首屏\"（标题、副标题、一句 not-Notion 的差异化、一行注册后预期）：聊天第 1、3 条都不是一句副标题能装的\n2. Depth — A/B 前加 5 秒对齐测试，别把 3 版弱文案直接丢进 A/B\n3. Range — 加一个红队角色（扮 Notion 现有用户）\n4. 读数 — \"3.5%\" 是 organic 的历史水位，paid_social 从未有过基线；3.5% × 21000 ≈ 735 注册/周，比现在 399 高 84%，单靠首屏可能到不了，建议先认 2.8–3.0% 为第一站\nDeclined: 改定价（保持现有价格页，只修入口）、弹窗、承诺未上线功能 — 你已设为墙\n\n## Task\nPurpose: 挑出 1 版可上线的首屏并验证它是否真的拉回 paid_social 注册率（同时判断瓶颈在文案还是渠道/注册流程）\nContext: B2B 协作工具；付费社媒来的新访客多不懂我们和 Notion 的区别。【查得，待你确认】转化率 4.0%/3.9% → 2.0%/1.9% 的那一周，top_source 恰好从 organic 换成 paid_social；同期访问 12.0k→21.0k（+75%），注册 480→399（−17%）。所以\"掉一半\"主要是分母变大的混合效应，不是注册量腰斩；两件事同时发生，是待检验的相关，不是已证明的因果\nMaterials: 主=analytics/weekly.csv、support/chats-sample.md、index.html 现有首屏；次=你自己的投放素材与落地页承诺；禁=网上竞品文案；空位=paid_social 访客的原始掉落语音/聊天（目前没有）\nBoundaries: 不改定价页内容、不加弹窗、不承诺没有的功能\nDone: 3 版首屏标题+副标题摆在你面前（每版附它押的假设与判定指标）→ 你挑 1 版 → 我出 A/B 方案（单变量、效应量、停止规则）→ 上线开跑\n\n## Open\n- support 只有 3 条聊天，且没有来源标签：不清楚它们来自 organic 还是 paid_social，n=3 不足以下判断。有没有 paid_social 访客的掉落原因（退出问卷、客服标签、广告评论）？\n- 其他解释是否已排除：那周的广告素材/受众是否换过、落地页是否改过分流、注册流程近期是否改动？\n- \"注册\"的口径是什么（提交表单？完成邮箱验证？）A/B 里以哪个事件为准\n- 3.5% 是硬目标还是方向？若是方向，第 4 条建议可以接受\n\nReady: no — 4 条 Proposed 等你裁定（接受/改写/拒绝），3 个 Open 会影响 A/B 方案与归因\n"}

RESULT: Successfully wrote to /tmp/pf-27-with_skill-1x4flbgw/local/plans/paid-social-homepage-copy.md

ASSISTANT: Plan 已写到 `local/plans/paid-social-homepage-copy.md`（一屏）。

先说两个从文件里查到的、会改变结论的事实：

1. **“掉一半”是分母变大的混合效应，不是注册腰斩。** 10-20 那周访问从 12.0k 涨到 19.5k/21.0k（+75%），注册从 480 到 399（−17%）。转化率腰斩和来源切换是同一周发生的两件事——这是待检验的相关，不是已证明的因果。现在的首屏（"all-in-one platform"、"seamless, AI-powered workspace"）确实没有讲清任何差异化，但它不是已确认的病灶。
2. **3.5% 没有 paid_social 基线。** 4.0%/3.9% 是 organic 的水位。3.5% × 21000 ≈ 735 注册/周，比现在 399 高 84%。建议先认 2.8–3.0% 为第一站。
3. **support 第 3 条不在文案能管的范围内**："注册后要连日历，我就放弃了"是注册流程里的流失。文案最多设定预期，改不动它——这记在 Ceiling 里。

Task 五个槽你已答全（Done 还带了检查点：3 版→你挑→再 A/B），所以计划缺的只有两样：

- **4 条 Proposed 等你裁定**：①把"3 版标题+副标题"扩成"3 版完整首屏"（聊天第 1、3 条一句副标题装不下）；②A/B 前加 5 秒陌生人对齐测试；③加红队角色；④接受分两站的目标读数。
- **3 个 Open**：3 条聊天没有来源标签、n=3；那周广告素材/落地页/注册流程是否另有变动；"注册"以哪个事件为准。

Ready: **no**，等你裁定 Proposal 并回 Open。确认后可以用 `/define-goal` 以这份 plan 为源。