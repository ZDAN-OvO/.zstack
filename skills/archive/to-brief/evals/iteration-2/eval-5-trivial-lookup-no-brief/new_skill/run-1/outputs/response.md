**不需要写 brief —— 这是一次查表级的问题，直接给答案。**

Node.js 22 LTS（代号 "Jod"）：

| 阶段 | 日期 |
|---|---|
| 首个发布 | 2024-04-24 |
| 进入 LTS（Active） | 2024-10-29 |
| 进入 Maintenance LTS | 2025-10-21 |
| **End-of-Life** | **2027-04-30** |

也就是说，Node 22 目前（2026-11）处于 Maintenance LTS 阶段，只剩安全修复和关键 bug 修复，到 **2027 年 4 月 30 日**停止支持。

依据：Node.js 官方发布计划 `nodejs/Release` 的 `schedule.json`（v22 条目：`maintenance: 2025-10-21`, `end: 2027-04-30`）。

按 `/to-brief` 的「When not to brief」规则，一次快速查询重做的成本远低于写成 brief 的成本，所以我没有在 `docs/briefs/` 下创建任何文件。如果你接下来要的是**基于这个 EOL 做升级决策**（比如"规划从 Node 22 迁到 24/26 的时间线"），那才是需要 brief 的执行型任务——告诉我，我再走正式流程。