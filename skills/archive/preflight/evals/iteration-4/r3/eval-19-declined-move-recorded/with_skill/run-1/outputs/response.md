已写：`/tmp/pf-19-with_skill-1xv1tkm8/local/plans/login-null-user-crash.md`

核对材料时发现三处值得改的地方：

1. **栈行号错一行**：日志写 `login.ts:5`，真正读 `s.user.name` 在 `login.ts:6`。按栈行号改会改到 `fetch` 那行上。11 月这个错 **789 次**（412 + 377），占日志绝大多数。
2. **PR 提不出来**：这目录不是 git 仓库（`git rev-parse` 失败），`git init` 还是推远端，你定。
3. **测试跑不起来**：`npm test` 指向 `vitest run`，但 devDependencies 里没有 vitest。装它要改 `package.json` + lockfile。

Ready 还是 **no**，卡在两点：Depth/Range 你没过目（我只提了一个便宜的"测试先行"：先喂 `{}` 让测试失败、再改代码，省得改动看着过了其实没修），以及 **session 缺 user 时 UI 要什么**——空表单、跳登录还是提示重试？这一条直接决定改法，你给一句话我就把它补进计划并翻成 Ready: yes。

要不要接着用 `/define-goal`，以这份 plan 为源？