你的判断对：骨架屏只是把白屏换成了“永远转圈”，崩溃日志里那条错误一次都没少。真正的原因在日志和代码里已经写得很清楚了。

## 根因

`logs/crashes-2026-11.csv` 里 2.3.1 的主错误是 377 次/天：

```
TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5
```

对应 `src/login.ts` 的 `s.user.name`。链路是：

1. token 过期/无效时 `/api/session` 返回 **401 + `{error: "..."}`**，但代码没查 `r.ok`，直接把错误体当 session；
2. `s.user` 是 `undefined` → `.then` 里抛异常；
3. 异常发生在 promise 回调里，所以 `root.innerHTML = ...` **永远执行不到**，页面保持空白；
4. 另外 `localStorage` 无 token 时会发出 `Bearer null`，必然 401 —— 这是最先复现的那条路径。

骨架屏盖不住第 3 步：请求成功后那行渲染代码依然不会执行。而且原代码没有 `catch`，用户侧只剩一个 unhandled rejection。

## 已做的修复

`src/login.ts`
- 无 token 直接渲染空表单，不再发必失败的请求；
- 检查 `res.ok` 和 `session.user`，不符合就抛错；
- 统一 `catch`，渲染 `role="alert"` 的错误提示（含重试引导），不再白屏。

`src/login.test.ts` 新增 5 个回归用例：正常 200、401 错误体、200 但无 user、网络失败、无 token。已装 vitest（`package.json` devDependency），`npm test` 5/5 通过。

## 与 plan 的差距，需要你确认

- plan 写的 `Depth: 先看崩溃日志`，上一轮执行显然跳过了，才会去做骨架屏这种通用兜底；
- 本 PR 只覆盖登录这条 TypeError。日志里另有 `ChunkLoadError`（88 次，发版缓存问题）和 `cart.ts:41` 栈溢出（19 次），**不在本次范围**，建议单独开任务；
- `Judge` 里的“一周内崩溃日志该错误为 0”只能上线后验证，PR 里能保证的只有回归测试通过。如果演示前只想要最低风险，这条修复足够；如果要求“白屏不再出现”，那 `ChunkLoadError` 也得一起处理，需要我继续吗？