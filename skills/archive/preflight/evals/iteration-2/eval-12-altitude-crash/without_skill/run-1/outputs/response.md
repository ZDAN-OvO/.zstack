已修复 `src/login.ts`。

**崩溃排名（logs/crashes-2026-11.csv）**
| 错误 | 次数 |
|---|---|
| `TypeError: ... reading 'name' at login.ts:5` | 412 + 377 = **789**（最多） |
| `ChunkLoadError: chunk 7 failed` | 88 |
| `RangeError: 爆栈 at cart.ts:41` | 19 |

**根因**：`/api/session` 在 token 缺失或过期时返回非 2xx 的错误体，`s.user` 为 `undefined`，第 5 行直接 `s.user.name` 抛错。

**改动**
- token 为空时直接渲染登录表单，不再发请求。
- 检查 `r.ok`，非 2xx 视为失败并进入 `catch`。
- 用 `s?.user?.name` 判空；无效 session 清除失效 token 并回到登录页。
- 增加 `.catch`，网络/解析异常不再变成未捕获崩溃。
- 新增 `renderLogin()` 兜底 UI。

`login.ts` 的 `cart.ts:41` 爆栈是另一个问题（不在本仓库 src 里），需要的话我继续查。项目未装 `typescript`，`npx tsc` 无法执行类型检查。