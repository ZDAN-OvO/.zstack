TOOL bash: {"command": "pwd; ls -la; echo \"---\"; git status 2>&1 | head -20; echo \"---\"; ls local 2>/dev/null"}

TOOL bash: {"command": "find . -maxdepth 3 -not -path '*/.git/*' -not -path '*/node_modules/*' | head -60"}

RESULT: /tmp/pf-21-with_skill-7ufdwvcq
total 172
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 64 root root 167936 11月 10 22:46 ..
-rw-rw-r--  1 zdan zdan      0 11月 10 16:17 .keep
---
fatal: not a git repository (or any of the parent directories): .git
---


Command exited with code 2

RESULT: .
./.keep


TOOL bash: {"command": "cat /home/zdan/.zstack/skills/plan/preflight/references/ambition.md; echo \"==========\"; cat /home/zdan/.zstack/skills/plan/preflight/references/task-definition.md"}

RESULT: # Ambition: distilled

Source of the Requirement axes and the judge in `/preflight`. Distilled from Felix Rieseberg (engineering lead on Claude at Anthropic):

- **[E]** Essay, "How to be more ambitious: A tutorial for humans with models", 2026-10-13. <https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/>
- **[I]** Interview, Silicon Valley Girl, "Claude Engineering Lead: Stop Using Claude Like It's 2024", 2026-10-20. <https://www.youtube.com/watch?v=D-SVFneJ_Nk>. Timestamps are approximate and come from the auto-captions.

## Thesis

- **Best guess.** A task given to the model is the user's best guess at a route to an outcome. The model runs the guess. [E]
- **Four types.** Ambition comes in four types: speed, altitude, depth and range. Speed means the same work done faster. It is well established and needs no new thinking, so the skill leaves it out. [E]
- **Self-efficacy.** People are held back by what they believe is possible. Specific, hard goals beat "do your best" (Locke and Latham, 35 years of studies). Belief, a visible precedent and permission to fail all raise what gets attempted. The studies are on humans; carrying them over to models is Felix's extension. [E]

## Altitude

- **Goal beyond the goal.** Ask what should happen next, then hand that over. The crash example climbs from "fix this crash" to "keep the apps crash-free". [E]
- **Ceiling.** Keep climbing until the model fails. "Go make money" is past the line today. Work at the ceiling sits at the frontier and gains the most from the next model. [I 39:05]
- **Fit.** Altitude fits work after an ultimate outcome. Work that will be discussed in meetings is a good sign. It fits creative work less well. [E]
- **Workflow cost.** Climbing usually means rebuilding access first. Crash-free needed crash-report fetching, a version-to-commit map, and Windows, macOS and Linux machines to reproduce and verify on. The setup cost is real and worth paying. [E] [I 22:39]
- **Conveyor belt.** A user who carries items to the model one at a time is the bottleneck. Give the model the whole data source and let it choose what to act on. [I 22:39]

Worked ladder, a quarterly business review [E]:

1. Update the template's numbers.
2. What changed this quarter, why, and what to do.
3. The three most urgent decisions, with the case for and against each.
4. Replace the deck with a better way for leadership to catch problems early and move money and people. Prove on past history that it would have caught them sooner, then run it beside the deck for a quarter.

## Depth

- **Instruments, not costume.** A persona switches the vocabulary and keeps the method. Ask which tools the top of the field uses, then require those tools, and get the result explained plainly. The leap in AI 3D and motion work came from using Blender, not from a better grasp of animation. [E] [I 10:28, 25:20]
- **Stretch target.** Set an unreasonable goal and treat it as reasonable: 200 ms, not 5 s. When the model says it is impossible, tell it to keep going. [E]
- **Challenge beliefs.** Give the model the raw data and have it try to reproduce a belief the user holds ("churn is an onboarding problem"). [E]
- **New knowledge.** From inside the data, look for the blind spot: an unknown early signal, shown to predict data it has not seen. [E]
- **Expert questions.** Before the task is rewritten, name four things: (1) what a top professional would do that is not being asked; (2) the rawest material they would start from; (3) their specific methods and tools; (4) what, other than the model or the user, would show the result is right. Then rewrite the task to ask for exactly that. [E]
- **Process.** For work that rests on taste, the gain comes from copying the steps professionals take, since good work comes out of a refined process. [I 8:26–9:52]

## Range

