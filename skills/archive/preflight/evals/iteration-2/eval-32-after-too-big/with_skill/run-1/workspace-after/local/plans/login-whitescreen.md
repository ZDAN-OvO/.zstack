# Plan: 登录页白屏不再出现

- Asked: 帮我修一下登录页偶尔白屏的 bug
- Stage: execute
- Date: 2026-11-08（2026-11-10 改）

## Requirement
Hand over: 只修 `login.ts:5` 那一个白屏：先给复现测试，再给最小修复，diff 只动 `src/login.ts` + 它的测试
Fallback: 先只交复现测试（在旧代码上必须红），修复留到你看过测试之后再动
Depth: 按 error × app_version 排序日志，只认 2.3.1 上仍在发生的行；不是"先看日志"，是"用日志排除掉已消失的错误"
Range: not needed
Judge: 回归测试在未修复代码上失败、修复后通过（可自己跑）。删掉"一周内崩溃日志为 0"——演示前拿不到一周数据，判不了
Needs: 那 40 个文件的分支/diff（这里不是 git 仓库，我看不到，需要你给）
Proposed: 从 Fallback 起步，先出测试给你看，你点头再改实现
Declined: —

## Task
Purpose: 下周演示前登录稳定
Context: React 前端，登录依赖 /api/session。查得：2.3.1 上仍在发生的是 `login.ts:5` 的 `s.user` 为 undefined（377 次，11-03 之后没新行）；`ChunkLoadError` 只在 2.3.0 出现；`cart.ts:41` 栈溢出是另一个 bug
Materials: 1) logs/crashes-2026-11.csv（只看 app_version=2.3.1 的行）2) src/login.ts 3) 本轮不查 cart.ts、不查 chunk ——未找到: 无
Boundaries: 不改后端接口；不碰 cart.ts；不处理 ChunkLoadError；单个 PR ≤ 2 个源文件；不做顺手重构
Done: ①先给一条能在旧代码上变红的复现测试 ②再给最小 null 守卫让测试变绿 ③PR 只含 src/login.ts + 测试 ④diff 我 5 分钟能读完

## Open
那 40 个文件的 PR 怎么处置：整分支回滚，还是只挑测试留下？重跑之前得定。

## Tries
- 2026-11-10 · 未通过：跑了整晚、40 个文件、PR 审不动、白屏还在。原因两条：①计划给的是最上层要求（"白屏不再出现"），范围没封口，日志里 4 条不同错误没有排序，于是顺手把 cart.ts 和 chunk 都动了 → 收回到 Fallback；②Done 里没有中途检查点，一夜无人值守没有刹车 → 改成先交红的测试再改实现，并加 diff ≤ 2 文件、PR 5 分钟能读完两条墙。

Ready: no —— 等你定 Open 里那条，并确认 Fallback 这个起点
