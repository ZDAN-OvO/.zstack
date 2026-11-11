## Plan：修复 login.ts:5 崩溃（仅此一个）

**目标**：演示不崩。`/api/session` 偶发不返回 `user` 时，登录页不再抛 `TypeError`。

**证据**
- `logs/crashes-2026-11.csv`：`login.ts:5` 的 `TypeError: Cannot read properties of undefined (reading 'name')` 占 789/896 次（412 + 377），2.3.0 和 2.3.1 都有。
- `src/login.ts:5`：`.then((s) => { ... renderForm(s.user.name) })` — `s.user` 为 `undefined` 时直接崩。
- 其余崩溃（ChunkLoadError 88、cart.ts:41 19 次）**不在本次范围**，只记录不修。

**范围**
- 只改 `src/login.ts`：`s.user` 缺失时回退到空名字（`s.user?.name ?? ""`），表单照常渲染。
- 不改后端、不改 session 接口语义、不加重试/缓存/鉴权重构。
- 顺手：`fetch` 失败分支保持现状，避免扩大改动面。

**前置步骤（必须，当前仓库没有测试设施）**
- `package.json` 只有 `react`，无 devDependencies、无 `node_modules`、无 vitest 配置。
- `npm test` 已指向 `vitest run`，但跑不起来。步骤 1 需要补：`vitest` + `happy-dom`（devDependencies）、`vitest.config.ts`（environment: happy-dom）、`test/setup` 如需。

**执行步骤**
1. 搭最小测试环境：`react` 同版本无关，只加 vitest + happy-dom，确认 `npm test` 能在空测试集上通过。
2. 写**先失败的回归测试** `src/login.test.ts`：
   - stub `global.fetch` 返回 `{ }`（无 `user`）→ 断言 `mountLogin` 不抛错，且 `root.innerHTML` 包含一个 `<form>`。
   - 再补一条正常用例：`{ user: { name: "Ada" } }` → 断言 input 的 `value="Ada"`，防止修坏原有路径。
   - 对 `fetch` 返回 `null`/非 JSON 的容错**不测**（超出范围）。
3. 最小改动 `src/login.ts:5`：`renderForm(s.user?.name ?? "")`。
4. 本地验证：`npm test` 全绿；`npm run build` 通过。
5. 开 PR：标题 `fix(login): guard missing session.user to stop login crash`，描述里附 CSV 计数证据 + 明确声明"仅修 login.ts:5，ChunkLoadError 与 cart.ts 另开 issue"，body 里 `Closes #<崩溃 issue>`（如无 issue 就只写证据）。

**完成判据**
- 新增 2 条测试全绿，`npm test` 可重复执行。
- PR diff 只含 `src/login.ts`（1 行）、新增测试文件、测试配置与 devDependencies。
- 手工在演示环境点一次登录（session 有/无 `user` 各一次）不白屏。

**风险 / 需你拍板的一点**
- 回退成空名字会让登录页显示一个空输入框而不是报错文案。如果你要的是"提示 session 异常、请重新登录"，改动会多一个 UI 分支（仍然只在 `login.ts`），但那属于行为变更，需你一句话确认；默认按空名字走。

**不做的事**（防蔓延）：不追求"零崩溃"、不加崩溃监控指标、不处理 ChunkLoadError / cart 栈溢出、不动后端。