# Plan: 修掉日志里占比最高的登录崩溃（起草，待你裁定）

- Asked: 把 logs 里那个最多的崩溃修掉 / 判断者：你自己检查一下就行
- Stage: execute
- Date: 2026-11-10

## Requirement
Hand over: 登录页在无有效会话时按设计走登录表单，7 天内同类"响应体字段缺失即崩"不在仓库里新增（修 + 回归测试）
Fallback: 只改 login.ts 的会话校验（401/非 2xx/网络失败不再解引用 `s.user`），附一条能复现的测试
Depth: 原始材料＝crashes-2026-11.csv 逐行聚合（不是眼扫那行代码）；先按 `r.ok`/异常把 789 次拆成"登出态正常分支被当错误"与"5xx/网络错误"两类，再用 vitest 假响应体复现两类；stretch＝拿 2.3.0(412) 与 2.3.1(377) 的量级对比判断"是否已被修过而没生效"
Range: 定位→归类→修复→证明→防回归；crew＝SRE（崩溃当分诊队列，看占比与版本趋势）、前端（错误分支与 UI 状态）、测试作者（先写会红的用例）；red team 专攻"`?.` 式修补："不崩了但登出用户看到空白表单"算不算修好
Judge: 模型自跑。先写复现用例（fetch 返回无 `user` 的 JSON / 401）跑红 → 改后跑绿，且有效会话用例仍绿。同时判方法：只加 `?.` 会通过"不崩"但失败"登出态应渲染登录表单"用例
Needs: 已确认事实——#1 TypeError 共 789/896=88%（2.3.0 412 + 2.3.1 377），src/login.ts:5 正是 `s.user.name` 那一行；无 `r.ok` 判断、无 catch。缺：真实响应体样本/错误上报平台（401 与 5xx 各占多少只能推断）；cart.ts 不在本仓库；非 git 仓库，2.3.0↔2.3.1 无法比对；`npm test` 无 vitest 依赖与用例，自查需先搭（node v26 可用）
Declined: （待你裁定后填写）

## Task
Purpose: [草稿] 止血线上并让下一版不复发——需你确认是"这次发版止血"还是"只要 2.4 不再崩"
Context: [草稿] 2.3.1 仍有 377 次，说明不是旧版残留；日志里的 cart.ts 不在本仓库，日志可能来自更大的构建
Materials: [草稿] 主：logs/crashes-2026-11.csv；次：src/login.ts、package.json；禁：臆造 2.3.0 源码差异；空槽：真实响应体/上报平台数据（没有）
Boundaries: [草稿] 不用 `s?.user?.name ?? ""` 把登出态静默成空表单；不吞 fetch 失败；不动 ChunkLoadError(88) 与 cart.ts(19)；不升级 React/Node；不做无测试的顺手重构
Done: [草稿] login.ts 有显式错误分支（401/非 2xx/网络失败→登录表单），`user` 缺失不解引用；新增 ≥2 条 vitest（无 user 不抛、有效 user 渲染 name）；`npm test` 绿。早检查点：先交"789 次的归类结论 + 用例名"再动代码

## Open
- cart.ts RangeError 是否在范围内（文件不在仓库）
- 是否需要发版/回滚说明
- 401 与 5xx 的真实占比（无数据，只能推断）

Ready: no — 三条 Requirement 未裁定；Task 五格为代填草稿待确认
