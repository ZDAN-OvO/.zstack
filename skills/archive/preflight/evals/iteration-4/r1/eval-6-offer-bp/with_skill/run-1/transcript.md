TOOL bash: {"command": "ls -la /tmp/pf-6-with_skill-ov8j2n25 2>/dev/null; echo \"---git---\"; cd /tmp/pf-6-with_skill-ov8j2n25 && git rev-parse --show-toplevel 2>/dev/null"}

TOOL bash: {"command": "ls /home/zdan/.zstack/skills/plan/preflight/references/"}

RESULT: total 172
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 63 root root 167936 11月 10 22:22 ..
-rw-rw-r--  1 zdan zdan      0 11月 10 16:17 .keep
---git---


Command exited with code 128

RESULT: ambition.md
task-definition.md


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


TOOL write: {"path": "/tmp/pf-6-with_skill-ov8j2n25/local/plans/investor-business-plan.md", "content": "# Plan: 投资人会前能用的商业计划书\n\n- Asked: \"给我搞一份商业计划书，投资人下周要看\"\n- Stage: execute（材料要给到外人，重做一次代价是一个会）\n- Date: 2026-11-10\n\n## Requirement\n\nHand over: 先做「投委会预演」——按目标基金自己的 thesis、阶段和投决逻辑判定这单会不会过，\n再反推出材料；交付物是预演结论 + 一页投资逻辑 + 正文。计划书是结论的副产品，不是起点。\nFallback: 把下周这场会当成一次独立事件——一页投资逻辑 + 10 页正文 + 一次路演彩排，\n目标是会后拿到明确下一步（进尽调 / 约下次），暂不做投委会反推。\nDepth: 原始材料＝真实经营数据（cohort 留存、CAC/LTV、毛利、现金 runway、pipeline、合同），\n不是自己写的介绍稿；工具＝单位经济学模型、bottom-up TAM（客户数 × 客单价 × 可及份额）、\n可比交易与估值倍数（一手披露优先）。专家不会问的那一步：先看目标基金已经投了谁、\n在哪一轮、为什么，再从那儿倒推该讲什么。\nStretch: 用空头视角审一遍——哪个数字最先崩，投资人当场会拿哪个数否掉你；\n以及用过去 12 个月真实数据回测增长预测的假设。\nRange: 名词还原成动词——让人 30 分钟内相信一条因果链、在不确定下愿意下注、愿意把有限时间给你。\nCrew: FA/投行（定价与可比交易）、行业分析师（bottom-up 市场）、增长数据（单位经济学）、\n记者+编辑（叙事与一页纸）、红队：做空机构＋投过同类公司的前投资人。\nJudge: 每个数字有一手出处（可自查）；财务模型能被投资人当场改假设跑通；\n两个攻击 session（前投资人 / 做空视角）+ 一个裁决 session 裁定哪些质疑成立；\n你若清楚对方会问什么，你的判断优先。\nNeeds: 经营数据与财务模型访问；本次融资额与让股比例；目标基金名单及其 thesis/portfolio；\n可比交易数据；客户访谈或合同。缺：以上全部（见 Open）。\n\n## Task\n\nPurpose:\nContext:\nMaterials:\nBoundaries:\nDone:\n\n## Open\n\n公司做什么、阶段（收入/用户/团队/runway）、上一轮谁投的、这次融多少让多少、\n下周见的是谁（基金/阶段/规模/关注点）——全未知。没有这些，写出来的必是通用稿。\n\nReady: no — 三轴一个都没定，五个槽全空。\n"}

RESULT: Successfully wrote to /tmp/pf-6-with_skill-ov8j2n25/local/plans/investor-business-plan.md

ASSISTANT: 已看过：工作区是空的（`/tmp/pf-6-with_skill-ov8j2n25`，无 git、无任何公司材料）。没有可查的事实，所以下面全是只有你能答的东西。计划草案：`local/plans/investor-business-plan.md`

## 请求的问题

"下周投资人要看"是把它当**文档**做——那样出来的是公司介绍册：市场千亿、我们占 1%、形容词满页、没有取舍。投资人翻 3 页就走。

## Requirement 三轴（每个都可以接受 / 改写 / 拒绝）

**Altitude** — 交给模型的是结果，不是这一步。
- 提议：不做"计划书"，做**投委会预演**——按目标基金自己的 thesis、阶段、投决逻辑，先判定这单会不会过；然后反推该交付什么。计划书变成结论的副产品。
- 下限（fallback）：只保下周这场会——一页投资逻辑 + 10 页正文 + 一次彩排，目标是会后拿到明确下一步。
- 再往上一级（大概率超出）：把融资做成常跑的线（名单打分、deck 变体、跟进节奏）。

**Depth** — 专家一步，比你要求的多一层。
- 原始材料是**你的真实经营数据**（cohort 留存、CAC/LTV、毛利、runway、pipeline），不是自己写的介绍稿。
- 工具：单位经济学模型、bottom-up TAM（客户数 × 客单价 × 可及份额）、可比交易与估值倍数。
- 专家会先做的、你没要求的那步：**先看这只基金已经投了谁、在哪一轮、为什么**，从那儿倒推讲什么。
- 拉伸目标：用空头视角审一遍，找出"投资人当场会拿哪个数否掉你"，并用过去 12 个月真实数据回测你的增长假设。

**Range** — 把"计划书"还原成动词：让人 30 分钟内相信一条因果链、在不确定下愿意下注、愿意把时间给你。班子：FA/投行（定价、可比交易）、行业分析师（bottom-up 市场）、增长数据（单位经济学）、记者＋编辑（一页纸叙事）、红队：做空机构＋投过同类的投资人。

**Judge** — 每个数字有一手出处；财务模型能被对方当场改假设跑通；两个攻击 session + 一个裁决 session。你清楚对方会问什么的话，你的判断优先。

## 五个槽，只有你能答

1. **Purpose**：下周这场会结束后，你要的**具体下一步**是什么？进尽调 / 给 term sheet / 只是先认识、为 6 个月后那轮铺路？（决定材料是"说服"还是"建立关系"）
2. **Context**：公司做什么、现在什么阶段（收入、用户、团队、runway）、上一轮谁投的、这次融多少让多少、下周见的是谁（基金、阶段、规模、看什么）？
3. **Materials**：一手优先——经营数据、客户合同/访谈、产品数据；目标基金的 public thesis 和 portfolio；可比公司融资与估值。**禁用**：二手行业报告摘要、AI 编的市场数字、没出处的 TAM。找不到的留空。
4. **Boundaries**：哪些输出会让你说"不是我要的"？（我的默认墙：编造 ARR/用户数/增长率；"市场规模千亿我们占 1%"式自上而下；只有形容词没有取舍；写成公司介绍册、没有风险与反方论证；不说明就改股权/估值口径；40 页）
5. **Done**：先给一页投资逻辑（问题–解法–为什么是现在–为什么是我们–数字–要多少钱做什么）＋目录，你确认后再写正文；正文 Markdown，每节 3–5 条；财务模型单独一张能改假设的表。

Ready 现在是 **no**。你把 1、2 答了（其余可以照抄默认），我就把三轴定稿、写好 Ready 行，再交给 `/define-goal` 以这份计划为源。