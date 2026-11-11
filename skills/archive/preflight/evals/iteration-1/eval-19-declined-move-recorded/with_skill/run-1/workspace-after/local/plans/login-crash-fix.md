# Plan: 登录页缺 user 崩溃修复

- Asked: 不接受，下周就演示了，只修这一个就行。目标：演示不崩；背景：React 前端，session 接口偶尔不返回 user；素材：logs 和 src/login.ts；边界：不改后端；完成：一个带回归测试的 PR。
- Stage: execute
- Date: 2026-11-10

## Requirement

Hand over: 只修 `login.ts:5` 的 `TypeError`（用户明确拒绝上提，见 Declined）。
Fallback: 若演示前仍定不到根因，在 `mountLogin` 外层加错误边界保证不白屏——只是兜底，不算完成。
Depth: 专家动作不是 `s.user?.name ?? ""` 一行守卫，而是修在"数据契约"这一层：`fetch` 对 401/500 也 resolve，`r.json()` 遇到 HTML 错误页会抛，`s` 本身也可能是 `undefined`——守卫打错层就仍然崩。原始素材：`logs/crashes-2026-11.csv` 里同签名的 412+377=789 次作为修复前基线。仪器：用真实响应形状做 fixture（`{}`、`{user:null}`、`{user:{}}`、非 JSON body、非 2xx），而不是只测 happy path。Stretch: 回归测试必须在**旧代码上失败**、新代码上通过（否则测的是空气）。
Range: 动词 = 让登录页在缺 user 时不崩 / 把"缺 user"变成可见状态而不是静默空表单 / 让同类缺失在 CI 里被抓住。Crew：前端可靠性（防御式渲染与错误边界）、可观测性（区分未登录 vs 后端异常）、测试（契约 fixture 与红队式反例）。
Judge: `npm test` 的回归测试 + 一个攻击 session 专门找"守卫写错层"的反例；同时评方法（是否修在根因层、测试能否在旧代码上失败），因此碰巧不崩也不算过。
Needs: session 接口缺 user 时的真实响应样例（日志里没有，**缺**）；git 仓库（当前目录不是 git repo，**缺**，没有它开不了 PR）；vitest 未出现在 `package.json` 依赖里且 `src/` 下无测试文件（**缺**，`npm test` 现在大概率跑不起来）。
Declined: 上提到"登录页零崩溃 + 一周崩溃日志归零"——原因：下周演示，用户只要修这一个；记录为退路之上的动作不做。

## Task

Purpose: 下周演示时登录页不崩，人能顺利看到产品。
Context: React 前端；`mountLogin` → `fetch /api/session` → `renderForm(s.user.name)`；日志中该签名 11/01–11/03 共 789 次，是最高频崩溃；另有 ChunkLoadError 88 次、`cart.ts:41` 栈溢出 19 次，本次不在范围。
Materials: 一手 = `logs/crashes-2026-11.csv`、`src/login.ts`；空缺 = session 接口响应样例（待补，不猜）。
Boundaries: 不改后端；不动 `cart.ts` / ChunkLoadError；不改登录页的整体交互与视觉。**待确认**：是否允许把崩溃改成"可见错误提示"（不做静默吞掉）。
Done: 一个带回归测试的 PR；checkpoint = 先给"缺 user 时应该显示什么"一句话方案 + 测试用例清单，确认后再写代码。

## Open

1. **缺 user 时到底显示什么**（跳转登录 / 空表单 / 错误提示）——唯一挡住 Done 的意图缺口，只有你能定。
2. 仓库在哪：当前目录无 `.git`，PR 要在哪儿开。
3. 测试基建：是否可以新增 vitest 依赖与 `src/*.test.ts`。

Ready: no，因为第 1 条未定，且 2/3 缺失使"带回归测试的 PR"当前不可达。
