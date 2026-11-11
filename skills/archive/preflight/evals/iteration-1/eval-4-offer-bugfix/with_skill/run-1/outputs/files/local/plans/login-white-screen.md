# Plan: 登录页白屏修复

- Asked: 帮我修一下登录页偶尔白屏的 bug，代码在 src/login.ts
- Stage: execute
- Date: 2026-11-10

## Requirement
Hand over（建议）：不只改 login.ts:5 的空指针，而是交付「登录页在 401 / 非 JSON 报错 / fetch 失败 / 慢响应 下都渲染出可见状态（loading、错误提示、重试），永不白屏」+ 一条可跑的回归测试。
- Fallback：只加 `s?.user?.name ?? ""` 与 `.catch` 兜底，消掉当期 789 次崩溃。
Depth：原始材料是 `logs/crashes-2026-11.csv`；仪器是错误日志按版本/次数分组 + vitest 断言。专家动作：把「偶尔」拆成分层原因——401 或非 JSON 响应导致 `s.user` 为 undefined（789 次，2.3.1 仍在涨），以及 ChunkLoadError 88 次（旧 chunk 缓存，同样表现为白屏），而不是只修一行就宣布收工。
Range：动词 = 复现 / 定位 / 修复 / 防回归 / 让用户看见状态。Crew：前端可靠性（挂载状态机 + 错误边界）、测试（构造 401、500+HTML、网络 reject、慢响应的 mock fetch）、red team（反问「token 过期且离线时呢？重试会不会打爆接口？」）。
Judge：仓库内自检 `npm test`——vitest 用上述四种响应断言 `root.innerHTML` 非空且出现错误提示；再逐条对照 crashes CSV 的错误行是否都被覆盖。注意：当前仓库没有任何测试文件，需新建。
Needs：错误日志 CSV（已有）；线上 401/超时的真实响应体样例（缺）；是否能接受「显示错误 + 手动重试」而非静默重试（待定）；工作目录不是 git 仓库，无法 diff 定位引入点（缺）。
Declined：—（待你裁决）

## Task
Purpose: ？（白屏挡住了什么：登录转化、客服工单、还是发布信心）
Context（我查到的事实，请确认）：`src/login.ts` 中 fetch 无 `.catch`，第 5 行无判空直接取 `s.user.name`；`logs/crashes-2026-11.csv` 显示该 TypeError 在 2.3.0/2.3.1 合计 789 次，另有 ChunkLoadError 88 次；仓库无测试、无 git、README 只说 React+vite。
Materials: ？
Boundaries: ？（例如「不许吞掉错误静默重试」「不许改接口协议」「不许在登录页加新依赖」）
Done: ？（先给什么当检查点：是先看「根因对照表 + 测试清单」，还是直接看 patch）

## Open
- 「偶尔」是否包含 ChunkLoadError 那 88 次，还是只修 TypeError？两者修法不同（前者要 chunk 重载/版本提示）。
- 白屏期间用户该看到什么：转圈、错误文案、还是自动重试？文案谁定？
- 是否需要顺手加错误上报（否则下次还是靠 CSV 猜）。

Ready: no —— Hand over 未裁决，Task 五问未答（Purpose / Materials / Boundaries / Done 为空）。
