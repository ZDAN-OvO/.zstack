TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/SKILL.md"}

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


TOOL bash: {"command": "cd /tmp/pf-34-with_skill-zl8nmlml && ls -la && echo \"---\" && ls -la logs 2>/dev/null | head -50"}

RESULT: total 188
drwxrwxr-x   4 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 108 root root 167936 11月 10 18:03 ..
drwxrwxr-x   2 zdan zdan   4096 11月 10 16:17 logs
-rw-rw-r--   1 zdan zdan    206 11月 10 16:17 package.json
-rw-rw-r--   1 zdan zdan    104 11月 10 16:17 README.md
drwxrwxr-x   2 zdan zdan   4096 11月 10 16:17 src
---
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  373 11月 10 16:17 crashes-2026-11.csv


TOOL bash: {"command": "cd /tmp/pf-34-with_skill-zl8nmlml && cat logs/crashes-2026-11.csv && echo \"=== package.json\" && cat package.json && echo \"=== README\" && cat README.md && echo \"=== src\" && ls -la src"}

RESULT: date,app_version,error,count
2026-11-01,2.3.0,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",412
2026-11-01,2.3.0,"ChunkLoadError: Loading chunk 7 failed",88
2026-11-03,2.3.1,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",377
2026-11-05,2.3.1,"RangeError: Maximum call stack size exceeded at cart.ts:41",19
=== package.json
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
=== README
# acme-web

React + TypeScript 前端。`npm test` 跑 vitest。
Node 版本见 package.json engines。
=== src
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  441 11月 10 16:17 login.ts


TOOL read: {"path": "/tmp/pf-34-with_skill-zl8nmlml/src/login.ts"}

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


TOOL bash: {"command": "cd /tmp/pf-34-with_skill-zl8nmlml && node -v 2>&1; ls node_modules 2>/dev/null | head -3; echo \"vitest installed? $?\"; ls -a src; git rev-parse --show-toplevel 2>&1 | tail -1"}

RESULT: v26.13.0
vitest installed? 0
.
..
login.ts
fatal: not a git repository (or any of the parent directories): .git


TOOL bash: {"command": "date +%F"}

RESULT: 2026-11-10


TOOL write: {"path": "/tmp/pf-34-with_skill-zl8nmlml/local/plans/top-crash-login-undefined-user.md", "content": "# Plan: 修掉最高频崩溃（登录 s.user.name 未判空）\n\n- Asked: 把 logs 里那个最多的崩溃修掉；谁判断修好了 → 「你自己检查一下就行」\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\n\n**查证到的事实**\n- 最多的一条：`TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5`，412 次（2.3.0）+ 377 次（2.3.1）= **789 次**，且当前版本 2.3.1 仍在报 → 是活的、没修的，不是旧噪音。\n- 根因已在源码看到：`src/login.ts:5` 直接取 `s.user.name`，而 `r.json()` 对 401/过期 token/网关错误页也照解不误，`s.user` 为 undefined 时整页白屏。\n- 第二条 `ChunkLoadError` 88 次 = 发版残留，另一类问题；第三条 `RangeError at cart.ts:41` 的源文件不在本仓库，**在这里修不了**（`src/` 只有 login.ts）。\n\n**Requirement（待你逐条 accept / 改写 / 拒绝）**\n- Hand over: 登录入口对「任何非 user 响应」（401、`{}`、HTML 错误页、网络失败）都不再白屏，要么渲染表单，要么渲染「请重新登录」状态。\n- Fallback: 只把 `src/login.ts:5` 改成 `s.user?.name ?? \"\"` 的最小判空。\n- Depth: 不是加个 `?.` 就完事——先 `r.ok` 判 401 再解析，把「会话无效」和「会话正常但无 user」分开处理；用日志里真实失败形态做复现。Stretch：一张表覆盖 401 空 body / 200 `{}` / HTML / reject 四种输入，全部不崩。\n- Range: 动词 = 复现、定位、修、证明、防。班子 = 前端会话/鉴权（认合同，不只认空值）+ 红队（扫其他 fetch 调用点是否有同一模式；顺带指出 `root.innerHTML` 未转义 name）。\n- Judge: 你说自查就够 → 我把它落成**能自己判的检查**：先写测试对着日志里的错误形态跑，**修复前必须红、修复后必须绿**。红→绿这一步是关键，否则我写的测试可能只是自我盖章。红队只提异议，裁定仍落在测试结果上。\n- Needs: 仓库没有 `node_modules`、没装 vitest、也**不是 git 仓库**（改坏了没有 `git diff` 可回退）→ 装 vitest 需联网；改前我先把 login.ts 备份成 `.bak`。\n- Declined: —\n\n## Task\n\n- Purpose: 未答 —— 修完之后要发生什么？（2.3.2 出包？先止血？这条崩溃是否在阻塞发布或客服工单？）\n- Context: 事实部分已由我查证（见上），确认即可；需要你补的：登录页白屏时线上用户看到什么、有没有监控告警。\n- Materials: `logs/crashes-2026-11.csv`（主）、`src/login.ts`（主）。禁用：猜测的第三方博客方案。缺失槽位：`cart.ts` 源文件、后端 `/api/session` 的失败响应样例。\n- Boundaries: 未答 —— 哪些做法你会说「不是我要的」？（例如：不许改公开 API 合同、不许顺手重构整个鉴权、不许只吞错误不提示用户）\n- Done: 未答 —— 什么出现在你面前算停？我提议的形态：`src/login.ts` 改动 + 1 个新测试文件 + 一段「修复前红 / 修复后绿」的输出，**checkpoint 放在测试先红那一步**给你看。\n\n## Open\n\n- Purpose 与 Boundaries 空着，风险是：我把「登录永不白屏」做成「静默吞掉 401」，线上问题从崩溃变成悄悄登录失败——这正是要你划墙的地方。\n- Done 里是否需要真机/浏览器验证，还是单测绿灯即可。\n- 第三条崩溃要不要单开一轮（需先把 `cart.ts` 找回来）。\n\nReady: no，因为 Purpose / Boundaries / Done 三个槽还只有我的提议，没有你的话。\n"}

RESULT: Successfully wrote to /tmp/pf-34-with_skill-zl8nmlml/local/plans/top-crash-login-undefined-user.md

ASSISTANT: 自查我按**能自己判的检查**来定，不按「我觉得改好了」：

- 最多的那条是 `login.ts:5` 的 `TypeError ... reading 'name'`，412+377 = 789 次，而且当前 2.3.1 还在报 → 活的崩溃。
- 根因在源码就看得见：`r.json()` 对 401/过期 token 也照解，`s.user` 为 undefined 直接白屏。
- 判据落地：对着日志里的失败形态先写测试，**修复前必须红、修复后必须绿**。没有红这一步，我写的测试只是自我盖章。
- 另外两条顺带查清：`ChunkLoadError` 是发版残留；`RangeError at cart.ts:41` 的源文件不在本仓库，这里修不了。
- 一个前提：这目录不是 git 仓库、也没装 vitest → 改前备份 `.bak`，装 vitest 需联网。

计划已写到 `/tmp/pf-34-with_skill-zl8nmlml/local/plans/top-crash-login-undefined-user.md`。

Ready: no——Purpose（修完要出 2.3.2 还是先止血）、Boundaries（最要紧：别把「不白屏」做成「静默吞 401」）、Done（单测绿够了，还是要浏览器/真机验证）这三个槽还只有我的提议。你回这三行，或直接说「按你提议的执行」即可。

确认后可用 `/define-goal`，以这份计划为源。