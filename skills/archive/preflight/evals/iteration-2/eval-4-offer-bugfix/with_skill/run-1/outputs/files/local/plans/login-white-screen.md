# Plan: 登录页不再白屏

- Asked: 帮我修一下登录页偶尔白屏的 bug，代码在 src/login.ts
- Stage: execute
- Date: 2026-11-10

## Requirement

Hand over: 登录页的每条会话失败路径都渲染确定界面（表单 / 错误提示 / 自动重试一次），失败有记录——而不是只补 `login.ts:5` 那一行。
Fallback: 只加一行保护 `s.user?.name ?? ""`。能挡住 789 次 TypeError，挡不住 ChunkLoadError 白屏。
Depth: 原始材料 = `logs/crashes-2026-11.csv`。方法 = 按失败类型分类修（401 有 error body / 返回非 JSON / 网络 reject / 旧 chunk 404），用 mock fetch 的 vitest 复现每种 payload。拉伸点 = 用日志计数检验"偶尔"这个判断（11-03 单日 377 次，说明 TypeError 是主路径，不是罕见现象）。
Range: 动词 =「root 不留空」「用户仍能登录回去」「失败在日志里可见」。crew = 前端可靠性（错误态）＋安全（name 转义）＋运维（chunk 失效/发布策略）；红队专门用 401、HTML 响应、超时、旧 chunk 打这个修复。
Judge: vitest 断言四种失败 payload 下 root 都有内容，外加一次手动复现（本地让 `/api/session` 返 401 或断网）。按"是否区分了失败类型"评分，不只看白屏是否消失。
Needs: 缺 ChunkLoadError 与发布时间的对应关系（CSV 里没有 deploy 时间戳）；缺错误上报（Sentry？）与可复现环境；仓库目前没有任何测试文件，测试要新写。
Proposed: ① ChunkLoadError 是否一起修（一次 reload 兜底 + 版本探针，会动 login.ts 之外）？② `cart.ts:41` 的 RangeError 是否在范围内？
Declined: —

## Task

Purpose: （待确认）
Context: 已查明，请你确认——
- `login.ts:5` 的 `s.user.name`：`/api/session` 返回不含 `user` 的 body 时（401 错误体等）抛 TypeError；`fetch` 没查 `r.ok`、没有 `.catch`，promise 链静默失败，`root` 保持空 → 白屏。日志行号与它一致，2.3.0/2.3.1 两天合计 789 次，2.3.1 仍未修。
- `ChunkLoadError: Loading chunk 7 failed` 88 次，只出现在 2.3.0，像发布后旧标签页取不到旧 chunk——这个更贴合你说的"偶尔"。
- `cart.ts:41` 的 RangeError 19 次，与登录无关。
- 另外两处隐患：`renderForm` 把 name 直接拼进 `innerHTML`（未转义）；无 token 时会发 `Bearer null`。
Materials: `logs/crashes-2026-11.csv`（唯一一手数据，已读）；`src/login.ts`；`package.json` / `README.md`；缺：前端错误上报、复现环境、发布记录。
Boundaries: （待确认）
Done: 建议——先给你失败分类＋改动清单（早期 checkpoint）→ 改代码并新增 vitest 用例覆盖 401 / 500 / 网络失败 / 缺 user 字段 → `npm test` 通过，且手动复现不再白屏。

## Open

1. Purpose：这次要的是"登录页绝不白屏"，还是"把 crash 数降下来"？两者范围不同。
2. 白屏发生在哪一步——一打开就白 / 输入提交后白 / 刷新后白？这决定 ChunkLoadError 是不是你说的那个"偶尔"。
3. 会话失败时页面显示什么：直接出登录表单，还是错误页＋重试按钮？
4. ChunkLoadError 一起修吗？`cart.ts:41` 算范围内吗？
5. （可选）有没有 Sentry 之类的上报，能定位到 URL 和版本？

Ready: no — 需要你回答 Open 1–4（第 5 条可选）。
