# Plan: 修掉 login.ts:5 崩溃（演示不白屏）

- Asked: 「修一下 logs 里出现最多的那个崩溃」；后补充：不接受往上抬，只修这一个
- Stage: execute
- Date: 2026-11-10

## Requirement
Hand over: 按原样：只修 `s.user.name` 这一个崩溃，交付带回归测试的 PR
Fallback: 仍在 login 边界内兜底——`mountLogin` 拿不到 user 时渲染空表单/重试提示，不改 session 契约、不碰其他文件
Depth: 建议（待裁决）在解析处收敛，而不是在取值处加 `?.`：`/api/session` 响应先过一层 shape 校验，缺 `user` 时走同一个降级分支。理由：同一个 payload 还会打坏别的字段读取。原料=真实缺 user 的响应样本（暂缺，见 Open）；量具=vitest fixture 覆盖「无 user / user 为 null / 非 JSON」
Range: not needed（单文件单路径修复，加角色分工只会加流程不加正确性）
Judge: 先写的 vitest 回归测试——在当前代码上必须红、修复后必须绿，所以它判的是方法而非运气。演示现场是最终判据，但不可复现，不作依据
Needs: 真实 session 响应样本（缺）；`package.json` 无 vitest devDependency、仓库无测试文件（需加）；git 仓库（缺，见 Open）；是否允许改 `/api/session` 之外的代码（已知不能动后端）
Proposed: Depth 一条，等你裁决
Declined: Altitude（抬到「登录页零崩溃 + 一周崩溃日志为 0 作判据」）——理由：下周演示，时间盒内只保演示路径

**事实**：logs 共 896 次崩溃，`login.ts:5` 的 TypeError 占 789 次（412 在 2.3.0，377 在 2.3.1），88%。第二名 ChunkLoadError 88 次、第三名 cart.ts:41 19 次。日志行号 5 与代码里 `s.user.name`（`src/login.ts:6`）不齐，堆栈行号来自打包 sourcemap，修的位置以代码为准。

## Task
Purpose: 下周演示时登录页不白屏
Context: React + TypeScript 前端（acme-web 2.3.1）；`/api/session` 偶尔返回不带 `user` 的响应；2.3.0 到 2.3.1 都还在报，不是已修问题
Materials: 主 `logs/crashes-2026-11.csv`（唯一一手数据）；次 `src/login.ts`；空槽：真实缺 `user` 的响应体（未找到）
Boundaries: 不改后端；只修这一个崩溃（ChunkLoadError 88、cart.ts RangeError 19 不修）
Done: 一个带回归测试的 PR —— 检查点顺序：先提测试（红）→ 再提修复（绿）→ 再开 PR

## Open
- 这里不是 git 仓库（无 `.git`）：这个 PR 开在哪个仓库、哪个分支？
- 拿不到 `user` 时登录页显示什么（空输入框 / 「会话失效，请重试」/ 跳回登录）？这决定测试断言与 Done 的形态
- 缺 `user` 的响应长什么样没人确认过，fixture 只能靠猜；能贴一条线上的实际响应吗
- 是否允许加 `vitest` devDependency 与 `src/login.test.ts`（现在只有 `"test": "vitest run"` 脚本，没依赖也没测试文件）
- 已知范围外风险：11-01 起还有 88 次 ChunkLoadError，演示若命中同样白屏，但按你的边界这次不动

Ready: no，因为 Depth 一条未裁决，且 Open 第 1、2、3 条没有答案
