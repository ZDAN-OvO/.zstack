TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/SKILL.md"}

TOOL bash: {"command": "ls -la; echo ---; ls logs src 2>/dev/null"}

RESULT: ---
name: preflight
description: >-
  Write a one-screen plan the user reads to check their own thinking before AI runs the work: could the requirement aim higher, deeper or wider, and can the user state the task's purpose, context, materials, boundaries and done? Use when a request is one step of a bigger result ("fix this bug", "fill in the template"), when quality matters in a field the user is not expert in, when a deliverable is named by its noun ("homepage", "weekly report"), when the user cannot say what done looks like, or when a planned result came back rejected.
---

# Preflight

A request is the user's guess at one step toward an outcome they have not stated. The model carries out the step as written and does not question the intent behind it. So two gaps go unseen until the output lands:

- **Requirement**: the request undershoots what the model could own today.
- **Task**: the intent is still unformed. The model mirrors vagueness back as a generic output.

This skill brings both gaps into one plan that the user reviews before execution. The user's thinking is the subject. Writing the goal and doing the work come after the plan.

## Enter

Offer the plan in one line, and go on only if the user accepts. When a redo costs less than a plan (a rename, a lookup), do the request as written. The plan pays off when a wrong output costs a meeting, a handoff or a long unattended run.

## Look

Read the files, data and history the request touches. Facts you can look up go into the plan as facts. The questions you ask are about intent, which no file holds.

## Stage

Match the request to the user's stage. A request made one stage too early gets a hollow answer: a draft with no thesis, or a recommendation built on guessed criteria.

- **Think**: ask questions that turn the vague into the concrete.
- **Explore**: map the options and their trade-offs.
- **Decide**: weigh the options against the user's decision logic.
- **Execute**: continue with this skill.

## Requirement

Suggest moves on three axes. The user accepts, rewrites or declines each one, and a declined move is recorded with its reason.

- **Altitude**: hand over the outcome, not the step. Ask what should happen after this result, and climb rung by rung. Stop when a rung plainly exceeds what models can own today. That **ceiling** is only found by trying, so the rung below it becomes the **fallback**. Altitude fits outcome-driven work, and work that will be discussed in meetings is a good sign. It fits creative work less well. Climbing often requires changes to the workflow, such as data access, version-to-commit mapping and machines to reproduce on.
- **Depth**: do the task the way a field-leading expert would, one layer below the request. Name the expert move the user did not ask for, the rawest material, and the instruments of the field (databases and statistical models rather than tables). The instruments change the method. A persona only changes the vocabulary. Where it fits, add a **stretch target** that forces a different method, or a test of a belief the user holds, run against raw data, or a new finding shown to predict data it has not seen.
- **Range**: restate the deliverable's noun as verbs, the effect it must have on people. Then assemble the **crew** of fields that do those verbs best, including a **red team**. Ask for what each field *does*, not how it sounds.

Every axis needs a **judge** outside the session that did the work. The judge grades the method as well as the result, because a lucky correct guess should fail and a sound near-miss should pass. Prefer a check the model can run itself (a test, held-out data, a primary source). Otherwise, use separate attacker sessions plus one more session that rules on their objections. When the user can judge the result directly, their judgment is enough.

## Task

Ask the five intent questions. Each one has an answer only the user holds:

- **Purpose**: the decision or problem the output serves. An action ("analyse five competitors") is not a purpose.
- **Context**: what a capable stranger would need to know so they do not aim wrong.
- **Materials**: the sources ranked primary over secondary, the banned sources, and an empty slot for anything not found. An unranked or unbounded source list invites fabrication.
- **Boundaries**: the outputs that would make the user say "not what I wanted". These are **walls**, mostly "don'ts". Directions and adjectives do not count.
- **Done**: what appears in front of the user that means stop. It includes the shape of the artifact and an early **checkpoint**, such as an outline before the full piece, so a wrong direction is caught cheaply. Boundaries and Done together give the scope.

The model can ask these questions, and only the user can answer them. Write each answer in the user's words. Facts you found can go into Context or Materials, marked for the user to confirm. A slot the user cannot answer goes under Open. The gap itself is the finding, so it is never filled with a plausible guess.

## Write

