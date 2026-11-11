TOOL bash: {"command": "pwd; ls -la; git rev-parse --show-toplevel 2>/dev/null || echo \"no git root\""}

TOOL ls: {"path": "/tmp/pf-9-with_skill-hoqaraf_"}

RESULT: /tmp/pf-9-with_skill-hoqaraf_
total 172
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 64 root root 167936 11月 10 22:35 ..
-rw-rw-r--  1 zdan zdan      0 11月 10 16:17 .keep
no git root


RESULT: .keep

TOOL bash: {"command": "cd /home/zdan/.zstack/skills/plan/preflight && wc -l references/*.md SKILL.md"}

TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/references/task-definition.md"}

RESULT:    61 references/ambition.md
   66 references/task-definition.md
  103 SKILL.md
  230 total


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


TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/references/ambition.md"}

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


TOOL bash: {"command": "date +%F"}

RESULT: 2026-11-10


TOOL write: {"path": "/tmp/pf-9-with_skill-hoqaraf_/local/plans/ai-coding-article.md", "content": "# Plan: 一篇关于 AI 编程的文章，先定主题\n\n- Asked: 「我想写一篇讲 AI 编程的文章，但还没想好要说什么」\n- Stage: think（还不到写作：现在缺的是论点，不是文笔）\n- Date: 2026-11-10\n\n## Requirement\n> 以下每条都待你 接受 / 改写 / 拒绝；拒绝请给理由，我记进 Declined。\n\nHand over: **待裁决** — 建议停在「一个聪明且有经验的读者可能不同意的那个立场，并且由你自己的原始材料撑住」。再往上（「让某位具体读者下周改掉一个做法」）在今天的模型里验不了，也超出创作类工作适合的高度，所以建议它就是天花板。\nFallback: 交付一篇有明确立场的文章骨架＋证据表（没有立场就退回这里）。\nDepth: **待裁决** — 不从观点出发，从你自己的记录出发：某个仓库的 `git log`（提交粒度分布、回滚率、首次可运行提交的时间）、你实际的 prompt/对话记录。仪器是这些日志和一份最朴素的统计，不是「我觉得」。拉伸目标：把你已有的一个信念放上秤——比如「AI 让写代码变快，瓶颈挪到了 review」——用提交数据试着证伪它；或在数据里找一个你没想到的早期信号。\nRange: **待裁决** — 名词拆成动词：这篇文章要做到 (a) 让一个怀疑 AI 编程的人 adopt 或明确放弃某一个具体做法；(b) 给读者一个他感觉到但叫不出名字的东西；(c) 扛住一线工程师一句「不是这么回事」。班组：每天用 AI 出货的实践者（判断哪些细节是真疼）、编辑（这篇到底是什么、砍掉 40%）、工具史的人（IDE / 调试器 / Stack Overflow 当年的争论怎么落地）。红队：一个认为 AI 编程是泡沫的强工程师，加一个「数字警察」——任何没有一手来源的数字都打回。\nJudge: **待裁决** — 红队两个会话负责证伪（泡沫派攻击论点，数字警察攻击每个数字和引用的出处），再一个会话裁定哪些反对成立，回给作者，作者可以拒绝但要写理由。评判的是方法而不只是结论：猜对但没证据也算失败，方法对但差半步算通过。你自己读一遍也算一票。\nNeeds: 你的仓库历史和 prompt 记录（**缺**，且要不要交出来由你定）；读者是谁、发在哪（**缺**）；你目前对 AI 编程到底站哪边（**缺**）。\nDeclined: —\n\n## Task\nPurpose:\nContext:\nMaterials:\nBoundaries:\nDone:\n\n## Open\n- **论点本身**：这是当前唯一的缺口。五个槽位填不上，是因为它们都在等这一句。可以先用下面的候选缩小：你想说的是「AI 让编程这件事的性质变了」，还是「AI 让某些人误以为自己会编程了」，还是「我这半年用 AI 干活，实际发生的事和预期不一样」？\n- **读者**：写给怀疑的人、已经在用的人、还是不做技术的决策者？三者的文章完全不是一篇。\n- **材料**：愿不愿意把自己真实的提交记录 / prompt 记录当一手材料？愿意 → 上面 Depth 那条成立；不愿意 → 只能退回二手材料，文章的强度会掉一档。\n- **走向**：这篇文章要到哪去——自己发、某个平台、还是给团队看？\n\nReady: no — 论点未定，五个槽位全空，Requirement 三条待你裁决。\n"}

RESULT: Successfully wrote to /tmp/pf-9-with_skill-hoqaraf_/local/plans/ai-coding-article.md

ASSISTANT: 已写入 `local/plans/ai-coding-article.md`。

先说我看到的事实：工作区是空的（只有 `.keep`），没有任何草稿、笔记或历史可读。所以这次没有可查的东西——缺口全在意图上，而意图只有你能填。

**阶段：think。** 现在要写的不是那篇文章，是"这篇文章到底在说什么"这一句。这个阶段直接开写，出来的就是谁都能写的那一版：有覆盖，没立场。

我在计划里替你起了三个可裁决的提案（Altitude / Depth / Range，各配一个会话外的裁判），都标了「待裁决」，你可以接受、改写或拒绝。真正卡住的是下面这一句，回它比回别的都值：

> 你想说的更接近哪一个——
> 1. AI 让"编程"这件事的性质变了；
> 2. AI 让一部分人误以为自己会编程了；
> 3. 我这半年用 AI 干活，实际发生的事和预期不一样。

还有两个会决定文章形态的问题：**写给谁**（怀疑的人 / 已在用的人 / 不做技术的决策者，三者不是同一篇），以及**愿不愿意拿自己真实的 git log 和 prompt 记录当一手材料**（愿意，Depth 那条就成立；不愿意，就只能靠二手材料，强度掉一档）。

`Ready: no`。你回完这几条，我把槽位填实，再交给你确认 Ready 行。

确认后可以直接接 `/define-goal`，以这份计划为输入。