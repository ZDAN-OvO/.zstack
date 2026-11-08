看了 `src/login.ts`，白屏的原因基本可以定位到这一段：

```ts
const res = await fetch('/api/session');
const s = await res.json();
root.innerHTML = s.user ? '' : '<form id="login"></form>';
```

`mountLogin` 只在 fetch 和 `res.json()` 都成功之后才写 DOM。只要 `/api/session` 请求失败（网络抖动、5xx、超时），或者返回的不是 JSON（网关返回 HTML 错误页、Session 过期返回空 body），promise 就直接 reject 了，`innerHTML` 一行都没执行 —— `root` 保持空的，用户看到的就是白屏。这也解释了为什么是"偶尔"：正常情况下请求成功，看不出问题。

已改成兜底渲染：

```ts
export async function mountLogin(root: HTMLElement) {
  try {
    const res = await fetch('/api/session');
    if (!res.ok) throw new Error(`/api/session returned ${res.status}`);
    const s = await res.json();
    root.innerHTML = s?.user ? '' : '<form id="login"></form>';
  } catch (err) {
    console.error('[login] session check failed', err);
    root.innerHTML = '<form id="login"></form>';
  }
}
```

改动点：
1. `try/catch` 包住，异常时至少渲染登录表单，不再留空 DOM。
2. 加了 `res.ok` 判断，5xx/4xx 不再被当成正常 JSON 去解析。
3. `s?.user` 防止 body 是 `null` 时抛 TypeError。

两点需要你确认：

- 兜底时渲染登录表单是我的判断（用户至少还能登录）。如果你们更希望这种场景显示"服务暂时不可用，请重试"之类的错误态、而不是表单，我改成那个。
- Session 校验失败就展示登录表单，前提是这份代码不负责"已登录则跳转"。如果已登录用户本该被重定向走，那 `s.user ? ''` 这个分支本身就是另一个白屏来源，需要一起看。

另外这只是按代码路径的推断，我没有运行环境复现。要确认根因，最直接的办法是在白屏时看 Console 有没有 `[login] session check failed` 和 Network 里 `/api/session` 的状态码——如果确实是 5xx/中断，那这个改动就修掉了。需要的话我可以把这段抽成可测的函数，补一个 fetch 失败时仍渲染表单的用例。
