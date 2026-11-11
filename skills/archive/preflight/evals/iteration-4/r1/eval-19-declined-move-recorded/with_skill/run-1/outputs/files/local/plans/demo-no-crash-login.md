# Plan: 演示登录页不崩

- Asked: 修一下 logs 里出现最多的那个崩溃
- Stage: execute
- Date: 2026-11-10

## Requirement
Hand over: 修掉 `login.ts:5` 这一个 TypeError（`s.user.name`），演示路径不崩。
Fallback: 若本周内回归测试落不了地（仓库无 git、无 vitest），退回"防御性修复 + 手写复现步骤"，不带测试。
Depth: 原始素材是 `logs/crashes-2026-11.csv` 的原始 5 行（2.3.0 412 次 + 2.3.1 377 次 = 788 次）和 `src/login.ts` 第 5 行。专家动作你没要求：把"session 偶尔不返回 user"当作契约而不是意外 —— 同一行其实有三条未处理路径（`s.user` 缺失、`r.ok` 非 2xx、`fetch` reject），一个 `?.` 只挡住第一条。做法是用 payload 形状建模，而非就地加判空。Stretch: 测试先红后绿 —— 用 `user` 缺失 / 为 null / 为字符串 + 一条 fetch reject 喂给 mock，先复现日志里的崩溃再改代码。
Range: 动词是"演示不中断"和"让人看出未登录而不是崩"。Crew: 前端错误路径（把三种失败归一到同一状态）、测试工程（用真实 payload 形状喂 mock）、red team（拿 logs 里另两类错误和 token 过期来攻这次修复是否只挡了一种）。
Judge: 可自跑的 vitest 回归测试，且判据是"先红后绿"（空实现必须失败）；red team 单独会话出异议，再一个会话裁决。你本人能看演示，模拟演示也是判据。
Needs: git 仓库（**缺**，当前目录不是 git repo，PR 无载体）；vitest 可跑（**缺**，`package.json` 有 test 脚本但未安装、无测试文件）；演示环境里 user 缺失时应显示什么。
Declined: 抬到"登录页零崩溃 + 一周崩溃日志为 0"，理由：下周就演示，只修这一个。

## Task
Purpose: 演示时不崩。
Context: React 前端，session 接口偶尔不返回 user。
Materials: `logs/crashes-2026-11.csv`、`src/login.ts`（一手）。未找到：无 session 接口响应样例、无 token 过期场景记录。
Boundaries: 不改后端。
Done: 一个带回归测试的 PR（早期检查点：先看测试失败用例是否复现了日志里的 TypeError，再改代码）。

## Open
- PR 的载体：本地 `git init` 开分支，还是给你一个 patch 文件？
- 缺 user 时页面显示什么（"未登录"提示 / 空表单 / 跳登录）—— 未定，测试要据此断言。
- vitest 需要 `npm i -D vitest`，演示机是否可联网安装？

Ready: no，因为 Depth / Range / Judge 三项待你裁决，且 git 与 vitest 两个缺口未定。
