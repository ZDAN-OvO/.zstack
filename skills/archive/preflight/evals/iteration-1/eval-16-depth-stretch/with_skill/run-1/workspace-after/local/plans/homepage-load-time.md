# Plan: 首页加载 5s → 3s

- Asked: 首页加载 5 秒，帮我优化到 3 秒
- Stage: execute
- Date: 2026-11-10

## Requirement

Hand over（提议，待裁定）: 真实设备/网络分布上的 **p75 LCP ≤ 2.5s**，用 RUM 前后同 cohort 对比证明，并加 CI 性能预算门禁防止回升。理由：3s 在 Core Web Vitals 里仍属 "needs improvement"，而 5s→3s 如果只在本机热缓存跑一次，等于没修。
Fallback: 固定 lab 条件（4G 限速 + 4× CPU 降速、冷缓存）下 LCP ≤ 3s 达成一次，附前后 trace。
Depth: 原始材料用浏览器 waterfall/trace（WebPageTest filmstrip + DevTools Performance），RUM 按设备/网络/百分位分桶的 web-vitals，prod bundle 分析，服务端 TTFB 日志，并与崩溃日志里 `ChunkLoadError` 做相关性。工具：web-vitals + CrUX、Lighthouse CI、WebPageTest、bundle analyzer、React 19 streaming/Suspense。
Stretch: p75 LCP ≤ 1.5s（逼出流式渲染/边缘缓存/去瀑布，而不是抠 bundle KB）。
挑战信念: 先证伪"慢=JS 包太大"——用 waterfall 把 5s 拆成 TTFB / JS 解析执行 / 渲染前请求瀑布 三段，看各占多少毫秒。
Range: 动词 = 量出分桶的慢 → 定位关键路径阻塞 → 砍关键路径字节 → 去掉渲染前请求瀑布 → 边缘缓存/预连接 → 同 cohort 证明变快 → 做成门禁。
Crew: 字段性能工程师（CWV/RUM）、浏览器运行时工程师（解析/执行/hydration）、网络与 CDN 工程师（TTFB/缓存/Early Hints）、数据分析师（百分位与 cohort 定义）；红队：质疑"5 秒是测量假象"的人 + 一台低端安卓真机验证者。
Judge: 同一 cohort 的 RUM p75 LCP 前后对比，加一台干净环境跑的 Lighthouse CI。评分含方法：是否同设备同网络、样本量是否够、是否冷缓存。一次本机热缓存跑出 3.0s 判失败。
Needs: 线上 URL 或可复现的 prod build（缺）、RUM 或 CrUX 数据（缺）、设备/限速矩阵（缺）、首页源码（缺，见下）、构建依赖（缺，vite/vitest 未列入 dependencies）、版本→commit 映射（缺，非 git 仓库）。
Declined: —

## Task

Purpose: 待答 —— 3 秒达标之后要拿它做什么？（放行上线 / 止住用户投诉 / 交一个 KPI？）动作不是目的。
Context: 待答 + 已核事实 —— `acme-web` 2.3.1，React 19 + TS，无 vite 配置、无 index.html、无 lockfile，`npm run build` 与 `npm test` 现在跑不起来；仓库里没有任何性能埋点，也没有首页代码，只有 `src/login.ts`；`logs/crashes-2026-11.csv` 里 `login.ts:5` 的 `s.user.name` undefined 出现 412/377 次，且 `ChunkLoadError: chunk 7` 88 次 —— 用户感知的"5 秒"很可能来自渲染前那次 session 请求，或分包加载失败后的空白/重试。
Materials: 待答 —— 已找到的：`logs/crashes-2026-11.csv`、`src/login.ts`、`package.json`。缺首页源码。请给一份排序后的清单，并点名禁用来源。
Boundaries: 待答 —— 候选墙（请裁）：不为数字牺牲功能；不动视觉稿；不引入付费 RUM 供应商；不改 `/api/session` 契约；不出具没有前后对比的数字。
Done: 待答 —— 建议早期 checkpoint：先交"5 秒由哪几段构成、各多少毫秒"的分解 + 改造清单，确认后再改代码。最终形态待你定。

## Open

- "5 秒"是谁测的：哪台机器、什么网络、冷缓存还是热缓存、哪个指标（白屏？LCP？可交互？首屏数据到位）？仓库里查不到来源。
- "首页"指 `login.ts` 这个页吗？仓库里没有别的页面。
- 3 秒是哪个指标的 3 秒，取第几分位（p50 / p75 / 最慢用户）？
- 有没有线上环境的观测入口（RUM/APM/CrUX 可用性）？

Ready: no —— 三条 Requirement 提议未裁定，五个 Task 槽未答。

## Tries