- **Noun to verb.** A deliverable's name hides its job. A quarterly review is not "a deck". It gets busy people to believe a cause-and-effect story and decide under uncertainty in 30 minutes. The verbs show which fields can help. The idea comes from Kelley and Littman, *The Art of Innovation*. [E]
- **Crew.** Ask which team would be assembled if the stakes were extreme. For the review: an analyst, a journalist and an editor; a motion and audio designer if it is presented; a short seller and a forensic accountant as the red team. [E]
- **Do, not write.** Use the crew to find fields and techniques. Ask the model to do the short seller's research, not to write in a short seller's voice. Role play makes the transcript stranger and the output no better. [E]

## Judge

- **Outside session.** The session that did the work is a poor judge of it. Far more tasks are unsafe to trust to a single session than to the model. Prefer a check the model can run and get feedback from at once. [E] [I 26:10]
- **Grade the process.** A correct guess of the temperature fails. A half-degree miss that came from the right location and a reputable source passes. [I 7:35]
- **Adversarial review.** When nothing hard can check the work, spin off sessions whose only job is to prove the output wrong, as red teams and short sellers do. Finding flaws is easier than building, so a cheaper model can do the attacking. Then one more session rules on which objections hold. Valid objections go back to the maker, which can decline them. [I 12:57–15:39]
- **User as client.** When the user can tell good from bad themselves, their judgment of the result is enough. When they cannot, add more AI review. [I 16:15]
- **Fact checks.** Requiring a verified primary source for every number in a document can be trusted to a single session. [I 17:03]

## Access

- **Model experience.** Picture yourself as the model doing this task. You would want the raw data, a computer, the ability to install software, and room to decide for yourself. [I 22:01]
- **Prerequisite.** Every type of ambition needs a computer that can install software, plus access to the relevant data. [E]
- **Start cheap.** Let the model drive the user's tools in a browser first. Build connectors only after a workflow has proven itself. [I 24:00]
- **Generalists.** Give a generalist model the tools and the data rather than a cast of narrow persona agents with pre-sliced data. Generalist models overtook a purpose-built math system within months. [I 17:37]

## On skills

- **Half-life.** Skills often carry advice meant for the previous model generation, and removing a skill sometimes improves the output. Making that call takes an eval and a clear sense of good and bad output. [I 21:26]
==========
# Task definition: distilled

Source of the stages and the five slots in `/preflight`. Distilled from Gary Chen, 《Prompt 再完整也没用：先学会定义任务》, Bilibili BV1fseX6vE2L, about 20 min. <https://www.bilibili.com/video/BV1fseX6vE2L/>. Timestamps come from the auto transcript.

## Thesis

- **Two layers.** Writing a prompt makes the words precise. Defining the task decides what is wanted. The prompt is the floor, the task decides the height. An empty task gives an empty output however polished the words; a defined task makes the prompt write itself. [0:34–1:30]
- **Senior, not intern.** Current models read, revise, verify and re-plan on their own. Scripting the steps is intern-era management. Brief the what, the why, the walls and the stop, and leave the how to the model. [2:53–3:58]
- **Content, not intent.** The model challenges facts. It never questions what the user wants, and it acts on receipt. [4:11, 15:32]
- **Mirror.** Vague intent comes back as generic output. "Ask me if unsure" only turns an essay question into a fill-in-the-blank. The model can ask, but the blanks are still the user's to fill. [16:02–16:27]
- **Management.** Defining a task is thinking (what do I want, what does it support, what counts as good) plus communication (making it clear to another capable mind). A good brief is hard to write mostly because the thinking is unfinished. Human reports often do not dare to ask back either. [17:16–18:31]

## Stages

Serious knowledge work moves through **think → explore → decide → execute**. A request made at the wrong stage gets the wrong job [5:07–6:14]:

| Stage | What the model should do | What a request from the next stage gets |
|---|---|---|
| Think | Ask the user questions until the vague becomes concrete | A full draft: the version anyone could write, with no thesis |
| Explore | Map the options and the trade-offs | A recommendation: a guess at criteria the user has not set |
| Decide | Weigh the options against the user's decision logic | — |
| Execute | Work from the five slots | — |

The model never says the stage is wrong. The skill is to pause and name the stage first. [5:54]

## Five slots

| Slot | Question the user asks themselves | Without it |
|---|---|---|
| Purpose | What will I do with this output? | The model performs the action textbook-style: everything covered, nothing to decide on. |
| Context | What would a capable stranger need to know before taking over? | The model assumes the generic case: a big company, free to change prices, competing with everyone. |
| Materials | What should it work from? | Anything not banned counts as allowed. Sources go unranked, and gaps get plausible inventions. |
| Boundaries | What output would make me say "not what I wanted"? | The open space fills with directions nobody imagined. |
| Done | What appears in front of me that means I can stop? | A wrong direction surfaces at page 30, not at the outline. |

