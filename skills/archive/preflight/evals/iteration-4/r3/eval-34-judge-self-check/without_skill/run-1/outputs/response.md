修完了，并且我自己做了验证。

**定位**：`logs/crashes-2026-11.csv` 里 `TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5` 合计 789 次（2.3.0 的 412 + 2.3.1 的 377），是第二名的 ~9 倍，且跨版本仍在发生 → 就是它。

**根因**：`src/login.ts:5` 无条件读 `s.user.name`。未登录 / token 过期时 `/api/session` 返回 401 或 `{}`，`s.user` 为 `undefined`，渲染即崩，登录页整个白屏（连表单都出不来，用户无从登录 —— 所以量这么大）。另外 `fetch` 失败时没有 `.catch`，网络抖动会变成 unhandled rejection。

**改动**（仅 `src/login.ts`）：
- 非 2xx 响应不再 `json()` 解析
- `s?.user?.name ?? ""` 兜底，缺少会话时渲染空表单而不是抛错
- 补 `.catch`，失败也降级到空表单

**验证**：本机无 `node_modules`（`npm test` 跑不了 vitest），所以用 Node 26 原生 TS 直接跑了一个临时 harness，覆盖 5 种响应 × 有/无 token：
- 修复前：`TypeError: Cannot read properties of undefined (reading 'name')`，进程退出码 1 —— 与线上日志同一行
- 修复后：10/10 通过，全部渲染出 `<form>`，正常登录仍正确渲染 `alice`，退出码 0

**顺带发现但未改动**：`renderForm` 把 `name` 直接拼进 HTML 属性且未转义，属 XSS 面（需另行确认接口是否可信）；`cart.ts:41` 的栈溢出（19 次）和 `ChunkLoadError`（88 次）是独立问题。要我一起处理哪个说一声。