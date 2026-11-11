## 崩溃点

`src/login.ts` 第 5–6 行：

```ts
5   .then((r) => r.json())
6   .then((s) => { console.log("session", s); root.innerHTML = renderForm(s.user.name); });
```

报错文案是 **reading 'name'**，说明 `s` 本身是有值的，**是 `s.user` 为 `undefined`**，于是 `undefined.name` 抛错。（如果响应体为空，报文会是 "reading 'user'"。）线上报的行号是 5 而不是 6，是打包／source map 把链式调用的行号归到了上一行，位置就是这句。

## 为什么 `s.user` 会是 undefined

三条叠加的原因：

1. **第 3 行 `localStorage.getItem("token")` 很可能返回 `null`**（未登录、被清缓存、隐私模式）。于是第 4 行发出的是 `Authorization: Bearer null`。
2. 服务端对非法 token 返回 401，body 类似 `{"error":"unauthorized"}`。**`fetch` 不会因为 4xx/5xx 而 reject，`r.json()` 照样成功解析**，所以第 6 行的 `s` 是一个错误对象，`s.user` 不存在。
3. **没有 `r.ok` 检查、也没有 `.catch()`、也没有 `?.`**，所以第一个真实失败直接变成线上 TypeError。

这也是 `logs/crashes-2026-11.csv` 里 2.3.0/2.3.1 每天 400 次左右、跨版本持续出现的原因——它不是偶发，而是「未登录用户进入登录页」这条必经路径。

顺带一提：TypeScript 没能在编译期拦住这里，是因为 `Response.json()` 返回 `Promise<any>`，`s.user.name` 一路静默通过类型检查。

## 建议的修法

```ts
export function mountLogin(root: HTMLElement) {
  const token = localStorage.getItem("token");
  if (!token) return showLoginForm(root);          // 没有 token 就别请求

  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
    .then(async (r) => {
      if (r.status === 401) { showLoginForm(root); return null; }
      if (!r.ok) throw new Error(`session failed: ${r.status}`);
      return r.json() as Promise<{ user?: { name?: string } }>;
    })
    .then((s) => {
      if (!s?.user?.name) return showLoginForm(root);
      root.innerHTML = renderForm(s.user.name);
    })
    .catch((err) => { console.error(err); showLoginForm(root); });
}
```

要我直接改到文件里吗？另外目前 `src/` 下只有 `login.ts`，没有对应测试，`npm test` 里也没有覆盖这条 401 分支。