[7:20–13:11, summary 19:19]

- **Purpose is a decision, not an action.** "Analyse five competitors" is an action. "Support next quarter's call between easier and cheaper, and end with one recommendation" is a purpose, and it lets the model narrow its focus on its own. [7:33–8:17]
- **Context sets the angle.** Context is not extra information. It decides how the model looks at the task. [9:09]
- **Narrowing is defining.** Studying three overlapping rivals in depth beats scanning five. [9:50]
- **Leave blank.** Write "not found, leave it blank, do not invent" into Materials, and ban low-trust sources by name. [10:08]
- **Walls versus directions.** Purpose, Context and Materials give direction. Boundaries are the walls, mostly "don'ts". Most briefs give direction and no walls. [11:14]
- **What, not how.** Specifying the artifact (an outline, Markdown, 3–4 bullets per section) is part of Done. Micromanagement governs the process; the artifact's shape is the user's call. [12:27]
- **Checkpoint.** The most valuable line in Done: "give me the framework first, not the full report". [12:54]
- **Scope.** Boundaries say what not to do, and Done says where to stop. Together they give the scope. [13:11]

## When to skip

There is one test: is a redo expensive? Skip the brief for a quick question or a lookup. Write it for output that goes to a meeting, to another person, or comes from a long unattended run. Ten minutes of briefing beats three reruns. [15:04]

## Worked brief, a SaaS competitor analysis

| Slot | Brief [7:54–12:26] |
|---|---|
| Purpose | Next quarter's product direction: should the USP lean easier or cheaper? End with one recommendation and the reasons. |
| Context | A ~$2M-revenue marketing-automation SaaS. Customers are mostly firms under 50 people who say the product is complex and expensive. Last year's price change landed badly. |
| Materials | Primary: three rivals' sites and product docs. Secondary: the user's compiled reviews. No second-hand review articles. Not found → leave blank. |
| Boundaries | No invented ARR, user counts or growth rates. Do not touch the tier structure (pricing position is open). No adjective-only output without trade-offs. |
| Done | An outline first: key differences, the recommended USP, and the reasoning. The full report only after review. Markdown, 3–4 bullets per section. |

The vague prompt gave five near-identical rivals and no direction. The brief gave an outline that picks easier, benchmarks the rival with three-step onboarding, and flags that easier and cheaper conflict. That outline is ready for a meeting. The figures are the video's case setup, not industry data. [13:52–14:37]

## Unverified

- The video gives no tested wording for making the model ask back.
- It cites the Microsoft and LinkedIn 2024 Work Trend Index without quoting it. Check the report before citing it.


TOOL write: {"path": "/tmp/pf-21-with_skill-7ufdwvcq/local/plans/competitor-analysis.md", "content": "# Plan: 竞品功能/定价/优缺点对比\n\n- Asked: 帮我分析 5 家竞品的功能、定价和优缺点\n- Stage: think（请求早于意图一步：没有产品、没有客群、没有这 5 家是谁）\n- Date: 2026-02-12\n\n## Requirement\n\nHand over: 一份能支撑一个决定的对比——「我们下一季度该往更便宜还是更好用走」，结尾给一条推荐和理由。\nFallback: 只做 5 家 × 维度的事实表，不做推荐。\nDepth:\n- 原始材料：定价页快照（带抓取日期、含 annual/monthly、加购项、隐藏费用、\"联系销售\"档），产品文档/API/更新日志/招聘 JD，1–3 星评论（G2/Capterra/Reddit/HN）含评分分布与评论量。\n- 仪器：单价还原表（每席位每年真实成本 = 标价 × 折扣信号 × 年付系数）、能力矩阵按\"能否做到/需几步/要不要付费解锁\"打分、价格历史用 web.archive 拉三条时间线。\n- 不用营销落地页当功能证据，不用\"优缺点\"抄自厂商自述。\n- Stretch target：一条可被推翻的断言，用原始数据检验，例如\"X 只在 N 席以下更便宜\"或\"差距在 onboarding 而不在功能\"。\nRange:\n- 动词：比较 → 支撑决策 → 在会上辩护 → 交给销售做成对战卡。\n- 班底：定价/打包分析师（还原真实单价）、产品经理（能力分类学）、win-loss 销售工程师（客户为什么选/不选）、客户研究员（评论挖掘）、红队（攻击竞品集选错、价格过期、把营销话术当功能）。\nJudge: 每条价格必须挂来源 URL + 抓取日期，每条功能必须挂文档/更新日志而非落地页；缺来源或超 90 天即判失败（可脚本自查）。另开攻击会话挑错，再由一个会话裁决哪些成立。你懂这个市场时，你看过来源后的判断就够。\nNeeds: 你们的产品与客群、这 5 家是谁（或选它们的标准）、读者与用途、内部 win/loss 与现价表；公开定价页（部分只有\"联系销售\"，拿不到就留空）、G2/Capterra 可访问、web.archive。**目前工作目录为空，无任何产品资料——这是缺口，不是待办。**\nDeclined: 暂无\n\n## Task\nPurpose: （待你回答）这份对比要支撑哪个决定？\"分析 5 家竞品\"是动作，不是目的。\nContext: （待你回答）卖什么、卖给谁、什么价位、什么阶段；谁读、什么时候要。\nMaterials: （待你回答）主用哪些一手来源，哪些来源禁用。已知可用：各家定价页、产品文档、评论平台、web.archive。空位：内部客户访谈/流失原因、真实成交价——没有就留空，不猜。\nBoundaries: 建议设墙：不编造 ARR/用户数/增长率；不把不同客群的厂商放在一张表里比；不输出只有形容词没有取舍的\"优缺点\"；不给没日期的价格。待你确认或改写。\nDone: 建议：先要一个骨架（竞品集 + 能力分类 + 1 家样例行），你点头后再出全表 + 一条推荐；Markdown，每节 3–4 条。待你确认。\n\n## Open\n- 哪个产品、哪个市场、哪 5 家——缺这个，任何输出都是通用模板。\n- 背后的决定是什么（定价/定位/融资/路线图/销售对战卡）。\n- 内部数据（win-loss、成交价、流失原因）能不能拿到。\n\nReady: no — 产品与竞品集未知，五个 Task 槽位都还空着。\n"}

