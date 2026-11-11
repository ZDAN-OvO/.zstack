## 结论

**报错行号是错的（或来自压缩后的构建）；真正出错的是第 6 行的 `s.user.name`。**

```ts
1 export function mountLogin(root: HTMLElement) {
2   console.log("mount login");
3   const token = localStorage.getItem("token");
4   fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
5     .then((r) => r.json())
6     .then((s) => { console.log("session", s); root.innerHTML = renderForm(s.user.name); });
7 }
```

第 5 行只有 `r.json()`，没有 `.name` 访问。崩溃日志里的 `login.ts:5` 与 2.3.0/2.3.1 两个版本都一样，是典型的 sourcemap/构建行号偏移（整条 `.then` 链被打包压到一行或映射差一行）。

## 为什么是 `s.user.name`

报错是 `reading 'name'`，说明被读 `.name` 的对象是 `undefined`，即 **`s.user === undefined`**。
如果 `s` 本身是 `undefined`，报文会是 `reading 'user'`。所以问题不是「响应为空」，而是**响应里没有 `user` 字段**。

最可能的触发路径：

1. `localStorage.getItem("token")` 返回 `null`（首次访问 / token 被清 / 过期），请求头变成 `Authorization: Bearer null`；
2. `/api/session` 返回 401，body 是 `{"error":"unauthorized"}`；
3. `fetch` **对 4xx/5xx 不会 reject**，代码里也没有检查 `r.ok`，这个错误体一路进到 `s`；
4. `s.user` 是 `undefined` → `s.user.name` 抛错。

次要可能：接口返回结构变了（比如实际字段是 `session.user` 或 `data.user`）。

## 怎么最快确认

第 6 行的 `console.log("session", s)` 在崩溃前就执行了 —— 打开控制台看那条 `session` 日志，打印出来的是 `{error: "unauthorized"}` 还是别的结构，一眼就能定位。

## 顺带两个隐患

- `r.json()` 返回 `any`，TS 完全不校验，`s.user` 没有任何保护；
- 整个链没有 `.catch()`，`mountLogin` 也不返回 Promise，所以异常变成未处理的 unhandled rejection，表单根本不渲染（白屏）。

修复建议：

```ts
export function mountLogin(root: HTMLElement) {
  const token = localStorage.getItem("token");
  fetch("/api/session", { headers: token ? { Authorization: `Bearer ${token}` } : {} })
    .then((r) => (r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`))))
    .then((s) => { root.innerHTML = renderForm(s?.user?.name ?? "guest"); })
    .catch((err) => { console.error("session fetch failed", err); root.innerHTML = renderForm(""); });
}
```

需要我直接改 `src/login.ts` 吗？