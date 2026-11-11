已修好并自检过。

**定位**：`logs/crashes-2026-11.csv` 里压倒性多的是 `TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5`（789 次，另两类合计 107 次）。原因是 `/api/session` 返回的响应体里没有 `user`（token 缺失/过期时常见），代码直接读 `s.user.name`。

**改动**：`src/login.ts`
- 没有 token 时不再发请求，直接渲染登录入口
- 非 2xx（如 401）不解析响应体
- `user.name` 缺失时回退到登录入口，而非读取 `undefined`
- 加上 `.catch`，网络失败不会变成未处理的 rejection

**自检**：用 Node 原生类型剥离跑了 5 个场景（无 token、正常 session、**无 user 的 session**、401、网络异常），全部通过且无 unhandledRejection；同时用改动前的代码复现了同一个 `TypeError`，确认诊断没跑偏。

顺带提一句：项目里没有装依赖也没有测试文件，`npm test` 目前跑不起来，所以这次是临时脚本验证的；要长期防回归，得补个 vitest 用例。