TOOL bash: {"command": "pwd; ls -la; echo \"---\"; git rev-parse --show-toplevel 2>/dev/null; echo \"---\"; cat package.json 2>/dev/null | head -60"}

TOOL ls: {"path": "/home/zdan/.zstack/skills/plan/preflight"}

RESULT: /tmp/pf-16-with_skill-rdnxrxh4
total 188
drwxrwxr-x  4 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 64 root root 167936 11月 10 22:36 ..
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 logs
-rw-rw-r--  1 zdan zdan    206 11月 10 16:17 package.json
-rw-rw-r--  1 zdan zdan    104 11月 10 16:17 README.md
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 src
---
---
{
  "name": "acme-web",
  "version": "2.3.1",
  "engines": {
    "node": ">=20"
  },
  "scripts": {
    "test": "vitest run",
    "build": "vite build"
  },
  "dependencies": {
    "react": "^19.2.0"
  }
}


RESULT: evals/
references/
SKILL.md

TOOL bash: {"command": "cd /tmp/pf-16-with_skill-rdnxrxh4; cat README.md; echo \"=== src ===\"; ls -la src logs; echo \"=== files ===\"; wc -l src/* logs/* 2>/dev/null"}

TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/references/ambition.md"}

RESULT: # acme-web

React + TypeScript 前端。`npm test` 跑 vitest。
Node 版本见 package.json engines。
=== src ===
logs:
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  373 11月 10 16:17 crashes-2026-11.csv

src:
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  441 11月 10 16:17 login.ts
=== files ===
 12 src/login.ts
  5 logs/crashes-2026-11.csv
 17 total


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


TOOL bash: {"command": "cd /tmp/pf-16-with_skill-rdnxrxh4; echo \"=== login.ts ===\"; cat -n src/login.ts; echo; echo \"=== crashes ===\"; cat logs/crashes-2026-11.csv"}

TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/references/task-definition.md"}

RESULT: === login.ts ===
     1	export function mountLogin(root: HTMLElement) {
     2	  console.log("mount login");
     3	  const token = localStorage.getItem("token");
     4	  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
     5	    .then((r) => r.json())
     6	    .then((s) => { console.log("session", s); root.innerHTML = renderForm(s.user.name); });
     7	}
     8	
     9	function renderForm(name: string) {
    10	  console.log("render", name);
    11	  return `<form><input value="${name}"/></form>`;
    12	}

=== crashes ===
date,app_version,error,count
2026-11-01,2.3.0,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",412
2026-11-01,2.3.0,"ChunkLoadError: Loading chunk 7 failed",88
2026-11-03,2.3.1,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",377
2026-11-05,2.3.1,"RangeError: Maximum call stack size exceeded at cart.ts:41",19


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


TOOL write: {"path": "/tmp/pf-16-with_skill-rdnxrxh4/local/plans/homepage-load-time.md", "content": "# Plan: 首页加载从 5 秒到 3 秒（并查清 5 秒花在哪）\n\n- Asked: 首页加载 5 秒，帮我优化到 3 秒\n- Stage: execute（但缺测量，\"优化\"前必须补归因）\n- Date: 2026-11-10\n\n## Requirement\nHand over: 首页 p75 真实用户在 3 秒内可交互，且 CI 里有性能预算断言 + RUM 监控——回到 5 秒会在合并前失败。\nFallback: 先只做归因与一次性改动：一页时间线拆解 + 改动前后同条件三次测量。\nDepth: 从真实用户分布和 trace 出发，不从\"包太大\"出发；工具用 RUM/web-vitals、Lighthouse CI、DevTools trace（限速 4G、冷缓存）、bundle 分析、服务端耗时日志。拉伸目标：p75 LCP ≤ 1.5s。检验一个信念：「5 秒是前端包大」——拿原始数据对它投票（见 Context 里的崩溃证据，怀疑主因是阻塞的 /api/session）。\nRange: 动词＝测量·归因·削减·兜底·防回归。Crew：性能工程师（trace/waterfall）、构建（拆包/预加载/缓存）、后端与网关（/api/session 耗时、超时、边缘缓存）、可观测（RUM、预算告警）；红队＝专门证明\"3 秒只是你这台机器快\"（登出态、弱网、冷缓存、真机）+ 一个 session 裁定谁的反驳成立。\nJudge: 干净环境下的 Lighthouse CI 断言 + 限速真机三次取 p75；判方法不只判数字——解释不了收益来源的改动算不通过，数字碰巧达标也算不通过。\nNeeds: 首页代码（本仓库只有 src/login.ts，无首页、无 vite 配置、无构建产物）；5 秒的测法与设备/网络/冷热缓存；RUM/APM；/api/session 服务端耗时；能跑 Lighthouse 的 CI 与真机。全部缺失。\nDeclined: —（三条待你逐条裁决）\n\n## Task\nPurpose: 未答。猜测（待确认）：3 秒是某个外部门槛——落地页转化指标、体验考核、或别人给的 deadline？\nContext: 事实（已查）：仓库只有 src/login.ts 和 logs/crashes-2026-11.csv，没有首页、没有 vite.config、没有性能测试、没有 RUM。崩溃日志里 2.3.0+2.3.1 共 789 条 `Cannot read properties of undefined (reading 'name')` 指向 login.ts 的 `s.user.name`（session 拿不到 user 就炸），另有 88 条 ChunkLoadError、19 条 cart.ts 栈溢出。→ 对这批用户，首页不是\"慢 5 秒\"，是永远不出来。待确认：5 秒在哪测的、首页代码是否在本仓库之外。\nMaterials: 主＝真实用户 RUM、/api/session 服务端耗时、限速 4G 冷缓存下的 DevTools trace、Lighthouse 报告、构建产物与 bundle 分析。次＝崩溃日志（已给）。禁＝\"感觉快了\"当证据；禁把开 gzip/压图当结论而不测。缺失项留空，不编。\nBoundaries: 不许只在一台机器一次测量上宣布达标；不许为提速砍掉登录态校验或错误兜底（那会换来更多白屏）；不改视觉与交互；不许默默删第三方脚本，要列出来单独说。\nDone: 先交一页归因——TTFB／下载／解析／首屏渲染／可交互 五段时间线，每段带数据出处；你看过这页才动手改。最终：改动 PR + 同条件前后三次对比 + CI 预算断言。\n\n## Open\n- Purpose 未答（谁在等这个 3 秒，等到了要做什么）。\n- 5 秒的测法：谁的机器、什么网络、冷缓存还是热缓存、p50 还是 p75。\n- 首页代码在哪：本仓库里没有。\n- 3 秒这个数能不能谈（p75 下的 1.5s 比一次性 3s 更值）。\n- 可动范围：仅前端？含服务端/网关/边缘？\n\nReady: no —— 三条 Requirement 未裁决，Task 五槽里 Purpose 与 Materials 的测量口径还空着。\n"}

