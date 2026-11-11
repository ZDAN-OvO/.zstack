计划已写入：`local/plans/homepage-load-3s.md`

先说 Look 查到的关键事实（它们改变问题的形状）：

- 仓库 `acme-web` 2.3.1 里**没有首页**：只有 `src/login.ts`、`package.json`、`README.md`，没有首页组件、没有 `vite.config`，也没有任何性能数据。“5 秒”在本仓库里找不到出处。
- 代码里唯一确定性的瓶颈候选：`src/login.ts` 先 `fetch('/api/session')`，再 `root.innerHTML = renderForm(...)` —— 首屏内容被接口阻塞，接口延迟直接叠加到用户可见时间。
- `logs/crashes-2026-11.csv`：ChunkLoadError 88 次(2.3.0) → 0 次(2.3.1)，同期 `TypeError ... 'name' at login.ts:5` 412→377 仍未消除。只有 5 行、两个版本——这是可测的相关性，不是因果。

计划里给了三项待裁决的提议（我按"3 秒要成为守住的上限"而不是"跑一次变快"来写）、五个 Task 槽位，其中 Purpose 留空——3 秒是给谁、为了什么（转化？SEO 门槛？投诉？）只有你知道，我不替你填。

**Open 里三个问题决定了后面砍哪里**：这是不是正确的仓库、5 秒是字段还是 lab 数据、3 秒是硬约束还是拍的数。

Ready: no。你回答 Open 1–3 并对提议裁决后，我可以把它交给自己或 `/define-goal`（以这份计划为源）继续。