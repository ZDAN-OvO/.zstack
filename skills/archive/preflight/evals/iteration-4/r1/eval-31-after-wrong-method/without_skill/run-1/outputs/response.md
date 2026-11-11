问题不在骨架屏；真正原因就在 `logs/crashes-2026-11.csv` 中，执行时没有读取该文件。

## 真正原因

崩溃日志中占绝对多数（412 + 377 = 789 次）的错误是：

```
TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5
```

这对应 `src/login.ts` 第 6 行：

```ts
.then((s) => { console.log("session", s); root.innerHTML = renderForm(s.user.name); });
```

当 `/api/session` 返回 401 JSON，例如 `{"error":"unauthorized"}`，或者返回空对象时，`s.user` 实际上是 `undefined`，于是读取 `.name` 会直接抛出异常。这个异常发生在 promise 链中，导致：

1. `root.innerHTML = renderForm(...)` 永远不会执行，页面因此保持空白；
2. 代码没有 `r.ok` 判断，也没有 `.catch`，网络失败或非 2xx 响应会产生未处理的 rejection，表现同样是白屏；
3. token 不存在时还会发送 `Authorization: Bearer null`，更容易得到 401。

加载骨架屏会在请求发出前让页面不空白，但请求返回后仍然抛出异常，骨架屏之后照样白屏，所以“结果不行”。而且当前工作区的 `src/login.ts` 还是原始有 bug 的版本，没有骨架屏改动，估计那边改动没有同步过来。

## 已修

`src/login.ts`
- 先渲染空白登录表单，保证任何路径都有内容；
- 增加 `!r.ok` 判断：401 等直接视为无会话；
- 改用 `session?.user?.name`，并校验类型，不再假定 `user` 存在；
- 增加 `.catch` 处理网络失败；
- 没有 token 时不发 `Bearer null`；
- 对用户名做 HTML 转义，因为原来会直接拼进 `value="..."`。

`src/login.test.ts`（新增 6 个用例）
- 401 → 渲染表单，不留下白屏；
- 200 但 `{}`（崩溃日志签名）→ 不抛出异常、渲染表单；
- fetch 抛出异常 → 渲染表单；
- 正常会话 → 渲染用户名；
- 用户名转义；
- 无 token 时不发 Authorization 头。

`package.json` 加了 `vitest` devDependency。

## 验证

```
npm test  →  6 passed
```

我还用原始 `login.ts` 跑了一遍这套测试：5 个用例失败（含未处理 rejection），说明测试确实能拦住这个回归，不是只覆盖了正常路径。

## 计划本身的问题

计划里 `Depth: 先看崩溃日志`、`Materials: logs/crashes-2026-11.csv` 都写对了，但执行跳过了这一步，直接进入 UI 空态处理。另外 `Judge` 要求“一周内崩溃日志该错误为 0”，这只能在发布后验证；建议在 `Done` 里补上“无会话、空 payload、网络失败三种路径都不白屏”的可测条件，否则下次还会优先做骨架屏这类表面修法。