# Plan: 登录页白屏不再出现

- Asked: 帮我修一下登录页偶尔白屏的 bug
- Stage: execute
- Date: 2026-11-10

## Requirement
Hand over: 登录页白屏不再出现，并有回归测试
Fallback: 只修当前复现的那一个白屏
Depth: 先按日志计数排因，再动代码。原始材料是 logs/crashes-2026-11.csv：2.3.0 的 `TypeError … reading 'name' at login.ts:5` 412 次、2.3.1 同日 377 次 → 跨版本不降，说明不是版本回归，而是"session 无效时没有分支"的结构问题；`ChunkLoadError: chunk 7` 88 次只出现在 2.3.0，属另一条独立成因。辅助工具：2.3.1 构建的 sourcemap 把 login.ts:5 落到真实行、以及一次"token 过期/缺失"时 /api/session 的真实响应体。专家动作（没被要求）：把崩溃按错误×版本×天聚合排序，写一个在未修代码上会红、报出日志里那条 TypeError 的复现；stretch：复现断言的是抛错路径而非 DOM 是否存在。
Range: —
Judge: 评方法不只评结果 —— PR 必须有一行根因说明（哪条日志、命中哪个帧、为什么变成空白页），回归测试必须在未改动的 2.3.1 上跑红过（附失败输出）；只加骨架屏能过的那种测试判失败。
Needs: sourcemap（缺）；token 过期时 /api/session 的响应体（缺，需 stub 或抓包）
Declined: —

## Task
Purpose: 下周演示前登录稳定
Context: React 前端，登录依赖 /api/session；崩溃日志跨 2.3.0/2.3.1 两条版本都在，所以症状与版本无关
Materials: logs/crashes-2026-11.csv, src/login.ts（以上为已确认）；2.3.1 构建 sourcemap、过期 token 的 /api/session 响应（待确认是否可得）
Boundaries: 不改后端接口
Done: 先交 5 行根因说明（计数最高的成因、命中的帧、空白页的机制、本次纳入范围的那几条成因）作 checkpoint，确认后再出 PR；PR 含回归测试

## Tries
- 2026-11-10 判为方法错（没做根因定位就改 UI）：Depth 由"先看崩溃日志"改成按计数排因＋先红后绿的复现，Judge 增加方法评分与"未修代码上必须跑红"。

Ready: yes
