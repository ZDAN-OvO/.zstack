计划已写好：`local/plans/login-crash-fix.md`

要点（已按你的约束把上一轮"往上修"记为 Declined，不并入本次范围）：

- **范围**：只修 `src/login.ts:5` 的 `TypeError`。日志里同签名 789 次（11/01–11/03），是最高频；ChunkLoadError 88 次、`cart.ts:41` 19 次明确排除。
- **深度**：真正会再崩的不是 `s.user.name` 这一处，而是守卫打错层——`fetch` 对 401/500 也 resolve、`r.json()` 遇 HTML 错误页会抛、`s` 自身可能是 `undefined`。回归测试要用 `{}` / `{user:null}` / `{user:{}}` / 非 JSON / 非 2xx 做 fixture，并验证它在旧代码上失败。
- **三个缺口**（挡住 Ready）：
  1. 缺 user 时该显示什么（跳登录 / 空表单 / 错误提示）——只有你能定，这是唯一意图缺口；
  2. 当前目录不是 git 仓库，PR 无处可开；
  3. `package.json` 里没有 vitest 依赖、`src/` 无测试文件，`npm test` 现在跑不起来。

`Ready: no`。等你定完第 1 条、并确认 2/3 怎么补，我再改成 yes 并开工；也可以接着用 `/define-goal` 以这份 plan 为源。