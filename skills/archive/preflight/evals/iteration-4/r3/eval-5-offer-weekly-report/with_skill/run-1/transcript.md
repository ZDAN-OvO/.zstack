TOOL bash: {"command": "pwd; ls -la; echo \"---GIT---\"; git log --oneline -20 2>/dev/null | head -30; echo \"---ROOT---\"; git rev-parse --show-toplevel 2>/dev/null"}

TOOL bash: {"command": "ls -la /home/zdan/.zstack/skills/plan/preflight/references/ 2>/dev/null"}

RESULT: /tmp/pf-5-with_skill-df5ci4xp
total 172
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 65 root root 167936 11月 10 22:44 ..
-rw-rw-r--  1 zdan zdan      0 11月 10 16:17 .keep
---GIT---
---ROOT---


Command exited with code 128

RESULT: total 24
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:13 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 21:54 ..
-rw-rw-r-- 1 zdan zdan 6608 11月 10 16:13 ambition.md
-rw-rw-r-- 1 zdan zdan 5855 11月 10 16:13 task-definition.md


TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/references/task-definition.md"}

TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/references/ambition.md"}

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


TOOL bash: {"command": "cd ~ && ls -la 2>/dev/null | head -40; echo \"---candidates---\"; find ~ -maxdepth 3 \\( -iname \"*周报*\" -o -iname \"*weekly*\" -o -iname \"*report*\" \\) -not -path \"*/node_modules/*\" -not -path \"*/.git/*\" 2>/dev/null | head -20"}

