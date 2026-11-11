## 结论

真正抛出错误的那段代码其实是**第 6 行**，也就是 `s.user.name`；日志里的 `login.ts:5` 是打包或 sourcemap 对齐后的行号，不要把它当作源码行号。

```ts
6  .then((s) => { ... renderForm(s.user.name) });
```

`s` 本身是能正常解析出来的 JSON 对象，但 **`s.user` 是 `undefined`**，因此再读 `.name` 就会抛 `Cannot read properties of undefined (reading 'name')`。注意区分几种情况：

| 服务端返回 | 崩溃位置 | 报错信息 |
|---|---|---|
| JSON 里没有 `user`（如 `{"error":"unauthorized"}`，或 `user: null`） | 第 6 行 | `reading 'name'` ← 你遇到的 |
| 空响应体（204） | 第 5 行 | `Unexpected end of JSON input` |
| 返回 HTML（SPA fallback / 登录重定向页） | 第 5 行 | `Unexpected token '<'` |

最可能的触发路径是：`localStorage` 里没有 token（第 3 行拿到 `null`），于是请求头变成 `Authorization: Bearer null`，服务端返回 **401，并附带一个 JSON 错误体**。因为 fetch 对非 2xx 不会 reject，`r.json()` 会照常解析成功，于是流程走到第 6 行：`s = { error: "unauthorized" }`，`s.user` 是 `undefined`，然后崩溃。

## 修复建议

用 `r.ok` 判断状态，并对缺字段做保护；顺带不要拼接未经转义的 `name`，因为它会进入 HTML，带来 XSS 风险：

```ts
export async function mountLogin(root: HTMLElement) {
  const token = localStorage.getItem("token");
  if (!token) return renderLoggedOut(root);

  const r = await fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } });
  if (!r.ok) return renderLoggedOut(root);          // 401/500 都不再往下走
  const s = await r.json();
  const name = s?.user?.name ?? "guest";            // 关键保护
  root.innerHTML = renderForm(name);
}
```

`renderForm` 内部也建议对 `name` 做 HTML 转义（或改用 `input.value = name`），避免用户名带引号时把 DOM 撑破。

要我直接改 `src/login.ts` 吗？