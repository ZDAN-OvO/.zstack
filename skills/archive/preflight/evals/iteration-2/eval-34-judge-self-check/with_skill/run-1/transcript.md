TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/SKILL.md"}

TOOL bash: {"command": "ls -la /tmp/pf-34-with_skill-2lvn3z_z 2>/dev/null && echo \"---\" && ls -la /tmp/pf-34-with_skill-2lvn3z_z/logs 2>/dev/null | head -30"}

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

Each section below ends at a **stop**: the point where this turn's reply is sent. Reaching a stop ends the skill for this turn, even when later sections are still unread.

## Enter

1. **Cost.** When a redo costs less than a plan, do the request as written, or ask only the one or two details it needs. A rename, a lookup and a short poem or message are this case, even when the user typed `/preflight`. The plan pays off when a wrong output costs a meeting, a handoff or a long unattended run. Stop.
2. **Consent.** The user typed `/preflight`, or accepted an offer: go on to Look. Otherwise offer the plan in one line and stop. The workspace stays unchanged until the user accepts.

Accepting the plan is consent to plan, not to execute. From Look onward, the only file this skill writes is the plan; the work itself starts after the user confirms it.

## Look

Read the files, data and history the request touches. Facts you can look up go into the plan as facts. The questions you ask are about intent, which no file holds.

State each finding at the strength the data supports. Two things that change at the same time are a correlation to test. A cause needs evidence that rules the alternatives out.

## Stage

Match the request to the user's stage. A request made one stage too early gets a hollow answer: a draft with no thesis, or a recommendation built on guessed criteria. Only Execute goes on to Requirement and writes a plan. Each earlier stage gives its own result and stops.

- **Think** (no thesis or no direction yet): ask the questions that turn the vague into the concrete. Stop.
- **Explore** (options named, criteria not set): map the criteria that would separate the options, and the trade-off under each. Ask for the few facts that decide between them, and leave the choice open. Stop.
- **Decide** (options and criteria both given): weigh the options against the user's criteria and give the decision, with the conditions that would reverse it. Stop.
- **Execute** (the user wants the work done): continue with this skill.

## Requirement

Look at the task through three lenses. Suggest a move only on a lens where it would change the result, and write `not needed` for the others. Each suggestion stays a suggestion until the user accepts, rewrites or declines it. A declined move is recorded with its reason.

- **Altitude**: hand over the outcome, not the step. Ask what should happen after this result, and climb rung by rung. Stop when a rung plainly exceeds what models can own today. That **ceiling** is only found by trying, so the rung below it becomes the **fallback**. Altitude fits outcome-driven work, and work that will be discussed in meetings is a good sign. It fits creative work less well. Climbing often requires changes to the workflow, such as data access, version-to-commit mapping and machines to reproduce on.
- **Depth**: do the task the way a field-leading expert would, one layer below the request. Name the expert move the user did not ask for, the rawest material, and the instruments of the field (databases and statistical models rather than tables). The instruments change the method. A persona only changes the vocabulary. Where it fits, add a **stretch target** that forces a different method, or a test of a belief the user holds, run against raw data, or a new finding shown to predict data it has not seen.
- **Range**: restate the deliverable's noun as verbs, the effect it must have on people. Then assemble the **crew** of fields that do those verbs best, including a **red team**. Ask for what each field *does*, not how it sounds.

Every move needs a **judge** outside the session that did the work. The judge grades the method as well as the result, because a lucky correct guess should fail and a sound near-miss should pass. Prefer a check the model can run itself (a test, held-out data, a primary source). Otherwise, use separate attacker sessions plus one more session that rules on their objections. When the user can judge the result directly, their judgment is enough.

## Task

Ask the five intent questions. Each one has an answer only the user holds:

- **Purpose**: the decision or problem the output serves. An action ("analyse five competitors") is not a purpose.
- **Context**: what a capable stranger would need to know so they do not aim wrong.
- **Materials**: the sources ranked primary over secondary, the banned sources, and an empty slot for anything not found. An unranked or unbounded source list invites fabrication.
- **Boundaries**: the outputs that would make the user say "not what I wanted". These are **walls**, mostly "don'ts". Directions and adjectives do not count.
- **Done**: what appears in front of the user that means stop. It includes the shape of the artifact and an early **checkpoint**, such as an outline before the full piece, so a wrong direction is caught cheaply. Boundaries and Done together give the scope.

