已修复。

**崩溃统计**（`logs/crashes-2026-11.csv`）：
| 错误 | 次数 |
|---|---|
| `TypeError: Cannot read properties of undefined (reading 'name')` | 412 + 377 = **789** ← 最多 |
| `ChunkLoadError` | 88 |
| `RangeError: Maximum call stack size exceeded` | 19 |

**根因**：`src/login.ts:6` 直接读 `s.user.name`。当 token 缺失/过期时 `/api/session` 返回 401 或 `{ error: ... }`，`s.user` 为 `undefined`，`.then` 里抛错且无人捕获 → 整个登录页白屏崩溃。v2.3.1 仍有 377 次，说明并非旧版本遗留。

**改动**（`src/login.ts`）：
1. 无 token 时直接渲染空白登录表单，不再发无效请求。
2. 校验 `r.ok`，非 2xx 抛错走 `catch`。
3. `s?.user?.name ?? ""` 兜底，session 无效时回退到空白表单而不是崩溃。
4. 加上 `.catch` 记录错误并渲染表单（React 中未捕获的 Promise 拒绝还会冒到全局 error boundary）。

**验证**：用 Node 的类型剥离 + mock `localStorage`/`fetch` 跑了 4 个用例（401、无 user、正常 user、无 token），均不再抛错，正常用户仍渲染出名字。仓库里没有可运行的测试/依赖（无 `node_modules`，未装 vitest），所以没跑 `npm test`；另外 csv 里的 `ChunkLoadError` 和 `cart.ts` 的栈溢出属于另外两个独立问题，本次未动。