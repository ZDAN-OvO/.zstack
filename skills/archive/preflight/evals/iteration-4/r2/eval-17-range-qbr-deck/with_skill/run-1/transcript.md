TOOL bash: {"command": "pwd; ls -la; git rev-parse --show-toplevel 2>/dev/null; echo \"---\"; ls -la local 2>/dev/null"}

TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/references/task-definition.md"}

RESULT: /tmp/pf-17-with_skill-a7tml773
total 184
drwxrwxr-x  4 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 64 root root 167936 11月 10 22:36 ..
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 data
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 notes
-rw-rw-r--  1 zdan zdan    131 11月 10 16:17 template.md
---


Command exited with code 2

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


TOOL bash: {"command": "cd /tmp/pf-17-with_skill-a7tml773 && ls -la data notes && echo \"=== template.md ===\" && cat template.md && echo \"=== data files ===\" && for f in data/*; do echo \"--- $f ---\"; head -50 \"$f\"; done && echo \"=== notes files ===\" && for f in notes/*; do echo \"--- $f ---\"; head -50 \"$f\"; done"}

TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/references/ambition.md"}

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
=== template.md ===
# Q3 业务回顾

## 收入
本季收入：{{revenue}}

## 客户
新增：{{new}}，流失：{{churn}}

## 下季计划
{{plan}}
=== data files ===
--- data/q3-metrics.csv ---
month,revenue_usd,new_customers,churned_customers,nps
2026-07,182000,41,12,38
2026-08,176000,35,19,31
2026-09,171000,30,24,27
=== notes files ===
--- notes/worklog.md ---
# 工作日志

- 9 月 8 日起，客服工单里"太难上手"的投诉明显变多。
- 8 月中旬把免费试用从 14 天改为 7 天。
- 老板说 QBR 下周四给 VP 看。


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


TOOL bash: {"command": "date +%F; cd /tmp/pf-17-with_skill-a7tml773 && awk -F, 'NR>1{r+=$2;n+=$3;c+=$4; printf \"%s: 净增 %d, 流失/新增 %.0f%%\\n\",$1,$3-$4,100*$4/$3} END{printf \"Q3收入合计 %d, 7→9月 %+.1f%%\\n\",r,100*(171000-182000)/182000}' data/q3-metrics.csv"}

RESULT: 2026-11-10
2026-07: 净增 29, 流失/新增 29%
2026-08: 净增 16, 流失/新增 54%
2026-09: 净增 6, 流失/新增 80%
Q3收入合计 529000, 7→9月 -6.0%


