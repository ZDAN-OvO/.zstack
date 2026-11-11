TOOL bash: {"command": "cd /tmp/pf-20-with_skill-598iqud_ && ls -la && echo \"--- git ---\" && git rev-parse --show-toplevel 2>/dev/null || echo \"no git\""}

TOOL bash: {"command": "cd /tmp/pf-20-with_skill-598iqud_ && find . -maxdepth 3 -not -path '*/.git/*' | head -50 && echo \"--- plans ---\" && ls -la local/plans 2>/dev/null || echo \"no local/plans\""}

RESULT: total 172
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 64 root root 167936 11月 10 22:46 ..
-rw-rw-r--  1 zdan zdan      0 11月 10 16:17 .keep
--- git ---
no git


RESULT: .
./.keep
--- plans ---
no local/plans


TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/references/ambition.md"}

TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/references/task-definition.md"}

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


RESULT: # Task definition: distilled

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


TOOL write: {"path": "/tmp/pf-20-with_skill-598iqud_/local/plans/competitive-analysis.md", "content": "# Plan: 竞品分析（意图待收窄）\n\n- Asked: 帮我做个竞品分析\n- Stage: think（意图未成形，先问清再动笔；此时直接写会得到一份谁都能写的五家对比）\n- Date: 2026-11-10\n\n## Requirement\n\n（三轴皆为建议，请逐条 接受 / 改写 / 拒绝）\n\n- **Hand over**: 第 3 级 —— 讲清竞品各自在取舍什么，并落到下季度一个方向建议，附正反论证。第 4 级（持续追踪竞品价格/功能/融资/评价，并自动驱动定价决策）今天超出模型能独立承担的范围，是本次的天花板。\n- **Fallback**: 第 2 级 —— 只讲差异与取舍，不给建议（当你还没准备好在会上被要求拍板时用）。\n- **Depth**: 起点不是竞品官网的营销文案，而是它们无意中留下的痕迹：定价页历史快照、changelog / release notes、招聘 JD、客户差评原文、财报与融资披露。工具决定方法：抓取加存档、价格历史比对、评价语料统计。拉伸目标 —— 从评价语料里找出一个\"所有竞品都没满足\"的需求，并给出可被后续数据推翻的预测。\n- **Range**: 这份东西要干的动词是「让人在半小时内相信一条因果关系、并在不确定下做一次取舍」，不是「罗列五家」。所以要的班底：行业分析师（拆商业模式与单位经济）、调查记者（挖未公开的动机、人事、融资）、定价策略师、一线销售（真实的赢单输单异议）。红队：做空机构 + 前竞品员工，任务只有一个 —— 证明\"我们的差异点其实不成立\"。\n- **Judge**: 每条结论必须挂一手来源（定价页快照 / changelog / JD / 评价原文），挂不上就删。另起独立 session 只做证伪，再由第三个 session 裁定哪条反驳成立；被驳回的反驳记下理由。你自己就在这个市场里，若你能直接判断好坏，以你的判断为准，但仍要求逐条有源。\n- **Needs**: 我们的产品与客群（缺）、竞品名单或筛选标准（缺）、内部赢单/输单与流失数据（缺）、联网抓取许可（未确认）。\n- **Declined**: 暂无\n\n## Task\n\n- **Purpose**: 未答 —— 这份分析之后，你要做的那个决定是什么？\n- **Context**: 未答。已查到的事实：工作区为空，没有你们产品的任何材料，也没有既有分析，所以 Context 只能由你给。\n- **Materials**: 未答。请排优先级（一手：竞品定价页 / changelog / 产品文档 / JD / 财报；二手：你已整理过的评测）。建议写入\"查不到就留空，不许编\"，并点名禁止二手评测聚合站。\n- **Boundaries**: 未答 —— 哪种结果会让你说\"这不是我要的\"？（例：不要凭空给出 ARR、用户量、增长率）\n- **Done**: 未答。建议 checkpoint：先给一页框架（差异维度 + 建议方向 + 理由），过审后再写全文；成品 Markdown，每节 3–4 条。\n\n## Open\n\n- 我们的产品是什么、卖给谁\n- \"竞品\"指哪几家，按什么标准选（重叠度高的三家挖深，胜过扫五家）\n- 这份东西给谁看、在哪个会上用\n- 最终要的是\"一个建议\"，还是\"一张可以自己比对的表\"\n\n## Ready\n\nno —— Task 五槽全空，Requirement 三轴待你裁决。\n"}

RESULT: Successfully wrote to /tmp/pf-20-with_skill-598iqud_/local/plans/competitive-analysis.md

ASSISTANT: 计划已写入 `/tmp/pf-20-with_skill-598iqud_/local/plans/competitive-analysis.md`。

**Look 的结果**：工作区是空的（只有一个 `.keep`），没有你们产品的任何材料，也没有既有分析。所以 Context 和 Materials 只能由你给 —— 我不会替它们填一个"典型 SaaS 公司"。

**这条请求目前卡在 think 阶段**：一句话的"竞品分析"，最可能产出的是五家官网功能的对照表 —— 谁都能写，会上没人能用它做决定。

### 需要你答的五件事

1. **Purpose** —— 这份分析之后你要做的那个决定是什么？（"分析五个竞品"是动作，不是目的）
2. **Context** —— 一个有能力但完全不懂你们业务的陌生人，需要知道什么才不会瞄错方向？产品是什么、卖给谁、多大规模、最近踩过什么坑。
3. **Materials** —— 允许它读什么？请分一手/二手并排序，点名禁止哪些来源，以及"查不到就留空，不许编"。
4. **Boundaries** —— 哪种结果会让你说"不是我要的"？这是墙，不是方向。
5. **Done** —— 什么东西出现在你面前就算结束？建议的第一步是"先给一页框架，过审再写全文"。

### Requirement 三轴需要你裁决

- **Altitude**：建议交到"下季度一个方向建议 + 正反论证"这一级；保底是"只讲差异与取舍"。上一级（持续自动追踪竞品并影响定价）是本次天花板。
- **Depth**：不从官网文案读，从定价页历史快照、changelog、招聘 JD、客户差评原文读 —— 工具换了，方法才算换了。拉伸目标是从差评里挖出一个所有竞品都没满足的需求。
- **Range**：成品要做的事是"让人半小时内相信一条因果并做取舍"，所以班底是行业分析师 + 调查记者 + 定价策略师 + 一线销售，红队是做空机构和前竞品员工，专门证明你的差异点不成立。

每一条回我「接受 / 改写 / 拒绝 + 理由」就行，拒绝的会记进 Declined。答完我改好 Ready 行，然后可以 `/define-goal` 拿这份计划当输入。