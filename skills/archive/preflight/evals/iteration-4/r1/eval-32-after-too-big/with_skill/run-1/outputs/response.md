已按 “After a try” 的诊断结果更新了 `local/plans/login-whitescreen.md`。

**判定：问题出在计划本身，不是执行不力——Too big。**

依据（日志统计，`logs/crashes-2026-11.csv`）：
- 789/896 是同一条：`TypeError: ... reading 'name' at login.ts:5` → `s.user` 为 undefined。
- 机制就是 `src/login.ts:4-6`：无 token 时发 `Bearer null` → 401 → 响应体没有 `user` → `.then` 抛错、无 `.catch` → `root.innerHTML` 从不写入 = 白屏（“偶尔”= 过期/缺失 token 时）。
- 真正要改的是几行 guard + 一个 401 测试。上一轮却动了 40 个文件——因为计划把 Hand over 定到“一周内该错误为 0”，这个判据在会话内不可判定，模型没有停手条件；Done 也没有早期 checkpoint；Boundaries 只拦了后端，没拦重构范围。顺带被卷进去的还有 ChunkLoadError(88) 和 cart.ts 栈溢出(19)，两者都不在这条路径上。

改了什么：
- Hand over 降到窄修：只修 401→`s.user` undefined，单 PR ≤ 2 文件；Fallback 改为“只交根因+失败测试”。
- Judge 换成可自跑的“红→绿”（新测试旧代码失败、新代码通过），“一周 0 错误”降级为事后验证。
- Boundaries 加了墙：不动 cart.ts / 打包配置 / 依赖。Done 加了 checkpoint：先交根因一句话 + 失败测试，你确认后才改代码。

需要你两件事（计划里 Ready 还是 no）：
1. 窄修 + ≤2 文件这个范围，点头还是改？
2. 那 40 文件的 diff 在哪个分支（此工作区没有 git 仓库，`src/` 只有 12 行），以及演示是哪天——我好判哪些改动该丢、是否还给 ChunkLoadError 留余量。

确认后可以用 `/define-goal` 以这份计划为源。