RESULT: total 4164
drwxr-x--- 109 zdan zdan    4096 11月 10 20:21 .
drwxr-xr-x   3 root root    4096  9月  5 22:42 ..
drwxrwxr-x   3 zdan zdan    4096 10月 22 09:43 .agent
drwx------   3 zdan zdan    4096 10月 20 16:21 .agent-browser
drwxrwxr-x   3 zdan zdan    4096  9月 30 20:13 .agent-plugins.worktrees
drwxr-x---   2 zdan zdan    4096 10月 20 16:21 .android
drwx------   4 zdan zdan    4096 11月 10 19:49 .answer-me-with-html
drwx------   5 zdan zdan    4096 10月 28 14:24 .ao
drwxrwxr-x   3 zdan zdan    4096 10月  2 00:22 backups
-rw-------   1 zdan zdan   31829 11月 10 18:20 .bash_history
-rw-r--r--   1 zdan zdan     220  9月  5 22:42 .bash_logout
-rw-r--r--   1 zdan zdan    5178 10月 28 23:50 .bashrc
drwxrwxr-x   2 zdan zdan    4096 11月  8 18:00 bin
-rw-rw-rw-   1 zdan zdan  154273 10月 26 21:04 Boris Cherny's CLAUDE.md.jpg
drwxr-xr-x   4 zdan zdan    4096 10月  9 10:05 .bun
drwxrwxr-x  57 zdan zdan    4096 11月 10 20:26 .cache
drwxrwxr-x   4 zdan zdan    4096 10月  8 09:01 .cargo
drwx------   3 zdan zdan    4096  9月 10 14:30 .cc-safety-net
drwxrwxr-x   5 zdan zdan    4096 10月 26 16:11 .cc-switch
drwxrwxr-x   8 zdan zdan    4096  9月 24 11:04 chat_space
drwxrwxr-x   6 zdan zdan    4096 10月  3 16:35 .clamtk
drwxrwxr-x  28 zdan zdan    4096 11月 10 16:36 .claude
-rw-------   1 zdan zdan   93642 11月 10 20:21 .claude.json
-rw-------   1 zdan zdan   91060 11月  6 18:25 .claude.json.backup
-rw-------   1 zdan zdan    6581  9月 12 21:18 .claude.json.backup.1789219107914
-rw-------   1 zdan zdan    6619  9月 12 21:18 .claude.json.backup.1789219107918
-rw-------   1 zdan zdan    6665  9月 12 21:18 .claude.json.backup.1789219118031
-rw-------   1 zdan zdan    7252  9月 12 21:18 .claude.json.backup.1789219120098
-rw-------   1 zdan zdan    7280  9月 12 21:18 .claude.json.backup.1789219120100
drwxrwxr-x   9 zdan zdan    4096 10月 29 11:56 .codebuddy
drwxrwxr-x   3 zdan zdan    4096  9月 11 16:15 CodeBuddy
drwxrwxr-x   3 zdan zdan    4096  9月 10 09:30 .codebuddycn
drwxrwxr-x   3 zdan zdan    4096  9月  7 10:25 codeup
drwxr-xr-x 108 zdan zdan    4096 11月 10 19:43 .config
drwxrwxr-x   3 zdan zdan    4096 11月  6 14:42 .continue
drwx------   7 zdan zdan    4096 11月  6 14:41 .copilot
drwxrwxr-x   2 zdan zdan    4096 11月  4 16:33 .cursor
drwx------   8 zdan zdan    4096 10月 20 12:10 .cursor-byok-v3
drwxr-xr-x   3 zdan zdan    4096 10月  9 15:37 data
---candidates---
/home/zdan/.npm/_logs/2026-09-26T12_39_51_484Z-eresolve-report.txt
/home/zdan/.npm/_logs/2026-09-26T12_43_04_350Z-eresolve-report.txt
/home/zdan/.npm/_logs/2026-09-26T12_56_45_565Z-eresolve-report.txt
/home/zdan/.npm/_logs/2026-09-26T02_23_04_718Z-eresolve-report.txt
/home/zdan/.npm/_logs/2026-09-26T03_09_50_997Z-eresolve-report.txt
/home/zdan/.npm/_logs/2026-09-26T03_24_13_665Z-eresolve-report.txt
/home/zdan/.npm/_logs/2026-09-26T03_16_40_486Z-eresolve-report.txt
/home/zdan/.npm/_logs/2026-10-18T04_11_09_630Z-eresolve-report.txt
/home/zdan/.npm/_logs/2026-09-26T12_52_48_971Z-eresolve-report.txt
/home/zdan/.npm/_logs/2026-09-26T03_20_19_728Z-eresolve-report.txt
/home/zdan/.npm/_logs/2026-09-26T02_41_08_582Z-eresolve-report.txt
/home/zdan/.npm/_logs/2026-10-02T15_46_57_234Z-eresolve-report.txt
/home/zdan/.npm/_logs/2026-09-26T03_44_45_756Z-eresolve-report.txt
/home/zdan/.npm/_logs/2026-09-26T04_03_35_081Z-eresolve-report.txt
/home/zdan/.npm/_logs/2026-09-26T04_21_25_339Z-eresolve-report.txt
/home/zdan/.npm/_logs/2026-09-26T04_41_15_748Z-eresolve-report.txt
/home/zdan/.npm/_logs/2026-10-02T15_43_19_302Z-eresolve-report.txt
/home/zdan/.npm/_logs/2026-09-26T13_17_27_557Z-eresolve-report.txt
/home/zdan/.npm/_logs/2026-09-24T06_26_10_688Z-eresolve-report.txt
/home/zdan/.npm/_logs/2026-09-26T12_49_48_496Z-eresolve-report.txt


TOOL bash: {"command": "cd /tmp/pf-5-with_skill-df5ci4xp && date +%F && mkdir -p local/plans && ls local/plans"}

RESULT: 2026-11-10


