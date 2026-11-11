# Plan: 登录页不再白屏

- Asked: 「帮我修一下登录页偶尔白屏的 bug，代码在 src/login.ts」
- Stage: execute
- Date: 2026-11-10

## Requirement

Hand over（建议）: 登录页面对崩因清单里的每一种失败都有确定可见状态（加载 / 未登录 / 会话失效 / 网络失败 / 加载新版本），且下一次崩溃可在日志里定位。范围 = src/login.ts + 一个回归测试文件。
Fallback: 只修 `s.user.name` 这一条路径（守卫 + 空状态），不加其他失败态。
Ceiling（估计，未验证）: 应用外壳保证任何运行时异常都不产生白屏（全局 error boundary + 部署 chunk 缓存策略）；超出单个 PR 且需要部署/基础设施权限。

Depth:
- 原始材料: `logs/crashes-2026-11.csv` —— login.ts:5 同一 TypeError 共 789 次（2.3.0: 412，2.3.1: 377），另有 ChunkLoadError 88 次。
- 专家动作（你没要求的那一层）: 不只补 null 判断，而是枚举所有能让 `root.innerHTML` 永不执行的分支：无 token 仍发 `Bearer null` → 401；401 响应体可能不是 JSON 或没有 `user`；`r.json()` 对非 JSON 体直接 reject；没有 `.catch` → unhandled rejection；解析期无 loading/失败占位，所以白屏；`${name}` 直接拼进 innerHTML（注入面）。
- 仪器: vitest + 假 fetch，用日志里真实出现过的响应形状建用例表，而不是靠肉眼验证。
- 拉伸目标: 先写能复现日志中 TypeError 的失败用例（红），再修到绿；并加入日志里没出现过、但真实会发生的形状（401 HTML 体、离线、超时）作为 held-out 用例。

Range:
- 动词化交付物: 不白屏（拦住崩溃）→ 说清原因（可见失败态）→ 能重试（恢复路径）→ 留下证据（上报 + 测试）。
- Crew: 前端可靠性工程师（mount 状态机）；安全审查（innerHTML 注入）；测试作者（回归套件）；红队（找其他白屏路径：ChunkLoadError、cart.ts RangeError、未捕获 promise）。

Judge: 模型可自跑 —— 用日志形状建成的 vitest 套件，必须在现行代码上红、修完后绿；评分方法而非结果（只守 `user.name` 一条路径应判不合格）。用户侧补充判定: 下周崩溃日志中 login.ts:5 计数归零。

Needs:
- 缺: 无 vitest 依赖与配置（`package.json` 只有 `test` 脚本，无 devDependencies、无 vitest/vite 配置、无任何测试文件）。
- 缺: `/api/session` 契约——401 时返回什么体、是否恒为 JSON。
- 缺: ChunkLoadError 的部署/缓存信息（不在本仓库）。
- 有: 崩溃日志（原始一次材料）；仓库无 git 历史。

Declined: 待你裁决后记录。

## Task

Purpose: ？（待你回答）—— 是「止住用户报障」，还是「让下一次故障可定位」，还是「上线前通过评审」？决定修的范围。
Context: 事实（请确认）—— `mountLogin` 在 `token` 为 null 时仍请求 `/api/session`；`.then` 链无 catch、无空态；`root.innerHTML` 只在成功路径被赋值是白屏的直接机制。缺的是：谁触发登录页（直接访问 / 会话过期跳转 / 多标签页）、token 由谁写入与清除、白屏是否是用户唯一的报障渠道。
Materials: `logs/crashes-2026-11.csv`（一次）；`src/login.ts`（一次）；README/package.json 为辅助（二次）。禁用源: ？（待填：如推测性的第三方文章、无出处的「最佳实践」）。未找到: 后端 `/api/session` 代码、错误上报 SDK 代码。
Boundaries: ？（待填「不要什么」）候选: 不改后端；不改 UI 视觉；不在本次引入状态管理/框架级重构。
Done: ？（待填）候选: 提交前看到 ① 复现日志错误的失败测试 ② 修复后全绿 ③ mountLogin 的失败态截图或 DOM 断言；checkpoint 是先给你看崩因清单 + 用例表再动手改。

## Open

- 五问全未答（Purpose / Context / Boundaries / Done 为 ?，Materials 的禁用源与未找到项待确认）。
- 后端 `/api/session` 失败响应形状未知，白屏的具体触发条件（无 token？会话过期？）需一次真实复现或抓包才能定。
- ChunkLoadError 是第二个独立的白屏成因，是否纳入本次范围未定。
- 仓库没有测试脚手架，测试判定线需要先搭起来（依赖能否安装未确认）。

Ready: no —— 三轴动作未裁决，五问未答，且 API 契约与测试脚手架缺失。
