# Plan: 登录页白屏不再出现

- Asked: 帮我修一下登录页偶尔白屏的 bug
- Stage: execute
- Date: 2026-11-08（2026-11-10 改）

## Requirement
Hand over: 登录页白屏不再出现，并有回归测试
Fallback: 只修当前复现的那一个白屏
Depth: 原料=logs/crashes-2026-11.csv（一手）+ src/login.ts。日志按 error×count 排序后，白屏主要是同一处：`TypeError: ...reading 'name' at login.ts:5`，2.3.0 有 412 次、2.3.1 有 377 次 —— 两个版本都在，所以不是新版本引入的回归。代码里唯一读 `.name` 的地方是 `.then` 里的 `s.user.name`，推断 `s.user` 为 undefined（待复现确认）。仪器：把日志做成 error×version 的计数表，只处理占比 >1% 的错误；用 mock 的 `/api/session` 响应喂 `mountLogin`，跑 401、body 无 `user`、无 token 三种响应形态。拉伸目标：写一条在**改动前**就失败的用例，而不是事后补一条能过的。
Range: not needed
Judge: ① 红绿：401 / 无 `user` / 无 token 三条用例在旧代码上必须失败，改后通过（骨架屏方案通不过这一条，会被判失败）；② 另起一次会话，只给日志 CSV 和 diff，不看 PR 描述，判断根因是否被消除；③ 上线后该 error 字符串在日志里为 0。
Needs: 崩溃日志（已有）；能跑 vitest 与 mock fetch 的本地环境（缺则说明）
Proposed: Depth 按上面改写（用日志定位到具体行与响应形态，而不是"先看日志"）；Judge 换成"旧代码上必须失败"的红绿判据，并加一个外部判分会话
Declined: —

## Task
Purpose: 下周演示前登录稳定
Context: React 前端，登录依赖 /api/session
Materials: logs/crashes-2026-11.csv（一手）, src/login.ts；无二手来源；缺服务端日志
Boundaries: 不改后端接口；不用骨架屏/兜底文案掩盖错误，根因没写清不算完成
Done: 一个 PR：修根因 + 回归测试（旧代码红、新代码绿），PR 描述写明哪一行、哪种响应触发

## Open
`ChunkLoadError: Loading chunk 7 failed` 有 88 次，只出现在 2.3.0，也会白屏 —— 算不算这次范围内？如果不算，Done 里要排除它。

## Tries
2026-11-10 · 拒收（只加 loading 骨架屏，根因未查）。原因=方法不足：Depth 只写了"先看崩溃日志"，没给出从日志定位到行与响应形态的方法；Judge 只要求"测试通过"，空测试也能过。已改：Depth 写明两个版本各 412/377 次、定位到 `.then` 里的 `s.user.name`、复现三种响应形态；Judge 改为"旧代码上必须失败"的红绿判据 + 外部判分。

Ready: no，因为新的 Depth 与 Judge 待你拍板；Open 里 ChunkLoadError 的范围要你定。
