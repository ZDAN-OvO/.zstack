已修复 `src/login.ts`。

**根因**（和 `logs/crashes-2026-11.csv` 对得上）

崩溃日志里出现 377~412 次的正是这一条：
```
TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5
```

`mountLogin` 里有三处会直接导致白屏：

1. **`s.user.name` 无保护**：未登录 / token 过期时 `/api/session` 返回 `{}` 或 `{user: null}`，`s.user` 是 `undefined`，抛错。
2. **没检查 `r.ok`**：401/403 通常返回 HTML 错误页，`r.json()` 直接抛错。
3. **完全没 `catch`，且 `innerHTML` 只在成功路径设置**：任何一个异常都让 `root` 永远为空 → 白屏，而且用户连登录框都看不到。

**改动**

- 进入函数先渲染兜底表单（空用户名），保证首屏永远有内容，网络慢也不白屏。
- 检查 `r.ok`，非 2xx 归入失败路径。
- 用 `s?.user?.name` 并校验是字符串，结构异常时保留兜底表单。
- 加 `.catch()` 记录错误，避免未处理的 rejection。
- 顺手对回填的 `name` 做了 HTML 转义（该值来自服务端，直接拼进 `value="..."` 有注入风险）。

需要注意的两点：

- 兜底表单目前是空用户名的登录框；如果 token 失效你还想区分「已登录」和「未登录」文案，可以再加一个 `renderForm(null)` 的分支。
- 日志里另有 88 次 `ChunkLoadError` 和 19 次 `cart.ts:41` 栈溢出，是独立的另一个问题，本次没动。