TOOL write: {"path": "/tmp/pf-17-with_skill-a7tml773/local/plans/qbr-q3-deck.md", "content": "# Plan: Q3 QBR——给 VP 的决策材料\n\n- Asked: 帮我做一份 QBR 的 PPT\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\n\nHand over: 不是\"填好模板的 PPT\"，而是让 VP 在会上拍板：Q3 增长为什么停摆 + 3 个待决项（7 天试用是否恢复、onboarding 是否投人、Q4 目标怎么定），每项给支持与反对的理由。\nFallback: 只讲清\"本季发生了什么、为什么、接下来做什么\"的叙事 deck，不要求当场决策。\nDepth: 原始材料用 CSV 逐月/按 cohort 重算，不引用二手结论；工具用净增客户瀑布、流失/新增比、8 月中试用期改动的前后对比（天然实验）、工单主题计数；挑战你的信念\"流失是 onboarding 问题\"——看 9 月投诉上升是先于还是跟随新客下滑；stretch target：找出工单里\"难上手\"占比作为领先指标，用未见过的月份验证，数据不够就明说不够。\nRange: 动词 = 让 VP 相信一个因果故事、在信息不全下取舍、把钱和人放对地方。班底：分析师（拆数）、记者（找出真正的故事）、编辑（30 分钟叙事，每页一个结论）、演示设计；红队 = 空头 + 法务会计式审计，专攻\"相关不是因果\"\"三个月样本太小\"；最后一场只做裁决。\nJudge: 所有数字回原始 CSV/工单重算，每个因果句标证据等级；红队 session 攻击 + 裁决 session。VP 只能判断\"是否可决策\"，判断不了方法。\nNeeds: 工单导出（9 月\"难上手\"量级与趋势）、试用期改动的决策记录（谁批、有无 A/B）、Q4 目标与预算、客户基数/ARR 明细、PPT 工具。缺的见 Open。\nDeclined: （暂无）\n\n## Task\n\nPurpose: __待答__ —— VP 看完这 30 分钟要拍板什么？只知情，还是要在试用期 / onboarding 投入 / Q4 目标里选？\nContext: 已查事实（待你确认）：Q3 收入 529k，7→9 月 −6.0%；新增 41→35→30，流失 12→19→24（翻倍），净增 29→16→6；NPS 38→31→27；8 月中试用 14 天改 7 天；9/8 起\"太难上手\"工单增多；老板下周四给 VP 看，约一周准备。缺：客户基数、ARR、上季基数、VP 关注点。\nMaterials: 主：data/q3-metrics.csv、notes/worklog.md、template.md。补：工单导出、试用改动记录、上季 QBR。禁：臆造的行业基准/ARR/增长率。找不到的留空，不编。\nBoundaries: __待答__ —— 什么会让你说\"不是我要的\"？（候选：不许把 −6% 说成\"稳健\"；不许把试用期改动写成唯一原因；不许编数字；不超过 10 页）\nDone: __待答__ —— 建议：先交 1 页结论 + 8–10 页大纲给你点头（checkpoint），再出完整 .pptx + 讲稿备注；明天下班前出大纲。\n\n## Open\n\n- Purpose / Boundaries / Done 三项只有你能定，现在空着。\n- 试用期改动有无实验设计？没有的话因果只能写成\"时间吻合的假设\"。\n- 工单原始数据缺失，9 月投诉量目前无法量化。\n- 客户总数未知，算不出流失率，只能给\"流失/新增比\"（29%→54%→80%）。\n- template.md 只有三节：必须沿用，还是结构可改？\n\nReady: no —— 三项 Task 未答，三条 Requirement 提议待你接受/改写/拒绝。\n"}

RESULT: Successfully wrote to /tmp/pf-17-with_skill-a7tml773/local/plans/qbr-q3-deck.md

ASSISTANT: 我已看过文件，并把计划放在：`/tmp/pf-17-with_skill-a7tml773/local/plans/qbr-q3-deck.md`

**数据里已经能看出的故事**（不是"收入小跌"）：
- 收入从 182k 跌到 171k（−6%），但净增客户从 29 到 16 再到 6，几乎停了
- 流失翻倍 12→24，流失/新增比 29%→54%→80%，NPS 38→27
- 时间线：8 月中试用 14→7 天 → 9/8 起"太难上手"投诉变多 → 9 月数据最差。像因果，但只有 3 个月、且没有工单数据，现在只能算假设

**需要你拍三件事**（这三项只有你知道，我没有猜）：
1. **Purpose**：VP 看完要拍板什么？只是知情，还是要在"恢复 14 天试用 / 投 onboarding / 改 Q4 目标"里选？
2. **Boundaries**：哪些做法会让你说"不是我要的"？（比如把 −6% 说成稳健、把试用改动写成唯一原因、超过 10 页）
3. **Done**：能不能先给 1 页结论 + 8–10 页大纲，你点头后再出完整 deck？

**三档野心，请选/改/拒**：
- 交给 VP 一个决定（推荐，Fallback 是纯叙事版）
- 深度：用 cohort/瀑布/前后对比重算，红队攻击因果
- 班底：分析师 + 记者 + 编辑 + 红队，最后一轮裁决

另外缺三样原始材料：工单导出、试用改动的决策记录、客户基数（没有它只能给比值，算不出流失率）。

你回答后更新 Ready，再走 `/define-goal`，以这份计划为源。