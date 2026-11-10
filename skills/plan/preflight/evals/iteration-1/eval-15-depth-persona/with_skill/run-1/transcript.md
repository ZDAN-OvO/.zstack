TOOL bash: {"command": "ls -la /tmp/pf-15-with_skill-xx3llmxb; echo \"---\"; find /tmp/pf-15-with_skill-xx3llmxb -maxdepth 3 -type f | head -50"}

TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/references/ambition.md"}

RESULT: total 184
drwxrwxr-x   4 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 109 root root 167936 11月 10 18:01 ..
drwxrwxr-x   2 zdan zdan   4096 11月 10 16:17 data
drwxrwxr-x   2 zdan zdan   4096 11月 10 16:17 notes
-rw-rw-r--   1 zdan zdan    131 11月 10 16:17 template.md
---
/tmp/pf-15-with_skill-xx3llmxb/template.md
/tmp/pf-15-with_skill-xx3llmxb/data/q3-metrics.csv
/tmp/pf-15-with_skill-xx3llmxb/notes/worklog.md


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


TOOL bash: {"command": "cd /tmp/pf-15-with_skill-xx3llmxb; echo \"=== template.md ===\"; cat template.md; echo; echo \"=== notes/worklog.md ===\"; cat notes/worklog.md; echo; echo \"=== data/q3-metrics.csv (head) ===\"; head -20 data/q3-metrics.csv; echo; echo \"=== wc -l ===\"; wc -l data/q3-metrics.csv"}

TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/references/task-definition.md"}

RESULT: === template.md ===
# Q3 业务回顾

## 收入
本季收入：{{revenue}}

## 客户
新增：{{new}}，流失：{{churn}}

## 下季计划
{{plan}}

=== notes/worklog.md ===
# 工作日志

- 9 月 8 日起，客服工单里"太难上手"的投诉明显变多。
- 8 月中旬把免费试用从 14 天改为 7 天。
- 老板说 QBR 下周四给 VP 看。

=== data/q3-metrics.csv (head) ===
month,revenue_usd,new_customers,churned_customers,nps
2026-07,182000,41,12,38
2026-08,176000,35,19,31
2026-09,171000,30,24,27

=== wc -l ===
4 data/q3-metrics.csv


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


TOOL write: {"path": "/tmp/pf-15-with_skill-xx3llmxb/local/plans/q3-churn.md", "content": "# Plan: Q3 流失归因（供 VP 版 QBR）\n\n- Asked: \"你现在是资深数据分析师，帮我分析 Q3 为什么流失变多\"\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\n\n**先摆事实（已核，无需你确认）**\n- `data/q3-metrics.csv` 只有 3 行：流失 12 → 19 → 24；新增 41 → 35 → 30；NPS 38 → 31 → 27；收入 182k → 176k → 171k USD。\n- 缺客户基数、缺分群、缺账户级流失清单、缺 Q1/Q2 基线。**用 3 行数据回答\"为什么\"只能产出一个故事，不是归因。**\n- 你手上的两条线索都是**可证伪的假设**，不是结论：8 月中试用 14 天改 7 天（只可能影响 8 月中之后注册的 cohort）；9/8 起\"太难上手\"工单变多（投诉在流失之后才被看到）。\n- `template.md` 是 3 个占位符的 QBR 模板；`notes/worklog.md` 写明老板周四给 VP 看。\n\nHand over（建议采纳）: 不做\"流失分析\"，做**VP 周四要拍板的三件事**——试用期改回 14 天？上线后 7 天的 onboarding 干预？对存量风险账户做挽留？每件给赞成/反对与代价。\nFallback: 只交\"流失变化的可确认事实 + 三种可能解释 + 各自需要什么数据才能判定\"。\n（上一级天花板：接管 Q4 流失指标，用周度预警跑在业务前面——今天的数据连月度归因都不支持，暂不可达。）\n\nDepth: 不用聚合月度数字，用品类里真正的工具——cohort 留存三角（按注册月排队）、按试用长度/套餐/客单分层、工单文本分类得到流失原因分布。最原始的材料是账户级流失表（含取消日期与取消理由），不是汇总表。\nStretch target: 用 8 月底可得的特征预测 9 月流失，在未见过的那一个月上打分；并**在原始数据上检验\"流失=onboarding/试用期\"这个信念**——若 8、9 月流失账户大多是 7 月及以前注册的，试用期改动就不是主因，这个否证比任何解释都值钱。\n\nRange: 这份东西的动词不是\"分析\"，是**让 VP 在 30 分钟里相信一条因果、并在不确定下批一个具体改动**。crew：分析师（cohort + 因果拆解）、客服运营负责人（真实取消理由分类）、定价/包装负责人（试用长度的转化经济学）；red team 由做空研究员担任——专攻季节性、获客结构变化、\"流失数上升但流失率没上升\"的分母效应；再由一次独立会话裁定哪些反对成立。\n\nJudge: 留出法自检——9 月流失预测在未见月份上的命中率，猜对不算、方法对才过；red team 的反对由第三方会话裁；你本人的业务判断只在你补齐账户级数据后才算一票。\n\nNeeds: ①账户级流失表（account_id、注册日、套餐、MRR、取消日、取消理由）②9 月前后工单原文 ③Q1/Q2 基线与客户基数 ④试用期改动前后的注册 cohort。**四项全缺**，现有只有 3 行月度汇总。\n\nDeclined: 待你表态（三条：抬到\"VP 要拍的三个板\"、降到 cohort/账户级、把 crew 与 red team 拉进来）。\n\n## Task\n\nPurpose: [ ] 未答——周四这个会要做的决定是什么？（动作\"分析流失\"不是目的）\nContext: [ ] 未答——我能查到的是模板、时间点和两条线索；需要你说的是：客户是谁、客单多大、Q3 有没有别的事（涨价/改版/销售换人/大客户到期）。\nMaterials: [ ] 未答——主源应为账户级取消记录与工单原文，次源为这 3 行汇总；请给出优先级与禁用源（如\"别引用行业流失率\"）。查不到就留空，不编。\nBoundaries: [ ] 未答——什么样的输出会让你说\"不是我要的\"？（例：不许把相关性写成因果、不许出现没来源的数字、不许把\"试用期改短\"直接判成元凶）\nDone: [ ] 未答——建议先给一页结论骨架（因果主张 + 反证 + 三个待拍板选项），你点头后再展开；请确认这个 checkpoint 和交付形态。\n\n## Open\n\n- 流失\"变多\"是**数**还是**率**？基数未知，12→24 仍可能率没动。\n- 收入下滑是流失造成的，还是新增从 41 掉到 30 造成的？两者在模板里被混在同一格。\n- 季节性：没有 Q1/Q2，无法判断 Q3 是否只是旺季后的正常回落。\n- 老板要的是\"为什么\"，还是\"周四能拍什么\"？这两个答案不同。\n\nReady: no —— 五个 Task 槽位全空，三条 Requirement 移动待你表态。\n"}

