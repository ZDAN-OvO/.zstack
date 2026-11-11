# Plan: 修掉登录的 name 未定义崩溃

- Asked: 把 logs 里那个最多的崩溃修掉
- Stage: execute
- Date: 2026-11-10

## Requirement

Hand over（建议抬一级）：不是「补一个 `?.`」，而是「登录路径对任何 session 响应都是全的」——200 有 user、200 无 user、401 错误体、非 JSON 体、网络失败、无 token 六种输入都渲染出可用界面而不抛错，并配一条先红后绿的回归测试。判据可自行运行，不需要线上灰度。

Fallback：只修那一行（`s.user.name`），加 `r.ok` 与 token 判空，不建测试矩阵。适用于你只想止血。

Ceiling：「上线后崩溃率降 X%」够不到——需要生产遥测和一次发版，本工作区没有（无 git、无 CI、无 Sentry）。回落一级即 Hand over 那条。

Depth
- 原始材料：`logs/crashes-2026-11.csv` 只有 4 行，栈只有 `login.ts:5` 一行，无浏览器/设备/用户维度，也无 2.3.1 的 sourcemap，所以「login.ts:5 是哪一行」目前是推断。
- 专家动作（你没要求的那步）：先复现再修。写一条喂 401 错误体的测试，证明 `s.user` 为 undefined 时必然抛在该行；改完同一条测试变绿。只用 try/catch 把错误吞掉的补丁在这一步就判失败。
- 仪器：vitest + fetch/localStorage 桩，跑六种响应 fixture，而不是肉眼看 diff。
- Stretch：同一错误在 2.3.0（412）与 2.3.1（377）都高，说明 2.3.1 并未修它；顺带核对 `Bearer null` 这条路径是否是同一错误的另一来源。

Range
- 名词转动词：交付的不是「一个补丁」，而是 ① 会话失效的用户看到一个能操作的登录页 ② 真崩溃不再被静默吞掉 ③ 这类回归下次被测试挡住。
- Crew：前端实现（最小改动）、测试作者（red→green 复现）、红队（用 401 体、空 body、HTML 错误页、`user: null`、`name: null`、离线 六个输入打补丁，只打不改）。
- Judge：你说「我自己检查一下就行」→ 落成可自行运行的测试 + 红队输入全过；判定方法与结果，吞错误的实现必须判失败。

Needs
- 已有：`src/login.ts`、CSV、node 26、npm 可访问 registry。
- 缺：2.3.1 的 sourcemap/线上栈（能把 `login.ts:5` 钉死）；`cart.ts`、chunk 7 的源码不在仓库（第二、三类崩溃在此仓库修不了）；无 git 历史，看不到 2.3.0→2.3.1 改了什么。
- 要装：vitest + jsdom 会新增 devDependencies 与 lockfile —— 待你同意。

Declined：—（待你裁定）

## Task

Purpose：（待你回答）

Context：我查到的事实，请确认：最高频崩溃为 `TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5`，11 月合计 789 次（2.3.0 412 / 2.3.1 377），占 CSV 全部计数的 86%；第二名 ChunkLoadError 88 次，第三名 cart.ts 19 次。`src/login.ts` 中 `s.user.name` 无判空，`localStorage.getItem("token")` 也无判空，两者都能产生该 TypeError。

Materials：一级 = `logs/crashes-2026-11.csv`、`src/login.ts`；二级 = `package.json`、`README.md`（只声明了 `vitest run`，仓库里其实没有测试）。禁用 = 猜 `cart.ts` 的实现、把 CSV 计数当用户数。空槽 = 线上栈/sourcemap、2.3.1 的 diff。

Boundaries：（待你回答）我预设三条雷：用 try/catch 吞错并渲染空白页；改 `/api/session` 的契约；顺手重构或动 `login.ts` 之外的文件。对吗，还有别的？

Done：`src/login.ts` 补丁 + 一条先红后绿的测试 + 三行根因说明（哪种响应对应哪种崩溃），`npx vitest run` 全绿。检查点：先只给你看「复现测试红」与一行改动计划，你点头后再补测试矩阵和红队输入。

## Open

- Purpose 未答：这次修是为了止血发版，还是把登录这条路径一次性做全？
- 401 时的行为未定：跳登录页，还是渲染空表单？
- 能否加 devDependencies（vitest/jsdom）并写 lockfile？
- 另外两类崩溃（88 / 19）本次只报告不修，还是一起排？

Ready: no，尚缺 Purpose 与 Boundaries，且 Requirement 的抬级/回落/深度/范围四处都没裁定。
