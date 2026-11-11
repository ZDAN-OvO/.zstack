计划已写好：`local/plans/homepage-load-time.md`

先说我查到的、会影响判断的事实：

- 这个仓库里**没有首页代码**，只有 `src/login.ts`；也没有 `index.html`、vite 配置、lockfile —— `npm run build` / `npm test` 现在跑不起来（vite/vitest 不在依赖里）。
- 仓库里**没有任何性能埋点或 RUM**，所以"5 秒"这个数字在本项目里查不到来源。不是 git 仓库，版本也对不到 commit。
- `logs/crashes-2026-11.csv` 有两个线索：`login.ts:5` 读 `s.user.name` undefined 出现 412/377 次（页面渲染等 `fetch("/api/session")` —— 典型渲染前请求瀑布）；`ChunkLoadError: chunk 7` 88 次（分包加载失败，通常表现为白屏或重试）。用户感知的"5 秒"很可能出在这两处，而不是 JS 包大小。

**要你裁定的三条 Requirement 提议**（计划里写的是我的建议，不是定论）：

1. **交付到哪一层**：建议做到 p75 LCP ≤ 2.5s，用同 cohort 的 RUM 前后对比证明，并加 CI 预算门禁。3s 在 Core Web Vitals 里仍算 "needs improvement"；只在本机热缓存跑出 3s 等于没修。退路：固定 lab 条件（4G + 4× CPU、冷缓存）LCP ≤ 3s 一次，附前后 trace。
2. **深度**：先证伪"慢 = 包太大"，用 waterfall 把 5 秒拆成 TTFB / JS 解析执行 / 渲染前请求瀑布三段。拉伸目标 p75 ≤ 1.5s，逼出流式渲染和边缘缓存，而不是抠 KB。
3. **红队**：一个人专门证明"5 秒是测量假象"，一台低端安卓真机做验证。判断标准里包含方法分 —— 本机热缓存跑出 3.0s 判失败。

**五个槽位我不能替你填**，最关键的四个：

- 3 秒达标之后你要拿它做什么？（放行上线 / 止投诉 / 交 KPI）
- "5 秒"是谁测的：哪台机器、什么网络、冷还是热缓存、哪个指标（白屏 / LCP / 可交互 / 首屏数据到位）？
- "首页"就是指 `login.ts` 这个页吗？
- 有没有线上 RUM/APM/CrUX 入口？

现在 Ready: **no**。你把这四条答了、三条提议裁了，我就把计划改成 Ready: yes；想先定义目标，可以接着跑 `/define-goal`，用这份计划当输入。