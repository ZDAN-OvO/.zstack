TOOL bash: {"command": "ls -la; echo '---'; ls -R logs src 2>/dev/null | head -50"}

TOOL bash: {"command": "cat src/login.ts 2>/dev/null; echo '--- LOGS ---'; head -40 logs/*.csv 2>/dev/null"}

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
--- LOGS ---
date,app_version,error,count
2026-11-01,2.3.0,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",412
2026-11-01,2.3.0,"ChunkLoadError: Loading chunk 7 failed",88
2026-11-03,2.3.1,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",377
2026-11-05,2.3.1,"RangeError: Maximum call stack size exceeded at cart.ts:41",19


TOOL bash: {"command": "cat package.json; echo '---'; cat README.md; echo '--- tail logs ---'; tail -8 logs/crashes-2026-11.csv"}

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
--- tail logs ---
date,app_version,error,count
2026-11-01,2.3.0,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",412
2026-11-01,2.3.0,"ChunkLoadError: Loading chunk 7 failed",88
2026-11-03,2.3.1,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",377
2026-11-05,2.3.1,"RangeError: Maximum call stack size exceeded at cart.ts:41",19


ASSISTANT: ## Plan：修 login.ts:5 的 TypeError（唯一崩溃）

### 1. 事实核对（已读素材）

- `logs/crashes-2026-11.csv` 共 4 条记录、896 次：`login.ts:5` 的 `Cannot read properties of undefined (reading 'name')` 占 789 次（2.3.0: 412 + 2.3.1: 377），是最多的一条。其余 `ChunkLoadError`（88）和 `cart.ts:41 RangeError`（19）本次不处理。
- 崩溃点：`src/login.ts:5` → `s.user.name`。`/api/session` 偶尔返回不带 `user` 的 body（或 `null`），`s.user` 为 `undefined`，`.name` 即抛错，整个登录页白屏。
- 修复面只在前端单文件，符合“不改后端”。

### 2. 目标与验收

- 目标：演示路径上登录页不再因 session 缺 `user` 而崩。
- 完成判据（DoD）：
  1. `mountLogin` 在 `user` 缺失时**不抛错**，渲染一个可用的降级界面（登录表单占位），控制台不再出现该 TypeError。
  2. 新增 1 个回归测试：mock `fetch` 返回 `{}`（无 `user`），断言 `mountLogin` 不 throw 且 DOM 被渲染。
  3. PR 只包含 `src/login.ts` + 1 个测试文件（+ 测试依赖），不含后端与其他崩溃的改动。
- 上线后指标：下一个版本 `login.ts:5` TypeError 计数 = 0（不承诺总崩溃为 0）。

### 3. 步骤

1. **改 `src/login.ts`（最小改动）**
   - 把 `s.user.name` 改为可选读取，例如 `s?.user?.name ?? ""` / 提前 `if (!s?.user) { root.innerHTML = renderForm(""); return; }`。
   - 保持函数签名与调用方不变；不引入状态管理、不改路由。
   - 顺带确认 `fetch` 失败/非 2xx 不会产生第二个未捕获异常（加一个 `.catch` 兜底到同一降级界面），仍在同文件内。
2. **补测试基建**（当前 `package.json` 有 `test: vitest run` 但无 vitest 依赖，也无测试目录）
   - devDependencies 加 `vitest`、`jsdom`（或 `happy-dom`），加最小 vitest 配置。
   - 新建 `src/login.test.ts`：用例 = session 返回 `{}` → 不抛错 + 表单存在；再加一个正常返回 `{user:{name:"x"}}` 的用例，防止把正常路径改坏。
3. **本地验证**：`npm test` 全绿、`npm run build` 通过。
4. **提 PR**：标题 `fix(login): don't crash when /api/session has no user`；描述里贴日志占比（789/896）与“只修这一个”的范围声明。

### 4. 风险与回滚

- 风险低：降级界面在 `user` 缺失时展示空用户名表单，用户可重新登录，行为可从“白屏”变为“可操作”。
- 风险点：`renderForm` 用 `innerHTML` 拼接 `name`；本次不改，仅记录（若演示要求严格可另开 issue）。
- 回滚：单文件改动，revert 该 commit 即恢复原状。

### 5. 明确不做

- 不改 `/api/session` 后端返回契约；不修 `ChunkLoadError`；不修 `cart.ts:41`；不做“零崩溃”整体治理。演示后再单独立项。

要我现在按这个 plan 动手改 `src/login.ts` 并加测试吗？