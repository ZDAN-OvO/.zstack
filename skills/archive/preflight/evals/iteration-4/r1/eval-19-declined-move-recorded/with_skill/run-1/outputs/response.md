Plan 已写好：`local/plans/demo-no-crash-login.md`

要点：

- **Altitude 已按你的意愿放平**：只修 `login.ts:5`，升到"登录页零崩溃"已记为 Declined，附你的理由。
- **一个事实要你知道**：第 5 行其实是三条未处理路径（`s.user` 缺失、`r.ok` 非 2xx、`fetch` reject），只加 `?.` 只挡第一条。Depth 建议按形状建模而不是就地判空，你决定要不要。
- **两个缺口**：当前目录不是 git repo（PR 无载体），vitest 也没装。
- **Ready: no** — 等你裁决 Depth / Range / Judge 三项 + 两个缺口。

确认 Ready 后可以接 `/define-goal`，以这份 plan 为输入。