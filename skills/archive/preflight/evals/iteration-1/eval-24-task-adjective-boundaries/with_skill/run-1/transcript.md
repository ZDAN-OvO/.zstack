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


TOOL bash: {"command": "ls -la /tmp/pf-24-with_skill-mrmjvi76; echo ---; find /tmp/pf-24-with_skill-mrmjvi76 -maxdepth 3 -not -path '*/.git/*' -not -path '*/node_modules/*' | head -60"}

RESULT: total 184
drwxrwxr-x   4 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 109 root root 167936 11月 10 18:02 ..
drwxrwxr-x   2 zdan zdan   4096 11月 10 16:17 analytics
-rw-rw-r--   1 zdan zdan    151 11月 10 16:17 index.html
drwxrwxr-x   2 zdan zdan   4096 11月 10 16:17 support
---
/tmp/pf-24-with_skill-mrmjvi76
/tmp/pf-24-with_skill-mrmjvi76/index.html
/tmp/pf-24-with_skill-mrmjvi76/support
/tmp/pf-24-with_skill-mrmjvi76/support/chats-sample.md
/tmp/pf-24-with_skill-mrmjvi76/analytics
/tmp/pf-24-with_skill-mrmjvi76/analytics/weekly.csv


TOOL bash: {"command": "cd /tmp/pf-24-with_skill-mrmjvi76; echo '=== index.html'; cat index.html; echo; echo '=== analytics/weekly.csv'; cat analytics/weekly.csv; echo; echo '=== support/chats-sample.md'; cat support/chats-sample.md"}

RESULT: === index.html
<h1>The all-in-one platform for modern teams</h1>
<p>Boost productivity with our seamless, AI-powered workspace.</p>
<a href="/signup">Get started</a>

=== analytics/weekly.csv
week,visits,signups,conversion,top_source
2026-10-06,12000,480,4.0%,organic
2026-10-13,11800,460,3.9%,organic
2026-10-20,19500,390,2.0%,paid_social
2026-10-27,21000,399,1.9%,paid_social

=== support/chats-sample.md
- "我还是没搞懂你们和 Notion 有什么区别"
- "价格页在哪？"
- "注册后要连日历，我就放弃了"


TOOL bash: {"command": "date +%F; cd /tmp/pf-24-with_skill-mrmjvi76; git rev-parse --show-toplevel 2>/dev/null || echo \"no git root\""}

RESULT: 2026-11-10
no git root


