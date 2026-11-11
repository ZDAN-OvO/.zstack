已修复 `src/login.ts`。

**根因**（与 `logs/crashes-2026-11.csv` 一致，共 789 次崩溃）：
- 崩溃日志里 `TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5` 指向 `s.user.name`。
- token 缺失/过期时，`/api/session` 会返回 401 或缺少 `user` 的响应体，`.then` 里直接取 `s.user.name` 抛异常；而 `fetch` 链路没有 `.catch`，异常未捕获，`root.innerHTML` 永远不会被赋值 → 白屏。
- 另外 token 为 `null` 时还会发出 `Authorization: Bearer null` 的无效请求。

**改动**：
1. 无 token 时不发请求，直接渲染空登录表单。
2. 检查 `r.ok`，非 2xx 走错误分支，不再把错误响应当 session 解析。
3. `s?.user?.name ?? ""` 兜底，响应结构异常也不会抛错。
4. 增加 `.catch`：记录错误、清除失效 token、渲染空表单，保证页面始终能显示。

顺带提醒：`renderForm` 用模板字符串把 `name` 直接拼进 `innerHTML`，如果用户名来自服务端且含 `"`/`<`，存在 XSS 风险，建议后续用 `textContent` 或做 HTML 转义——这次没动，以免影响现有渲染输出。