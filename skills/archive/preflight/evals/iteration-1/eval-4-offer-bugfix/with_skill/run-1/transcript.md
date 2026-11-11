TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/SKILL.md"}

TOOL ls: {"path": "/tmp/pf-4-with_skill-s22fw48f"}

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


RESULT: logs/
package.json
README.md
src/

TOOL read: {"path": "/tmp/pf-4-with_skill-s22fw48f/src/login.ts"}

TOOL read: {"path": "/tmp/pf-4-with_skill-s22fw48f/package.json"}

TOOL bash: {"command": "cd /tmp/pf-4-with_skill-s22fw48f && cat README.md; echo ---; ls -la src logs; echo ---; git log --oneline -20 2>&1 | head -30"}

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


RESULT: # acme-web

React + TypeScript 前端。`npm test` 跑 vitest。
Node 版本见 package.json engines。
---
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
---
fatal: not a git repository (or any of the parent directories): .git


TOOL read: {"path": "/tmp/pf-4-with_skill-s22fw48f/logs/crashes-2026-11.csv"}

RESULT: date,app_version,error,count
2026-11-01,2.3.0,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",412
2026-11-01,2.3.0,"ChunkLoadError: Loading chunk 7 failed",88
2026-11-03,2.3.1,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",377
2026-11-05,2.3.1,"RangeError: Maximum call stack size exceeded at cart.ts:41",19


TOOL write: {"path": "/tmp/pf-4-with_skill-s22fw48f/local/plans/login-white-screen.md", "content": "# Plan: 登录页白屏修复\n\n- Asked: 帮我修一下登录页偶尔白屏的 bug，代码在 src/login.ts\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\nHand over（建议）：不只改 login.ts:5 的空指针，而是交付「登录页在 401 / 非 JSON 报错 / fetch 失败 / 慢响应 下都渲染出可见状态（loading、错误提示、重试），永不白屏」+ 一条可跑的回归测试。\n- Fallback：只加 `s?.user?.name ?? \"\"` 与 `.catch` 兜底，消掉当期 789 次崩溃。\nDepth：原始材料是 `logs/crashes-2026-11.csv`；仪器是错误日志按版本/次数分组 + vitest 断言。专家动作：把「偶尔」拆成分层原因——401 或非 JSON 响应导致 `s.user` 为 undefined（789 次，2.3.1 仍在涨），以及 ChunkLoadError 88 次（旧 chunk 缓存，同样表现为白屏），而不是只修一行就宣布收工。\nRange：动词 = 复现 / 定位 / 修复 / 防回归 / 让用户看见状态。Crew：前端可靠性（挂载状态机 + 错误边界）、测试（构造 401、500+HTML、网络 reject、慢响应的 mock fetch）、red team（反问「token 过期且离线时呢？重试会不会打爆接口？」）。\nJudge：仓库内自检 `npm test`——vitest 用上述四种响应断言 `root.innerHTML` 非空且出现错误提示；再逐条对照 crashes CSV 的错误行是否都被覆盖。注意：当前仓库没有任何测试文件，需新建。\nNeeds：错误日志 CSV（已有）；线上 401/超时的真实响应体样例（缺）；是否能接受「显示错误 + 手动重试」而非静默重试（待定）；工作目录不是 git 仓库，无法 diff 定位引入点（缺）。\nDeclined：—（待你裁决）\n\n## Task\nPurpose: ？（白屏挡住了什么：登录转化、客服工单、还是发布信心）\nContext（我查到的事实，请确认）：`src/login.ts` 中 fetch 无 `.catch`，第 5 行无判空直接取 `s.user.name`；`logs/crashes-2026-11.csv` 显示该 TypeError 在 2.3.0/2.3.1 合计 789 次，另有 ChunkLoadError 88 次；仓库无测试、无 git、README 只说 React+vite。\nMaterials: ？\nBoundaries: ？（例如「不许吞掉错误静默重试」「不许改接口协议」「不许在登录页加新依赖」）\nDone: ？（先给什么当检查点：是先看「根因对照表 + 测试清单」，还是直接看 patch）\n\n## Open\n- 「偶尔」是否包含 ChunkLoadError 那 88 次，还是只修 TypeError？两者修法不同（前者要 chunk 重载/版本提示）。\n- 白屏期间用户该看到什么：转圈、错误文案、还是自动重试？文案谁定？\n- 是否需要顺手加错误上报（否则下次还是靠 CSV 猜）。\n\nReady: no —— Hand over 未裁决，Task 五问未答（Purpose / Materials / Boundaries / Done 为空）。\n"}

RESULT: Successfully wrote to /tmp/pf-4-with_skill-s22fw48f/local/plans/login-white-screen.md

ASSISTANT: 我已经先查了代码和日志，根因其实基本锁定；但“白屏”有三种可能来源，改法不同，所以先给你一屏计划，你确认后我再动手。

计划：`local/plans/login-white-screen.md`

查到的事实（可直接确认）：
- `src/login.ts:5` 无判空取 `s.user.name`，且 `fetch` 没有 `.catch` → 401/非 JSON 响应时 `s.user` 为 undefined，抛错后 `root.innerHTML` 永不赋值 = 白屏。
- `logs/crashes-2026-11.csv`：该 TypeError 在 2.3.0 + 2.3.1 合计 **789 次**，2.3.1 仍在涨；另有 **ChunkLoadError 88 次**，也是白屏但修法完全不同。
- 仓库无测试文件、非 git 仓库（`npm test` 现在跑不出任何断言）。

需要你裁决的四件事：
1. **Hand over**：只兜底修 TypeError（Fallback），还是升级为“任何后端/网络异常都不白屏 + 回归测试”（建议）。
2. **白屏期间用户看到什么**：loading、错误文案+重试，还是自动重试？
3. **范围**：这 88 次 ChunkLoadError 算不算在内？
4. **完成的样子**：先看“根因对照表+测试清单”当检查点，还是直接看 patch？

你回一句（或直接说“按建议走，范围只修 TypeError，先看 patch”），我就开始改并补 vitest 用例。