TOOL write: {"path": "/tmp/pf-24-with_skill-mrmjvi76/local/plans/paid-social-homepage.md", "content": "# Plan: 付费社媒访客的首页首屏\n\n- Asked: \"帮我重做首页视觉\" — 目标是付费社媒来的新访客 5 秒内看懂我们是干嘛的；边界是\"高级、简洁、有科技感\"\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\n\n**Hand over**: 付费社媒访客在首屏知道「这是什么品类 / 给谁用 / 和 Notion 差在哪 / 多少钱」→ paid_social 转化率从 1.9% 回到 organic 的 4% 区间。\n**Fallback**: 只改首屏（hero + 首屏 CTA），做 A/B，两周后用 paid_social 队列判定。\n\n**Depth**: 你问的是视觉，但数据先说话。10-20 起 paid_social 流量翻倍（11.8k→21k），转化同时腰斩（3.9%→1.9%）——这是信息不匹配，不是审美问题。chat 里的三条真实反对意见是：跟 Notion 没区别、找不到价格页、注册要连日历就放弃。所以专家动作是：首屏先回答这三个反对意见，再谈高级感。\n原始材料：support/chats-sample.md 的原文措辞；analytics/weekly.csv 的分渠道队列。\n工具：按 top_source 拆分的周转化、5 秒测试（目标用户看首屏 5 秒后复述）、CTA 点击埋点。\n**Stretch**: 找 5 个付费社媒画像的陌生人做 5 秒测试，≥4 人能一句话说出品类 + 和 Notion 的区别。\n\n**Range**: \"首页视觉\"是个名词，它要产生的效果是三个动词 —— 读懂（品类与差异化）、信任（专业度）、行动（点 CTA）。\ncrew：定位/信息层级（决定首屏只留几句话）· 转化文案（一句话说清品类、对象、差异）· 视觉设计（把高级/简洁/科技感落成具体版式与字体）· 前端首屏性能（科技感常和首屏加载打架）· 增长实验（A/B + paid_social 队列口径）。\nred team：一个 Notion 老用户 + 一个从付费广告点进来的陌生人，任务是\"给我一个关掉这个页面的理由\"。\n\n**Judge**: 短期你自己看 3 个文案方向 + 2 个缩略 moodboard（便宜、能直接否定）；上线后 paid_social 两周转化 vs 1.9% 基线。审美由你判，\"5 秒看懂\"不能由我们互判。\n\n**Needs**: 缺产品品类/目标用户/价格/与 Notion 的差异点（不是我该猜的）· 缺\"高级科技感\"的参考站点 2–3 个 · 缺现有页面埋点与 A/B 权限。\n\n**Declined**: —\n\n## Task\n\n**Purpose**: 付费社媒的投放要不要继续加预算 —— 首页得让这批人看懂并转化。\n**Context**（我查到的，请确认）：现首页是占位文案，通篇\"all-in-one platform / seamless / AI-powered\"，无品类、无对象、无价格、无差异化。10-06→10-27 期间 paid_social 从 0 变主要来源，转化由 3.9% 掉到 1.9%。support 样本三条都在抱怨理解成本和注册摩擦。\n**Materials**: 一手 —— index.html、analytics/weekly.csv、support/chats-sample.md。二手/禁用 —— 暂未指定（建议禁用竞品营销话术，那是空话的来源）。\n**Boundaries**: 你给的是方向词（高级/简洁/科技感），不是墙。需要你点头的候选墙：\n1. 不许出现\"all-in-one / seamless / AI-powered\"这类无品类空话\n2. 首屏只留一个 CTA，不做多按钮并列\n3. 本次不动注册流程（日历授权那一步另开）\n4. 不加价格页，只在首屏点明价格区间\n**Done**: checkpoint —— 先给你 3 条 hero 文案（品类 + 对象 + 差异化）＋ 2 个灰度 moodboard，你选定后才做整页。交付 —— 可上线的移动端首屏页 + 5 秒测试记录 + 埋点方案。看到这三样就停。\n\n## Open\n- 产品到底是哪个品类、卖给谁、和 Notion 的一句话区别是什么（没有这个，重做视觉只会更精致地空洞）\n- \"高级/简洁/科技感\"的参照物：给 2–3 个你认可的站点\n- 上面 4 条墙，哪几条接受、哪几条否掉\n- 时间/资源：两周 A/B 窗口能不能接受，还是必须先上线再测\n\nReady: no —— 五问里 Purpose 只答了一半（目标有了，决策没用说），Materials 缺产品事实，Boundaries 还只是形容词，Done 未确认 checkpoint。Requirement 的 Hand over / Depth / Range 三个提议也待你点头或否掉。\n"}

RESULT: Successfully wrote to /tmp/pf-24-with_skill-mrmjvi76/local/plans/paid-social-homepage.md

ASSISTANT: 已写入 `/tmp/pf-24-with_skill-mrmjvi76/local/plans/paid-social-homepage.md`（一屏）。

先说一个你可能不想听但数据已经写好的事：**你要的是"重做视觉"，而这批人看不懂的不是视觉。** 10-20 起 paid_social 流量翻倍（11.8k→21k），转化同时腰斩（3.9%→1.9%）；support 里的原话是"跟 Notion 没区别""价格页在哪""注册要连日历就放弃了"。所以我把交接物从"新首页"抬到了"首屏先答掉这三个问题，再看付费社媒转化能不能回到 4%"。回退档是只改 hero 做 A/B —— 你说"太大了"我就退到这里。

三件需要你裁定的事：

1. **产品事实**：品类、给谁、和 Notion 的一句话区别、价格。这个我猜不了，缺了它，视觉只会更精致地空洞。
2. **"高级/简洁/科技感"是形容词，不是墙**。我给转了 4 条具体的 don'ts（禁 all-in-one/seamless 类空话、首屏单 CTA、本次不动注册流程、不加价格页），逐条接受或否掉。另外给 2–3 个你觉得"高级"的站点，这比形容词有用十倍。
3. **Done**：我提议先只给你 3 条 hero 文案 + 2 个灰度 moodboard，选定后才做整页 —— 现在否掉比做完再否掉便宜。

Ready 是 **no**。你读完确认 Ready 行（或改掉上面几条）我再动手。要不要把这份计划交给 `/define-goal` 收敛成目标？