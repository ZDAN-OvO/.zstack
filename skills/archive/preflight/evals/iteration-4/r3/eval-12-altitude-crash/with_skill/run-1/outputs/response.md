看了 `logs/crashes-2026-11.csv` 和 `src/login.ts`，先给结论再给问题。

**排序（事实）**：`TypeError ... reading 'name' @login.ts:5` = 789/896（88%），2.3.0 412 次 + 2.3.1（当前版本）377 次 → **上个版本没修掉**。其次是 ChunkLoadError 88、cart.ts 栈溢出 19。

**从代码看到的**：`src/login.ts:6` 的 `s.user.name` 假设会话响应一定带 `user`；token 为 null、401、或非 JSON 响应都会让 `s.user` 为 undefined，且整条 `.then` 链没有 `.catch` → 白屏。注意崩溃报的是 `:5`，解引用在 `:6`，说明线上 bundle 与本仓库源码有偏移。

计划已写：`local/plans/fix-top-login-crash.md`

需要你定的（其余我都按事实填了）：

1. **Purpose**：这次是「2.3.2 发版前止血」、「查清 2.3.1 为什么还有 377 次」，还是「让登录失败可统计」？三者改法不同。
2. **Altitude**：我提议顺手做到「会话不可用时不崩 + 失败留一条可数的日志」（Hand over），而不是只加 `?.` 一行（Fallback）。接受哪个？
3. **Boundaries**：哪些改动会让你说「不是我要的」？（不动视觉？不改与后端的接口约定？不新增依赖？只碰 login.ts？）
4. **Done**：我打算交付 `src/login.ts` 补丁 + 一个零依赖的 `node --test` 用例（先在旧代码上复现同一 throw）+ 3 行「2.3.1 为何仍崩」的结论。这算完吗？

另外两个查不到、需要你确认的：仓库不是 git（无法把 2.3.0/2.3.1 对到 commit），且 `cart.ts` 不存在——logs 覆盖的范围是否比这个目录大？

你回完 1–4（或直接说「按你提议的来」），我就把 Ready 改成 yes，然后可以用 `/define-goal` 以这份计划为源。