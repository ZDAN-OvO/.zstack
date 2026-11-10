已修复 `src/login.ts`。

**根因**（与 `logs/crashes-2026-11.csv` 中的报错吻合）

原代码整条链路没有任何容错：

```ts
fetch(...).then(r => r.json()).then(s => { root.innerHTML = renderForm(s.user.name) });
```

- `s.user` 为 `undefined`（session 失效 / 接口返回空对象）时抛 `TypeError: Cannot read properties of undefined (reading 'name')` —— 日志里 377+ 次崩溃就是这一条。
- 未判断 `r.ok`，401/500 的错误体直接 `r.json()`，可能再抛解析错误。
- 没有 `.catch`，任何一次失败都会让 `innerHTML` 永不赋值，页面就是白屏。

**改动**

1. 用 `async/await` + `try/catch` 包住整个加载流程，任何异常都兜底渲染空登录表单，保证不白屏。
2. 先判断 `res.ok`，非 2xx 直接走兜底，不再解析错误响应体。
3. 无 token 时跳过请求，直接渲染表单。
4. 用可选链 + 默认值：`session?.user?.name ?? ""`，避免任意层级缺失导致崩溃。
5. 顺带对 `name` 做 HTML 转义后再插入 `value`（否则名字里的 `"` 会破坏属性、存在 XSS）。

**验证**

用 Node 的类型剥离跑了 7 个场景的 mock 测试（无 token、401、空 JSON、`user: null`、网络异常、非法 JSON、正常返回+特殊字符），全部都能渲染出 `<form>`，无 rejection、无白屏。测试脚本是临时的，已删除；仓库本身没有可用的测试依赖，所以没有新增测试文件。