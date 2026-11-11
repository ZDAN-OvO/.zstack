计划已写入 `PLAN.md`，要点如下：

**范围**：只修 `src/login.ts:5` 的 `TypeError`（日志里 412+377=789 次，占本月约 88%）。`ChunkLoadError`(88) 和 `cart.ts:41`(19) 另开 issue，不动。

**根因**：`.then((s) => root.innerHTML = renderForm(s.user.name))`，`user` 为 `undefined` 时读 `.name` 抛错导致白屏。

**改动**：单文件约 3 行 —— `s?.user?.name` 取不到时回退 `""`，并给 `fetch`/`json()` 加 `.catch` 与 `r.ok` 分支；`mountLogin(root)` 与 `renderForm(name: string)` 签名不变。

**回归测试**：先要补基建 —— `vitest` 只在 `scripts.test` 里被调用，但 `package.json` 只有 `react` 依赖，`node_modules`、`vitest.config.*` 都不存在，所以 PR 里要加 devDeps。测试用 `vi.stubGlobal` 打桩 `fetch`/`localStorage` + `{innerHTML:""}` 当 root，不需要 jsdom；三个 case：缺 `user`（修复前必红）、正常路径不回归、接口异常不产生未处理 rejection。要求先看到 case A 失败再改代码。

**完成判据**：`npm test` 全绿 + `npm run build` 通过 + 本地 mock `{}` 冒烟；不做长周期崩溃率观测，不把"一周为 0"当门槛。

**PR**：分支 `fix/login-session-missing-user`，描述里贴红转绿的两次输出，并写明其余两个崩溃另开 issue。