## 结论

`login.ts` 第 5 行（`.then((r) => r.json())`）本身不会读 `name`。整个文件里只有第 6 行读取了 `.name`：

```ts
.then((s) => { console.log("session", s); root.innerHTML = renderForm(s.user.name); });
```

日志里的 `at login.ts:5` 是**打包/压缩后产物的行号**（或 sourcemap 偏差）：压缩后第 6 行的链式调用会并到上一行，所以真实出错点是第 6 行的 `s.user.name`。

真正的错误是 **`s.user` 是 `undefined`**，即 `/api/session` 返回的 JSON 里没有 `user` 字段。最常见的原因：

- `localStorage.getItem("token")` 返回 `null`（未登录/被清掉），请求头变成 `Bearer null`，服务端返回 401
- token 过期/无效，服务端返回 401，且响应体是 `{"error": "..."}` 之类
- **`fetch` 对 4xx/5xx 不会 reject**，所以 `r.json()` 照样成功解析错误响应体，然后 `.then` 里访问 `s.user.name` 才炸

## 验证

把第 5–6 行临时改成：

```ts
.then(async (r) => { const text = await r.text(); console.log("status", r.status, "body", text); return JSON.parse(text); })
```

看 `status` 是不是 401、body 里有没有 `user`。

## 修复

```ts
export function mountLogin(root: HTMLElement) {
  const token = localStorage.getItem("token");
  if (!token) {
    root.innerHTML = renderForm(""); // 或跳转登录
    return;
  }
  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
    .then((r) => {
      if (!r.ok) throw new Error(`session failed: ${r.status}`);
      return r.json();
    })
    .then((s) => root.innerHTML = renderForm(s?.user?.name ?? ""))
    .catch((e) => {
      console.error(e);
      root.innerHTML = renderForm(""); // 显示登录态失效
    });
}
```

关键两点：**检查 `r.ok`**、**用 `s?.user?.name` 兜底**，否则同类 401 在生产里还会以 `reading 'name'` 的形式报上来。