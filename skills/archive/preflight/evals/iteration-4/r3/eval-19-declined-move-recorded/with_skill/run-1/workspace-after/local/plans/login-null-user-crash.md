# Plan: 演示前修掉 login.ts 的空 user 崩溃

- Asked: /skill:preflight 修一下 logs 里出现最多的那个崩溃
- Stage: execute
- Date: 2026-11-10

## Requirement
Hand over: 只修 login.ts 这一个 TypeError，演示路径不白屏（已按你的否决收窄，不再抬到"登录页零崩溃"）。
Fallback: 演示前装不上测试框架时，退回"加空值保护 + 演示机手测登录页"的最小改动，PR 里注明回归测试待补。
Depth: 原始材料是 logs/crashes-2026-11.csv 与 src/login.ts。事实：该 TypeError 在 11 月共 **789 次**（2.3.0: 412，2.3.1: 377），栈指向 login.ts:5，真正读 `s.user.name` 在 **login.ts:6**（构建映射偏移一行）；`/api/session` 返回 200 但不带 user 时 `s.user` 为 undefined。专家动作（你没要求，但便宜）：**测试先行**——先写一个喂 `{}` / `{user: null}` 的回归测试，贴出它在旧代码上失败，再改代码。Stretch target（可选）：回归测试同时覆盖 token 为空导致的 401/非 JSON 响应，因为那条路径同样会进 `.then`。
Range: 动词是"演示时不崩"和"崩了当场能看见原因，不是白屏"。班组：一个前端修复会话；一名**红队**只读代码，专找"用 try/catch 或空字符串兜底把失败吞掉""只改渲染不管 s.user 判定"这类糊弄；另加一名会话对红队意见做裁决。
Judge: 场内自测——`npm test`；判据是回归测试在修复前**失败**、修复后通过，且改动不超出 src/login.ts + 测试文件。场外：演示机（或本地浏览器）手测登录页一次，由你亲自看。
Needs: 缺 git 仓库（`git rev-parse` 失败，PR 无处可提）；缺 vitest 依赖（package.json 只有 react，`npm test` 指向 `vitest run`）；缺一份 `/api/session` 真实响应样本；缺演示机/浏览器手测环境。
Declined: 抬到"登录页零崩溃，以一周崩溃日志为 0 为判据"——理由：下周就演示，只修这一个。

## Task
Purpose: 演示时不崩——演示中打开登录页，即使 session 缺 user 也不白屏、不报 TypeError。
Context: React 前端，session 接口偶尔返回 200 但不带 user（token 过期）；崩溃栈的 login.ts:5 与真实出错行 login.ts:6 差一行，别按栈行号改错行；789 次占日志绝大多数；另有 ChunkLoadError:88、cart.ts:41 RangeError:19 不在本次范围。
Materials: 主源 `logs/crashes-2026-11.csv`、`src/login.ts`；`package.json`（测试入口 `vitest run`）。禁用源：未指定。缺：后端 `/api/session` 的响应形状样本（不改后端，但需要一份样本喂测试）。
Boundaries: 不改后端。
Done: 一个带回归测试的 PR——改动限于 src/login.ts（+ 测试文件），`npm test` 通过，回归测试修复前失败的输出贴在 PR 里，分支可评审。

## Open
- 没有 git 仓库，PR 从哪提？（先 `git init` 还是推到远端？）
- vitest 未在依赖里，是否允许改 package.json + lockfile 装它？
- session 缺 user 时 UI 要什么：空表单 / 跳登录 / 提示重试——未定，而它决定了改法。
- 边界只写了"不改后端"；是否再加一条"不许用 try/catch 或空字符串静默吞掉失败"？待你裁决。

Ready: no，because Depth/Range 未经你过目，Open 里 4 项未定，且 git 与 vitest 两个前置缺失。