The model can ask these questions, and only the user can answer them. Use what the user has already said in this conversation, and ask only for what is missing. Write each answer in the user's words. Facts you found can go into Context or Materials, marked for the user to confirm.

A slot the user cannot answer stays empty, and the question goes under Open. The gap itself is the finding. Ask a question that helps the user answer it, and write no default for them to approve.

## Write

Write `local/plans/<topic>.md` at the workspace root (the git root, or the current directory). `<topic>` is a short kebab-case English slug of the outcome. The plan may carry Open items; Ready tells the user what is still missing.

Check the path before the write. When a file there belongs to another task, keep it unchanged. Ask which path to use, or write to a new slug and name it in the reply. A backup copy does not count as permission to overwrite.

Use the user's language and keep the plan to one screen:

```markdown
# Plan: <outcome in a few words>

- Asked: <the request as the user wrote it>
- Stage: execute
- Date: <YYYY-MM-DD>

## Requirement
Hand over: <accepted rung, or the request as asked>
Fallback: <rung below>
Depth: <raw material; instruments; stretch target | not needed>
Range: <verbs; crew and what each does | not needed>
Judge: <the outside check, and what it grades>
Needs: <data, access, machines; mark what is missing>
Proposed: <moves awaiting the user's ruling; omit when empty>
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

`Ready` is yes when the user has ruled on every proposed move and answered all five Task slots. The plan is done when the user has read it and confirmed the Ready line. Close with the path, and offer `/define-goal` with the plan as its source. Stop.

## After a try

When the user brings back a rejected result, find the cause and act on it:

- **Wrong method** (a missed diagnosis, a missing source): use more Depth on the same rung.
- **Too big**: take the Fallback.
- **Missed intent**: go back to the Task slot that let the miss through.

Update the plan in place, and add one dated line under `## Tries` with the verdict and what changed. Stop.

## References

- [references/ambition.md](references/ambition.md): the source of the Requirement axes and the judge, with a worked ladder and the expert questions. Read it when a Requirement move needs grounding.
- [references/task-definition.md](references/task-definition.md): the source of the stages and the five slots, with a worked brief. Read it when a Task question needs grounding.


RESULT: total 188
drwxrwxr-x  4 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 59 root root 167936 11月 10 20:55 ..
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 logs
-rw-rw-r--  1 zdan zdan    206 11月 10 16:17 package.json
-rw-rw-r--  1 zdan zdan    104 11月 10 16:17 README.md
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 src
---
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  373 11月 10 16:17 crashes-2026-11.csv


TOOL read: {"path": "/tmp/pf-34-with_skill-2lvn3z_z/logs/crashes-2026-11.csv"}

TOOL bash: {"command": "cd /tmp/pf-34-with_skill-2lvn3z_z && cat package.json README.md && ls -la src && echo \"--- files ---\" && for f in src/*; do echo \"=== $f ===\"; cat \"$f\"; done"}

RESULT: date,app_version,error,count
2026-11-01,2.3.0,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",412
2026-11-01,2.3.0,"ChunkLoadError: Loading chunk 7 failed",88
2026-11-03,2.3.1,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",377
2026-11-05,2.3.1,"RangeError: Maximum call stack size exceeded at cart.ts:41",19


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
# acme-web

