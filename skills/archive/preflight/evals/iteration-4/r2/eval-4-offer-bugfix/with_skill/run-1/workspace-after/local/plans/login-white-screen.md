# Plan: 登录页不再白屏

- Asked: 帮我修一下登录页偶尔白屏的 bug，代码在 src/login.ts
- Stage: execute
- Date: 2026-11-10

## Requirement

**Look 到的事实（不用你回答，可反驳）**
- `src/login.ts` 只有一条链：`fetch("/api/session")` → `r.json()` → `s.user.name`。没有 `res.ok` 判断、没有 `.catch`、没有 loading/错误态。任何一个环节失败，`root.innerHTML` 都不会被写 → 页面就是白屏。
- `logs/crashes-2026-11.csv` 里 2.3.0+2.3.1 共 789 次 `TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5`，正好是 `s.user` 缺省。**这不是"偶尔"**：两天内近 800 次，更像是"未登录 / token 过期 / 401 空体"的常态路径。
- 同一份日志里还有 88 次 `ChunkLoadError`（部署后旧 chunk 拉不到）和 19 次 `cart.ts` 栈溢出。前者同样表现为白屏，但根因不同 —— 混修会把两件事搞成一件。
- 仓库只有这一条一手数据；`/api/session` 的真实 401 响应体、线上 sourcemap 都拿不到，所以"`s.user` 为什么缺"目前是推断而不是证明。

**Altitude**（建议：接第二档；第一档为 fallback）
- 第一档（请求原样）：`s.user` 加空值保护，别崩。
- 第二档（建议接）：**任何单点失败都不再白屏** —— 无 token / 网络失败 / 非 2xx / 非 JSON 都渲染出可操作的错误态或登录表单。
- 第三档：全站统一会话失效处理（401 拦截 + error boundary），所有页面受益。
- 天花板：白屏能从日志闭环到复现（可观测 + sourcemap + 本地复现环境）—— 超出这次能own的范围，就此停在第二档。

**Depth**（建议：接）
- 专家动作：先看日志分布再动代码，用 789 次这个数字证明"这是常态路径"而不是竞态。
- 原始材料：`logs/crashes-2026-11.csv` 全量 + 一次真实 401 响应体（缺）。
- 工具：仓库已装 vitest 但零测试文件 —— 把四种失败（token=null、401 空体、非 JSON、网络 reject）写成参数化挂载用例，先红后绿。这改变方法：不是"看代码觉得对了"，而是"证明它不再崩"。
- 拉伸目标：在同一个 PR 里给出"88 次 ChunkLoadError 是另一个原因"的判定依据，而不是顺手改。

**Range**（建议：接；词表里的"修"拆成四个动词）
- 能定位（从日志行号回溯到代码路径）｜能防回归（测试）｜能自愈（错误态 UI）｜能诊断（下次白屏留下可读信息）。
- 班组：前端（错误态渲染）｜SRE（日志字段够不够定位、sourcemap 是否可查）｜安全（`token` 为 null 时拼出 `Bearer null`；`name` 直接插进 `innerHTML` 是注入面）｜红队（构造 `s.user` 缺失之外的白屏路径：fetch 悬挂、JSON 畸形、`root` 未挂载）。

**Judge**
- 可自跑部分：vitest 用例，红 → 绿。
- 不可自跑部分：这 789 次到底是不是同一条路径 —— 判据是能拿到一条真实 401 响应体并与日志行号对齐。判方法也判结果：吞掉异常让测试变绿算失败。

**Needs**
- `/api/session` 的真实 401/未登录响应样本（**缺**）
- v2.3.1 sourcemap（**缺**）
- vitest 的 jsdom 环境配置（**缺**，`package.json` 里没有 devDependencies）

**Declined**：截至写计划时为空。

## Task

- Purpose: **待你回答** —— 这个白屏挡住的是哪个决定？（例如"2.3.2 能不能发"、"2.3.1 要不要先回滚"）
- Context: 事实已写在上面 Requirement 的 Look 段，请你确认或推翻；另外只有你知道：这个登录页的量级（日均多少人 / 多少是未登录首次访问）、是否有灰度或回滚窗口。
- Materials: 一手 = `logs/crashes-2026-11.csv`、`src/login.ts`、真实 401 响应（缺）；空槽 = 线上 sourcemap。禁用：无证据的归因（如"React 19 的锅"）。**待你补充**：是否有前端埋点/会话 SDK 文档。
- Boundaries: **待你回答** —— 哪些结果会让你说"不是我要的"？我猜可能包括：改 `/api/session` 契约、为了让测试过而吞异常、顺手重构整个文件。
- Done: **待你回答**；建议形状 = 一个 PR（`login.ts` 改动 + 4 条 vitest 用例 + 一段"为什么是这 377 次"的说明）。早期检查点 = 先只给你两行"根因假设 + 触发路径"，你点头后再写代码。

## Open

- `s.user` 缺失的上游原因（会话过期？匿名访问？代理返回 HTML 错误页？）—— 没有真实响应体，这一格不猜。
- 88 次 `ChunkLoadError` 是否算本次范围 —— 它同样是白屏，但需要单独判因。
- 无 token 时该显示登录表单还是错误提示 —— 取决于 Purpose（是止血还是修好常态路径）。

Ready: no —— 3 条 Requirement 提议未裁决，5 个 Task 槽未答。
