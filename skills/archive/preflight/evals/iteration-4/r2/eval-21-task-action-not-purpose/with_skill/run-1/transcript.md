TOOL bash: {"command": "cd /tmp/pf-21-with_skill-iznu6uy6 && ls -la && echo \"--- git ---\" && git rev-parse --show-toplevel 2>/dev/null; echo \"--- tree ---\" && find . -maxdepth 3 -not -path '*/.git/*' | head -60"}

TOOL bash: {"command": "ls /home/zdan/.zstack/skills/plan/preflight/references/ && wc -l /home/zdan/.zstack/skills/plan/preflight/references/*.md"}

RESULT: total 172
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 64 root root 167936 11月 10 22:36 ..
-rw-rw-r--  1 zdan zdan      0 11月 10 16:17 .keep
--- git ---
--- tree ---
.
./.keep


RESULT: ambition.md
task-definition.md
   61 /home/zdan/.zstack/skills/plan/preflight/references/ambition.md
   66 /home/zdan/.zstack/skills/plan/preflight/references/task-definition.md
  127 total


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


TOOL bash: {"command": "date +%F && echo \"---\" && ls /tmp/pf-21-with_skill-iznu6uy6/local 2>/dev/null; echo \"no local dir\""}

RESULT: 2026-11-10
---
no local dir


TOOL write: {"path": "/tmp/pf-21-with_skill-iznu6uy6/local/plans/competitor-analysis-5.md", "content": "# Plan: 五家竞品的功能、定价与优缺点\n\n- Asked: 「帮我分析 5 家竞品的功能、定价和优缺点」\n- Stage: think（先把意图问实，填满即转 execute）\n- Date: 2026-11-10\n\n## Requirement\n\nHand over: 决策档 —— 下一季度的产品/定价取舍：差异定位图 + 一个推荐 + 反方论证 + 改判触发条件\nFallback: 现状档 —— 五家的能力矩阵、定价结构、优缺点对照（只给事实与差异，不给建议）\nDepth: 拿原始材料，不读营销页——定价页的 Wayback 快照（看 SKU 与计费单位怎么演化）、G2/知乎/应用商店的真实吐槽、赢单输单记录；把「价格数字」换成「计费单位与毛利结构」。拉伸目标：用这些材料重建每家过去 12 个月的功能/定价变更时间线，让未参与的人仅凭时间线预测对手下一步动作，命中 ≥2/3。\nRange: 不是「一份报告」，而是让人在不确定中取舍、让销售在客户面前说清差别、让下一次调价不再重蹈上次。crew：产品分析师（能力边界）、定价分析师（SKU / 计量单位）、买方研究员（采购路径、赢单输单）、记者（一手来源核对）；红队：做空者 + 对手的销售（逐条攻击结论）。\nRange 附带建议: 范围收窄为 3 家重叠对手做深 + 2 家只做价格与定位快照（五家平铺会得到五份雷同结论，判断不了任何取舍）\nJudge: 每个数字必须挂一手来源链接，缺源即删；再由攻击会话与裁决会话过一轮。你若能自己判断好坏，你的判定就够。\nNeeds: 自家产品与客群（缺，阻断项）；五家名单（缺，由你给，不由模型猜）；定价页历史与评论数据（可采）；赢单输单材料（缺）\nDeclined: —\n\n## Task\n\nPurpose: 待答 —— 这份输出之后要拍哪个决定？（例：主打「更易用」还是「更便宜」、「要不要跟用量计费」）\nContext: 待答 —— 自家产品、客群规模、价格带、上一轮调价的后果\nMaterials: 待答 —— 五家的一手站点与文档、定价页历史、你手上的评论/输单记录；二手评测文章一律不用；查不到就留空，不许编\nBoundaries: 待答 —— 哪些输出你会说「不是我要的」？（例：编造的 ARR/用户量、只堆形容词不给取舍、动自家定价区间）\nDone: 待答 —— 停下来的标志与形状：先给一份框架（差异在哪、空位在哪、推荐与理由），你点头后再出全文；Markdown，每节 3–4 条\n\n## Open\n\n- 自家是谁、和谁抢同一批客户——这个不定，五家名单与「优缺点」都没有参照系\n- 「竞品」的边界：同客群？同价格带？还是同品类\n- 五家平铺还是三家做深（Range 附带建议尚未裁定）\n\nReady: no —— Requirement 各档与 Task 五栏均待你裁定或作答\n"}

RESULT: Successfully wrote to /tmp/pf-21-with_skill-iznu6uy6/local/plans/competitor-analysis-5.md

ASSISTANT: **Look**：`/tmp/pf-21-with_skill-iznu6uy6` 是空目录，无 git、无 README、无产品线索。也就是说「竞品」没有参照系——优缺点相对谁而言，缺这个答案，五家表只能写成五份雷同的评测摘要。

**Plan** 已写到 `local/plans/competitor-analysis-5.md`（Stage: think）。

要点：

- **Requirement** 提了三档：决策档（下一季产品/定价取舍 + 改判触发条件）／Fallback 现状档（纯对照表）；Depth 换掉营销页，用定价页 Wayback 快照、评论区吐槽、赢单输单记录，并给一个拉伸目标（重建 12 个月变更时间线，预测对手下一步命中 ≥2/3）；Range 附一条范围建议：3 家做深 + 2 家只做快照。
- **Judge**：每个数字挂一手来源，缺源即删；再开攻击会话与裁决会话。
- **Task** 五栏全是待答，我没有替你填。

需要你回四件事：

1. 自家产品与客群、价格带（以及上次调价的后果）
2. 五家名单，或同意「3 深 + 2 浅」
3. 这份东西之后要拍哪个决定
4. 「不是我要的」长什么样，和停下来的标志

回完我把 Ready 改成 yes。确认后可以用 `/define-goal`，以这份 plan 为输入。