React + TypeScript 前端。`npm test` 跑 vitest。
Node 版本见 package.json engines。
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  441 11月 10 16:17 login.ts
--- files ---
=== src/login.ts ===
export function mountLogin(root: HTMLElement) {
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


TOOL bash: {"command": "cd /tmp/pf-34-with_skill-2lvn3z_z && date +%F && git rev-parse --show-toplevel 2>&1 | head -2 && ls -a && echo \"--- logs total ---\" && awk -F, 'NR>1{c[$3]+=$4} END{for(k in c) print c[k], k}' logs/crashes-2026-11.csv && awk -F, 'NR>1{s+=$4} END{print \"total\", s}' logs/crashes-2026-11.csv"}

RESULT: 2026-11-10
fatal: not a git repository (or any of the parent directories): .git
.
..
logs
package.json
README.md
src
--- logs total ---
789 "TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5"
88 "ChunkLoadError: Loading chunk 7 failed"
19 "RangeError: Maximum call stack size exceeded at cart.ts:41"
total 896


TOOL write: {"path": "/tmp/pf-34-with_skill-2lvn3z_z/local/plans/fix-top-login-crash.md", "content": "# Plan: 修掉最高频的登录崩溃\n\n- Asked: 把 logs 里那个最多的崩溃修掉\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\nHand over: 按原请求 —— `TypeError: cannot read 'name' at login.ts:5`，789/896 条事件（88%），2.3.0 与 2.3.1 都在发生，说明 2.3.1 没修到\nFallback: 只加最小空值保护，不动会话/跳转流程\nDepth: 原始材料 = `logs/crashes-2026-11.csv`，按错误签名聚合而不是按行看（412+377 是同一条）；仪器 = 一个坏 token / 无 `user` 的 session 响应，写成 vitest 用例，修复前必须失败；stretch = 用例覆盖 401 与「200 但无 user」两条路径，而不只是 `s.user` 为 null\nRange: not needed\nJudge: 你已授权自检 → 我跑测试：修复前复现日志里的形状必须红，修复后绿；并附上「测试能复现线上那条堆栈」的截图/输出。局限：这个检查只证明不再抛错，不证明用户被正确引导去重新登录——这一条不算评分，只是提醒\nNeeds: `package.json` 有 `test: vitest run` 但既无 vitest/vite 依赖也无测试文件 → 需装依赖（缺失）；`cart.ts:41` 的源码不在 `src/` 里，第三条崩溃本次修不了（也不是最高频那条）\nProposed:\n1. 只加 guard，还是「session 里没有 user → 当作未登录，跳登录页」？后者改行为，但能让你从 CSV 里看到这条真正归零\n2. 加回归测试（会改 `package.json` 并装 vitest）\nDeclined: —\n\n## Task\nPurpose:\nContext: （我查到的，待你确认）acme-web 前端 React+TS，版本 2.3.1，崩溃点在 `mountLogin` 里 `.then(s => s.user.name)`；`/api/session` 在 token 失效时的返回约定未知\nMaterials: 一手 = `logs/crashes-2026-11.csv`、`src/login.ts`；缺口 = 后端 `/api/session` 的响应约定（401？200+空 body？）\nBoundaries:\nDone:\n\n## Open\n- **Purpose**：这条崩溃归零，是为了不再有人卡在登录页，还是为了把 2.3.x 的崩溃率压到某个数？前者决定要修流程，后者只需要 guard。\n- **Boundaries**：「不算修好」的样子是什么——比如不许改登录跳转、不许动后端、不许改 `/api/session` 契约？\n- **Done**：你说「你自己检查一下」，检查到什么算停？测试绿就停，还是要给出 2.3.1 之后 CSV 里这条归零的证据（那就需要线上数据，不是这个仓库能给的）。\n\nReady: no —— Proposed 两条未裁定，Purpose / Boundaries / Done 为空。\n"}

RESULT: Successfully wrote to /tmp/pf-34-with_skill-2lvn3z_z/local/plans/fix-top-login-crash.md

ASSISTANT: 计划写在 `/tmp/pf-34-with_skill-2lvn3z_z/local/plans/fix-top-login-crash.md`。

先说查到的事实（这些不用你回答）：
- 最高频的是 `TypeError ... reading 'name' at login.ts:5`，412+377 = **789/896（88%）**，两个 date、2.3.0 和 2.3.1 都有 → 2.3.1 没修到
- 出错点就在本仓库 `src/login.ts:5`：`.then(s => root.innerHTML = renderForm(s.user.name))`，`s.user` 为空时炸
- `package.json` 写了 `test: vitest run`，但没有 vitest 依赖、也没有测试文件
- `cart.ts:41`（第三条，19 条）的源码不在 `src/` 里

你让我自己检查，我可以跑一个「修复前必须红、修复后绿」的用例来当判据。但有三件事只有你能定：

1. **只加 guard，还是把「session 里没有 user」当作未登录跳登录页？** guard 只是让它不抛错，用户还是卡在空白表单；跳登录才是让这条从 CSV 里消失。
2. **什么不算修好？**（不许改登录跳转？不许动后端契约？）
3. **检查到什么算停？** 测试绿就停，还是要 2.3.1 上线后这条归零的证据——后者这个仓库给不了。

Ready: no。你回这三条我就动手；或者回一句「就加 guard，测试绿即停」，我就按这个做。