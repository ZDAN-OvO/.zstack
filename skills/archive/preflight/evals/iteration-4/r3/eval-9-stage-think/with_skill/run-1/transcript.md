TOOL bash: {"command": "pwd; ls -la; git rev-parse --show-toplevel 2>/dev/null"}

TOOL bash: {"command": "ls -la /home/zdan/.zstack/skills/plan/preflight/references/ 2>/dev/null"}

RESULT: /tmp/pf-9-with_skill-51nt9_cx
total 172
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 65 root root 167936 11月 10 22:44 ..
-rw-rw-r--  1 zdan zdan      0 11月 10 16:17 .keep


Command exited with code 128

RESULT: total 24
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:13 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 21:54 ..
-rw-rw-r-- 1 zdan zdan 6608 11月 10 16:13 ambition.md
-rw-rw-r-- 1 zdan zdan 5855 11月 10 16:13 task-definition.md


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


TOOL write: {"path": "/tmp/pf-9-with_skill-51nt9_cx/local/plans/ai-coding-essay.md", "content": "# Plan: 一篇有立场的 AI 编程文章\n\n- Asked: 我想写一篇讲 AI 编程的文章，但还没想好要说什么\n- Stage: think\n- Date: 2026-11-10\n\n## Requirement\nHand over: 候选 rung 2 —— 文章让读者用自己仓库里的数据检验一个具体主张，并给出反证方法\n\n- Rung 1（原样）: 写一篇讲 AI 编程的文章\n- Rung 2: 一个可证伪的主张 + 读者能自己跑的检验\n- Rung 3: 改变读者下周的工作方式（超出写作能单独承担的天花板）\n\nFallback: rung 1\n\nDepth: 原始材料 = 你自己的 git 历史、AI 会话记录，或一次对照实验（同一任务有/无 AI）; 工具 = 提交/revert/缺陷数据、session log、评测脚本; 拉伸目标 = 给一个能预测未见数据的主张（例：\"AI 参与的提交 revert 率更高，且能用 X 提前识别\"）\n\nRange: 动词 = 让人怀疑一个信念、给出判断标准、给出可执行步骤; 班底 = 一线工程师（原始日志）、编辑（结构）、科学记者（可证伪与出处）、红队 = 见过 AI 代码评审翻车的资深工程师 + 专找无出处数字的做空者\n\nJudge: 以你自己的判断为主（这是你的领域）; 另加 2 个只负责证伪的攻击会话 + 1 个裁定会话; 文中每个数字须有一手出处\n\nNeeds: 仓库/会话记录访问权、发布渠道。缺: 发布平台与读者、你自己的那个主张\n\nDeclined: —\n\n## Task\nPurpose:\nContext:\nMaterials:\nBoundaries:\nDone:\n\n## Open\n- Purpose 空: 文章要落到谁的哪个决定上（读者读完会做什么不同的事）\n- Depth 的挑战对象未定: 你自己关于 AI 编程的直觉是哪一条\n- Done 的形状未定: 发布位置、篇幅、有没有\"先给大纲\"的检查点\n- 这是 Think 阶段的问题，答案只有你有；不替你猜\n\nReady: no —— Requirement 三轴未裁定，Task 五槽全空\n"}

RESULT: Successfully wrote to /tmp/pf-9-with_skill-51nt9_cx/local/plans/ai-coding-essay.md

ASSISTANT: 看了工作区：空的（只有一个 `.keep`），没有已有素材，所以素材得从你身上来。

**阶段：think。** “还没想好要说什么”不是缺措辞，是缺主张。现在直接开写，只会得到谁都写得出的那篇综述。所以先不产出文章，先把“说什么”定下来。

### Requirement（三条，各自接受 / 改写 / 拒绝）

**Altitude** — 原样落地是 rung 1（写成一篇讲 AI 编程的文章）。我建议爬到 rung 2：**一个可证伪的主张 + 读者能自己跑一遍的检验**。rung 3（改变读者下周一的工作方式）超出写作能单独承担的，标为天花板，不推荐。接受的话 rung 1 留作 fallback。

**Depth** — 你没要求、但专家会做的那一步：不综述“AI 编程”，而是用最原始的材料——你的 git 历史、AI 会话记录，或者一次对照实验（同一任务有/无 AI），去检验你自己心里那条直觉。拉伸目标：给一个能预测**未见数据**的主张，比如“AI 参与的提交 revert 率更高，且能用某个信号提前识别”。

**Range** — “一篇文章”其实是三个动词：让人怀疑一个信念、给出判断标准、给出可执行步骤。对应班底：一线工程师（出原始日志）、编辑（结构）、科学记者（可证伪与出处）、红队（见过 AI 评审翻车的资深工程师 + 专找无出处数字的做空者）。用他们**做事**，不是用他们的口吻写作。

**Judge** — 这是你的领域，你自己的判断算数。再加两个只负责证伪的会话和一个裁定会话，兜住自评的盲点；数字一律要一手出处。

### Task（五个槽，只有你能填）

1. **Purpose** — 写完给谁、帮他们做哪个决定？（“分析 AI 编程现状”是动作，不是目的）
2. **Context** — 一个聪明的陌生人要事先知道什么，才不会瞄错方向？你的读者以为自己已经知道什么？
3. **Materials** — 可用的原始材料排序（你的提交记录？会话日志？别人的实测？），明确禁用的（比如二手转述的“AI 让效率提升 10 倍”新闻），以及“找不到就留空”的槽位。
4. **Boundaries** — 出现什么你会说“不是我要的”？（例：不写工具横评、不预言取代、不出现无出处数字）
5. **Done** — 什么出现在你面前就算停？建议含一个早期检查点：先给主张 + 大纲，再写全文。

计划已写到 `/tmp/pf-9-with_skill-51nt9_cx/local/plans/ai-coding-essay.md`，`Ready: no`。

最省力的一步：先只回答第 1 条——**你自己关于 AI 编程最想说、也最容易被人反驳的那句话是什么**。有这一句，其余四个槽就能顺着定。你确认 Ready 之后，可以用 `/define-goal` 以这份计划为源继续。