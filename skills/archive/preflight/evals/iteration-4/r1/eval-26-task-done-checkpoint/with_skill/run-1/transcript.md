TOOL bash: {"command": "cd /tmp/pf-26-with_skill-xn99qrxl && ls -la && echo \"---\" && git rev-parse --show-toplevel 2>/dev/null; echo \"---\"; find . -maxdepth 3 -not -path './.git/*' -type f | head -50"}

TOOL bash: {"command": "cat /home/zdan/.zstack/skills/plan/preflight/references/ambition.md; echo \"==========\"; cat /home/zdan/.zstack/skills/plan/preflight/references/task-definition.md"}

RESULT: total 172
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 63 root root 167936 11月 10 22:25 ..
-rw-rw-r--  1 zdan zdan      0 11月 10 16:17 .keep
---
---
./.keep


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


TOOL bash: {"command": "date +%F"}

RESULT: 2026-11-10


TOOL write: {"path": "/tmp/pf-26-with_skill-xn99qrxl/local/plans/usp-ease-vs-cheap.md", "content": "# Plan: 下季度 USP：易用还是便宜\n\n- Asked: “写一份我们 SaaS 的竞品分析报告” ／ 目的：支撑下季 USP 往易用还是便宜走；完成＝直接给完整报告\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\nHand over: 不是“一份竞品分析”，而是**一条能拿去开会的选边结论**：易用 vs 便宜，选定一个，附 3 个可核对的依据，以及“为什么不是另一个”。\nFallback: 只做 2–3 家真正撞车的对手，深度对比 + 一条推荐。\nDepth: 专家不问“功能清单”，问 **从注册到第一个价值交付要走几步几分钟**，以及价格页的锚点结构（档位、免费档、按量项）。最原始材料：对手官网价格页、帮助文档、changelog、发布说明、评论区用户原话（不是二手评测）。工具：定价拆解模型（按你们典型客户规模算 TCO）+ 可复现打分表。Stretch：拿你们最近 20 个赢单/丢单原话，检验“太复杂”“太贵”这两个抱怨是否真的在成交环节起作用——能预测没看过的单子才算数。\nRange: 动词＝让决策者 30 分钟内相信一个因果并选边；挖出对手没说的事；挑破你们自己的信念。Crew：竞品分析师（拆定价与 onboarding 路径）、单位经济分析师（TCO/毛利）、一线销售或客服（客户原话）、记者（追一手来源）、红队＝做空视角＋“前竞品销售”。\nJudge: 每个数字都要点得开的一手来源；再加一个红队 session 专攻“为什么便宜才是对的”，另一个 session 裁定哪些反驳成立。判方法也判结论：蒙对不算过。\nNeeds: 你们的收入量级/客户规模/上季度调价结果、3 个竞品名单、客户评论导出、赢单丢单记录。**以上全部缺失。**\nDeclined: 大纲检查点 — 理由：要直接拿成品。代价记在这里：方向错了会在第 30 页才发现。\n\n## Task\nPurpose: 下季度 USP 往易用还是便宜走，最后要一条推荐和理由。（已答）\nContext: **未答** — 只有“我们 SaaS”四个字。缺：客户是谁、多少钱、上季度调价出了什么事、现在打谁。\nMaterials: **未答** — 不排源就等于允许任何源。必须点名 2–3 家对手，并禁掉二手评测站。\nBoundaries: **未答** — 最该有的是“不许编 ARR、用户数、增长率”“不许只给形容词不给取舍”。\nDone: 完整报告一份。（已答；不含大纲）\n\n## Open\n1. 上季度调价“落得不好”具体是什么？这条直接决定“便宜”是不是伪选项。\n2. 三家对手是谁？你们现在主要在谁手里丢单？\n3. 有没有客户原话或丢单记录能给？（没有的话，第 2 层深度做不了，只能降级）\n4. 报告给谁看、多长时间？30 分钟会和 5 页备忘写法不同。\n\nReady: no，因为 Context / Materials / Boundaries 三格空着，Requirement 的四条也还没被裁定。\n"}

RESULT: Successfully wrote to /tmp/pf-26-with_skill-xn99qrxl/local/plans/usp-ease-vs-cheap.md

ASSISTANT: 计划已写好：`/tmp/pf-26-with_skill-xn99qrxl/local/plans/usp-ease-vs-cheap.md`

先说结论：这份计划现在还是 **Ready: no**。目的和完成标准这两项你已经回答，但仍有四类信息缺失；如果按“直接给完整报告”这个要求去做，最后只会得到一份功能对照表，里面配上编造的 ARR；它在会上没有用。

最关键的三个问题：

1. 上季度那次调价，具体出了什么问题？
2. 三家竞争对手分别是谁？你主要在谁手里丢单？
3. 你能否提供客户原话，以及赢单、丢单记录？

有这三点，就可以做到“用你们自己的成交数据检验易用还是便宜”；没有这三点，就只能退回到“对比 2–3 家并给一条推荐”。

另外请注意：你选择不做大纲检查点，我把代价记在计划里了。成本不高时我照做；但这份报告要影响定价，所以我先问你：要不要先给半页结论框架？

请阅读计划，并确认 Ready 那一行；确认后我用 `/define-goal` 以它为源启动工作。