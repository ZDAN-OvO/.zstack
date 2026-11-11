你说得对，骨架屏只是遮住了症状，没有修到真正的崩溃点。日志里的白屏主因可以直接对上代码：

**根因**
- `logs/crashes-2026-11.csv`：`TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5`，2.3.0 有 412 次、2.3.1 有 377 次，是登录页最主要的崩溃。
- 原 `src/login.ts:5`：`s.user.name`。当 `/api/session` 返回 401/过期会话（响应体只有 `{error: ...}`，没有 `user`）时，这里抛异常。
- 该异常发生在 `.then()` 回调里，没有 `.catch()`，于是 `root.innerHTML = renderForm(...)` 永远不会执行，根节点保持空白 → 白屏。
- “偶尔”出现是因为只有 token 缺失/过期的用户会走到这条路径；加了 loading 骨架后，这类用户会一直停在骨架屏，反而更像白屏。

**已改**
- `src/login.ts`：检查 `r.ok`；用 `s.user?.name ?? ""` 兜底；整条链加 `.catch()`，失败也渲染登录表单，不再让异常吞掉渲染。
- 新增 `src/login.test.ts`：覆盖正常会话、401 无 `user`、200 但无 `user` 三种情况。

**验证**
用 Node 直接跑了三种响应，均能渲染出 `<form>`（401 不再空白）。但 `npm test` 目前跑不了：`package.json` 里有 `"test": "vitest run"`，却没有 vitest 依赖，也没有 `node_modules`，需要先补依赖才能执行回归测试。

**还没覆盖**
日志里另有 `ChunkLoadError: Loading chunk 7 failed`（88 次），是发版后旧 chunk 失效导致的另一条白屏路径，和本次 `user.name` 崩溃无关，需要单独的刷新/重试策略。