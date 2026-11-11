# Plan: 首页 3 秒内可用

- Asked: 「首页加载 5 秒，帮我优化到 3 秒」
- Stage: execute
- Date: 2026-11-10

## Requirement
Hand over: 按原话执行 —— 首页加载 3 秒（"加载"的定义见 Open，未定前无法验收）
Fallback: 若实测基线证明 3 秒不可达：先做到「首屏内容 3s 内出现 + 登录表单可交互且不崩」，完整加载与资源体积留作下一步
Depth: 你要的动作是"改"，专家先"量"。仓库里既没有首页代码也没有任何耗时数据，5 秒无法归因。原始材料＝真实用户 RUM（web-vitals LCP/INP）+ 一次冷缓存 WebPageTest 瀑布图；仪器＝Lighthouse CI、bundle 分析、React Profiler、缓存/压缩配置审查，而不是凭经验压图片。stretch：把 5s→3s 变成 CI 回归门禁，让它不再退回 5 秒
Range: 动词＝看见（首屏内容出现）／敢用（登录不再 TypeError）／能用（表单可交互、可提交）／留住（二次访问命中缓存）。crew：性能工程师（定口径与预算、lab+field 双测）｜前端构建（拆包、裁首屏依赖、去掉 login.ts 三处 console.log）｜边缘与缓存（CDN、压缩、缓存头）｜可用性（骨架屏、渐进渲染，改的是感知时间）｜红队（专攻"3 秒"结论：冷启 vs 热缓存、移动 vs 桌面、lab vs 真实用户）
Judge: 我可在本机跑 Lighthouse CI 固定节流（4G、4× CPU、冷缓存、N≥5 取中位）复测，判方法也判结果：口径变了、只跑一次、热缓存、只测桌面的，一律判失败。真实用户 p75 我拿不到（见 Needs）
Needs: 首页源码（缺，仓库只有 src/login.ts）｜现状 5 秒的测量记录：谁测的、设备/网络/版本（缺）｜vite 构建配置（缺）｜RUM 与目标用户设备分布（缺，需你提供）｜p75 达标比例（缺，多少用户达标算完成）
Proposed（未裁定）:
1. 把"加载"定成一个可测事件（建议 LCP，或"登录可交互"），并固定设备/网络/冷缓存口径
2. 先埋点+跑基线、出瓶颈清单，再动代码
3. 顺手修 `login.ts:5` 的崩溃（789 次/月，`s.user` 为空读 `.name`）——与慢是否相关待验证
Declined: 无

## Task
Purpose: （未答）3 秒达标后哪件事会变好？转化、投诉量、SEO，还是老板要的数字？
Context: 事实——acme-web 2.3.1，React 19 + TS，`npm test` 跑 vitest；仓库仅有登录页挂载代码，无首页；崩溃日志显示 2.3.0/2.3.1 两版共 789 次 `TypeError` at login.ts:5（`s.user` 为 undefined），另 88 次 `ChunkLoadError`（分块加载失败会直接伤首屏）
Materials: 提议排序（待裁定）：① 真实用户 RUM 与现场 5 秒的测量记录 ② 冷缓存 WebPageTest/Lighthouse 报告 ③ 构建产物与 bundle 分析 ④ 第三方优化博客（降级为参考）。禁用：无出处的"行业平均"、二手转载的优化清单；查不到的项留空，不许编
Boundaries: （未答）
Done: （未答）

## Open
- Purpose 空：说不出 3 秒换来什么，这数就是拍的
- Done 空：什么形状的东西摆在你面前算完成？建议加早期检查点——先交「基线报告 + 瓶颈清单」，再改代码，免得方向错了返工
- Boundaries 空：什么结果会让你说"不是我要的"？例如只改代码没数据佐证、砍功能换速度、只优化桌面端
- "5 秒"的口径未定（指标/设备/网络/冷热缓存/样本量），"3 秒"同样未定
- 首页代码在哪？另一个仓库，还是我没看到
- 崩溃与慢的关系：同期出现，因果未验证

Ready: no —— Purpose／Boundaries／Done 三项未答，Hand over 口径与三条 Proposed 待你裁定，首页源码缺失
