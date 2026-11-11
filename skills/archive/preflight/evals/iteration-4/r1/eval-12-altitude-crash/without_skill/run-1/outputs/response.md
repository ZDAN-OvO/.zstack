修好了。崩溃排行第一的是：

| error | 次数 |
|---|---|
| `TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5` | 412 + 377 = **789**（占全部 896 条的 88%） |

**根因**：`src/login.ts` 里直接访问 `s.user.name`。当会话失效/未登录时，`/api/session` 返回的 `s` 里没有 `user`，于是抛 TypeError。

**改动**（`src/login.ts`）：
- 用可选链安全取值 `s?.user?.name`，并校验是字符串，缺失时回退为空的登录表单（而不是崩溃）。
- 加了 `.catch()`，网络错误/JSON 解析失败时记录日志并渲染空表单。
- 顺手把 `name` 做了 HTML 属性转义，避免会话数据注入到 `value="..."` 造成 XSS。

```ts
.then((s) => {
  console.log("session", s);
  const name = s?.user?.name;
  root.innerHTML = renderForm(typeof name === "string" ? name : "");
})
.catch((err) => {
  console.error("failed to load session", err);
  root.innerHTML = renderForm("");
});
```

仓库里没有 node_modules（`tsc`/`vitest` 都不可用），所以只做了人工检查，没能跑类型检查/测试。

另外两个崩溃没动：`ChunkLoadError: chunk 7`（88 次，通常是发版后旧 chunk 被删，需要构建配置或刷新策略）和 `cart.ts:41` 的栈溢出（19 次，但仓库里没有 `cart.ts`）。需要的话可以继续查。