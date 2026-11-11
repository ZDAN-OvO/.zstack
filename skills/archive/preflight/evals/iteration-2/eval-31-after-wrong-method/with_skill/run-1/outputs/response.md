我把这次拒收按“方法不足”处理，原地改了 `local/plans/login-whitescreen.md`。

查到的关键事实（日志里本来就有，上一轮没用上）：
- `TypeError: ...reading 'name' at login.ts:5` —— 2.3.0 有 412 次，2.3.1 有 377 次。两个版本都在，不是新版本引入的回归。
- 代码里唯一读 `.name` 的是 `.then` 里的 `s.user.name`，推断 `/api/session` 在 401 或返回无 `user` 的 body 时 `s.user` 为 undefined（推断，待复现确认）。
- 另一条 `ChunkLoadError` 88 次只出现在 2.3.0，也是独立的白屏来源，没算进来。

改了四处：
- **Depth**：从“先看崩溃日志”改成具体的定位法 —— 日志做 error×version 计数、只处理占比 1% 以上、mock 三种响应形态喂 `mountLogin`；拉伸目标是一条改动前就失败的用例。
- **Judge**：换成红绿判据（三条用例在旧代码上必须失败）+ 只拿日志和 diff 判根因的外部会话。上一版“测试通过”就是让骨架屏混过去的口子。
- **Boundaries**：明确写了“不用骨架屏/兜底文案掩盖错误”。
- **Tries**：加了一行日期、结论和改动。

两件事等你拍板：
1. 新的 Depth 与 Judge 认不认。
2. `ChunkLoadError` 那 88 次算不算这次范围内；不算的话 Done 里要写明排除。

确认 Ready 后可以用 `/define-goal`，以这份计划为源。