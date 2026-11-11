`src/login.ts` 只有 11 行，第 5 行本身不可能报这个错：

```ts
5    .then((r) => r.json())          // 这里只解析 JSON，没有任何 .name 读取
6    .then((s) => { ... s.user.name ...})  // 真正读 .name 的是这一行
```

所以有两层要分开看：

**1. 行号是错的（误导项）**
`reading 'name'` 只可能来自第 6 行的 `s.user.name`。线上堆栈里的 `login.ts:5` 来自打包后的 bundle + sourcemap，`.then().then()` 链常被压成同一个生成表达式，映射回源码就落在链首的第 5 行。仓库里没有 `vite.config.*`/构建产物，无法核对映射，所以行号只能当线索，不能当结论。

**2. 真正的错误：`s.user` 是 undefined**
`s` 是 `/api/session` 的响应体，能导致 `s.user === undefined` 的路径在第 4 行已经有了：

- `localStorage.getItem("token")` 返回 `null` → 请求头变成 `Authorization: Bearer null`，服务端返回 401；
- token 过期/被吊销 → 同样是 401；
- 这两种情况下服务端通常回 `{ "error": "..." }` 这类错误体，而代码**没有检查 `r.ok`**，直接把错误体当 session 用，于是 `s.user` 不存在。

`logs/crashes-2026-11.csv` 和这个推断一致：2.3.0 每天 412 次、2.3.1 每天 377 次，是稳定复现的主路径错误，不是偶发；而 2.3.1 这份源码里没有任何 `r.ok` 或 `s?.user` 防护。

一个反向证据值得记一下：如果服务端在未登录时返回 HTML（网关 401 页面），第 5 行会抛 `SyntaxError: Unexpected token '<'` 而不是你这个 `TypeError`。日志里没有这类错误，说明接口确实返回了 JSON，只是这个 JSON 里没有 `user` —— 这进一步支持“把错误响应当成功响应”这个判断。

**修复方向（按优先级）**
1. 请求前判空：没有 token 直接跳登录，不发请求；
2. 判 `r.ok`（或 `r.status === 401`）→ 清理 token + 跳登录，不要 `r.json()` 后继续；
3. 兜底 `s?.user?.name`，避免数据异常时白屏。

需要我直接把这三处改到 `login.ts` 里吗？