TOOL bash: {"command": "pwd; ls -la; git rev-parse --show-toplevel 2>/dev/null"}

TOOL ls: {"path": "/home/zdan/.zstack/skills/plan/preflight"}

RESULT: /tmp/pf-20-with_skill-36h90b4m
total 172
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 64 root root 167936 11月 10 22:36 ..
-rw-rw-r--  1 zdan zdan      0 11月 10 16:17 .keep


Command exited with code 128

RESULT: evals/
references/
SKILL.md

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


TOOL bash: {"command": "ls -R /home/zdan/.zstack/skills/plan/preflight/evals | head -50"}

RESULT: /home/zdan/.zstack/skills/plan/preflight/evals:
eval-fixtures
evals.json
iteration-1
iteration-2
iteration-3-repeat
iteration-4
README.md
scripts

/home/zdan/.zstack/skills/plan/preflight/evals/eval-fixtures:
empty
existing-plan
homepage
qbr
qbr-rejected
rejected
webapp

/home/zdan/.zstack/skills/plan/preflight/evals/eval-fixtures/empty:

/home/zdan/.zstack/skills/plan/preflight/evals/eval-fixtures/existing-plan:
emails
local

/home/zdan/.zstack/skills/plan/preflight/evals/eval-fixtures/existing-plan/emails:
welcome.md

/home/zdan/.zstack/skills/plan/preflight/evals/eval-fixtures/existing-plan/local:
plans

/home/zdan/.zstack/skills/plan/preflight/evals/eval-fixtures/existing-plan/local/plans:
onboarding-email.md

/home/zdan/.zstack/skills/plan/preflight/evals/eval-fixtures/homepage:
analytics
index.html
support

/home/zdan/.zstack/skills/plan/preflight/evals/eval-fixtures/homepage/analytics:
weekly.csv

/home/zdan/.zstack/skills/plan/preflight/evals/eval-fixtures/homepage/support:
chats-sample.md

/home/zdan/.zstack/skills/plan/preflight/evals/eval-fixtures/qbr:
data
notes
template.md



TOOL bash: {"command": "date +%F"}

RESULT: 2026-11-10


TOOL write: {"path": "/tmp/pf-20-with_skill-36h90b4m/local/plans/competitor-analysis.md", "content": "# Plan: 竞品分析，落在一个要做的决定上\n\n- Asked: 帮我做个竞品分析\n- Stage: think（请求像 execute，意图还停在 think；先问清再动手）\n- Date: 2026-11-10\n\n## Requirement\n\n**建议的做法（每一条你都可以采纳 / 改写 / 否掉）**\n\n- Hand over: rung 3 —— 这次分析要改变哪三个决定（定价、路线图、目标客户），每个决定给出正反两面的理由和一条建议。而不是一张功能对比表。\n- Fallback: rung 2 —— 讲清每个对手靠什么赢下它赢的客户，我们在哪一处定位是漏的。\n- Ladder（往上爬）：① 填对比表 → ② 解释对手为什么赢 → ③ 三个该变的决定 → ④ 常驻的竞争情报回路：持续抓对手的定价页 diff、changelog、招聘岗位、评论语料，产出一个能提前预判对手下一步动作的信号，并用过去 12 个月的历史回测它能不能提前发现。「去赢下这个市场」在模型今天的能力之上，所以 ④ 就是天花板下的那一级。\n- Depth: 不从对手的营销页开始，从最原始的材料开始 —— 定价页的历史快照（Wayback）、changelog 提交节奏、招聘 JD 里暴露的技术栈和方向、G2/Capterra/应用商店里你自家客户的抱怨、win/loss 记录。仪器不是表格，是定价与功能的**时间序列**加一层对评论语料的分类统计。拉伸目标：预测某对手下一季度会发什么，并接受事后打分。测一个你持有的信念：「我们的差异点是 X」—— 拿评论原文去验客户到底有没有提过 X。\n- Range: 交付物的名词换成动词 —— 不是「一份报告」，是**让一个忙人在 30 分钟里相信一条因果故事并下注**。为此组队：定价分析师（从公开价格史反推档位结构和付费意愿）、采访型记者（把客户原话从评论和 win/loss 里挖出来）、短线做空者（专找能推翻结论的那个数字）、编辑（压成一页能进会的纸）。\n- Judge: 报告里的每个数字都要有可点开的一手来源，这一条单个会话就能核；再用两个只负责攻击的会话分别挑「方法错在哪」和「数字错在哪」，第三个会话裁定哪些反对成立。方法分和结果分分开打 —— 猜对了但来源不可靠，算不过。\n- Needs: 你自己的收入/流失数据、win/loss 记录、客服工单、对手名单、以及一台能联网抓页面的机器。**目前全部缺**：当前目录是空的（只有一个 `.keep`），所以「从自家数据反推」这一层现在做不了，只能先做公开信息那一半。\n- Declined: 暂无（等你裁决）\n\n## Task\n\n五问，只有你能答：\n\n- Purpose: 这份分析支撑哪个决定？做完之后你会因此改什么？（「分析五个竞品」是动作，不是目的）\n- Context: 一个能干的外人接手前必须知道什么？—— 你们做什么、收入量级、客户是谁、最近一次定价或定位为什么没打响。\n- Materials: 一手（对手官网、产品文档、定价页、changelog）优先于二手；要禁掉的来源请点名；查不到的**留空，不要编**。\n- Boundaries: 什么样的输出会让你说「这不是我要的」？（例：不许出现编造的 ARR/用户数/增速；不许只给形容词不给权衡）\n- Done: 什么东西出现在你面前就算停？建议第一道检查点：**先只要大纲** —— 关键差异、建议的定位、理由，三条以内，你点头之后再写全文。\n\n## Open\n\n- 目的未定：现在无法判断该深挖 3 个重叠对手，还是扫 5 个。按经验，3 个挖深胜过 5 个扫过。\n- 自家数据不在手上：没有收入、流失、win/loss，就只能做外部视角，结论会弱一档 —— 你能补哪几样？\n- 「竞品」指谁还没定：是同价位直接对手，还是客户预算的实际另一个去处（含「什么都不做」）？\n\nReady: no —— 五问一个都还没答，三个 rung 也没裁决。你回一句「按 rung 3，边界是 X，先给大纲」，我就能开工。\n"}

RESULT: Successfully wrote to /tmp/pf-20-with_skill-36h90b4m/local/plans/competitor-analysis.md

ASSISTANT: 写好了：`/tmp/pf-20-with_skill-36h90b4m/local/plans/competitor-analysis.md`

先说我看出来的两件事：

1. **请求的层级放错了。** 「做个竞品分析」听起来是执行，但背后没有决定 —— 所以照做只会得到一张谁都写得出的对比表。计划里把它往上抬了三级，推荐交一份「这次分析要改哪三个决定」，再上一级是能持续跑、能回测的竞争情报回路（那是今天模型能力的天花板）。
2. **目录是空的。** 只有一个 `.keep`，没有收入、流失、win/loss、客户反馈。所以「从自家数据反推」这一层现在做不了，硬做就只能靠公开页面，结论会弱一档 —— 这条我写进了 Open，没有替你猜。

计划分两半：Requirement 里三条建议（往上抬到哪个层级、从什么原始材料入手、谁来组队）每条你都能采纳或否掉；Task 里五个问题只有你能答，我一个都没填。

现在缺的是你的一句话，比如：**「按 rung 3，不许编数字，先给大纲」**。给了我就动手；想先改计划也行，直接说改哪条。

确认 Ready 之后，可以接着 `/define-goal`，把这份计划当输入。