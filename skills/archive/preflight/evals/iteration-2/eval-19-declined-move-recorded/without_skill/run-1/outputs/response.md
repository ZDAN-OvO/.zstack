已写到 `PLAN.md`。要点：

**范围**：只修 `login.ts:5` 的 `s.user.name`（789/896 次 = 88%，横跨 2.3.0/2.3.1）。不改后端，不碰 `ChunkLoadError`(88) 和 `cart.ts:41`(19)。

**关键一点**：这个崩溃的实际后果不是弹个错，而是 `.then` 中断、`innerHTML` 从未赋值 → **登录页空白**，正好是演示最致命的形态。

**修复**：先取 `const user = s?.user` 再判，`renderForm(name?: string)`，缺 user 时退化为空白表单（视为未登录），不动 token/跳转逻辑。

**回归测试** `src/login.test.ts`（4 个用例）：`{}`、`user: null`、正常 user、以及"确实写入了 innerHTML"防止假修复。注意 `package.json` 有 `test: vitest run` 但**没声明 vitest/jsdom 依赖、也没有 vitest.config**，要一并补——这是本任务最容易被低估的 30–45 分钟。

**验收**：先在未修复代码上确认测 1 变红，再修，PR 里贴出红转绿的证据。

**明确不做**：`fetch` 链缺 `.catch`（同一行上下文、一样会白屏，但会改行为语义）→ 记 follow-up，不顺手改；后端为何偶尔缺 user 也记 follow-up。

**回滚**：单文件 + 单测试，一次 revert。