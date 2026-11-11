# Plan: 修掉占 88% 的登录页崩溃

- Asked: 修一下 logs 里出现最多的那个崩溃
- Stage: execute
- Date: 2026-11-10

## 事实（已查，非提问）
- `logs/crashes-2026-11.csv` 只有 3 类崩溃、4 行数据。榜首是 `TypeError: ... (reading 'name') at login.ts:5`：412 次（2.3.0）+ 377 次（2.3.1）= **789 / 896 = 88%**。2.3.1 发版后仍在，说明上一次发版没定位到 `user` 缺失。
- `src/login.ts:5`：`root.innerHTML = renderForm(s.user.name)`。三个未防的口子：`s.user` 为 undefined；`r.json()` 在 401/HTML 响应上直接抛；`name` 未转义就拼进 HTML。
- 仓库里没有任何测试、没有 `node_modules`、没有 lockfile；npm registry 可达 → vitest 可装。Node v26（engines >=20 满足）。
- **不是 git 仓库**，改完没有 diff/回滚可对照。
- 仓库里没有：`/api/session` 的实现或契约、`cart.ts`（第 3 类崩溃 19 次）、ChunkLoadError 的来源（88 次，属另一个 bug）。

## Requirement
- Hand over: `R2` 让这个洞没法再犯 —— 在 session 边界做响应校验 + 未登录兜底，并用测试锁住
- Fallback: `R1` 只修 session 引导：200有 user / 200无 user / 401 或非 JSON 三条路径都有兜底 + 一条回归测试
- Ceiling: `R3` 接管崩溃上报与 triage（去重、告警、runbook）—— 只有 4 行 CSV，没有原始上报通道，今天做不到
- Depth: 专家动作是你没写的那一步——**先用失败测试复现再改**，把"症状"换成"服务端三种返回下的确切行为"；原料是 CSV + 真实堆栈（缺）；仪器是 fetch 替身 + vitest，而不是靠读代码猜。Stretch：一条"登录成功路径必须保持绿"的测试，防止修复顺手打断正常登录
- Range: 动词 —— 让用户在白屏之前看到"请重新登录"；让同类崩溃被测试挡住。Crew：前端可靠性（改 `login.ts`）、接口契约（`/api/session` 到底返回什么）、红队（问：正常登录被弄坏没有？`token` 为 null 时呢？`renderForm` 未转义是不是同一个洞？）
- Judge: 自跑 —— 三条失败路径先红后绿，登录成功路径保持绿；红队会话单独读 diff。判方法：空 catch 吞错让测试变绿的，算失败
- Needs: 装 vitest（可）；`/api/session` 真实返回（**缺**）；git 仓库（**缺**）；`cart.ts`（**缺**，本次不修）
- Declined: —

## Task
Purpose: 待确认 —— 目标是"用户别白屏、给个重新登录的出口"，还是"把 crash-free 会话率拉回 2.3.0 之前"？这决定只补兜底还是连根因（token 过期后的服务端契约）一起动
Context: 事实：2.3.1 没修掉，说明前一次只看到了报错没看到 `user` 缺失的条件；「not a git repo」意味着改动要靠测试兜底而不是回滚。待确认：服务端在 token 过期 / 未登录时返回什么（200 + `{user:null}`？401？HTML？）
Materials: 已用 —— `logs/crashes-2026-11.csv`、`src/login.ts`。缺 —— `/api/session` 契约或实现、一条完整堆栈。禁用来源：待确认（我默认不引博客里的通行写法）
Boundaries: 待确认 —— 我的猜测是你不想看到：改 API 契约、碰 `cart.ts`、除测试外加依赖、用空 catch 把错误吞成静默、把 token 从 localStorage 搬走。哪几条是"不是我要的"？
Done: 提议 —— 先给一行根因 + 兜底后的返回结构（checkpoint，等你点头）→ 再给 `login.ts` diff + 先红后绿的测试 + "2.3.0/2.3.1 是否都要单独发"的结论

## Open
- 三条 Requirement 待你接受 / 改写 / 拒绝（尤其 R2 与 R1 选哪个当交付）
- 五个 Task 槽的"待确认"项
- 88% 之外还有 ChunkLoadError 88 次（另一个 bug，与本次无关）、cart.ts 19 次（代码不在仓库）

Ready: no —— Requirement 三条未定，Task 五个槽未答
