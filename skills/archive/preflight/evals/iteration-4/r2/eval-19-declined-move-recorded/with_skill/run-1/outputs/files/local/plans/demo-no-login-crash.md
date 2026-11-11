# Plan: 演示不崩 —— 修掉登录页最高的那个崩溃

- Asked: 修一下 logs 里出现最多的那个崩溃
- Stage: execute
- Date: 2026-11-10

## Requirement
Hand over: 修掉 `login.ts` 那个 `TypeError ... reading 'name'`（logs 里 789 次，最高），以带回归测试的 PR 交付 —— 你已拒绝往上抬到"登录页零崩溃"。
Fallback: 若测试+PR 在演示前赶不及：先合一个最小空值守卫（今天上线），测试与 PR 演示后补。**待你确认是否接受这条退路。**
Depth: 专家动作是你没要的那一步 —— 先分清这是"接口少返字段"（契约违约）还是"session 比 user 先到"（竞态）：2.3.0 与 2.3.1 都在崩（412 / 377 次），说明它不是新版本引入的，而是长期存在、每次登录都可能踩。做法是在边界处一次性收口：把 `/api/session` 的响应解析成一个明确的类型（有 user 且有 name / 没有 → 走错误分支），让 `renderForm` 拿到的名字永不为空，而不是在 `s.user.name` 上贴一层 `?.`。
仪器: 用 CSV 按 app_version 算崩溃率（不是原始次数）；一个手写的 parse 边界 + vitest 用例，fixture 取日志里真实出现过的响应形态。
Stretch target: 用例必须先在当前代码上失败（红），修完转绿；覆盖 2.3.0 与 2.3.1 两条路径。
Range: 动词 —— 让演示不崩 / 说清接口到底回了什么 / 别让同一个人下次再崩。Crew: 前端工程师（边界收口）；可观测性（从 CSV 按版本给崩溃率，用来判断 2.3.1 线上是否真被修好）；红队（拿空 body、无 user、user 无 name、500、慢响应去撞登录页）。
Judge: 回归测试自己当判据 —— 它必须在未修改的代码上复现日志里那个 TypeError，再在修改后通过。它判方法也判结果：用真实日志形态而非手编的假数据，才算过；侥幸不崩但没复现原崩溃的用例判失败。
Needs: 已有 `logs/crashes-2026-11.csv`、`src/login.ts`、`npm test` 脚本。缺：真实的 session 响应样本（后端不改，但读一下响应体不算改）；`package.json` 里没有 vitest 依赖，`npm test` 现在跑不起来，需先装；日志写 `login.ts:5` 而源码里 `.name` 在第 6 行，需 sourcemap 或 2.3.x 构建产物确认是同一处。**这两项待你确认。**
Declined: 抬高到"登录页零崩溃 + 一周崩溃日志为 0" —— 理由：下周就演示，只修这一个。

## Task
Purpose: 演示不崩。
Context: React 前端，session 接口偶尔不返回 user。
Materials: logs 和 src/login.ts（按主次：日志是主，源码是次）。
Boundaries: 不改后端。
Done: 一个带回归测试的 PR。

## Open
- 演示流程真的走登录页吗？如果演示用的是预置 token 直接进主界面，这个守卫对演示的价值要重新算。
- 拿不到 user 时页面该显示什么（错误提示 / 重试 / 静默降级成匿名表单）—— 边界只说了不改后端，没说这层。
- 周末前有没有人能跑一遍真机（staging）登录，确认修完不崩？测试绿不等于演示不崩。

Ready: no —— Fallback 与 Needs 里两项待你点头；Open 三条还没定。