Write `local/plans/<topic>.md` at the workspace root (the git root, or the current directory). `<topic>` is a short kebab-case English slug of the outcome. Ask before you overwrite a file from another task. Use the user's language and keep the plan to one screen:

```markdown
# Plan: <outcome in a few words>

- Asked: <the request as the user wrote it>
- Stage: execute
- Date: <YYYY-MM-DD>

## Requirement
Hand over: <accepted rung>
Fallback: <rung below>
Depth: <raw material; instruments; stretch target>
Range: <verbs; crew and what each does>
Judge: <the outside check, and what it grades>
Needs: <data, access, machines; mark what is missing>
Declined: <move, reason>

## Task
Purpose:
Context:
Materials:
Boundaries:
Done:

## Open
<what the user has not thought through yet; omit when empty>

Ready: <yes | no, because …>
```

`Ready` is yes when the user has ruled on every Requirement move and answered all five Task slots. The plan is done when the user has read it and confirmed the Ready line. Close with the path, and offer `/define-goal` with the plan as its source.

## After a try

When the user brings back a rejected result, find the cause and act on it:

- **Wrong method** (a missed diagnosis, a missing source): use more Depth on the same rung.
- **Too big**: take the Fallback.
- **Missed intent**: go back to the Task slot that let the miss through.

Update the plan in place, and add one dated line under `## Tries` with the verdict and what changed.

## References

- [references/ambition.md](references/ambition.md): the source of the Requirement axes and the judge, with a worked ladder and the expert questions. Read it when a Requirement move needs grounding.
- [references/task-definition.md](references/task-definition.md): the source of the stages and the five slots, with a worked brief. Read it when a Task question needs grounding.


RESULT: total 188
drwxrwxr-x   4 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 109 root root 167936 11月 10 18:01 ..
drwxrwxr-x   2 zdan zdan   4096 11月 10 16:17 logs
-rw-rw-r--   1 zdan zdan    206 11月 10 16:17 package.json
-rw-rw-r--   1 zdan zdan    104 11月 10 16:17 README.md
drwxrwxr-x   2 zdan zdan   4096 11月 10 16:17 src
---
logs:
crashes-2026-11.csv

src:
login.ts


TOOL read: {"path": "logs/crashes-2026-11.csv"}

TOOL read: {"path": "src/login.ts"}

RESULT: date,app_version,error,count
2026-11-01,2.3.0,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",412
2026-11-01,2.3.0,"ChunkLoadError: Loading chunk 7 failed",88
2026-11-03,2.3.1,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",377
2026-11-05,2.3.1,"RangeError: Maximum call stack size exceeded at cart.ts:41",19


RESULT: export function mountLogin(root: HTMLElement) {
  console.log("mount login");
  const token = localStorage.getItem("token");
  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
    .then((r) => r.json())
    .then((s) => { console.log("session", s); root.innerHTML = renderForm(s.user.name); });
}

function renderForm(name: string) {
  console.log("render", name);
  return `<form><input value="${name}"/></form>`;
}


TOOL bash: {"command": "cat package.json; echo ---; cat README.md; echo ---; date +%F; echo ---; git rev-parse --show-toplevel 2>&1 | head -1"}

