计划已写好：`local/plans/login-white-screen.md`

查到的关键事实（这些不是提问，是证据）：

- `src/login.ts:3-6` — `getItem("token")` 可为 `null` → `Bearer null` → 非 2xx 时响应体里没有 `user` → `s.user.name` 抛 TypeError，且没有 `.catch`，所以 `root.innerHTML` 永不执行 = 白屏。
- `logs/crashes-2026-11.csv` — `reading 'name' at login.ts:5` 在 2.3.0 出现 412 次、2.3.1 仍是 377 次：**2.3.1 并没有修掉它**，这是主因。
- 同一份日志里有 **88 次 `ChunkLoadError: Loading chunk 7 failed`** —— 第二种白屏原因，不在 `login.ts` 里。「偶尔」可能是两个 bug。
- 仓库没有测试目录、vitest 未安装（`npm test` 现在跑不起来）、`/api/session` 无后端、无路由/错误边界；`login.ts` 是裸 DOM 操作（README 说是 React）。

需要你裁决的三条轴（抄在计划里，接受/改写/拒绝都行）：

1. **Altitude**：直接交结果 ——「所有失败路径都渲染可恢复界面 + 按原因打点 + 修前必红/修后必绿的测试」，还是退一格只止血（判空 + `r.ok` 兜底）？天花板我试到「含 ChunkLoadError 与部署缓存/SLO」，那需要后端契约和发布配置，超出我能自主验证的范围。
2. **Depth**：专家动作是**先分离因果再改**，拉伸目标是失败注入矩阵先红后绿 —— 只加 `?.` 的"侥幸修复"会被判不合格。
3. **Range**：定位 / 兜住 / 预防 / 观测四个动词，拼 前端排障 + 接口契约人 + 发布SRE + 红队。

以及五个只有你能答的问题：Purpose（止血 vs 可观测）、Context、Materials（禁用源是哪些？）、Boundaries（比如"401 静默跳转会丢草稿"算不算 wall）、Done（建议先交病因分离+测试矩阵做检查点）。

`Ready: no`。确认或改完之后，可以用 `/define-goal` 以这份计划为源。