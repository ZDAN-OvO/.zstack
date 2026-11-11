# Plan: 首页加载从 5 秒到 3 秒（并查清 5 秒花在哪）

- Asked: 首页加载 5 秒，帮我优化到 3 秒
- Stage: execute（但缺测量，"优化"前必须补归因）
- Date: 2026-11-10

## Requirement
Hand over: 首页 p75 真实用户在 3 秒内可交互，且 CI 里有性能预算断言 + RUM 监控——回到 5 秒会在合并前失败。
Fallback: 先只做归因与一次性改动：一页时间线拆解 + 改动前后同条件三次测量。
Depth: 从真实用户分布和 trace 出发，不从"包太大"出发；工具用 RUM/web-vitals、Lighthouse CI、DevTools trace（限速 4G、冷缓存）、bundle 分析、服务端耗时日志。拉伸目标：p75 LCP ≤ 1.5s。检验一个信念：「5 秒是前端包大」——拿原始数据对它投票（见 Context 里的崩溃证据，怀疑主因是阻塞的 /api/session）。
Range: 动词＝测量·归因·削减·兜底·防回归。Crew：性能工程师（trace/waterfall）、构建（拆包/预加载/缓存）、后端与网关（/api/session 耗时、超时、边缘缓存）、可观测（RUM、预算告警）；红队＝专门证明"3 秒只是你这台机器快"（登出态、弱网、冷缓存、真机）+ 一个 session 裁定谁的反驳成立。
Judge: 干净环境下的 Lighthouse CI 断言 + 限速真机三次取 p75；判方法不只判数字——解释不了收益来源的改动算不通过，数字碰巧达标也算不通过。
Needs: 首页代码（本仓库只有 src/login.ts，无首页、无 vite 配置、无构建产物）；5 秒的测法与设备/网络/冷热缓存；RUM/APM；/api/session 服务端耗时；能跑 Lighthouse 的 CI 与真机。全部缺失。
Declined: —（三条待你逐条裁决）

## Task
Purpose: 未答。猜测（待确认）：3 秒是某个外部门槛——落地页转化指标、体验考核、或别人给的 deadline？
Context: 事实（已查）：仓库只有 src/login.ts 和 logs/crashes-2026-11.csv，没有首页、没有 vite.config、没有性能测试、没有 RUM。崩溃日志里 2.3.0+2.3.1 共 789 条 `Cannot read properties of undefined (reading 'name')` 指向 login.ts 的 `s.user.name`（session 拿不到 user 就炸），另有 88 条 ChunkLoadError、19 条 cart.ts 栈溢出。→ 对这批用户，首页不是"慢 5 秒"，是永远不出来。待确认：5 秒在哪测的、首页代码是否在本仓库之外。
Materials: 主＝真实用户 RUM、/api/session 服务端耗时、限速 4G 冷缓存下的 DevTools trace、Lighthouse 报告、构建产物与 bundle 分析。次＝崩溃日志（已给）。禁＝"感觉快了"当证据；禁把开 gzip/压图当结论而不测。缺失项留空，不编。
Boundaries: 不许只在一台机器一次测量上宣布达标；不许为提速砍掉登录态校验或错误兜底（那会换来更多白屏）；不改视觉与交互；不许默默删第三方脚本，要列出来单独说。
Done: 先交一页归因——TTFB／下载／解析／首屏渲染／可交互 五段时间线，每段带数据出处；你看过这页才动手改。最终：改动 PR + 同条件前后三次对比 + CI 预算断言。

## Open
- Purpose 未答（谁在等这个 3 秒，等到了要做什么）。
- 5 秒的测法：谁的机器、什么网络、冷缓存还是热缓存、p50 还是 p75。
- 首页代码在哪：本仓库里没有。
- 3 秒这个数能不能谈（p75 下的 1.5s 比一次性 3s 更值）。
- 可动范围：仅前端？含服务端/网关/边缘？

Ready: no —— 三条 Requirement 未裁决，Task 五槽里 Purpose 与 Materials 的测量口径还空着。
