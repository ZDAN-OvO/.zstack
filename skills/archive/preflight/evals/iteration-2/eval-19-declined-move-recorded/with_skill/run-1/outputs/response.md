按你的边界写好了，只修这一个，不再往上抬。

`local/plans/fix-login-session-crash.md`

写计划时查到几条你需要知道的硬事实：
- 789 / 896 次崩溃都是它（88%），2.3.0 有 412、2.3.1 有 377，**升级没修掉它**
- 日志写 `login.ts:5`，但真正抛错的是 `src/login.ts:6` 的 `s.user.name`，堆栈行号是打包后的
- **这里不是 git 仓库**，`package.json` 里有 `"test": "vitest run"` 却没有 vitest 依赖，也没有任何测试文件 —— 你的 Done（带回归测试的 PR）现在缺落脚点

计划里留了一个待裁决项（在解析处校验 session 形状，而不是在取值处加 `?.`）和 5 条 Open。Ready 是 no：把「PR 开哪个仓库」和「拿不到 user 时页面显示什么」定下来就能开工。

确认 Ready 后，可以用 `/define-goal` 把这份 plan 当输入。