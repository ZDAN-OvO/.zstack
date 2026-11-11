看了下 `local/plans/login-whitescreen.md`、`logs/crashes-2026-11.csv` 和 `src/login.ts`——这个 bug 根本不需要 40 个文件。

**根因（范围只有一处）**

`logs` 里 400+ 次的那个错误是 `TypeError: Cannot read properties of undefined (reading 'name')`，指向 `login.ts` 里这条链：

```ts
.then((r) => r.json())
.then((s) => { root.innerHTML = renderForm(s.user.name); });  // s.user 为 undefined
```

token 缺失/过期时 `/api/session` 仍返回 200（body 没有 `user`，否则日志会是 SyntaxError），而 `fetch` 不会因 4xx/5xx 抛错、`r.json()` 也不校验，最后在 promise 里裸抛，没人 catch → 白屏。修法就是判空 + 区分"未登录"和"已登录"，再加一个复现 `{}` / `{"user":null}` 的回归测试。**改动面：`src/login.ts` + 一个新测试文件，2 个文件。**

另外，CSV 里其实是三类东西：这个 `login.ts` 崩溃（412+377）、`ChunkLoadError`（88，发版缓存问题）、`cart.ts` 栈溢出（19，另一个 bug）。后两个都不该进这个 PR。

**PR 为什么会炸成 40 个文件**

计划文件本身没给边界，agent 只能自己猜：

- `Range: —` —— 唯一该收紧的字段是空的，等于授权它随便改。
- 只有 `Boundaries: 不改后端接口`，但没写"不改路由 / 不动 `cart.ts` / 不改 localStorage key / 不重构"。
- `Judge: 回归测试通过 + 一周内崩溃日志该错误为 0` —— 后半句在会话里无法验证，于是它用"改得多、覆盖所有日志行"来代替"验证过"，顺手把 `cart.ts` 和 chunk 问题也"修"了。
- `Done: 一个 PR，含回归测试` 没定义"最小"，`Fallback: 只修当前复现的那一个白屏` 又太软，起不到刹车作用。

**建议**

1. 先把那个 PR revert 掉，别在 40 个文件上做 review 手术。
2. 计划里补三行再跑：`Range: src/login.ts（+ 新增 src/login.test.ts），其他文件只读`；`Boundaries: 不动 cart.ts / 不改路由和 localStorage key / 不处理 ChunkLoadError`；`Done: 新增测试覆盖 s.user 缺失时不抛错并渲染登录表单；git diff 文件数 ≤ 2`。
3. 把 CSV 拆成三个问题单，这个 PR 只认第一类。

要我现在按这个范围直接出最小 patch（含测试）吗？