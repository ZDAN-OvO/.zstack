# Plan: 登录页白屏不再出现

- Asked: 帮我修一下登录页偶尔白屏的 bug
- Stage: execute
- Date: 2026-11-10（第 2 版，诊断重做）

## Requirement
Hand over: 先出一份"白屏归因"，把白屏拆成各自可复现的独立路径，每条路径各有失败测试转绿；不是先改 UI
Fallback: 只修计数最高的那一条路径（s.user undefined），其余开 issue
Depth: 按 (版本 × 错误 × 次数) 拆 CSV，而不是按"白屏"整体看；原始材料 = 崩溃行 + /api/session 真实响应体（401/500 各一次）+ 构建产物 chunk hash 与部署记录；工具 = 归因表 + 会先红的复现测试（mock fetch 返回 401、mock 动态 import reject），不是肉眼看 login.ts
Stretch: 用 2.3.0→2.3.1 两版数据检验"这是版本引入的 bug"这一信念；若是跨版本恒定的 377→412，则与版本无关，指向接口契约
Range: 归因、复现、修复、可观测（能区分是哪种白屏）；crew = 浏览器缓存/部署工程（ChunkLoadError）、API 契约（/api/session 的 user 与状态码）、测试工程（红→绿）、红队（专攻"骨架屏就算修好了"）
Judge: 独立会话不看修复只看测试——两条路径各一个在修前失败的测试；外加一个红队会话反驳"loading 骨架屏是修复"，第三个会话裁决
Needs: 2.3.0/2.3.1 部署与 chunk hash 记录（缺）、/api/session 401/500 实测响应（缺）、cart.ts（缺，RangeError 在它里面）、vitest 未在 devDependencies 且无测试目录（缺）
Declined: 第 1 版 Depth 只写"先看崩溃日志"——看完仍停在单行堆栈，未拆错误类型

## 已查清的事实
- `src/login.ts:5` 的 `s.user.name`：`.then(r=>r.json())` 不判 `r.ok`，401/500 的 JSON 错误体直接流入，`s.user` 为 undefined 抛 TypeError，且 catch 缺失 → `root.innerHTML` 从未被赋值 → 白屏。跨 2.3.0/2.3.1 恒在（412→377），不是新版本引入
- `ChunkLoadError: Loading chunk 7 failed`（88 次，只在 11-01）= 部署后旧 tab 拉已删除的 hash 文件，动态 import reject → 同样白屏。这条才更像"偶尔"
- `RangeError` 在 cart.ts:41（19 次），不在登录页，且源码缺失
- 骨架屏不修任何一条：路径 1 仍是永久骨架，路径 2 仍是白屏

## Task
Purpose: 下周演示前登录稳定
Context: React 前端，登录依赖 /api/session；"偶尔"与计数最高的错误不是同一件事，需你确认指的是哪个（我判是 ChunkLoadError）
Materials: 1) logs/crashes-2026-11.csv（按版本×错误×次数拆）2) /api/session 的 401 与 500 原始响应 3) src/login.ts；禁用：在浏览器里手点几下就下结论
Boundaries: 不改后端接口；不接受掩盖症状（骨架屏、重试遮罩、空 catch）作为修复
Done: 一份归因表（每行：路径/复现条件/证据/修复/测试）+ 每条路径一个修前失败的测试，先给我看归因表再动代码

## Open
- "偶尔"指 ChunkLoadError 还是 s.user 那条？决定先修哪个
- 路径 2 的修复若要动 index.html 缓存头/部署流程，算不算"改后端接口"
- 后端能否把 user 缺失变成 401（若可，路径 1 的正解在契约层）

## Tries
- 2026-11-10 否决：只加了 loading 骨架屏，白屏真因未找到。判定=方法错（漏诊断），Depth 加深为按错误类型拆解+红→绿复现，Range 补部署缓存与 API 契约两个视角

Ready: no —— 三条 Open 需你定；Depth/Range 的新动作待你确认或改写
