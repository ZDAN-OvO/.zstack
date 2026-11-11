# Plan: 登录页白屏不再出现

- Asked: 帮我修一下登录页偶尔白屏的 bug
- Stage: execute
- Date: 2026-11-08（2026-11-10 修订）

## Requirement
Hand over: 只修 login.ts:5 这一处 —— `/api/session` 没有 user 时渲染空表单，不再整页白屏（1 file，~6 行 diff）
Fallback: 连兜底都不改，只在挂载处加一层错误边界，把白屏换成错误提示（0 逻辑改动）
Depth: 原始材料=logs/crashes-2026-11.csv 按 error+文件行号聚合：896 次里 789 次（412+377）都是同一行 `login.ts:5`，只有一个根因；专家动作=先算清规模再动手，而不是边跑边改。Stretch：用 app_version 分布验证 2.3.1 是否真的修好（377 次仍在，说明没修）
Range: 动词=定位单行 / 只改一处 / 证明不复发。Crew：前端排障（聚合日志把 896 收敛到 1 行）、测试（只断言该行不抛）、红队（这次改动会不会把真实 401 吞掉，让用户看不到"请重新登录"）
Judge: 回归测试通过 **且** diff 只碰 1 个文件（≤2）、审阅 ≤5 分钟；改前先贴「根因一行 + 计划 diff」给人看一眼（checkpoint）
Needs: 崩溃日志 ✅；缺：overnight 那支分支的 diff（好判断哪些是噪音、哪些能留）、vitest 与测试目录（package.json 现无测试依赖、src 下无测试文件）
Declined: 原 Hand over「白屏不再出现，并有回归测试」——理由：范围吞进了 ChunkLoadError（88 次，另一个根因，部署后旧 chunk），于是 40 文件扫射；改为一次只吞一个根因

## Task
Purpose: 下周演示前登录稳定
Context: 实际崩溃是 `/api/session` 在未登录/token 过期时返回无 `user`，`s.user.name` 读 undefined；`r.json()` 在 401 非 JSON 时也会抛，两条路径都落到白屏。ChunkLoadError 是独立问题，不在本次范围
Materials: logs/crashes-2026-11.csv（按 error+行号聚合）、src/login.ts（primary）
Boundaries: 不改后端接口；不重构、不改目录结构、不动无关 console；单 PR 文件数 ≤2；不顺手修 ChunkLoadError
Done: 1 个文件 diff + 1 个断言该行不抛的测试 + 审阅 ≤5 分钟。Checkpoint：动手写代码前先出「根因一行 + diff 预览」

## Open
- overnight 那 40 个文件里，有没有值得保留的一处？（拿到 diff 才能判，否则整支丢弃重开）
- 无 vitest 环境：回归测试跑不起来，"Done" 里那条断言现在没人能执行

## Tries
- 2026-11-10 | 结果被拒：40 files / PR 审不动 / 问题未解决 | 判定 = Too big（接了 Hand over 的大范围）+ Missed intent（Boundaries 没有规模墙，Done 没有 checkpoint）| 改法 = 降到 Fallback，用日志把范围钉到 login.ts:5 一行；Boundaries 加文件数上限；Done 加"改前先看 diff 预览"

Ready: no，因为 overnight 分支 diff 与测试环境还没拿到；Hand over 已改为 Fallback 那一级，等你确认降级与两道墙
