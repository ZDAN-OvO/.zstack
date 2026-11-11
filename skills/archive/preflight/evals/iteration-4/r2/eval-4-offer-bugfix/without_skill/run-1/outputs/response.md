已修复 `src/login.ts`。

改动点：
1. **核心修复**：`session?.user?.name` 加校验，缺失时用空字符串；`session` 为 `null`/后端返回 `{}` 都不再抛 `TypeError`。
2. **兜底渲染**：整条链路加了 `.catch`，网络失败 / 非 JSON / 非 2xx 时也会渲染表单，不会再停在白屏。
3. **无 token 时直接渲染**：避免发 `Authorization: Bearer null` 的无效请求。
4. **XSS 防护**：`name` 会拼进 `innerHTML`，已做 HTML 转义（这个问题和原 bug 同源，顺手修掉）。

日志里另外两类错误不属于本次白屏：
- `ChunkLoadError: Loading chunk 7 failed`（88 次）→ 部署/缓存导致的懒加载 chunk 失效，需要处理资源版本或重试加载。
- `RangeError: Maximum call stack size exceeded at cart.ts:41`（19 次）→ 购物车逻辑的独立问题。

未安装依赖（无 `node_modules`），所以没能跑 `vitest`/`tsc` 验证。建议补一个用例：mock `fetch` 返回 `{}` 时断言 `root.innerHTML` 包含 `<form>`。需要我加上吗？