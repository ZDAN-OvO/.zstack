TOOL bash: {"command": "cd /tmp/pf-10-with_skill-0amxtwln && ls -la && git rev-parse --show-toplevel 2>/dev/null; echo \"---\"; find . -maxdepth 3 -type f -not -path './.git/*' | head -50"}

TOOL bash: {"command": "ls /home/zdan/.zstack/skills/plan/preflight/references/ 2>/dev/null"}

RESULT: total 172
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 64 root root 167936 11月 10 22:35 ..
-rw-rw-r--  1 zdan zdan      0 11月 10 16:17 .keep
---
./.keep


RESULT: ambition.md
task-definition.md


TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/references/task-definition.md"}

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


TOOL write: {"path": "/tmp/pf-10-with_skill-0amxtwln/local/plans/database-choice-criteria.md", "content": "# Plan: 新项目数据库选型\n\n- Asked: 「新项目的数据库选 Postgres 还是 MongoDB？我还没想好看什么标准」\n- Stage: think — 先问出标准，而不是先给对比\n- Date: 2026-11-10\n\n## Requirement\n\nHand over（建议，待你裁定）: 一份**属于这个项目自己的**选型标准（每条标准带「Postgres 胜 / MongoDB 胜 / 打平」，再加一句「如果这条反过来，结论会翻转」）。\nFallback: 只给标准清单，不下判断。\nCeiling（超出可交付范围）: 由模型直接拍板并写好迁移脚本 —— 后果由你承担，且业务事实只有你有。\nDepth: 不看产品对比表，看你的 workload：数据形状是否稳定、事务边界跨几条记录、查询模式、规模量级、团队能否运维、托管与备份成本。仪器 = 用你真实数据做一次百万行级读写 + 查询原型（Postgres JSONB 列 vs Mongo collection），而不是读博客。Stretch: 找出一个**能推翻结论的事实**，用你的数据验证它。\nRange: 动词 = 让这个决定半年后不用重做 / 让团队能听懂并被说服 / 不把团队拖进没人会运维的系统。\nCrew: 数据建模（查真实形状）、SRE（托管/备份/成本）、安全合规（审计、加密、最小权限）、红队（专门论证你选的那个会在哪先崩）。\nJudge: 一个独立 session 当红队，只审**方法**（标准是否来自真实 workload、引用是否可查证），不看结论；最后一条由你判 —— 你能不能在两分钟内为一票辩解。\nNeeds: 项目是什么（缺）、数据形状样本（缺）、团队技能与已有基础设施（缺）、规模与增长预估（缺）、合规/托管要求（缺）。\nDeclined: —\n\n## Task\n\nPurpose: （待你回答）\nContext: 待你回答；下面几条事实你可以拿去当背景，但**请自己核实**：① MongoDB 4.0 起支持多文档事务（副本集），4.2 起分片集群支持，代价高于单文档写入；② Postgres 的 JSONB + GIN 索引能存文档形状数据，schema 不必写死；③ Postgres 扩展生态（pgvector / PostGIS / TimescaleDB）让向量、地理、时序不必另起系统；④ 超大数据量原生分片 Mongo 更早可用，Postgres 通常要上 Citus。\nMaterials: （待你回答）建议等级：一手 = 你的真实数据/查询日志/压测、官方文档的限制章节；二手禁用 = 「XX 已死」「跑分对比」类博客。查不到就留空，不要补。\nBoundaries: （待你回答）\nDone: （待你回答）建议最低形态：先给 3–4 条标准让你审，通过后再落到结论。\n\n## Open\n\n1. Purpose —— 六个月后这个决定会在什么场合被审？选错了，第一个受害的是谁（写入延迟、迁移工期、招聘、账单）？\n2. Context —— 项目做什么、团队几人、有没有现成 DBA/托管平台、读多还是写多、数据形状已经定了还是天天变？\n3. Materials —— 你手上有哪些能作为依据的东西（压测、日志、公司已有基础设施、合规条款）？哪些来源你不想让它出现在论证里？\n4. Boundaries —— 什么输出会让你说「不是我要的」？（例如：直接给我一个结论 / 给一张对比表 / 给「两个都上」的折中方案 / 引用跑分）\n5. Done —— 看到什么形态就停？先标准清单，还是标准 + 结论一次给全？\n\nReady: no —— 五个 Task 槽全空，三条 Requirement 建议未裁定。\n\n<!-- 你回答上面 Open 里的问题后，我把答案原样写进 Task，并更新 Ready。 -->\n"}

RESULT: Successfully wrote to /tmp/pf-10-with_skill-0amxtwln/local/plans/database-choice-criteria.md

ASSISTANT: **阶段：Think。** 你说「还没想好看什么标准」——那现在给的任何「Postgres vs MongoDB 对比」都是我猜的标准，看着专业但对你没用。所以先不问答案，先问标准从哪来。

计划写在 `local/plans/database-choice-criteria.md`。需要你回答的五件事：

1. **Purpose** — 六个月后这个决定会在什么场合被审？选错了第一个受害的是谁：写入延迟、迁移工期、招不到人、还是账单？
2. **Context** — 项目做什么、团队几人、有没有现成托管/DBA、读多写多、数据形状已定还是天天变？
3. **Materials** — 你手上能当依据的都有什么（压测、日志、公司已有基建、合规条款）？哪些来源不许出现在论证里？
4. **Boundaries** — 什么输出会让你说「不是我要的」？比如：直接给结论 / 给一张对比表 / 给「两个都上」的折中 / 引用跑分博客。
5. **Done** — 看到什么就停：先给标准清单让你审，还是标准＋结论一次给全？

另外三条 Requirement 建议等你裁定（接受/改写/拒绝）：

- **Altitude**：交付「属于这个项目自己的标准」，每条附「这条反转则结论翻转」。上限是「我直接拍板并写迁移脚本」——后果你担，业务事实也只有你有。
- **Depth**：不看对比表，看你真实 workload——用你数据做一次百万行读写＋查询原型（Postgres JSONB vs Mongo collection）。Stretch：找一个**能推翻结论**的事实并用数据验证。
- **Range**：红队专门论证「你选的那个会在哪先崩」，只审方法不审结论；最后你能否两分钟为自己的一票辩解。

Ready: **no** —— 五个槽全空，三条建议未裁定。回答后我把你的原话填进 Task、更新 Ready。

答完可以直接 `/define-goal`，以这份计划为源。