TOOL write: {"path": "/tmp/pf-5-with_skill-df5ci4xp/local/plans/weekly-report.md", "content": "# Plan: 本周周报，交到主管手上能推动一个决定\n\n- Asked: 帮我写本周周报，下午要交给主管\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\n\nHand over: 第 3 级——周报结尾是「需要主管本周拍板/给资源的 3 件事」，每件带取舍（做与不做各付什么代价）。周报从\"我干了什么\"变成\"他要决定什么\"。\nFallback: 第 2 级——写清本周的变化、原因、卡点，不做推荐。\nDepth: 原始材料是本周的 commit / PR / 工单 / 会议记录，不是对本周的记忆；每句话挂一个能点开的凭据（PR 号、工单号、文档链接）。专家不会写进去的东西：不可验证的进度（\"完成度 80%\"）。Stretch target: 主管 60 秒内能逐条核验每个数字——查不到凭据的那句直接删。\nRange: 动词是 ①让主管 3 分钟内知道哪里会出问题 ②把\"我做了什么\"转成\"这值多少\" ③别制造新的疑问。班底：分析师（找凭据）、编辑（砍到一屏）、记者（最重要的放第一句）、红队（扮演没耐心的主管，逐条问\"所以呢 / 数字动了吗 / 为什么晚了\"）。\nJudge: 先跑红队——一个会话只负责扮演主管挑刺，另一个会话裁定哪些质疑站得住；站得住的重写，站不住的补一句预防。主管本人的反应是终审。\nNeeds: 本周原始材料（PR / commit / 工单导出 / 日历）、上周周报、团队模板、主管当前最在意的事。**全部缺失**：工作目录内无 git 仓库、无任何文件。\nDeclined: 第 4 级（用常设的风险/决策台账替掉周报，并用历史数据证明它更早发现问题）——今天下午交不出，需要数周历史和主管配合，留待下季度。\n\n## Task\n\nPurpose: （待填——这份周报之后，主管要做的是哪一个决定）\nContext: （待填）\nMaterials: 事实：工作区 `/tmp/pf-5-with_skill-df5ci4xp` 为空，无 git，无可参考文件（待你确认）。待填：本周 PR/工单、上周周报、团队模板。找不到的留空，不编。\nBoundaries: （待填——什么样的周报你会说\"不是我要的\"）\nDone: 先给 5 行提纲（本周最重要的 3 件事 + 3 个待决定项 + 1 个风险），点头后再写全文；markdown、一屏、每节 2–3 条。\n\n## Open\n\n- 这周你实际做了什么——唯一的信息源是你\n- 主管读周报是为了什么：追进度 / 分资源 / 评绩效？这决定落在第 2 级还是第 3 级\n- 有没有上周周报，用来对齐格式和口径\n\nReady: no——五问全空，且上面三条建议你还没表态\n"}

RESULT: Successfully wrote to /tmp/pf-5-with_skill-df5ci4xp/local/plans/weekly-report.md

ASSISTANT: 计划已写到 `local/plans/weekly-report.md`。先说 **Look 的结果**：工作目录是空的，无 git 仓库、无任何文件，也找不到上周周报或团队模板。所以这周的素材只能来自你——我不会替你编"我本周推进了 XX"。

**三条建议，各表态（接受 / 改 / 拒）：**

| 轴 | 建议 | 一句话 |
|---|---|---|
| 交付高度 | 从"把本周事项汇总"抬到"结尾给出**需要主管本周拍板的 3 件事**，各带取舍" | 周报从"我干了什么"变成"他要决定什么" |
| 深度 | 每条结论挂一个**能点开的凭据**（PR 号/工单/文档），查不到就删这句 | 顺手加个靶子：主管 60 秒能核验完每个数字 |
| 广度 | 加一轮红队：一个会话扮演没耐心的主管挑刺，另一个会话裁定哪些质疑站得住 | 下午交之前先自己挨一轮骂 |

**下面五问只有你能答**（每问一句就够）：

1. **用途**：这份周报交上去之后，主管会拿它做什么决定——放你继续、给你人/资源、还是评判你？决定了上面第一条接不接。
2. **背景**：一个不认识你项目的聪明人，需要知道什么才不至于瞄错方向？
3. **材料**：本周的 PR/commit/工单列表、上周周报、团队模板——有哪个就贴哪个。找不到的留空，别让我补。
4. **边界**：什么样的周报你会说"这不是我要的"？（例：不要写没验证的进度、不要提那个已黄的项目、不要超过一屏）
5. **完成**：先给 5 行提纲让你点头，再写全文，行不行？

下午的时间够走完"提纲 → 红队 → 定稿"。答完这五问我就把 Ready 改成 yes，然后是 `/define-goal`，拿这份计划当输入。