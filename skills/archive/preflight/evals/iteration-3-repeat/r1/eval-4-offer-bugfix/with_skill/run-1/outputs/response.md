我先查看了代码和日志，但还没有改动任何文件（等你确认后再动手）。

我看到的情况：
- `src/login.ts:5` 的 `s.user.name` 没有任何防御：`/api/session` 返回 401/HTML 错误页时，`s.user` 为 `undefined`，Promise 直接 reject，`root.innerHTML` 永远不会执行 → 白屏。
- `logs/crashes-2026-11.csv` 里 2.3.0/2.3.1 共 **789 次** `TypeError ... reading 'name' at login.ts:5`，是登录崩溃的绝对主力；另有 88 次 `ChunkLoadError`（是另一类白屏，发布更新时出现）。所以“偶尔”很可能对应 token 过期/会话失效这类条件，而不是随机。

要不要我先写一页 `local/plans/login-white-screen.md`（含：要修到哪一层——只补一个判空，还是把失败态、重试、ChunkLoadError 一起处理；以及用什么日志/测试判定修好了），你过一遍再让我改代码？回复“好”我就出 plan。