RESULT: Successfully wrote to /tmp/pf-21-with_skill-7ufdwvcq/local/plans/competitor-analysis.md

ASSISTANT: 计划已写到 `local/plans/competitor-analysis.md`（当前目录不是 git 仓库，工作区里只有 `.keep`，没有任何产品资料）。

**先说结论：这个请求早于阶段一步。** 有产品、有客群、有"这 5 家是谁"，才能谈功能/定价/优缺点；现在直接跑，只会得到一份谁都能写的通用模板。

**三个需求轴上的建议**（可接受 / 改写 / 拒绝，拒绝请给理由）：

- **拔高**：不要只交表，交"支撑一个决定"的对比——比如下一季度走更便宜还是更好用，结尾一条推荐。我能自己负责到底的天花板是"给出可辩护的推荐"；再往上是"直接改价并承担结果"，那需要你们的流失和成交数据，超出我今天的边界，所以那就是 fallback 的位置。
- **加深**：不用营销落地页当证据。价格按"每席位每年真实成本"还原（年付系数、加购、隐藏费、"联系销售"档），功能按文档/更新日志/招聘 JD 判定，优缺点从 1–3 星评论的评分分布里挖。另加一条可被推翻的断言，用原始数据验。
- **扩面**：这件事的动词是"比较 → 支撑决策 → 在会上辩护 → 交给销售"。班底：定价分析师、产品经理、win-loss 销售、客户研究员，外加一个红队——专门攻击"这 5 家是不是真竞品""价格是不是过期了"。
- **裁判**：每条价格挂来源 URL + 抓取日期，每条功能挂文档而非落地页，缺来源即失败（可脚本自查）；再加攻击会话挑错、一个会话裁决。你熟悉这个市场的话，你看过来源后的判断就够。

**需要你回答的五个问题**（只有你能答）：

1. **目的**：这份东西最后支撑哪个决定？定价、定位、融资故事、路线图，还是销售对战卡？
2. **背景**：你们卖什么、卖给谁、什么价位、什么阶段；谁读，什么时候要？
3. **材料**：主用哪些一手来源，哪些来源禁用（比如二手评测文章）？内部的 win-loss、成交价、流失原因能提供吗？没有就留空，我不会填。
4. **边界**：什么样的输出会让你说"不是我要的"？我给的建议墙是：不编造 ARR/用户数；不同客群不混在一张表里比；不输出只有形容词的"优缺点"；不给没日期的价格。
5. **完成**：先给你一个骨架（竞品集 + 能力分类 + 1 家样例行）再出全表，可以吗？

**最卡的一点**：哪 5 家。要么你点名，要么给选它们的标准（同客群、同价位、近 12 个月在销售里撞到过），我按标准去挑并由你确认。

回答后我把计划补成 Ready: yes。之后可以用 `/define-goal` 以这份计划为源。