# Plan: 登录页白屏不再出现

- Asked: 帮我修一下登录页偶尔白屏的 bug
- Stage: execute
- Date: 2026-11-08（2026-11-10 修订）

## Requirement
Hand over: 只修当前复现的那一个白屏——/api/session 拿不到 user 时 login.ts 不再白屏，一个 PR ≤ 2 个文件
Fallback: 只交根因 + 一个失败测试，不改产品代码
Depth: 崩溃日志里 789/896 是同一条 login.ts:5 的 TypeError；先钉死这一行（无 token → `Bearer null` → 401 → `s.user` 为 undefined → 未 catch 的 reject → `root.innerHTML` 从不写入），再动手。拉伸：模拟 401 复现“偶尔”，证明间歇性来自过期/缺失 token，而不是网络抖动
Range: 停手式修复（定位、加 guard、加测试），不是重构。红队角色：只看 diff 能否说出改了哪条错误路径
Judge: 会话内可跑——新回归测试在旧代码上红、在新代码上绿；`npm test` 通过。生产“一周 0 错误”保留为事后验证，不再当作停手条件
Needs: 401 响应样本（缺）；能复现的分支或 PR 链接（缺）；`npm test` 可跑（有）
Declined: 全仓 40 文件的“修白屏”（跑完了也没解决，审不动）；顺带修 ChunkLoadError（88）与 cart.ts 栈溢出（19）——不在本次错误路径上

## Task
Purpose: 下周演示前登录稳定
Context: React 前端，登录依赖 /api/session；日志显示主因是一条未处理的 401 分支，不是架构问题
Materials: logs/crashes-2026-11.csv（primary）, src/login.ts（primary）；禁用来路不明的“最佳实践”重构
Boundaries: 不改后端接口；不动 cart.ts 与打包配置；不升级依赖；单 PR ≤ 2 文件（login.ts + 测试）
Done: 先交根因一句话 + 失败测试（checkpoint，我确认后才改代码）；然后 PR ≤ 2 文件、含 1 个回归测试、本地 `npm test` 绿

## Open
- 那 40 个文件的 diff 在哪（此工作区无 git 仓库，src 只有 login.ts 12 行）——需要分支名才能判哪些该丢
- 演示具体日期，决定是否还有余量做 ChunkLoadError 的缓存兜底

## Tries
- 2026-11-10 — 否决：改了 40 文件、问题仍在。原因=Too big（Hand over 到“一周 0 错误”不可在会话内判定）+ 无 checkpoint + 范围无墙（只拦了后端）。改为取 Fallback 上一档的窄修，加文件上限、红→绿判据和“先交根因”检查点。

Ready: no，因为修订后的 Hand over（窄修 + ≤2 文件）和 Boundaries 需你点头，且缺分支/复现信息
