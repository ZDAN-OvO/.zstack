看了 `src/login.ts` 和 `logs/crashes-2026-11.csv`，结论如下。

## 报错位置不在第 5 行

当前源码里：

```
4  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
5    .then((r) => r.json())
6    .then((s) => { console.log("session", s); root.innerHTML = renderForm(s.user.name); });
```

真正解引用 `.name` 的是第 6 行的 `s.user.name`。日志里 `at login.ts:5` 是构建产物经 sourcemap 映射回来的行号——sourcemap 通常把整条 promise 链映射到链首那一行的起始位置，所以 "login.ts:5" 要读成"这条 session 请求的 then 链"。这也说明 2.3.0/2.3.1 打包时的源码排版和现在工作区里的不完全一致，行号别当准。

## 为什么会 undefined

关键鉴别点：报的是 `reading 'name'`，不是 `SyntaxError` / `Unexpected end of JSON input`。也就是说：

1. `fetch` 成功了（HTTP 401/500 不会让 fetch reject）；
2. `r.json()` 也成功解析了 —— 响应确实是合法 JSON；
3. 但那份 JSON 里**没有 `user` 字段**，所以 `s.user === undefined`，取 `.name` 抛出 `TypeError`。

最可能的路径是 token 不存在：

- `localStorage.getItem("token")` 在未登录、隐私模式、跨域 iframe、或 storage 被清时返回 `null`；
- 于是请求头变成 `Authorization: Bearer null`；
- `/api/session` 返回 401 + `{"error":"unauthorized"}` 这类 body；
- line 5 拿到 `{error: ...}`，line 6 炸掉。

`2.3.0` 和 `2.3.1` 两天各 ~400 次、量级基本不变，说明这是**常态路径**（未登录用户直接落到这个页面），不是偶发边界情况。另外仓库里没有后端代码，`/api/session` 的正常返回结构无法从代码确认，这也是一个待验证项。

## 三步确认（十分钟内）

1. DevTools Network → `/api/session` 的 status 和 Response body。是 `{error:...}` 还是 `{}` 还是 `{user:null}`，直接定性。
2. 第 6 行本来就有 `console.log("session", s)`，在崩溃前就执行了。翻崩溃报告的 breadcrumb / 控制台日志，能看到真实 body，不用复现。
3. `curl -i -H "Authorization: Bearer null" localhost/api/session` 对比有无 token 的返回差异。

## 修法

根因是"没检查 HTTP 状态就假设 body 形状"，只加 `?.` 会把未登录静默渲染成空表单，掩盖问题。建议同时补状态检查和可选链，并区分"未登录"和"接口挂了"：

```ts
export function mountLogin(root: HTMLElement) {
  const token = localStorage.getItem("token");
  fetch("/api/session", { headers: token ? { Authorization: `Bearer ${token}` } : {} })
    .then((r) => {
      if (r.status === 401) return null;          // 未登录是正常分支
      if (!r.ok) throw new Error(`session ${r.status}`);
      return r.json();
    })
    .then((s: { user?: { name: string } } | null) => {
      root.innerHTML = renderForm(s?.user?.name ?? "");
    })
    .catch((e) => {
      console.error(e);
      root.innerHTML = renderForm("");            // 或渲染错误态
    });
}
```

顺带一提，`package.json` 里声明了 `vitest` 但仓库里没有任何测试文件。这个函数很适合加一个用例：mock fetch 返回 401 + `{error:"unauthorized"}`，断言不抛异常。要不要我把测试和这个修复一起落下来？