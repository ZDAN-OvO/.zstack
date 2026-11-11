仓库和日志都看过了，先给结论：**"偶尔白屏"在日志里其实有两个不同来源，你要修的可能是第二个。**

- `login.ts:5` 的 `s.user.name`：`/api/session` 返回不带 `user` 的 body（401 错误体之类）就抛 TypeError；`fetch` 没查 `r.ok`、没有 `.catch`，链静默失败，`root` 留空 → 白屏。两天 789 次，2.3.1 也没修 —— 这个**不偶尔**，是主路径。
- `ChunkLoadError: Loading chunk 7 failed` 88 次，只在 2.3.0：典型发布后旧标签页取不到旧 chunk，这个才更像"偶尔"。
- 顺带：`cart.ts:41` 的 RangeError（19 次）与登录无关；`renderForm` 把 name 未转义拼进 `innerHTML`；无 token 时发 `Bearer null`。

计划写在 `local/plans/login-white-screen.md`（工作区代码我没动）。需要你回四件事：

1. 目标是"登录页绝不白屏"，还是"把 crash 数降下来"？
2. 白屏是在哪一步——一打开就白、提交后白、还是刷新后白？（决定 ChunkLoadError 是不是你说的那个"偶尔"）
3. 会话失败时页面应该显示登录表单，还是错误页＋重试？
4. ChunkLoadError 一起修吗？`cart.ts:41` 算不算范围内？

定了之后可以 `/define-goal` 拿这份计划当输入。