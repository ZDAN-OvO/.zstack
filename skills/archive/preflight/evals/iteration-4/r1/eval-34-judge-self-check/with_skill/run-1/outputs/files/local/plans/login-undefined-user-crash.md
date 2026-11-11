# Plan: 修掉最大的崩溃（login.ts 读取 undefined 的 name）

- Asked: 把 logs 里那个最多的崩溃修掉（判断标准：「你自己检查一下就行」）
- Stage: execute
- Date: 2026-11-10

## 查到的事实（可直接当依据）

- `logs/crashes-2026-11.csv` 共 4 行、896 次事件：`TypeError ... reading 'name' at login.ts:5` = 412（2.3.0）+ 377（2.3.1）= **789 次，占 88%**，是压倒性第一。
- 同一错误在**当前版本 2.3.1 仍然发生**（11-03，377 次），所以不是「升级就好」的历史残留，是线上活的。
- `src/login.ts:5` 正是 `root.innerHTML = renderForm(s.user.name)`，行号与日志吻合，栈能直接对到源码。
- 其余两条：ChunkLoadError 88 次、cart.ts 的 RangeError 19 次，量级差一个数量级。
- 仓库无测试、无 node_modules，`npm test` 指向的 vitest 也未安装；Node 为 v26。

## Requirement

- **Hand over**: 「未登录/无效 session」被当作一等状态处理 —— 崩溃消失且 2.3.2 该错误计数归零，而不只是把第 5 行的 `.name` 补个问号。
- **Fallback**: 只加固第 5 行读取，让该行不再抛错（一个提交的量）。
- **Declined**: 无（待你裁定）。
- **Depth**: 原始材料是 CSV 的逐版本计数 + 源码行；专家动作是**按 app_version 分段判定是否回归**（2.3.0→2.3.1 没修掉），以及从日志行号反推真实输入。仪器是**可运行的复现脚本**（Node 原生跑 TS，打桩 fetch/localStorage），不是靠读代码猜。Stretch：让脚本对「只加 `?.`」的偷懒补丁**报错**，即验证方法而非验证运气。
- **Range**: 动词 = 复现 → 定位输入 → 加固 → 回归验证 → 预测计数变化。Crew：on-call/SRE（按量与版本分诊）、前端（session 状态机）、QA（红→绿回归）、红队（token 过期、网络失败、非 JSON 响应、API 返回 500 时是否仍然崩）。
- **Judge**: 你自己检查 → 采用**会话内可自跑的判据**：新增 `scripts/repro-session-crash.mjs`，修前必须崩、修后必须过，且覆盖 401 无 user / 网络错误 / 非 JSON 三种输入。它同时给方法打分：只把异常吞掉或只加 `?.` 让空用户名表单照常渲染，应判为不通过。
- **Needs**: 后端 `/api/session` 的 401 响应体形状（仓库里没有后端，**缺失**）；2.3.0 是否仍在用户手里（决定是否需要回补旧版）；如需 vitest 需联网装包，当前改用零依赖脚本规避。

## Task

- **Purpose**: 待你确认 —— 我的猜测是「登录页在无有效 session 时不能白屏/崩，用户应被明确引导去登录」。
- **Context**: 一个陌生人需要知道：这是 React+Vite 前端，登录页在挂载时拉 `/api/session`，并把返回的 `user.name` 塞进表单；2.3.1 是线上版。
- **Materials**: 一手 = `logs/crashes-2026-11.csv`、`src/login.ts`、`package.json`；二手/禁用 = 不猜 API 响应结构（缺失即记为缺失）。日志只有 11 月一个窗口，不当作全量趋势。
- **Boundaries**（墙，待确认）：① 不接受「渲染出空用户名表单」当作修好；② 本轮不动 ChunkLoadError 与 `cart.ts`；③ 不引新依赖、不改 API 契约；④ 不整体 try/catch 吞异常。
- **Done**: 先给**检查点**——复现脚本在未改代码前跑出与日志一致的崩溃（贴输出）；然后 `src/login.ts` 加固后脚本转绿并覆盖上述三种输入；附一行「2.3.2 预期该错误 789→0」的验收口径。

## Open

- `/api/session` 在 401 / 失效 token 时到底返回什么（`{}`、`{user:null}`、还是 HTML）——查不到，脚本里只能三种都当输入。
- 无 session 时的期望 UX：跳转登录路由，还是就地渲染空登录表单？这决定墙 ① 是否成立。
- 2.3.0 的 412 次要不要一起覆盖（回补旧版 vs 只发 2.3.2）。

Ready: no —— 已定的只有 Judge（自检）；Requirement 三个轴与 Task 五格仍需你裁定或改写，尤其 Purpose 与 Open 第 2 条。

（文件：`local/plans/login-undefined-user-crash.md`）
