看完计划和现场了，先说结论：40 个文件不是执行跑偏，是计划本身没给范围。

**计划的问题**
- `Range: —` — 没有文件白名单，等于授权它动整个前端。
- `Boundaries` 只写了"不改后端接口"，前端随便改。
- `Done: 一个 PR` 没写规模门禁，也没有"超过 N 个文件就停下来问"这种止损条件。
- `Judge` 里"一周内崩溃日志为 0"是事后指标，一晚上根本验证不了，它只能靠"多改点总没错"来凑。

**真正的原因其实已经定死了**（日志 + `src/login.ts` 对得上）：

`src/login.ts:6` — `s.user.name`。未登录/会话过期时 `/api/session` 返回 401 或空 body，`s.user` 是 `undefined`，于是 `TypeError: Cannot read properties of undefined (reading 'name')`。日志里 2.3.0 和 2.3.1 各 400+ 次，报错位置 `login.ts:5` 就是这条 `.then` 链，完全吻合。白屏是因为异常抛在 `root.innerHTML` 赋值之前，容器一直是空的。

修法大约 3 行：`r.ok` 判断 + `s?.user` 兜底，未认证时渲染登录表单而不是渲染用户名；再加一个 `fetch` 返回 401 时 `renderForm` 不抛错、能拿到 `<form>` 的回归测试。改动应该是 `login.ts` + `login.test.ts`，两个文件。

**建议的处理顺序**
1. 那 40 个文件的 PR 先关掉，不要在上面接着改 —— 现在没人能判断里面哪几行是对的。
2. 从 main 重开一个分支，只做上面那 3 行 + 测试，PR 控制在 5 个文件内。
3. 在 `local/plans/login-whitescreen.md` 里补上 `Range: src/login.ts, src/login.test.ts` 和一条止损规则（"diff 超过 5 个文件或需要动 `cart.ts` 就停"），`Done` 改成"回归测试通过 + 复现 401 时不再抛错"，把"一周崩溃为 0"挪到观测项。

**我需要你一件事**：这 40 个文件里如果包含对 `s.user` 的正确处理（哪怕写法不同），把那个分支或 diff 给我，我只 cherry-pick 那部分，其余全丢。否则我直接按上面的最小方案重做，你说一声就开工。