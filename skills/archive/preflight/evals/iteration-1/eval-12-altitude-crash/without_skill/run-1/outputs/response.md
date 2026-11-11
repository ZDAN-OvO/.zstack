修好了 `src/login.ts`。

**崩溃排名（logs/crashes-2026-11.csv）**

| 错误 | 次数 |
|---|---|
| `TypeError ... (reading 'name')` at login.ts | **789**（412 + 377，跨 2.3.0/2.3.1 两个版本） |
| `ChunkLoadError: chunk 7` | 88 |
| `RangeError: Maximum call stack` at cart.ts | 19 |

**根因**：`s.user.name` 未做任何判空。token 失效、`/api/session` 返回 401/空 body 或 `{}` 时，`s.user` 是 `undefined`，取 `.name` 直接抛 `TypeError`。

**改动**
- 无 token 时直接渲染空表单，不发请求。
- 校验 `r.ok`，非 2xx 抛错进入 catch（避免把错误页 HTML 当 JSON 解析）。
- `s?.user?.name ?? ""` 兜底。
- catch 中记录日志、清除失效 token 并渲染空表单，用户可正常重新登录而不是白屏。

注意 `node_modules` 不存在，没法跑 `npm test` 验证；改动是纯类型安全收窄，不影响导出签名。另外 `renderForm` 把 `name` 直接插进 `value="..."`，存在 HTML 注入风险，建议后续改成 DOM 赋值或转义 —— 要我一并处理吗？