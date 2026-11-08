修好了，问题出在 `src/login.ts`：原来只有一条"成功路径"，任何一步抛异常，后面的 `root.innerHTML` 就永远不执行，页面停在空 shell 上——这就是"偶尔"白屏的来源。已改成失败也渲染登录表单。

改动（[src/login.ts](src/login.ts)）：

1. **加 try/catch 兜底**：`fetch` 网络失败、`/api/session` 返回 5xx（比如网关吐 HTML 错误页）、`res.json()` 解析失败，现在都会走 catch 渲染 `<form id="login">`，不会留白。
2. **检查 `res.ok`**：原来 500/502 也照样 `res.json()`，抛的是解析错误，日志里根本看不出是状态码问题。
3. **空 body 不再致命**：`/api/session` 若返回 204 或空字符串，`res.json()` 会抛 `Unexpected end of JSON input`。现在按"未登录"处理。
4. **加 8s 超时**：请求挂住时原来会一直白屏，现在 abort 后降级到登录表单。
5. **错误日志**：catch 里打一条 `console.error`，下次再出现能从控制台直接看出是哪一类失败。

验证情况：仓库里没有 `typescript` 依赖和 tsconfig，`npm run build`（`tsc`）跑不了，所以我只做了语法检查（`node --check`，通过），没有真实跑起来点页面。你那边 `npm run build` 之后，建议手动验三个场景：断网加载、DevTools 里把 `/api/session` 改成 500、延迟 10s 响应，应该都看到登录表单而不是白屏。

一个没动的地方，需要你确认：`session.user` 为真时渲染的是 `''`，也就是已登录用户打开登录页同样是一片空白。如果这是靠路由/外壳跳转接管的，那没问题；如果没有任何跳转，这是第二条白屏路径，我可以顺手加个重定向或"已登录"占位，你说了算。
