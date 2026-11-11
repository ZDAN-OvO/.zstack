TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/SKILL.md"}

TOOL bash: {"command": "ls -a; echo ---; ls logs src 2>/dev/null"}

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


RESULT: .
..
logs
package.json
README.md
src
---
logs:
crashes-2026-11.csv

src:
login.ts


TOOL bash: {"command": "cd /tmp/pf-19-with_skill-u6ba5_qu; git rev-parse --show-toplevel 2>&1; echo ---; cat package.json; echo ---; cat README.md; echo ---; ls -a local 2>/dev/null || echo \"no local\"; echo ---; head -20 logs/crashes-2026-11.csv; echo; wc -l logs/crashes-2026-11.csv"}

TOOL read: {"path": "/tmp/pf-19-with_skill-u6ba5_qu/src/login.ts"}

RESULT: fatal: not a git repository (or any of the parent directories): .git
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
no local
---
date,app_version,error,count
2026-11-01,2.3.0,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",412
2026-11-01,2.3.0,"ChunkLoadError: Loading chunk 7 failed",88
2026-11-03,2.3.1,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",377
2026-11-05,2.3.1,"RangeError: Maximum call stack size exceeded at cart.ts:41",19

5 logs/crashes-2026-11.csv


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


TOOL bash: {"command": "cd /tmp/pf-19-with_skill-u6ba5_qu; date +%F; awk -F, 'NR>1{gsub(/\"/,\"\",$3); s[$3]+=$NF} END{for(k in s) print s[k], k}' logs/crashes-2026-11.csv | sort -rn; echo ---; ls node_modules 2>/dev/null | head -3 || echo \"no node_modules\"; grep -rn vitest package.json || echo \"vitest not declared\""}

RESULT: 2026-11-10
789 TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5
88 ChunkLoadError: Loading chunk 7 failed
19 RangeError: Maximum call stack size exceeded at cart.ts:41
---
8:    "test": "vitest run",


TOOL write: {"path": "/tmp/pf-19-with_skill-u6ba5_qu/local/plans/fix-login-session-crash.md", "content": "# Plan: 修掉 login.ts:5 崩溃（演示不白屏）\n\n- Asked: 「修一下 logs 里出现最多的那个崩溃」；后补充：不接受往上抬，只修这一个\n- Stage: execute\n- Date: 2026-11-10\n\n## Requirement\nHand over: 按原样：只修 `s.user.name` 这一个崩溃，交付带回归测试的 PR\nFallback: 仍在 login 边界内兜底——`mountLogin` 拿不到 user 时渲染空表单/重试提示，不改 session 契约、不碰其他文件\nDepth: 建议（待裁决）在解析处收敛，而不是在取值处加 `?.`：`/api/session` 响应先过一层 shape 校验，缺 `user` 时走同一个降级分支。理由：同一个 payload 还会打坏别的字段读取。原料=真实缺 user 的响应样本（暂缺，见 Open）；量具=vitest fixture 覆盖「无 user / user 为 null / 非 JSON」\nRange: not needed（单文件单路径修复，加角色分工只会加流程不加正确性）\nJudge: 先写的 vitest 回归测试——在当前代码上必须红、修复后必须绿，所以它判的是方法而非运气。演示现场是最终判据，但不可复现，不作依据\nNeeds: 真实 session 响应样本（缺）；`package.json` 无 vitest devDependency、仓库无测试文件（需加）；git 仓库（缺，见 Open）；是否允许改 `/api/session` 之外的代码（已知不能动后端）\nProposed: Depth 一条，等你裁决\nDeclined: Altitude（抬到「登录页零崩溃 + 一周崩溃日志为 0 作判据」）——理由：下周演示，时间盒内只保演示路径\n\n**事实**：logs 共 896 次崩溃，`login.ts:5` 的 TypeError 占 789 次（412 在 2.3.0，377 在 2.3.1），88%。第二名 ChunkLoadError 88 次、第三名 cart.ts:41 19 次。日志行号 5 与代码里 `s.user.name`（`src/login.ts:6`）不齐，堆栈行号来自打包 sourcemap，修的位置以代码为准。\n\n## Task\nPurpose: 下周演示时登录页不白屏\nContext: React + TypeScript 前端（acme-web 2.3.1）；`/api/session` 偶尔返回不带 `user` 的响应；2.3.0 到 2.3.1 都还在报，不是已修问题\nMaterials: 主 `logs/crashes-2026-11.csv`（唯一一手数据）；次 `src/login.ts`；空槽：真实缺 `user` 的响应体（未找到）\nBoundaries: 不改后端；只修这一个崩溃（ChunkLoadError 88、cart.ts RangeError 19 不修）\nDone: 一个带回归测试的 PR —— 检查点顺序：先提测试（红）→ 再提修复（绿）→ 再开 PR\n\n## Open\n- 这里不是 git 仓库（无 `.git`）：这个 PR 开在哪个仓库、哪个分支？\n- 拿不到 `user` 时登录页显示什么（空输入框 / 「会话失效，请重试」/ 跳回登录）？这决定测试断言与 Done 的形态\n- 缺 `user` 的响应长什么样没人确认过，fixture 只能靠猜；能贴一条线上的实际响应吗\n- 是否允许加 `vitest` devDependency 与 `src/login.test.ts`（现在只有 `\"test\": \"vitest run\"` 脚本，没依赖也没测试文件）\n- 已知范围外风险：11-01 起还有 88 次 ChunkLoadError，演示若命中同样白屏，但按你的边界这次不动\n\nReady: no，因为 Depth 一条未裁决，且 Open 第 1、2、3 条没有答案\n"}

RESULT: Successfully wrote to /tmp/pf-19-with_skill-u6ba5_qu/local/plans/fix-login-session-crash.md

ASSISTANT: 按你的边界写好了，只修这一个，不再往上抬。

`local/plans/fix-login-session-crash.md`

写计划时查到几条你需要知道的硬事实：
- 789 / 896 次崩溃都是它（88%），2.3.0 有 412、2.3.1 有 377，**升级没修掉它**
- 日志写 `login.ts:5`，但真正抛错的是 `src/login.ts:6` 的 `s.user.name`，堆栈行号是打包后的
- **这里不是 git 仓库**，`package.json` 里有 `"test": "vitest run"` 却没有 vitest 依赖，也没有任何测试文件 —— 你的 Done（带回归测试的 PR）现在缺落脚点

计划里留了一个待裁决项（在解析处校验 session 形状，而不是在取值处加 `?.`）和 5 条 Open。Ready 是 no：把「PR 开哪个仓库」和「拿不到 user 时页面显示什么」定下来就能开工。

确认 Ready 后，可以用 `/define-goal` 把这份 plan 当输入。