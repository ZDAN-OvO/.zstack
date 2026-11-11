# Plan: 修掉登录链路最高频崩溃

- Asked: 修一下 logs 里出现最多的那个崩溃
- Stage: execute
- Date: 2026-11-10

## Requirement
Hand over: 让「会话拿不到 user 就白屏崩溃」这一类在登录链路里不可能再发生，并用一条先红后绿的回归测试锁住（不是只补一行 `?.`）。
Fallback: 只改 `src/login.ts` 的取值路径，加一条能复现 401/空响应的测试。
Depth: 原料是 CSV 的逐版本计数 —— 2.3.0 412 次、2.3.1 377 次，说明 2.3.1 没修掉它（占比 789/896 ≈ 88%）；缺的是 `/api/session` 在 token 缺失/过期时的真实响应体。器械：本地 vitest 复现 + 按版本切崩溃率，而不是只读栈顶一行。
Range: 动词是「登录不白屏、值夜班不被叫醒、发布能对账」；crew = 前端（登录态状态机，而非取值判空）、SRE（崩溃归因与发布对账）、红队（401、空 JSON、畸形响应、网络失败、`user` 存在但 `name` 缺失）。
Judge: 回归测试（先失败后通过）+ 红队攻击用例；只加 optional chaining 但仍给未登录用户渲染空表单的改法判失败。
Needs: `/api/session` 的响应样本或契约（缺）；`cart.ts`（CSV 里 `cart.ts:41` 引用了它，但仓库里没有这个文件，缺）；能否 `npm i -D vitest`（当前无 node_modules、无 lockfile、无 git，缺）。
Proposed: ① 按上面的 Hand over 抬到「消除这一类」而非「修这一行」；② 用版本崩溃率检验「2.3.1 已修」这个信念（数据已否掉）；③ 加红队用例而非只测 happy path。
Declined: —

## Task
Purpose: 待你回答 —— 是止住用户白屏，还是止住值班告警，还是发布前给出「修好了」的证据？
Context: 仓库 `acme-web` 2.3.1（React 19 + TS，`npm test` = vitest，但没装依赖）。崩溃点 `src/login.ts:6`：`fetch("/api/session")` 后直接读 `s.user.name`；token 缺失或过期时 `s.user` 大概率为 undefined —— 因果未证实，CSV 没有响应体。第二高频项 `ChunkLoadError`（88 次）是发布缓存问题，第三项 `cart.ts:41` 递归（19 次）在仓库里无源文件，均不在本次范围。
Materials: 一手 = `logs/crashes-2026-11.csv`、`src/login.ts`；缺失槽位 = `/api/session` 契约/样本、`cart.ts`、生产崩溃计数核对途径。
Boundaries: 待你回答（可加依赖吗？能改版本号/能发布吗？不许动 `cart.ts` 那条吗？）
Done: 待你回答 —— 建议检查点：先给「复现用例 + 改法说明」，你点头后再改代码。

## Open
- Purpose / Boundaries / Done 三项空白；这三项决定这是「改一行」还是「关掉一类问题」。
- 因果未证实：`s.user` 为 undefined 的触发条件（token 缺失 vs 过期 vs 非 200 响应的 JSON 错误体）需要一份真实响应样本才能定性，否则只是相关。
- 是否要顺手把 88 次的 `ChunkLoadError` 一起纳入（它会随发布继续复发）。

Ready: no —— 缺 Purpose / Boundaries / Done，且触发条件缺一手样本。
