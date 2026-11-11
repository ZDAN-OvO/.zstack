已修好，并且自己验证过了。

**logs 里最多的崩溃**（789 次，占全部 896 次的 88%）：
`TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5`

**根因**：`src/login.ts` 无条件访问 `s.user.name`。当 `/api/session` 返回 401/非 JSON、响应体缺 `user`，或 token 缺失时，`s.user` 为 undefined，直接抛错，且整条链没有 `catch`（还会产生未处理的 rejection）。

**改动**（`src/login.ts:1-14`）：
- 非 2xx 响应不再解析，直接按“无会话”处理
- JSON 解析失败降级为 `null`
- `s.user.name` 改为 `s?.user?.name ?? ""`，未登录就渲染空表单
- 补 `.catch()` 兜底网络错误（避免 unhandledRejection）
- token 为空时不再发 `Bearer null`

**自检结果**（本机无 vitest/node_modules，用 Node 26 原生类型剥离 + 假 DOM/fetch 直接跑 `mountLogin`）：

| 场景 | 结果 |
|---|---|
| 200 + `{user:{name:"Ada"}}` | PASS，渲染 `Ada` |
| 401 + `{error:...}` | PASS，空表单 |
| 200 + `{}` | PASS，空表单 |
| 200 + `{user:null}` | PASS，空表单 |
| 200 + HTML（非 JSON） | PASS，空表单 |
| fetch 网络失败 | PASS，空表单 |

6/6 通过，无未处理 rejection。验证脚本放在 `/tmp/verify-login.mts`（没往仓库里塞测试脚手架；若要纳入 CI 我可以改成 vitest 用例，但当前环境没装依赖，跑了也是假的）。

顺带一提，`cart.ts:41` 的 `Maximum call stack size exceeded`（19 次）是第二类问题，本次没动。