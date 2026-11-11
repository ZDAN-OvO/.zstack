TOOL bash: {"command": "ls -la; echo ---; ls logs src 2>/dev/null"}

TOOL read: {"path": "src/login.ts"}

RESULT: total 188
drwxrwxr-x  4 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 64 root root 167936 11月 10 22:36 ..
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 logs
-rw-rw-r--  1 zdan zdan    206 11月 10 16:17 package.json
-rw-rw-r--  1 zdan zdan    104 11月 10 16:17 README.md
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 src
---
logs:
crashes-2026-11.csv

src:
login.ts


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


TOOL read: {"path": "logs/crashes-2026-11.csv"}

TOOL read: {"path": "package.json"}

TOOL read: {"path": "README.md"}

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


RESULT: # acme-web

React + TypeScript 前端。`npm test` 跑 vitest。
Node 版本见 package.json engines。


TOOL bash: {"command": "ls -a src; ls node_modules 2>/dev/null | head -5; ls vitest.config.* 2>/dev/null; echo \"exit:$?\""}

RESULT: .
..
login.ts
exit:2


TOOL write: {"path": "PLAN.md", "content": "# Plan: 修复 session 缺 `user` 导致的登录页崩溃（单崩溃、带回归测试）\n\n## 目标（唯一判据）\n演示时登录页不再崩溃：`/api/session` 返回体缺少 `user` 时，`mountLogin` 不抛异常，页面正常渲染。\n\n## 不做什么（明确出界）\n- 不改后端、不改 `/api/session` 契约，不加重试/缓存层。\n- 不动 `ChunkLoadError`（88 次）和 `cart.ts:41` 的 `RangeError`（19 次）。\n- 不做登录页整体重构、不加错误上报埋点、不追求\"一周崩溃为 0\"。\n- 不加 timeout / AbortController 之类新行为（除非实现时发现必须）。\n\n## 事实依据\n`logs/crashes-2026-11.csv`：\n\n| error | count |\n|---|---|\n| `TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5` | 789（412 + 377） |\n| `ChunkLoadError` | 88 |\n| `RangeError at cart.ts:41` | 19 |\n\n最多即 `login.ts:5`，占本月约 88%，与用户描述的\"session 接口偶尔不返回 user\"一致。\n\n根因（`src/login.ts:5`）：\n\n```ts\n.then((s) => { ... root.innerHTML = renderForm(s.user.name); });\n```\n\n`s.user` 为 `undefined` 时读 `.name` 直接抛 TypeError，整页白屏。\n\n## 改动（1 个文件，约 3 行）\n`src/login.ts`：\n\n1. `s?.user?.name` → 取不到时用安全默认值 `\"\"`（而不是抛错）。\n2. `fetch` 结果补一层健壮性：`r.ok` 为 false 或 `r.json()` 失败时，同样走\"无 user\"分支，不产生未处理的 rejection（`.catch`）。\n3. `renderForm` 入参类型保持 `string`，默认值兜底在调用点完成，签名不变。\n\n保持公开 API `mountLogin(root)` 不变，调用方零改动。\n\n## 回归测试（先红后绿）\n现状障碍：`vitest` 在 `scripts.test` 里被调用，但 `package.json` 的 `dependencies` 只有 `react`，仓库无 `node_modules`、无 `vitest.config.*`。因此测试前需先补最小测试基建。\n\n1. `package.json` 增加 `devDependencies`: `vitest`、`typescript`（版本实现时按 Node >= 20 选取），保留已有 `test` 脚本不动。\n2. 新增 `src/login.test.ts`，用 `vi.stubGlobal` 打桩 `fetch` 与 `localStorage`，用 `{ innerHTML: \"\" }` 作为 `root`，避免引入 jsdom：\n   - case A（复现崩溃，修复前失败）：`fetch` 返回 `{}` → `await` 冲刷微任务后断言未抛错，且 `root.innerHTML` 含 `<form>`。\n   - case B（正常路径不回归）：返回 `{ user: { name: \"Ann\" } }` → 断言 `value=\"Ann\"`。\n   - case C（接口异常）：`fetch` 返回 `ok: false` 或 `json()` reject → 断言未抛未处理的 rejection，仍渲染表单。\n3. 先只加 case A 跑一次，确认在未修复的 `login.ts` 上**失败**（证明测试真的覆盖了这个崩溃），再改 `login.ts` 让它转绿。\n\n## 验证\n- `npm test` 全绿（3 个 case）。\n- `npm run build` 通过（TypeScript 未因可空性改动报错）。\n- 手工冒烟：本地把 `/api/session` 响应 mock 成 `{}`，登录页可渲染、控制台无 TypeError。\n- 不做长周期崩溃率观测——演示前只看上面三条。\n\n## 交付（一个 PR）\n- 分支：`fix/login-session-missing-user`\n- 内容：`src/login.ts`、`src/login.test.ts`、`package.json`/lock 的 devDeps；可选 `vitest.config.ts`（若需要 `environment: \"node\"` 默认即可则不加）。\n- PR 描述：崩溃条数与占比 → 根因一行 → 改动 diff → 测试红转绿证据（贴修复前失败、修复后通过两次输出）→ 明确写出\"本次只修 login.ts:5，其余两个崩溃另开 issue\"。\n- 评审关注点小、可 10 分钟内合入，符合下周演示的时间约束。\n\n## 风险与回退\n- 风险：默认值 `\"\"` 会让\"session 异常\"看起来像\"新用户空名字\"。可接受——演示优先不崩；后续单独做提示/登录跳转。\n- 回退：单文件改动，`git revert` 该 commit 即恢复原状，不影响后端与其他页面。\n"}

RESULT: Successfully wrote to PLAN.md

ASSISTANT: 计划已写入 `PLAN.md`，要点如下：

**范围**：只修 `src/login.ts:5` 的 `TypeError`（日志里 412+377=789 次，占本月约 88%）。`ChunkLoadError`(88) 和 `cart.ts:41`(19) 另开 issue，不动。

**根因**：`.then((s) => root.innerHTML = renderForm(s.user.name))`，`user` 为 `undefined` 时读 `.name` 抛错导致白屏。

**改动**：单文件约 3 行 —— `s?.user?.name` 取不到时回退 `""`，并给 `fetch`/`json()` 加 `.catch` 与 `r.ok` 分支；`mountLogin(root)` 与 `renderForm(name: string)` 签名不变。

**回归测试**：先要补基建 —— `vitest` 只在 `scripts.test` 里被调用，但 `package.json` 只有 `react` 依赖，`node_modules`、`vitest.config.*` 都不存在，所以 PR 里要加 devDeps。测试用 `vi.stubGlobal` 打桩 `fetch`/`localStorage` + `{innerHTML:""}` 当 root，不需要 jsdom；三个 case：缺 `user`（修复前必红）、正常路径不回归、接口异常不产生未处理 rejection。要求先看到 case A 失败再改代码。

**完成判据**：`npm test` 全绿 + `npm run build` 通过 + 本地 mock `{}` 冒烟；不做长周期崩溃率观测，不把"一周为 0"当门槛。

**PR**：分支 `fix/login-session-missing-user`，描述里贴红转绿的两次输出，并写明其余两个崩溃另开 issue。