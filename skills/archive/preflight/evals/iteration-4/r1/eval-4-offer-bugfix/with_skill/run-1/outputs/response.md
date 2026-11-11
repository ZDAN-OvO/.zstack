看完了，先把“能查的事实”摆出来（不是猜的）：

**根因机制**（`src/login.ts:5`）
- `localStorage.getItem("token")` 为 `null` 时仍然发请求，头是 `Bearer null` → 后端 401。
- 401 的响应体被 `r.json()` 解析，里面没有 `user` → `s.user.name` 抛 `TypeError`。
- 抛在 `.then` 里，链上**没有 `.catch`**，而 `root.innerHTML` 只在成功路径赋值 → 页面白白一片，控制台一条 unhandled rejection。
- “偶尔”是因为只在 token 缺失/失效那批请求上出现。

**日志证据**（`logs/crashes-2026-11.csv`）
- 同一个 `TypeError ... at login.ts:5`：2.3.0 有 412 次，2.3.1 有 377 次 —— 升级没修掉。
- 另有 `ChunkLoadError: Loading chunk 7 failed` 88 次：**第二个独立的白屏成因**（发版后旧 chunk 失效），不在 login.ts 里。
- `cart.ts:41` 的 RangeError 与登录无关。

**还看到一个你没问的**：`${name}` 直接拼进 `innerHTML`，是注入面。

所以“修一下这个 bug”有三种可能的落点，你选：

**Altitude**
1. `Hand over`：登录页对崩因清单里每种失败都有确定可见状态（加载 / 未登录 / 会话失效 / 网络失败 / 新版本待刷新），并且留证据。范围 = login.ts + 回归测试。
2. `Fallback`：只加守卫和空状态，堵住 `user.name` 这一条路径。
3. `Ceiling`（我判断超出单 PR，需部署权限）：应用外壳保证任何异常都不白屏 —— 全局 error boundary + chunk 缓存策略。

**Depth**：专家动作不是补 `if`，而是枚举所有让 `innerHTML` 永不执行的分支（无 token、非 JSON 体、`r.json()` reject、无 catch、无加载态），用 vitest + 假 fetch 按日志里真实出现过的响应形状建用例表；拉伸目标是**先写一条能在现在代码上复现该 TypeError 的失败用例**，再修到绿，并加日志里没出现但会发生的形状（401 HTML 体、离线）做 held-out。

**Range**：动词是 不白屏 → 说清原因 → 能重试 → 留证据；crew = 可靠性（mount 状态机）、安全（innerHTML）、测试作者、红队（找 ChunkLoadError / cart.ts 这类其他白屏口）。

**Judge**：模型自跑 —— 测试套件在现行代码上必须红、修完必须绿，且**只守 `user.name` 一条路径判不合格**（评方法不只评结果）；你侧的下周判定是日志里 `login.ts:5` 计数归零。

需要你回答的五问（只有你知道）：

1. **Purpose** —— 这次是止住用户报障、让下次故障可定位，还是过上线评审？这决定范围。
2. **Context** —— 谁触发登录页：直接访问、会话过期跳转、还是多标签页？token 由谁写入和清除？白屏是用户唯一的反馈渠道吗？（`/api/session` 失败时返回什么体，仓库里查不到，你知道或者能抓到吗）
3. **Materials** —— 主源我按 `crashes-2026-11.csv` + `src/login.ts` 排了；有没有禁用源？后端契约代码在哪？
4. **Boundaries** —— 哪些结果会让你说“不是我要的”？我暂列：不改后端、不动 UI 视觉、不在这次引入框架级重构。
5. **Done** —— 什么出现在你面前算完？我暂列：先看崩因清单+用例表（checkpoint），再要“红灯测试 + 修后全绿”。

一个硬约束：仓库里 `test` 脚本在，但**没有 vitest 依赖、没有配置、没有任何测试文件**，判定线得先搭起来。

计划已写在 `local/plans/login-white-screen.md`，`Ready: no`（三轴未裁决、五问未答、API 契约和测试脚手架缺失）。你回完这五点我就把 Ready 改成 yes，然后用 `/define-goal` 以这份计划为源。