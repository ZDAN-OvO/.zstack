# Plan: 登录页白屏不再出现（第 2 版）

- Asked: 帮我修一下登录页偶尔白屏的 bug
- Stage: execute
- Date: 2026-11-10

## Requirement
Hand over: 定位并修掉白屏根因，附一条修复前失败、修复后通过的回归测试
Fallback: 只修 `login.ts:5` 的 `s.user` 为 undefined 这一条路径
Depth: 从崩溃栈反推，而不是给白屏盖骨架屏。事实：`src/login.ts:5` 是 `root.innerHTML = renderForm(s.user.name)`；10 天日志里 `Cannot read properties of undefined (reading 'name')` 共 789 次（2.3.0 412 + 2.3.1 377），说明 `/api/session` 有时返回了没有 `user` 的 body（过期/无效 token），而代码既不查 `r.ok` 也不校验 body 形状，`.then` 里抛错后 `root` 永远为空 → 白屏。专家动作：按 token 状态枚举响应（正常 / 401 / 401 带空 body / 非 JSON），把失败响应固化成一个能跑的测试；再加 `catch` + 渲染登录表单的兜底，而不是 loading 骨架屏。仪器：崩溃日志按版本、失败响应样本、fetch mock。Stretch: 写一条以 `login.ts:5` 原始栈为断言的测试，先在当前代码上跑挂；再扫一遍 `src/` 里所有无 `.catch` 的 `.then`。
Range: 要的效果是「不再白屏、出错时仍能看到登录框」；crew：前端运行时（Promise/渲染时序）、SRE（从崩溃日志取真实 token 状态）、红队（构造让 `s.user` 缺失的响应并质疑兜底是否只是遮症状）。R→已收窄为单一前端职责，红队保留。
Judge: 回归测试对当前代码必须失败、对修复通过（只断言骨架屏出现的测试判失败）；上线后一周崩溃日志中 `login.ts:5` 该错误计数为 0。
Needs: 失败时的 `/api/session` 响应样本（primary，缺）；session 接口约定（缺）；浏览器一次白屏的 Network/Console 记录（缺）。已有：`logs/crashes-2026-11.csv`、`src/login.ts`。
Declined: 「加 loading 骨架屏」——已尝试，遮住症状且未触及根因。

## Task
Purpose: 下周演示前登录稳定（沿用）
Context: React 19 + TS 前端，登录依赖 `/api/session`；错误集中在 `login.ts:5`，跨两个版本仍存在；日志另有 `ChunkLoadError` 88 次（可能同属白屏，待定）
Materials: 主：`logs/crashes-2026-11.csv`、失败响应样本（缺）；次：`src/login.ts`、接口约定（缺）；禁：无
Boundaries: 不改后端接口；只加骨架屏、根因未定位的修复不接受（本次已拒绝）；不把 `ChunkLoadError` 当作已修
Done: 先交检查点——一句根因结论 + 一条能复现的失败测试（不写修复代码）；确认后再交一个 PR，含修复与通过的原测试
Open: 手头没有一次失败响应样本，需从后端日志或一次带过期 token 的请求里取；白屏那几次是 `login.ts:5` 崩溃还是 chunk 加载失败，需一次现场记录来区分（决定 `ChunkLoadError` 是否进本 PR）

## Tries
- 2026-11-10 拒绝：只加了 loading 骨架屏，未定位根因 → 判为方法错误（未用崩溃栈/失败响应），故加 Depth，补 Depth 的失败响应样本与「修复前测试必须失败」的判据；Task 的 Materials/Done 随之更新。

Ready: no，因为 Depth 的取样本方式待你确认，且 `ChunkLoadError` 是否纳入本 PR 未定。
