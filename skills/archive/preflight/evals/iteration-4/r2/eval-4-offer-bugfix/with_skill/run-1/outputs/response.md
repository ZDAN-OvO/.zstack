计划已写入 `/tmp/pf-4-with_skill-vpf1jww9/local/plans/login-white-screen.md`。

三条最关键的发现，都来自计划里 Look 到的材料：

1. **不是"偶尔"。** `logs/crashes-2026-11.csv` 里 `s.user` 空指针两天 789 次，这是未登录/会话过期的常态路径被当成了随机 bug。
2. **白屏是设计出来的。** `login.ts` 没有 `res.ok` 判断、没有 `.catch`、没有错误态 —— 任何一环失败 `innerHTML` 都不写，页面必白。
3. **同一份日志里有第二个白屏原因**（88 次 `ChunkLoadError`），混修会让两件事都修不准。

所以计划建议把"改这行空指针"上抬到"任何单点失败都不再白屏"，并配一条 vitest 用例（仓库装了 vitest 但零测试）。

`Ready: no` —— 需要你裁决三处：

- **Altitude**：接第二档，还是只做 fallback 第一档？
- **Task 的 Purpose / Boundaries / Done**：白屏挡住的决策是什么、哪些结果你不要、交付形状是否按我建议的（先给两行根因 + 触发路径作为检查点）。
- 以及两个缺口的确认：能不能拿到一条真实的 401 响应体、线上 sourcemap。

顺手提一句：`token` 为 null 时会把 `Bearer null` 发出去，`name` 直接插进 `innerHTML` 是注入面 —— 要不要并进这次改，也在 Boundaries 里定。

你确认 `Ready` 后，可以让我用 `/define-goal` 以这份计划为源来落地。