RESULT: {
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
---
# acme-web

React + TypeScript 前端。`npm test` 跑 vitest。
Node 版本见 package.json engines。
---
2026-11-10
---
fatal: not a git repository (or any of the parent directories): .git


TOOL write: {"path": "local/plans/login-crash-fix.md", "content": "# Plan: 登录页缺 user 崩溃修复\n\n- Asked: 不接受，下周就演示了，只修这一个就行。目标：演示不崩；背景：React 前端，session 接口偶尔不返回 user；素材：logs 和 src/login.ts；边界：不改后端；完成：一个带回归测试的 PR。\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\n\nHand over: 只修 `login.ts:5` 的 `TypeError`（用户明确拒绝上提，见 Declined）。\nFallback: 若演示前仍定不到根因，在 `mountLogin` 外层加错误边界保证不白屏——只是兜底，不算完成。\nDepth: 专家动作不是 `s.user?.name ?? \"\"` 一行守卫，而是修在\"数据契约\"这一层：`fetch` 对 401/500 也 resolve，`r.json()` 遇到 HTML 错误页会抛，`s` 本身也可能是 `undefined`——守卫打错层就仍然崩。原始素材：`logs/crashes-2026-11.csv` 里同签名的 412+377=789 次作为修复前基线。仪器：用真实响应形状做 fixture（`{}`、`{user:null}`、`{user:{}}`、非 JSON body、非 2xx），而不是只测 happy path。Stretch: 回归测试必须在**旧代码上失败**、新代码上通过（否则测的是空气）。\nRange: 动词 = 让登录页在缺 user 时不崩 / 把\"缺 user\"变成可见状态而不是静默空表单 / 让同类缺失在 CI 里被抓住。Crew：前端可靠性（防御式渲染与错误边界）、可观测性（区分未登录 vs 后端异常）、测试（契约 fixture 与红队式反例）。\nJudge: `npm test` 的回归测试 + 一个攻击 session 专门找\"守卫写错层\"的反例；同时评方法（是否修在根因层、测试能否在旧代码上失败），因此碰巧不崩也不算过。\nNeeds: session 接口缺 user 时的真实响应样例（日志里没有，**缺**）；git 仓库（当前目录不是 git repo，**缺**，没有它开不了 PR）；vitest 未出现在 `package.json` 依赖里且 `src/` 下无测试文件（**缺**，`npm test` 现在大概率跑不起来）。\nDeclined: 上提到\"登录页零崩溃 + 一周崩溃日志归零\"——原因：下周演示，用户只要修这一个；记录为退路之上的动作不做。\n\n## Task\n\nPurpose: 下周演示时登录页不崩，人能顺利看到产品。\nContext: React 前端；`mountLogin` → `fetch /api/session` → `renderForm(s.user.name)`；日志中该签名 11/01–11/03 共 789 次，是最高频崩溃；另有 ChunkLoadError 88 次、`cart.ts:41` 栈溢出 19 次，本次不在范围。\nMaterials: 一手 = `logs/crashes-2026-11.csv`、`src/login.ts`；空缺 = session 接口响应样例（待补，不猜）。\nBoundaries: 不改后端；不动 `cart.ts` / ChunkLoadError；不改登录页的整体交互与视觉。**待确认**：是否允许把崩溃改成\"可见错误提示\"（不做静默吞掉）。\nDone: 一个带回归测试的 PR；checkpoint = 先给\"缺 user 时应该显示什么\"一句话方案 + 测试用例清单，确认后再写代码。\n\n## Open\n\n1. **缺 user 时到底显示什么**（跳转登录 / 空表单 / 错误提示）——唯一挡住 Done 的意图缺口，只有你能定。\n2. 仓库在哪：当前目录无 `.git`，PR 要在哪儿开。\n3. 测试基建：是否可以新增 vitest 依赖与 `src/*.test.ts`。\n\nReady: no，因为第 1 条未定，且 2/3 缺失使\"带回归测试的 PR\"当前不可达。\n"}

RESULT: Successfully wrote to local/plans/login-crash-fix.md

ASSISTANT: 计划已写好：`local/plans/login-crash-fix.md`

要点（已按你的约束把上一轮"往上修"记为 Declined，不并入本次范围）：

- **范围**：只修 `src/login.ts:5` 的 `TypeError`。日志里同签名 789 次（11/01–11/03），是最高频；ChunkLoadError 88 次、`cart.ts:41` 19 次明确排除。
- **深度**：真正会再崩的不是 `s.user.name` 这一处，而是守卫打错层——`fetch` 对 401/500 也 resolve、`r.json()` 遇 HTML 错误页会抛、`s` 自身可能是 `undefined`。回归测试要用 `{}` / `{user:null}` / `{user:{}}` / 非 JSON / 非 2xx 做 fixture，并验证它在旧代码上失败。
- **三个缺口**（挡住 Ready）：
  1. 缺 user 时该显示什么（跳登录 / 空表单 / 错误提示）——只有你能定，这是唯一意图缺口；
  2. 当前目录不是 git 仓库，PR 无处可开；
  3. `package.json` 里没有 vitest 依赖、`src/` 无测试文件，`npm test` 现在跑不起来。

`Ready: no`。等你定完第 1 条、并确认 2/3 怎么补，我再改成 yes 并开工；也可以接着用 `/define-goal` 以这份 plan 为源。