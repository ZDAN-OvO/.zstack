已修好 `src/login.ts`。改动要点：

- **根因**：session 接口在 token 缺失/过期时返回的 `s.user` 是 `undefined`，`s.user.name` 直接抛 `TypeError`（正是崩溃日志里 377+412 次的那条），`innerHTML` 永不执行 → 白屏。
- **降级渲染**：非 2xx 响应、`user` 缺失、`name` 非字符串时，渲染空值登录表单，而不是抛错。
- **网络兜底**：`fetch` 失败或 `r.json()` 解析失败走 `.catch`，同样渲染登录表单。
- **无 token 不再发无效请求**：不带 `Authorization: Bearer null`。
- **顺带修复**：用户名插入 HTML 属性前做转义，避免名字里带 `"` 破坏表单结构（也可能表现为页面异常）。

日志里另外两条（`ChunkLoadError` 88 次、`cart.ts:41` 栈溢出）不在本次范围内；如果你也要一并处理，我可以继续看。