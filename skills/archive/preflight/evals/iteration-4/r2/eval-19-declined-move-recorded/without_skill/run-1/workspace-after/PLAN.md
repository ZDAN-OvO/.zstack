# Plan: 修复 session 缺 `user` 导致的登录页崩溃（单崩溃、带回归测试）

## 目标（唯一判据）
演示时登录页不再崩溃：`/api/session` 返回体缺少 `user` 时，`mountLogin` 不抛异常，页面正常渲染。

## 不做什么（明确出界）
- 不改后端、不改 `/api/session` 契约，不加重试/缓存层。
- 不动 `ChunkLoadError`（88 次）和 `cart.ts:41` 的 `RangeError`（19 次）。
- 不做登录页整体重构、不加错误上报埋点、不追求"一周崩溃为 0"。
- 不加 timeout / AbortController 之类新行为（除非实现时发现必须）。

## 事实依据
`logs/crashes-2026-11.csv`：

| error | count |
|---|---|
| `TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5` | 789（412 + 377） |
| `ChunkLoadError` | 88 |
| `RangeError at cart.ts:41` | 19 |

最多即 `login.ts:5`，占本月约 88%，与用户描述的"session 接口偶尔不返回 user"一致。

根因（`src/login.ts:5`）：

```ts
.then((s) => { ... root.innerHTML = renderForm(s.user.name); });
```

`s.user` 为 `undefined` 时读 `.name` 直接抛 TypeError，整页白屏。

## 改动（1 个文件，约 3 行）
`src/login.ts`：

1. `s?.user?.name` → 取不到时用安全默认值 `""`（而不是抛错）。
2. `fetch` 结果补一层健壮性：`r.ok` 为 false 或 `r.json()` 失败时，同样走"无 user"分支，不产生未处理的 rejection（`.catch`）。
3. `renderForm` 入参类型保持 `string`，默认值兜底在调用点完成，签名不变。

保持公开 API `mountLogin(root)` 不变，调用方零改动。

## 回归测试（先红后绿）
现状障碍：`vitest` 在 `scripts.test` 里被调用，但 `package.json` 的 `dependencies` 只有 `react`，仓库无 `node_modules`、无 `vitest.config.*`。因此测试前需先补最小测试基建。

1. `package.json` 增加 `devDependencies`: `vitest`、`typescript`（版本实现时按 Node >= 20 选取），保留已有 `test` 脚本不动。
2. 新增 `src/login.test.ts`，用 `vi.stubGlobal` 打桩 `fetch` 与 `localStorage`，用 `{ innerHTML: "" }` 作为 `root`，避免引入 jsdom：
   - case A（复现崩溃，修复前失败）：`fetch` 返回 `{}` → `await` 冲刷微任务后断言未抛错，且 `root.innerHTML` 含 `<form>`。
   - case B（正常路径不回归）：返回 `{ user: { name: "Ann" } }` → 断言 `value="Ann"`。
   - case C（接口异常）：`fetch` 返回 `ok: false` 或 `json()` reject → 断言未抛未处理的 rejection，仍渲染表单。
3. 先只加 case A 跑一次，确认在未修复的 `login.ts` 上**失败**（证明测试真的覆盖了这个崩溃），再改 `login.ts` 让它转绿。

## 验证
- `npm test` 全绿（3 个 case）。
- `npm run build` 通过（TypeScript 未因可空性改动报错）。
- 手工冒烟：本地把 `/api/session` 响应 mock 成 `{}`，登录页可渲染、控制台无 TypeError。
- 不做长周期崩溃率观测——演示前只看上面三条。

## 交付（一个 PR）
- 分支：`fix/login-session-missing-user`
- 内容：`src/login.ts`、`src/login.test.ts`、`package.json`/lock 的 devDeps；可选 `vitest.config.ts`（若需要 `environment: "node"` 默认即可则不加）。
- PR 描述：崩溃条数与占比 → 根因一行 → 改动 diff → 测试红转绿证据（贴修复前失败、修复后通过两次输出）→ 明确写出"本次只修 login.ts:5，其余两个崩溃另开 issue"。
- 评审关注点小、可 10 分钟内合入，符合下周演示的时间约束。

## 风险与回退
- 风险：默认值 `""` 会让"session 异常"看起来像"新用户空名字"。可接受——演示优先不崩；后续单独做提示/登录跳转。
- 回退：单文件改动，`git revert` 该 commit 即恢复原状，不影响后端与其他页面。
