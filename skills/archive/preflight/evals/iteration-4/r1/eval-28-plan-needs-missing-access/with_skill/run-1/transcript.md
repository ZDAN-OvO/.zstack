TOOL bash: {"command": "cd /tmp/pf-28-with_skill-3fjmp4y0 && ls -la && echo \"---\" && find . -maxdepth 3 -not -path '*/.git/*' | head -50"}

TOOL bash: {"command": "cd /tmp/pf-28-with_skill-3fjmp4y0 && ls -la data 2>/dev/null && echo \"--- files ---\" && for f in data/*; do echo \"== $f\"; head -5 \"$f\" 2>/dev/null; wc -l \"$f\" 2>/dev/null; done"}

RESULT: total 184
drwxrwxr-x  4 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 63 root root 167936 11月 10 22:25 ..
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 data
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 notes
-rw-rw-r--  1 zdan zdan    131 11月 10 16:17 template.md
---
.
./template.md
./data
./data/q3-metrics.csv
./notes
./notes/worklog.md


RESULT: total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  126 11月 10 16:17 q3-metrics.csv
--- files ---
== data/q3-metrics.csv
month,revenue_usd,new_customers,churned_customers,nps
2026-07,182000,41,12,38
2026-08,176000,35,19,31
2026-09,171000,30,24,27
4 data/q3-metrics.csv


TOOL bash: {"command": "cd /tmp/pf-28-with_skill-3fjmp4y0 && echo \"== template.md\"; cat template.md; echo; echo \"== notes/worklog.md\"; cat notes/worklog.md"}

TOOL bash: {"command": "cat /home/zdan/.zstack/skills/plan/preflight/references/ambition.md"}

RESULT: == template.md
# Q3 业务回顾

## 收入
本季收入：{{revenue}}

## 客户
新增：{{new}}，流失：{{churn}}

## 下季计划
{{plan}}

== notes/worklog.md
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


TOOL bash: {"command": "cat /home/zdan/.zstack/skills/plan/preflight/references/task-definition.md"}

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


TOOL bash: {"command": "date +%Y-%m-%d; ls /tmp/pf-28-with_skill-3fjmp4y0/local 2>/dev/null || echo \"no local dir\""}

RESULT: 2026-11-10
no local dir


