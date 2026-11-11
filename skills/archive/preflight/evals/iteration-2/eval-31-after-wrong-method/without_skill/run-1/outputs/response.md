`local/plans/login-whitescreen.md` 里唯一能定案的线索是「Depth: 先看崩溃日志」，但上一轮没看 `logs/crashes-2026-11.csv`，所以只加了个骨架屏。日志里的真因很明确：

```
2026-11-01 2.3.0 TypeError: ... undefined (reading 'name') at login.ts:5  412
2026-11-03 2.3.1 TypeError: ... undefined (reading 'name') at login.ts:5  377
```

对应原代码第 5 行 `root.innerHTML = renderForm(s.user.name)`：

1. `/api/session` 在未登录/会话过期时返回 `{}` 或 `{user:null}`，`s.user` 是 `undefined`，取 `.name` 直接抛 TypeError。
2. 这个异常发生在 `.then` 回调里，且整条链没有 `.catch`，于是 `root` 从未被写入 → 页面永久空白（骨架屏同理卡在骨架，等于换了个白屏）。
3. 附带问题：无 token 时仍发 `Bearer null`；`renderForm` 把用户名原样拼进 `value="..."`，有 XSS；请求无超时，挂住就永远是骨架。

已在 2.3.1 仍复现 377 次，说明上一轮的改动对 Judge 指标（该错误降为 0）无效。

## 实际修复

`src/login.ts`：
- `displayName()` 用 `session?.user?.name` 并校验类型，缺字段回退空串 → 未登录正常渲染表单，不再抛异常。
- `/api/session` 的 401/403 归一化为「未登录」，5xx/非 JSON/网络失败一律 reject。
- 请求加 10s `AbortController` 超时，避免无限骨架。
- 三态渲染：表单 / 加载 / 错误+「重试」，`attempt` 序号丢弃过期响应，同步抛错也会落到错误态，任何分支都不会留白。
- 用户名做 HTML 转义；无 token 时不发 `Authorization`。

`src/login.test.ts`（新增回归测试，13 条，含 `{}`、`{user:null}`、同步抛错、失败后重试恢复、超时中止、XSS、过期响应）：用 FakeRoot 直接测挂载点，不引 jsdom。

## 验证

```
npx vitest run   → 1 file, 13 tests passed
npx tsc --noEmit --strict ... → 0 errors
```

`package.json` 补了 `vitest`/`typescript` 到 devDependencies（原本有 `test: vitest run` 但没装）。

还剩两件不在本 plan 范围内、但会影响「白屏不再出现」的事：日志里 `ChunkLoadError: Loading chunk 7 failed`（88 次，发布后旧 chunk 失效，同样表现白屏，建议 `vite build` 加 `import.meta.url` 兜底或监听 `vite:preloadError` 后 reload）和 `cart.ts:41 Maximum call stack`（19 次，购物车递归）。要不要我接着看这两个？