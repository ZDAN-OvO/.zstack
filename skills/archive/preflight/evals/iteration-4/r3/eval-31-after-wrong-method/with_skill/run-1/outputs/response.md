已完成诊断并就地修订计划：`local/plans/login-whitescreen.md`

**问题归类**：判为「方法错」（漏诊断），在原 Hand over 这一档上加 Depth，不降 Fallback。

**日志里已经能看到的根因**（原计划写了"先看崩溃日志"，但执行时没做这一步）：
- 主因：`s.user` 为 undefined，`renderForm(s.user.name)` 在 `src/login.ts:5` 抛 TypeError。11-01 412 次、11-03 377 次，量级远超其他，且 2.3.1 并未修掉。
- 放大器：`.then()` 链没有 `.catch`，也不查 `r.ok`。token 缺失/过期，或网关返回 HTML 错误页时 `r.json()` 也抛错，整页不渲染 → 白屏。
- 次因：`ChunkLoadError` 88 次，是另一条白屏路径（旧 chunk），已放进 Open 待你裁定是否纳入。
- 干扰项：`cart.ts:41` 栈溢出 19 次，是购物车，不是这个问题。

**Depth 的落地方式**：不要"加个骨架屏"这种遮蔽式修法，而是——真实异常响应用例（401/403、HTML 502、空 body）+ 一条**在修复前 commit 上必须红**的渲染测试 + app_version→commit 对齐，解释 2.3.1 为什么没让错误数下降。

**当前 Ready: no**，缺三样：
1. 真实 `/api/session` 非 200 响应样本（或允许我按日志推断构造 fixture）
2. app_version→commit 对应表（决定 412→377 是不是同一行代码）
3. 401 时的预期行为：跳转登录，还是渲染空表单？

后两条只有你能答。你给方向后，可以把这份计划交给 `/define-goal` 转成目标再跑。