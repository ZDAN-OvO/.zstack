计划已写到 `/tmp/pf-12-with_skill-9kf7tpt7/local/plans/fix-top-login-crash.md`（无 git，工作区根即当前目录）。

**查到的事实**（不用你再答）
- 统计 `logs/crashes-2026-11.csv`：TypeError 789（2.3.0 412 + 2.3.1 377）、ChunkLoadError 88、RangeError 19 → 榜首唯一。
- 榜首指向 `src/login.ts:5` 的 `renderForm(s.user.name)`；该函数无 `res.ok` 检查、无 token 判空、无 `.catch`。
- **2.3.1 仍崩 377 次**，所以不是版本回归，而是会话响应缺 `user` 就必崩。

**三条 Requirement 动作，请你逐条接受/改写/拒绝**
1. Altitude：不只手护那一行，而是让会话加载每条失败路径都有定义的界面状态 + 回归测试（Fallback：只加空值保护，崩溃归零但显示 `undefined` 表单）。上限设为「登录页永不白屏/发布前拦住」，因为仓库只有 `login.ts`、无组件树与监控权限。
2. Depth：先分清是 `s.user` 空还是 `s` 非 JSON；用 vitest + 假 fetch 造响应形状，测试先红后绿，再用写测试时没见过的形状验证。
3. Range：交付物动词是「让登录页停在可用状态并说清为什么」，crew 为前端可靠性 / 测试 / 安全评审 / 红队。红队预登记质疑：只加 `?.` 是把崩溃换成静默错误，指标变好体验没修。

**空缺已记在 Needs/Open，不猜**：`/api/session` 真实失败响应样本与后端契约、vitest 安装许可、日志里的 `cart.ts` 不在 `src/`（仓库是片段）、无 git 不可回滚。

**Ready: no** —— Task 五格（Purpose / Context / Materials / Boundaries / Done）仍只有你能填，尤其 Purpose 决定修法；另有 Open 三条。

确认 Ready 行后，可以走 `/define-goal`，用这份计划作为输入。