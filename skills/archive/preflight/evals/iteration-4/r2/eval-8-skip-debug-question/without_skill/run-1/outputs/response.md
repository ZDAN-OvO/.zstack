## 结论：抛出错误的是 `s.user`，`s` 本身没有问题。

看源码 `/tmp/pf-8-without_skill-ka4db1iv/src/login.ts`：

```ts
1  export function mountLogin(root: HTMLElement) {
2    console.log("mount login");
3    const token = localStorage.getItem("token");
4    fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
5      .then((r) => r.json())
6      .then((s) => { console.log("session", s); root.innerHTML = renderForm(s.user.name); });
7  }
```

几个关键点：

**1. 行号对不上，应看语义而不是行号**

这条报错信息是 `reading 'name')`，说明出错的是对 undefined 取 `.name`；全文件只有第 6 行有 `.name`。第 5 行是 `r.json()`，不可能报这个错。日志里的 `login.ts:5` 是 Vite 打包、压缩后的位置，经过转译并删空行后，行号会整体偏移，因此不能按源码行号精确对应。真正出问题的是 `s.user.name`。

**2. 直接原因：`s.user` 是 undefined**

`/api/session` 的响应体里没有 `user` 字段。典型链路：

- `localStorage.getItem("token")` 返回 `null`（未登录，或换了存储域）
- 于是 header 变成 `Authorization: Bearer null`
- 服务端返回 401，body 是 `{"error":"unauthorized"}` 之类
- **`fetch` 对 4xx/5xx 不会 reject**，`r.json()` 照样成功解析这个错误体
- `s = {error: "unauthorized"}` → `s.user` 为 undefined → 取 `.name` 抛出错误

错误信息是 `reading 'name'` 而不是 `reading 'user'`，正说明 `s` 是个正常对象，只是少了 `user`——符合“拿到的是错误响应体”。

**3. 日志佐证**

```
2026-11-01,2.3.0,...,at login.ts:5,412
2026-11-03,2.3.1,...,at login.ts:5,377
```

两个版本都稳定复现数百次，说明这是必经的稳定路径（token 缺失或过期），并非偶发竞态；跟同一文件里的 `ChunkLoadError` 无关。

## 修复方向

```ts
const token = localStorage.getItem("token");
if (!token) { redirectToLogin(); return; }          // 别发 Bearer null

fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
  .then((r) => {
    if (r.status === 401) { redirectToLogin(); return null; }
    if (!r.ok) throw new Error(`session ${r.status}`);
    return r.json();
  })
  .then((s) => {
    if (!s?.user) return;
    root.innerHTML = renderForm(s.user.name ?? "");
  })
  .catch(() => redirectToLogin());
```

如果只是想让崩溃消失，`renderForm(s.user?.name ?? "")` 一行就够，但那样会把“未登录”静默渲染成一个空表单，掩盖真正的鉴权问题。建议同时补上 `r.ok` 检查。需要我直接改吗？