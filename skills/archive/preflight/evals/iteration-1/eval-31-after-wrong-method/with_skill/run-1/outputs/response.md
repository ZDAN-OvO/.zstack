已更新 `local/plans/login-whitescreen.md`（原地改，加了一行 Tries）。

判定：**方法错**，不是 rung 太大、也不是意图跑偏。原计划的 Depth 只写了"先看崩溃日志"——那是个动作，不是方法，所以跑的人没做聚合，就直接去补 UI 了。我做了一次聚合，日志已经给出答案：

- `TypeError … reading 'name' at login.ts:5`：2.3.0 412 次 + 2.3.1 377 次 ≈ 总崩渍的 88%，**跨版本不降** → 不是版本回归，是 `/api/session` 返回 401/无 `user` 时没有分支，`s.user.name` 直接炸，`fetch` 链上也没有 `.catch`，于是页面停在空白。
- `ChunkLoadError: chunk 7` 88 次、只在 2.3.0 → 白屏的**第二条独立成因**（发版后旧 chunk 失效）。
- `RangeError at cart.ts` 19 次 → 与登录无关，别顺手改。

所以骨架屏不但没修，还把抛错路径盖住了——用户看到的"加载中"永不结束，正是白屏的另一种长相。

改了三处：
- **Depth**：先按错误×版本×天计数排因，再生一个"在未修代码上跑红、报出日志那条 TypeError"的复现；断言抛错路径，不是 DOM 是否存在。
- **Judge**：评方法，PR 必须有一行根因说明，且测试必须在未改动的 2.3.1 上红过——只能靠骨架屏过的那种测试判失败。
- **Done**：加 checkpoint，先交 5 行根因说明再动手。

`Needs` 里两个缺口标为"缺"：2.3.1 的 sourcemap（把 `login.ts:5` 落到真实行，怀疑是打包后的行号）和过期 token 时 `/api/session` 的真实响应体。

Ready: yes —— 但有两处要你点头：`Materials` 里新加的两项你能拿到吗（拿不到就用 stub 顶，写进 stub 假设）；另外要不要顺手把那 88 次 ChunkLoadError 纳入范围，还是这次只清 TypeErrors。

确认后可以用 `/define-goal` 以这份计划为源。