修复完成，`src/login.ts`。

**崩溃排序**（`logs/crashes-2026-11.csv`，按次数）
- `TypeError ... reading 'name' at login.ts:5`：412 + 377 = **789**（最多）
- `ChunkLoadError`：88
- `RangeError: Maximum call stack`：19

**原因**：`mountLogin` 无条件读 `s.user.name`。未登录/会话过期时 `/api/session` 返回 `{"user":null}` 或 `{}`（非 2xx 时也可能返回 JSON 错误体），于是抛 TypeError。两个版本都有此问题，所以升级到 2.3.1 后仍持续。

**改动**
- 2xx 校验：非 `ok` 直接走失败分支，不再把错误体当会话解析。
- `s?.user?.name` 判空，无用户时渲染登录表单而不是崩溃。
- 加 `.catch()`，覆盖网络失败、JSON 解析失败（如返回 HTML 错误页）。

**我的自查方式**：仓库没有 `node_modules`，`npm test`（vitest）跑不起来，也没有现成测试文件，所以我用一个临时 Node 脚本 stub 了 `localStorage`/`fetch`/`root`，跑 8 种响应（正常会话、`user:null`、`{}`、`null`、401、500、fetch reject、JSON reject）：

- 改后：8/8 全部正常渲染，无异常。
- 同一脚本对改前代码：第 2 个用例即复现 `TypeError: Cannot read properties of null (reading 'name')`，确认脚本能抓到原 bug，不是空跑通过。

脚本已删除，未留在仓库里。建议后续把这两个用例固化成 vitest 测试，但那需要先装依赖，我没法在这里验证，就没擅自加。