TOOL bash: {"command": "pwd; ls -la; git rev-parse --show-toplevel 2>/dev/null || echo \"no git root\""}

TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/references/task-definition.md"}

RESULT: /tmp/pf-10-with_skill-t6ar210y
total 172
drwxrwxr-x   2 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 109 root root 167936 11月 10 18:00 ..
-rw-rw-r--   1 zdan zdan      0 11月 10 16:17 .keep
no git root


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


ASSISTANT: 这是一个 **Think** 阶段的请求（你自己说了还没定标准），不是 Decide 阶段。现在直接给你"A 还是 B"的结论，就等于替你猜了一套你没设的标准；直接给你两边的优缺点清单，就是任何人都能写的通用稿。所以先要问。

要不要我把下面几轮问答收成一页 `local/plans/db-choice.md`（含结论 + 什么条件下该反悔），你审完再定？下面是我需要你回答的、以及每个问题为什么会改变标准。

**先纠正一个前提**：真正的分岔不是"关系型 vs 文档型"。Postgres 的 `jsonb` 已经吃掉了大部分"我要存不固定的结构"的需求。所以对多数新项目，Mongo 的真实优势只剩两条：**无模式的高速写入**和**横向分片**。你项目的形状决定这两条对你是不是刚需。

**五个问题（按对答案的影响排序）**

1. **这笔钱/这个权限，能不能算错？** 有没有"多扣一次款、超卖一件货、两个人抢到同一个座位"这类不能发生的状态？→ 决定你是否真的需要事务和多表约束（这基本就钉死 Postgres）。
2. **读的模式是什么？** 主要是一堆前端页面按 id 取对象，还是要临时拼条件做报表和聚合？→ 前者两边都行，后者 Postgres 明显省事。
3. **数据的形状你有多确定？** 现在能画出表结构，还是字段每周都在变、来源是不受控的第三方？→ 后者才是文档库的场景（但通常 `jsonb` 一列就够）。
4. **谁在凌晨三点值班？** 团队里有几个人真会调 Mongo 的分片/副本集？会 Postgres 的有几个？→ 这是最常见的真实决定因素，且和"哪个技术更好"无关。
5. **18 个月后你会为什么后悔？** 是数据量上不去、是 schema 迁移做不动、是找不到人、是云账单、还是"当初没人告诉我 xxx"？→ 这个答案直接决定我要不要给你写第二条路和反悔条件。

**两处可以往上抬的地方（你决定要不要）**

- **Altitude**：把"选一个库"换成"一份 18 个月内可反悔的数据层决定" —— 我来做访谈、写决策备忘、给出触发反悔的具体指标（如 QPS / 数据量 / 一致性事件）。代价是我需要你回答上面 5 个问题。
- **Depth**：不靠博客和直觉，按你真实的表结构和前三大查询去跑一遍：两边各建最小原型，量迁移脚本、一个典型聚合查询的写法成本、以及"加一个字段"要动几处代码。代价是要花半天做实验。

我不建议现在就上 Depth —— 得先知道你的项目长什么样，否则实验对象错了。

**我暂时填不了的**：项目做什么、团队规模、数据量级、有没有合规/多地域要求。这几个空我只能留白，瞎猜出来的建议比没有更糟。