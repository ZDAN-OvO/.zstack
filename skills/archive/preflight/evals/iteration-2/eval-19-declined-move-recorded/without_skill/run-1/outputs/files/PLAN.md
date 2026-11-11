# PLAN: 修复登录页 session 缺 user 导致的崩溃

## 0. 边界确认
- 只修 **1 个** 崩溃：`TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5`
- 不改后端（`/api/session` 的行为保持原样）
- 不动其它崩溃：`ChunkLoadError`（88 次）、`cart.ts:41` RangeError（19 次）
- 不把目标扩展成"登录页零崩溃"；判据是**演示路径不崩 + 有回归测试**

## 1. 事实基座
- `logs/crashes-2026-11.csv` 共 4 类、896 次；本崩溃 **789 次（88%）**，横跨 2.3.0 / 2.3.1
- `src/login.ts:5`：`root.innerHTML = renderForm(s.user.name)`；`s.user` 为 `undefined` 时抛错
- 抛错的后果不是"一个错误弹窗"：`.then` 中断 → `innerHTML` 从未赋值 → **登录页整块空白**（演示当天直接白屏）
- 触发条件：`/api/session` 返回 200 但 body 里没有 `user`（或 `user: null`）

## 2. 修复（src/login.ts，最小 diff）
1. 不在表达式里取 `.user.name`，改为先取再判：
   ```ts
   .then((s) => {
     const user = s?.user;
     root.innerHTML = renderForm(user?.name);   // 缺 user 时退化为空表单，不抛错
   });
   ```
2. `renderForm(name?: string)` 内 `const value = name ?? ""`，保持输出 HTML 结构不变。
3. 语义选择（明确记录）：session 无 user ⇒ **视为未登录**，渲染空白登录表单。不跳转、不报错、不清 token（清 token 属于鉴权逻辑改动，超出本次范围）。

## 3. 回归测试（新增 src/login.test.ts）
环境：`vitest` + `jsdom`（当前 package.json 有 `test: vitest run` 但**未声明 vitest / jsdom 依赖，也没有 vitest.config**，需一并补上）。
- 测 1（回归，对应线上崩溃）：mock `fetch` 返回 `{}` → `mountLogin` **不抛错**，且 `root.innerHTML` 含 `<form>`
- 测 2：mock 返回 `{ user: null }` → 同上
- 测 3（happy path 防回归）：返回 `{ user: { name: "Ann" } }` → input 的 value 为 `Ann`
- 测 4：`root.innerHTML` 在请求完成后确实被写入（防止"不崩但也不渲染"的假修复）
- mock `fetch` 与 `localStorage`；不发真实网络请求

断言方式用原生 DOM 断言即可，不引入 testing-library。

## 4. 验收清单
- [ ] `npm test` 全绿，且**先在未修复代码上确认测 1 失败**（证明测试真的能抓到该崩溃）
- [ ] `npm run build` 通过
- [ ] 手动复现：devtools 把 `/api/session` 响应改成 `{}` → 修复前白屏、修复后空白表单可输入
- [ ] PR 描述里贴出 789/896 的统计与"测 1 修复前红、修复后绿"的证据

## 5. 明确不做（记录在 PR 里，避免后续被默认追认）
- `fetch` 链没有 `.catch`（网络失败/JSON 解析失败会成为 unhandled rejection，同样导致空白页）。这与本次崩溃**同一行上下文**，加一行 `.catch` 即可，但会改行为语义 → 默认不做，作为 follow-up issue 记录。
- 后端 `/api/session` 为何偶尔缺 user（真正的病根） → follow-up
- `ChunkLoadError`、`cart.ts` 栈溢出 → 不在本次

## 6. 风险 / 回滚
- 风险：若后端本该返回 user 却漏了，用户会被当成未登录，看到空表单而不是报错 → 演示可用，可接受；已在 PR 注明。
- 回滚：改动集中在 `src/login.ts` 一个文件 + 一个测试文件，`git revert` 单个 commit 即可。

## 7. 时间盒
约 1–2 小时：改动 15 分钟，测试脚手架（补依赖 + config）30–45 分钟，验证与 PR 30 分钟。
