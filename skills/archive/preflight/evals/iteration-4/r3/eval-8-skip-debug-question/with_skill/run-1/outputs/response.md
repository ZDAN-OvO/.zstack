看了 `src/login.ts` 和 `logs/crashes-2026-11.csv`，结论如下。

## 第 5 行只是报错位置，不是出错原因

`src/login.ts` 的 1–6 行：

```ts
1  export function mountLogin(root: HTMLElement) {
2    console.log("mount login");
3    const token = localStorage.getItem("token");
4    fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
5      .then((r) => r.json())
6      .then((s) => { console.log("session", s); root.innerHTML = renderForm(s.user.name); });
```

真正的取值在**第 6 行** `s.user.name`。生产堆栈里的 5 是打包 + sourcemap 映射到的行（整个 promise 链的首行），所以两者不是同一个位置。

## 是谁是 undefined

`Cannot read properties of undefined (reading 'name')` 只能说明 **`s.user` 是 undefined**。如果 `s` 是 undefined，报的会是 `reading 'user'`。所以：

- `fetch` 成功了，`r.json()` 也解析成功了
- 但返回的 JSON 里**没有 `user` 字段**

三个具体来源，按可能性排：

1. **`/api/session` 返回了非 200**。`fetch` 对 401/403/500 不抛异常，`r.json()` 照样把错误体解析出来，比如 `{"error":"unauthorized"}` → `s.user` 是 undefined。代码里没检查 `r.ok`，这条路径完全静默。
2. **`localStorage` 里没有 `token`**。第 3 行拿到 `null`，第 4 行发出 `Authorization: Bearer null`，服务端按未登录处理 → 回到第 1 种情况。
3. **接口返回的形状和这里假设的不一致**（包了一层，或者改成了 `{data:{user}}`）。

## 为什么 TypeScript 没拦住

`r.json()` 的类型是 `any`，所以 `s.user.name` 一路畅通。这是这个 bug 能上线的原因，不是运气问题。

## 这不是偶发

`logs/crashes-2026-11.csv` 里同一个错误：

| 版本 | 次数 |
|---|---|
| 2.3.0 | 412 |
| 2.3.1 | 377 |

两个版本合计 789 次，且 2.3.1 里还在发生——说明线上有稳定复现的未登录/过期 token 路径，不是边角情况。修复方向是把「没有 session」当作正常分支渲染登录表单，而不是当成有 user 的表单：

```ts
.then((r) => (r.ok ? r.json() : null))
.then((s: { user?: { name: string } } | null) => {
  root.innerHTML = renderForm(s?.user?.name ?? "");
});
```

要我直接改进 `src/login.ts` 并补一个 vitest 用例（401 时渲染空表单、不发 `Bearer null`）吗？