TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/SKILL.md"}

TOOL bash: {"command": "pwd && ls -la && ls -la src 2>/dev/null"}

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


RESULT: /tmp/pf-4-with_skill-vpqlmqie
total 188
drwxrwxr-x  4 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 59 root root 167936 11月 10 20:51 ..
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 logs
-rw-rw-r--  1 zdan zdan    206 11月 10 16:17 package.json
-rw-rw-r--  1 zdan zdan    104 11月 10 16:17 README.md
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 src
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  441 11月 10 16:17 login.ts


TOOL bash: {"command": "cat src/login.ts; echo ---; cat package.json; echo ---; cat README.md; echo ---; ls -la logs"}

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
---
# acme-web

React + TypeScript 前端。`npm test` 跑 vitest。
Node 版本见 package.json engines。
---
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  373 11月 10 16:17 crashes-2026-11.csv


TOOL bash: {"command": "cat logs/*.csv"}

RESULT: date,app_version,error,count
2026-11-01,2.3.0,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",412
2026-11-01,2.3.0,"ChunkLoadError: Loading chunk 7 failed",88
2026-11-03,2.3.1,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",377
2026-11-05,2.3.1,"RangeError: Maximum call stack size exceeded at cart.ts:41",19


TOOL bash: {"command": "date +%F; git rev-parse --show-toplevel 2>/dev/null; ls -la local/plans 2>/dev/null || echo \"no local/plans\"; find . -name \"*.test.*\" -o -name \"*.spec.*\" | grep -v node_modules || echo \"no test files\""}

RESULT: 2026-11-10
no local/plans
no test files


TOOL write: {"path": "/tmp/pf-4-with_skill-vpqlmqie/local/plans/login-white-screen.md", "content": "# Plan: 登录页不再白屏\n\n- Asked: 帮我修一下登录页偶尔白屏的 bug，代码在 src/login.ts\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\n\nHand over: 登录页的每条会话失败路径都渲染确定界面（表单 / 错误提示 / 自动重试一次），失败有记录——而不是只补 `login.ts:5` 那一行。\nFallback: 只加一行保护 `s.user?.name ?? \"\"`。能挡住 789 次 TypeError，挡不住 ChunkLoadError 白屏。\nDepth: 原始材料 = `logs/crashes-2026-11.csv`。方法 = 按失败类型分类修（401 有 error body / 返回非 JSON / 网络 reject / 旧 chunk 404），用 mock fetch 的 vitest 复现每种 payload。拉伸点 = 用日志计数检验\"偶尔\"这个判断（11-03 单日 377 次，说明 TypeError 是主路径，不是罕见现象）。\nRange: 动词 =「root 不留空」「用户仍能登录回去」「失败在日志里可见」。crew = 前端可靠性（错误态）＋安全（name 转义）＋运维（chunk 失效/发布策略）；红队专门用 401、HTML 响应、超时、旧 chunk 打这个修复。\nJudge: vitest 断言四种失败 payload 下 root 都有内容，外加一次手动复现（本地让 `/api/session` 返 401 或断网）。按\"是否区分了失败类型\"评分，不只看白屏是否消失。\nNeeds: 缺 ChunkLoadError 与发布时间的对应关系（CSV 里没有 deploy 时间戳）；缺错误上报（Sentry？）与可复现环境；仓库目前没有任何测试文件，测试要新写。\nProposed: ① ChunkLoadError 是否一起修（一次 reload 兜底 + 版本探针，会动 login.ts 之外）？② `cart.ts:41` 的 RangeError 是否在范围内？\nDeclined: —\n\n## Task\n\nPurpose: （待确认）\nContext: 已查明，请你确认——\n- `login.ts:5` 的 `s.user.name`：`/api/session` 返回不含 `user` 的 body 时（401 错误体等）抛 TypeError；`fetch` 没查 `r.ok`、没有 `.catch`，promise 链静默失败，`root` 保持空 → 白屏。日志行号与它一致，2.3.0/2.3.1 两天合计 789 次，2.3.1 仍未修。\n- `ChunkLoadError: Loading chunk 7 failed` 88 次，只出现在 2.3.0，像发布后旧标签页取不到旧 chunk——这个更贴合你说的\"偶尔\"。\n- `cart.ts:41` 的 RangeError 19 次，与登录无关。\n- 另外两处隐患：`renderForm` 把 name 直接拼进 `innerHTML`（未转义）；无 token 时会发 `Bearer null`。\nMaterials: `logs/crashes-2026-11.csv`（唯一一手数据，已读）；`src/login.ts`；`package.json` / `README.md`；缺：前端错误上报、复现环境、发布记录。\nBoundaries: （待确认）\nDone: 建议——先给你失败分类＋改动清单（早期 checkpoint）→ 改代码并新增 vitest 用例覆盖 401 / 500 / 网络失败 / 缺 user 字段 → `npm test` 通过，且手动复现不再白屏。\n\n## Open\n\n1. Purpose：这次要的是\"登录页绝不白屏\"，还是\"把 crash 数降下来\"？两者范围不同。\n2. 白屏发生在哪一步——一打开就白 / 输入提交后白 / 刷新后白？这决定 ChunkLoadError 是不是你说的那个\"偶尔\"。\n3. 会话失败时页面显示什么：直接出登录表单，还是错误页＋重试按钮？\n4. ChunkLoadError 一起修吗？`cart.ts:41` 算范围内吗？\n5. （可选）有没有 Sentry 之类的上报，能定位到 URL 和版本？\n\nReady: no — 需要你回答 Open 1–4（第 5 条可选）。\n"}

RESULT: Successfully wrote to /tmp/pf-4-with_skill-vpqlmqie/local/plans/login-white-screen.md

ASSISTANT: 仓库和日志都看过了，先给结论：**"偶尔白屏"在日志里其实有两个不同来源，你要修的可能是第二个。**

- `login.ts:5` 的 `s.user.name`：`/api/session` 返回不带 `user` 的 body（401 错误体之类）就抛 TypeError；`fetch` 没查 `r.ok`、没有 `.catch`，链静默失败，`root` 留空 → 白屏。两天 789 次，2.3.1 也没修 —— 这个**不偶尔**，是主路径。
- `ChunkLoadError: Loading chunk 7 failed` 88 次，只在 2.3.0：典型发布后旧标签页取不到旧 chunk，这个才更像"偶尔"。
- 顺带：`cart.ts:41` 的 RangeError（19 次）与登录无关；`renderForm` 把 name 未转义拼进 `innerHTML`；无 token 时发 `Bearer null`。

计划写在 `local/plans/login-white-screen.md`（工作区代码我没动）。需要你回四件事：

1. 目标是"登录页绝不白屏"，还是"把 crash 数降下来"？
2. 白屏是在哪一步——一打开就白、提交后白、还是刷新后白？（决定 ChunkLoadError 是不是你说的那个"偶尔"）
3. 会话失败时页面应该显示登录表单，还是错误页＋重试？
4. ChunkLoadError 一起修吗？`cart.ts:41` 算不算范围内？

定了之后可以 `/define-goal` 拿这份计划当输入。