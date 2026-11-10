# Plan: 修掉最高频崩溃（登录 s.user.name 未判空）

- Asked: 把 logs 里那个最多的崩溃修掉；谁判断修好了 → 「你自己检查一下就行」
- Stage: execute
- Date: 2026-11-10

## Requirement

**查证到的事实**
- 最多的一条：`TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5`，412 次（2.3.0）+ 377 次（2.3.1）= **789 次**，且当前版本 2.3.1 仍在报 → 是活的、没修的，不是旧噪音。
- 根因已在源码看到：`src/login.ts:5` 直接取 `s.user.name`，而 `r.json()` 对 401/过期 token/网关错误页也照解不误，`s.user` 为 undefined 时整页白屏。
- 第二条 `ChunkLoadError` 88 次 = 发版残留，另一类问题；第三条 `RangeError at cart.ts:41` 的源文件不在本仓库，**在这里修不了**（`src/` 只有 login.ts）。

**Requirement（待你逐条 accept / 改写 / 拒绝）**
- Hand over: 登录入口对「任何非 user 响应」（401、`{}`、HTML 错误页、网络失败）都不再白屏，要么渲染表单，要么渲染「请重新登录」状态。
- Fallback: 只把 `src/login.ts:5` 改成 `s.user?.name ?? ""` 的最小判空。
- Depth: 不是加个 `?.` 就完事——先 `r.ok` 判 401 再解析，把「会话无效」和「会话正常但无 user」分开处理；用日志里真实失败形态做复现。Stretch：一张表覆盖 401 空 body / 200 `{}` / HTML / reject 四种输入，全部不崩。
- Range: 动词 = 复现、定位、修、证明、防。班子 = 前端会话/鉴权（认合同，不只认空值）+ 红队（扫其他 fetch 调用点是否有同一模式；顺带指出 `root.innerHTML` 未转义 name）。
- Judge: 你说自查就够 → 我把它落成**能自己判的检查**：先写测试对着日志里的错误形态跑，**修复前必须红、修复后必须绿**。红→绿这一步是关键，否则我写的测试可能只是自我盖章。红队只提异议，裁定仍落在测试结果上。
- Needs: 仓库没有 `node_modules`、没装 vitest、也**不是 git 仓库**（改坏了没有 `git diff` 可回退）→ 装 vitest 需联网；改前我先把 login.ts 备份成 `.bak`。
- Declined: —

## Task

- Purpose: 未答 —— 修完之后要发生什么？（2.3.2 出包？先止血？这条崩溃是否在阻塞发布或客服工单？）
- Context: 事实部分已由我查证（见上），确认即可；需要你补的：登录页白屏时线上用户看到什么、有没有监控告警。
- Materials: `logs/crashes-2026-11.csv`（主）、`src/login.ts`（主）。禁用：猜测的第三方博客方案。缺失槽位：`cart.ts` 源文件、后端 `/api/session` 的失败响应样例。
- Boundaries: 未答 —— 哪些做法你会说「不是我要的」？（例如：不许改公开 API 合同、不许顺手重构整个鉴权、不许只吞错误不提示用户）
- Done: 未答 —— 什么出现在你面前算停？我提议的形态：`src/login.ts` 改动 + 1 个新测试文件 + 一段「修复前红 / 修复后绿」的输出，**checkpoint 放在测试先红那一步**给你看。

## Open

- Purpose 与 Boundaries 空着，风险是：我把「登录永不白屏」做成「静默吞掉 401」，线上问题从崩溃变成悄悄登录失败——这正是要你划墙的地方。
- Done 里是否需要真机/浏览器验证，还是单测绿灯即可。
- 第三条崩溃要不要单开一轮（需先把 `cart.ts` 找回来）。

Ready: no，因为 Purpose / Boundaries / Done 三个槽还只有我的提议，没有你的话。
