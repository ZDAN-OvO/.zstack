# Plan: 修掉最高频的登录崩溃

- Asked: 把 logs 里那个最多的崩溃修掉
- Stage: execute
- Date: 2026-11-10

## Requirement
Hand over: 按原请求 —— `TypeError: cannot read 'name' at login.ts:5`，789/896 条事件（88%），2.3.0 与 2.3.1 都在发生，说明 2.3.1 没修到
Fallback: 只加最小空值保护，不动会话/跳转流程
Depth: 原始材料 = `logs/crashes-2026-11.csv`，按错误签名聚合而不是按行看（412+377 是同一条）；仪器 = 一个坏 token / 无 `user` 的 session 响应，写成 vitest 用例，修复前必须失败；stretch = 用例覆盖 401 与「200 但无 user」两条路径，而不只是 `s.user` 为 null
Range: not needed
Judge: 你已授权自检 → 我跑测试：修复前复现日志里的形状必须红，修复后绿；并附上「测试能复现线上那条堆栈」的截图/输出。局限：这个检查只证明不再抛错，不证明用户被正确引导去重新登录——这一条不算评分，只是提醒
Needs: `package.json` 有 `test: vitest run` 但既无 vitest/vite 依赖也无测试文件 → 需装依赖（缺失）；`cart.ts:41` 的源码不在 `src/` 里，第三条崩溃本次修不了（也不是最高频那条）
Proposed:
1. 只加 guard，还是「session 里没有 user → 当作未登录，跳登录页」？后者改行为，但能让你从 CSV 里看到这条真正归零
2. 加回归测试（会改 `package.json` 并装 vitest）
Declined: —

## Task
Purpose:
Context: （我查到的，待你确认）acme-web 前端 React+TS，版本 2.3.1，崩溃点在 `mountLogin` 里 `.then(s => s.user.name)`；`/api/session` 在 token 失效时的返回约定未知
Materials: 一手 = `logs/crashes-2026-11.csv`、`src/login.ts`；缺口 = 后端 `/api/session` 的响应约定（401？200+空 body？）
Boundaries:
Done:

## Open
- **Purpose**：这条崩溃归零，是为了不再有人卡在登录页，还是为了把 2.3.x 的崩溃率压到某个数？前者决定要修流程，后者只需要 guard。
- **Boundaries**：「不算修好」的样子是什么——比如不许改登录跳转、不许动后端、不许改 `/api/session` 契约？
- **Done**：你说「你自己检查一下」，检查到什么算停？测试绿就停，还是要给出 2.3.1 之后 CSV 里这条归零的证据（那就需要线上数据，不是这个仓库能给的）。

Ready: no —— Proposed 两条未裁定，Purpose / Boundaries / Done 为空。
