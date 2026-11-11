你说得对，那份计划把“白屏”当成了“没内容先占位”，方向就错了。按 `logs/crashes-2026-11.csv` 看，真正的问题在 `src/login.ts`：骨架屏只是把“白屏”换成了“永远转圈”，因为渲染根本不会发生。

## 根因

```ts
fetch("/api/session", ...)
  .then((r) => r.json())
  .then((s) => { root.innerHTML = renderForm(s.user.name); });  // 崩在这
```

崩溃日志里 789/896 次是 `TypeError: Cannot read properties of undefined (reading 'name')`，就在这一行。`/api/session` 的响应体不保证有 `user.name`，而这段代码无条件相信它：

- token 过期或缺失 → `Authorization: Bearer null` → 401 → body 是 `{error:...}` → `s.user` 是 `undefined` → 抛错
- 204 空响应或网关返回 HTML 错误页 → `r.json()` 直接抛 `SyntaxError`
- 兜底路径也没有 catch → Promise rejection 被吞掉，`root.innerHTML` 保持空 → 白屏

也就是说，白屏的本质是**未捕获的 Promise 异常**，不是缺少 loading 态。加骨架屏反而把错误藏得更深（用户看到一个永远不消失的占位）。

另外日志里 88 次 `ChunkLoadError: Loading chunk 7 failed` 是发版后旧 chunk 的缓存问题，属于另一个 bug，别混进这次修复。

## 已做的修改

- `src/login.ts`：补 `token` 判空（不再发 `Bearer null`）、判 `r.status === 401/403` 清 token 并回登录表单、判 `!r.ok`、`json()` 失败兜底、`user.name` 类型校验；所有失败分支都渲染出可操作界面（重试按钮）而不是留空 DOM；顺手把 `name` 做了属性转义（原来有注入风险）。
- `src/login.test.ts`：7 个回归测试，覆盖 200 正常 / 401 / 200 缺 `user` / 非 JSON 响应 / 5xx / 无 token / 引号注入。`npx vitest run` 全绿。

## 需要你确认

1. 计划里 `Declined: —`，但 `Boundaries` 写的是“不改后端接口”，我严格遵守了；如果后端本来就应该在未登录时返回 `{user:{name}}` 的空壳，那需要另外推后端，前端这层校验只是防御。
2. `Judge` 里的“一周内该错误为 0”得等上线后看日志，现在只能保证测试通过。
3. 我装了 `vitest` 到 devDependencies（`node_modules` 之前是空的，`npm test` 本来跑不起来），`package.json` 里没有 `jsdom`，测试用假 root 对象，不需要 DOM 环境。
4. 计划本身要不要改？建议把 `Materials` 指到具体崩溃行、`Done` 补上“失败分支有可见 UI”，否则下次还会写出骨架屏这种答案。