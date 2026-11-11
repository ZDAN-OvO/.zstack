已修改 `src/login.ts`，具体改动：

1. **兜底渲染**：整个会话加载放进 `try/catch`，任何失败（网络错误、非 2xx、JSON 解析失败）都会渲染空白登录表单，不再白屏。
2. **空值安全**：`session?.user?.name ?? ""`，`user` 缺失时用空字符串，消除了日志里的 `TypeError ... reading 'name'`。
3. **HTTP 状态检查**：`res.ok` 为 false 时不再把错误 body 当 session 解析（401 时 body 通常没有 `user`）。
4. **无 token 处理**：`localStorage` 没有 token 时不发送 `Bearer null` 请求头。
5. **顺带修了 XSS**：`name` 被插进 `value="..."`，新增 `escapeAttr` 防止用户名里的引号/尖括号破坏 HTML（这也是白屏/渲染异常的潜在来源）。

还有一点建议：日志里 `ChunkLoadError: Loading chunk 7 failed`（88 次）是另一个独立问题，通常需要路由级错误边界 + 重试加载，不在本文件范围内，需要的话我可以一起看。