RESULT: Successfully wrote to /tmp/pf-16-with_skill-rdnxrxh4/local/plans/homepage-load-time.md

ASSISTANT: 计划已写好：`/tmp/pf-16-with_skill-rdnxrxh4/local/plans/homepage-load-time.md`

查到的三件事，先摆出来（它们会改变"优化到 3 秒"这个任务）：

1. **仓库里没有首页**。只有 `src/login.ts`，没有 `vite.config`、没有构建产物、没有任何性能测试或 RUM。所以"5 秒"现在没有出处。
2. **有 789 条崩溃指向登录态**：`Cannot read properties of undefined (reading 'name')`，即 `s.user.name` —— session 拿不到 user 就炸；`login.ts` 是 `fetch('/api/session')` 完成后才渲染，没有缓存、没有超时、没有骨架屏。对这批用户，首页不是慢 5 秒，是不出现。我怀疑 5 秒的主因是这条阻塞请求，不是包大——但这要靠数据验，不能靠猜。
3. 另有 88 条 `ChunkLoadError`、19 条 `cart.ts` 栈溢出，同一批日志。

**Requirement——三条请你逐条裁决（接受／改写／拒绝）：**

- **Altitude**：交出「首页 p75 真实用户 3 秒内可交互 + CI 预算断言 + RUM 告警，回 5 秒就合不进去」；回退档＝「一页归因 + 一次性改动」。往上是"全站都快"，再往上是"转化率上去"（超出今天能给的范围）。
- **Depth**：从真实用户分布和 trace 出发，而不是从"包太大"出发；工具用 RUM/web-vitals、Lighthouse CI、DevTools trace（限速 4G 冷缓存）、bundle 分析、服务端耗时。拉伸目标 p75 LCP ≤1.5s，并拿原始数据检验「慢是因为包大」这个信念。
- **Range**：动词是 测量·归因·削减·兜底·防回归；crew 是性能工程师／构建／后端网关／可观测，红队专职证明"3 秒只是你这台机器快"。判定用干净环境的 Lighthouse 断言 + 限速真机三次取 p75，且**判方法不只判数字**。

**Task——五个问题，只有你能答：**

1. **Purpose**：谁在等这个 3 秒？达标之后要拿它做什么（转化率、上线门槛、老板 deadline）？
2. **Context**：5 秒是怎么测出来的——你的机器还是用户机器、什么网络、冷缓存还是热缓存、p50 还是 p75？首页代码在别的仓库吗？
3. **Materials**：有 RUM/APM 吗？`/api/session` 服务端耗时能拿到吗？哪些源不许用？
4. **Boundaries**：哪些结果会让你说"不是我要的"？（我暂定了几条墙：不许单机单次宣布达标、不许砍登录校验换速度、不改视觉、不默默删第三方脚本）
5. **Done**：我建议第一个交付物是**一页归因**（TTFB/下载/解析/首屏/可交互 五段时间线，每段带出处），你看过再动手。这个 checkpoint 你认可吗？还是直接要 PR？

两个我建议现在就松动的地方：**3 秒这个数**（p75 的 1.5s 比一次性的 3s 值钱），以及**范围**（只前端，还是也含服务端/网关）。

**Ready: no** —— 三条未裁决，Purpose 和测量口径还空着。答完我就把它改成 Ready: yes，然后可以用 `/define-goal` 以这份计划为源。