TOOL write: {"path": "/tmp/pf-28-with_skill-3fjmp4y0/local/plans/daily-monitoring-alerts.md", "content": "# Plan: 用每日异常监控取代季度回顾\n\n- Asked: /skill:preflight 我想把季度回顾换成每日监控，异常才提醒老板\n- Stage: execute（请求本身已经是最顶层的一级，跳跃不是问题，原料是）\n- Date: 2026-11-10\n\n## Requirement\n\n**Hand over（接受的那一级）**：老板不看季报了，而是在问题变成数字之前，收到一条能照做的提醒。提醒里必须带三样：哪里变了、多确定、该动哪个杠杆。监控自己每月的误报记录，也要交给老板复盘。\n**Ceiling（试探）**：监控自己每天挑因、自己改产品。这一级今天基本超出模型能负责的范围（涉及定价、人头、产品路线）。\n**Fallback**：下周四 QBR 照旧，附一页「如果每天看，这件事几号就会被发现」。若原料拿不到，先交这页。\n\n**Depth**：不是给月度 KPI 设阈值。\n- 原始材料：事件级流水（注册、激活、扣款、取消、工单标签、埋点），带日期和客户 id，而不是 `data/q3-metrics.csv` 这样的月汇总。\n- 工具：变点检测与统计过程控制（CUSUM、EWMA、贝叶斯在线变点），流失做生存分析，而不是「跌 10% 就报警」。\n- 一个没被要求的专家动作：先做归因拆分——8 月里是哪个细分、哪一天先动的，把「试用 14→7 天」（8 月中）和「太难上手」工单（9 月 8 日起）在时间轴上的先后关系摆出来。\n- Stretch target：回测要求 lead time ≥ 30 天，且安静期误报 ≤ 1 次/月；同时在 8 月那段自动给出「先动的是谁」。做不到就说做不到，不许调低标准凑。\n- 测一个信念：`notes/worklog.md` 里已经有个假设——流失是因为上手难。用原始数据检验它：是上手难先动，还是试用变短/价格先动。\n\n**Range**：把「监控」还原成四个动词——察觉（detect）、说服（一条告警让老板三十秒内信）、归因（指向杠杆）、止损（触发动作）。\n- 值班/可观测性工程师：告警设计、误报预算、runbook。\n- 流行病学家：变点检测与 lead time 的度量方式（监测系统是他们的老本行）。\n- 做空机构/法务会计（红队）：季节性、扣款日历、大客户、口径变更会不会骗过检测器。\n- 财经记者/编辑：一条告警的措辞，让老板不用问第二句。\n- 产品分析师：把信号拆回试用期、引导链路、分群。\n\n**Judge**：预注册回测。规则和通过线在看到 8/9 月明细之前就写死，然后在留出期上评分：8 月、9 月各在几号报出、季报是几号、安静期误报几次。另开红队 session 专攻「用了未来信息 / 多重比较挑规则 / 口径泄漏」，再由第三个 session 裁定哪些指控成立。老板能不能一眼判断这条提醒值不值得看，他自己就是最后一道。\n\n**Needs**：\n- 缺失：日粒度/事件级原始数据（工作目录里只有 3 行月汇总）。\n- 缺失：至少 12 个月历史（现在只有 2026-07~09，覆盖不了季节性）。\n- 缺失：客户级明细、取消原因、工单标签体系。\n- 缺失：告警送达方式（邮件/企微/Slack）与谁值守。\n- 已有：一台能装软件、跑回测的机器；`data/`、`notes/`、`template.md`。\n\n**Declined**：暂无（还没有被拒绝的提案）。\n\n## Task\n\n**Purpose**：让老板在问题变成季报数字之前，就做一次钱和人手的调配决定。不是多看一张看板。\n**Context**：\n- 用户给的：SaaS，老板只看季报，异常才提醒。\n- 我查到的：`data/q3-metrics.csv` 只有 2026-07~09 三行——收入 182k→176k→171k，新增 41→35→30，流失 12→19→24，NPS 38→31→27；`notes/worklog.md` 记着 8 月中旬试用从 14 天改成 7 天、9 月 8 日起「太难上手」工单变多、老板说 QBR 下周四给 VP 看；`template.md` 是现有季度回顾模板。\n- 由此得到的关键事实：恶化从 **8 月** 就已经出现在月度数字里了。所以「每日监控比季报更早」这句话，用现有数据最多只能证明提前几周，证明不了「每天」的价值；要证明后者，必须有日粒度原始数据。\n**Materials**：一手——事件级原始表（注册/激活/扣款/取消/工单/埋点）、`data/q3-metrics.csv`、`notes/worklog.md`、`template.md`。二手——无。禁止——编造日粒度数据、凭印象定阈值、拿行业均值当基线。找不到的字段留空，不许填。\n**Boundaries**（墙）：\n- 不发垃圾提醒（需要量化，见 Open 2）。\n- 不拿月汇总冒充日粒度，不做没有回测就上线的告警。\n- 不发没有「该动什么」的提醒。\n- 下周四的 QBR 不能被这次改造弄没。\n- 不出现只有形容词、没有数字和取舍的结论。\n**Done**：\n1. **检查点**：先给一页《检测器设计与回测方案》——用哪些原始字段、检测方法、通过线、误报上限、留出期怎么划。确认后才跑。\n2. 回测报告：8 月和 9 月各自哪天被报出、对应季报是哪天、提前多少天、安静期误报几次、归因拆分结论（哪个细分/哪天先动）。\n3. 通过后才是并行一季度的管道 + 每月自动生成的误报复盘。\n\n## Open\n\n1. 有没有日粒度或事件级数据？没有的话「每日监控」的原料就不存在，第一步只能交数据补齐清单。这是最大的口子。\n2. 「垃圾提醒」的量化上限是多少——每月误报几次算垃圾？谁看、几点看、看不看手机？\n3. 下周四的 QBR 照旧开吗？它和「并行跑一个季度」是什么关系。\n4. 老板能动哪几个杠杆（价格、试用期、人手、产品排期）？这决定提醒指向哪里。\n5. 「更早」的及格线是几天？30 天还是 7 天。\n\nReady: no — 三处 Requirement 提案还没被逐条裁决；日粒度数据缺失；误报上限没定。\n"}

RESULT: Successfully wrote to /tmp/pf-28-with_skill-3fjmp4y0/local/plans/daily-monitoring-alerts.md

ASSISTANT: 计划已写到 `local/plans/daily-monitoring-alerts.md`。

**核心发现（会改掉这件事的前提）**：`data/q3-metrics.csv` 只有三行月汇总（2026-07~09）。而恶化在 **8 月**就已经出现在月度数字里了（流失 12→19、NPS 38→31）。所以：

- 「比季报更早」用现有数据最多证明提前几周；
- 「每天」的价值要证明，必须有日粒度/事件级原始数据，而它不在工作目录里。

`notes/worklog.md` 另外给了两条硬时间点：8 月中旬试用 14→7 天、9 月 8 日起「太难上手」工单变多 —— 这是回测里能验证因果先后的原材料，也顺手检验了「流失是上手难」这个现有信念。

要求部分我提了三条，等你逐条接受/改写/拒绝：
- **Altitude**：交的是「老板照做的一条提醒（哪里变了 / 多确定 / 动哪个杠杆）」，不是告警管道本身；fallback 是 QBR 那页「几号就会被发现」。
- **Depth**：变点检测 + 生存分析，不用「跌 10% 就报」；stretch 是 lead time ≥ 30 天、误报 ≤ 1 次/月，同时自动归因。
- **Range**：察觉 / 说服 / 归因 / 止损，配值班 SRE、流行病学家、做空机构红队、财经编辑。

Ready: **no** —— 上面三条还没裁决，日粒度数据缺失，而且「不发垃圾提醒」这条墙还没量化（每月几次算垃圾？）。这三件只有你能答。

确认后可以用 `/define-goal` 以这份 plan 为源。