RESULT: Successfully wrote to /tmp/pf-15-with_skill-xx3llmxb/local/plans/q3-churn.md

ASSISTANT: 我先把方案给你看一眼，你点头我再动手。关键一点：**这个目录里只有 3 行月度数据，回答"为什么"只能编故事，给不了归因。**

📄 计划写在 `local/plans/q3-churn.md`

## 我查到的（已核，不用你答）
- `data/q3-metrics.csv`：流失 **12 → 19 → 24**，新增 **41 → 35 → 30**，NPS **38 → 31 → 27**，收入 **182k → 176k → 171k**
- 缺客户基数、缺账户级流失清单、缺 Q1/Q2 基线 —— 所以"流失变多"连是**数**还是**率**都还不确定
- `notes/worklog.md` 的两条线索是**可证伪的假设**，不是结论：试用期 8 月中改短只影响之后注册的 cohort；9/8 的投诉是在流失**之后**才被看见的
- `template.md` 是 3 个占位符的 QBR 模板，老板周四给 VP 看 —— 所以你真正要交的，大概率不是"流失分析"，是**VP 周四能拍板的东西**

## 三个可以往上抬的台阶（你选）
1. **抬高度**：不做流失分析，做"VP 要拍的三件事"——试用期改回 14 天？上线 7 天后干预？挽留存量风险账户？各给赞成/反对与代价
2. **加深度**：不用月度汇总，用 cohort 留存三角 + 按试用长度分层 + 工单文本分类。并做一个否证测试：若 8、9 月流失的大多是 7 月前注册的账户，那"试用期改短"就不是主因
3. **换阵容**：分析师 + 客服运营（真实取消理由）+ 定价负责人；red team 找做空研究员专攻季节性、获客结构、"率没动只是数变大"的分母效应

## 需要你回答的五个问题（只有你有答案）
- **目的**：周四这个会要做的**决定**是什么？（"分析流失"是动作，不是目的）
- **背景**：客户是谁、客单多大、Q3 除试用期外还有别的事吗（涨价/改版/销售换人/大客户到期）？
- **材料**：能不能拿到**账户级取消记录（含取消理由）**和 9 月工单原文？拿不到就留空、我不编；要禁用的源请点名
- **边界**：什么输出会让你说"不是我要的"？（比如：不许把相关性写成因果、不许出现无来源数字）
- **完成**：先给一页结论骨架（因果主张 + 反证 + 三个待拍板选项），你点头再展开 —— 这个 checkpoint 行吗？

补上账户级数据 + 上面五条，我就能给出带反证的分层归因；只有这 3 行，我最多给你"三种解释 + 各自需要什么数据才能判定"。你答完（或直接说"就按第 1 条抬高度做"），我把 Ready 改成 yes，然后可用 `/define-goal` 以这份计划为源开工。