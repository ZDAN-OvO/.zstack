计划已写到 `/tmp/pf-12-with_skill-7oiz5ghs/local/plans/login-crash-fix.md`（工作区还没动代码）。

看日志得到的事实：
- 出现最多的是 `TypeError: Cannot read properties of undefined (reading 'name')`，2.3.0 412 次 + 2.3.1 377 次 = 789 次，占全部 896 条的 88%。**当前版本仍在崩，说明没修过**；`ChunkLoadError` 88 次、`cart.ts:41` 递归 19 次。
- 对应代码是 `src/login.ts:6`：`/api/session` 取回 `s` 后直接读 `s.user.name`。token 缺失或过期时 `s.user` 大概率不存在 —— 但 CSV 没有响应体，这只是假设，不是结论。
- 仓库没有 `cart.ts`（那条修不了）、没有测试、没有 node_modules。

计划里待你定的：Purpose / Boundaries / Done 仍是空的（对「修好」的定义会决定是补一行 `?.` 还是把这一类关掉），另外我发现一个可以抬高的地方（用版本崩溃率检验「2.3.1 已修」）和一条建议的检查点（先给复现用例和改法，你点头再动代码）——都在 `Proposed` 里等你裁决。

确认 Ready 行后可以 `/define-goal`，以这份计划为源。