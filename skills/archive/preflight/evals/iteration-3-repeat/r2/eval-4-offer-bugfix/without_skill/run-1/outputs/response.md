已修复 `src/login.ts`。

**白屏根因**（与 `logs/crashes-2026-11.csv` 中的报错吻合）：

- `localStorage` 里没有 token 时，代码仍发送 `Authorization: Bearer null`，接口返回 401/无 `user` 字段。
- 响应没有做 `res.ok` 判断，也没有 try/catch；`s.user.name` 抛 `TypeError` 后 Promise 中断，`root.innerHTML` 永远不会被赋值，页面就是白屏。
- token 过期时也会走同样的路径。

**修改内容**：

- 无 token 直接渲染空白登录表单，不再发无效请求。
- 401/403 时清除失效 token 并回退到登录表单。
- 检查 `res.ok`、`session?.user?.name`，并加 try/catch 兜底，网络错误或返回结构异常时也不会白屏。
- 改用 `async/await`，避免未捕获的 Promise rejection。

另外，日志里的 `ChunkLoadError`（chunk 7）和 `cart.ts` 栈溢出是独立问题；如果白屏问题仍有偶发，建议一并排查。