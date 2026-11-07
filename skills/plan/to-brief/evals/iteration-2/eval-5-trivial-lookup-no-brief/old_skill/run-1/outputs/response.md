**这个请求不需要 brief。** 按 `to-brief` 的「When not to brief」判据：这是一次快速事实查询，重做成本远低于写 brief 的成本，所以直接回答。

**答案：Node 22 LTS（codename "Jod"）的 end-of-life 是 2027-04-30。**

| 节点 | 日期 |
|---|---|
| 发布 | 2024-04-24 |
| 进入 LTS | 2024-10-29 |
| 转入 maintenance | 2025-10-21 |
| **EOL（停止支持）** | **2027-04-30** |

来源：Node.js Release Working Group 的官方排期 [`nodejs/Release/schedule.json`](https://raw.githubusercontent.com/nodejs/Release/main/schedule.json)（`v22.end = "2027-04-30"`）。

补充：现在（2026-11-06）Node 22 已进入 maintenance LTS 阶段，只收关键修复与安全补丁；它的继任者 Node 24（"Krypton"）EOL 为 2028-04-30。

没有写 `docs/briefs/` 文件。如果你的真实意图不是查日期，而是决定「要不要从 22 升级、升到哪个版本、排期怎么定」，那才需要 brief —— 告诉我，我按 think/decide 阶段来处理。