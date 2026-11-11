# Plan: 登录页白屏不再出现

- Asked: 帮我修一下登录页偶尔白屏的 bug
- Stage: execute
- Date: 2026-11-10（原 2026-11-08，已按失败结果重写）

## Requirement
Hand over: 同一个 rung 不变 —— 登录页不再白屏，且有能复现原崩溃的回归测试；但交付面收窄到一次最小补丁（先扔掉 40 文件的 PR）
Fallback: 只让 `s.user.name` 在 `s.user` 未定义时不再抛错，其余一行不动
Depth: 原始材料不是日志而是那三份真实响应 —— `/api/session` 失败时返回的 401 body、HTML 错误页、空 body。用 devtools/curl 拿到，逐份喂进 jsdom 的 mock fetch，确认每份都能复现白屏。仪器：vitest + jsdom，不是读日志推演。Stretch: 把"白屏"写成可断言的定义（`root.innerHTML` 为空 / 未渲染出错误态），让测试判定而不是人眼判定
Range: 复现 → 定位 → 最小修复 → 防回归。Crew: 一个只做复现、不许改代码的 session；一个红队 session 只找"还能白屏的第二条路径"；第三个 session 裁决哪些反对成立
Judge: 修复前先提交一个会失败的测试（红），修复后同一测试转绿 —— 这是模型自己能跑的检查。红队反对由裁决 session 定夺。diff 由你本人看，目标 ≤ 3 文件
Needs: `/api/session` 失败时的真实响应体（缺，见 Open）；Node ≥ 20 与 vitest（已有）
Declined: —

## Task
Purpose: 下周演示前登录稳定（不变）
Context: React 前端，登录依赖 `/api/session`。日志显示 2.3.0 与 2.3.1 都出现同一个 TypeError，回退版本解决不了
Materials: 1) `logs/crashes-2026-11.csv` 中 login.ts:5 的 TypeError 两行 —— 唯一在范围内；2) `src/login.ts`；3) `/api/session` 真实失败响应（待补，缺则留空）。明确排除：`cart.ts:41` RangeError、`ChunkLoadError`，另开 issue
Boundaries: 不改后端接口（不变）。补充的墙：只动登录路径文件，总改动 ≤ 3 个文件；不引入新依赖；不碰 `cart.ts` 与 chunk 加载；不重构、不重命名、不格式化；不写"以防万一"的错误处理
Done: 第一道 checkpoint —— 只交一个 ≤ 3 行补丁 + 一个修复前会失败的测试，然后停下等你审，通过后才开 PR。停的条件：该测试红→绿，diff ≤ 3 文件且 ≤ 40 行

## Open
- `/api/session` 失败时的真实响应体还没人拿到。这是本案缺的那块材料，缺它只能先按 401 / HTML / 空 body 三种假设写测试
- 那 40 个文件里是否有值得留的？建议整条分支丢弃，只从中捞回复现测试（如果有）

## Tries
- 2026-11-10 — 跑一整夜后：40 个文件、PR 无法审阅、白屏未解决。原因：Materials 给了整份崩溃 CSV（含两个无关错误）→ 范围外溢；Boundaries 没有改动面墙；Done 没有早期 checkpoint，于是"白屏不再出现"被读成"处理所有失败路径"；Depth 只写"先看崩溃日志"，方法停在读日志，没到复现那条坏响应。改动：收窄 Materials 与 Boundaries，加 checkpoint 与红队，Depth 换成复现真实响应

Ready: no，因为 `/api/session` 失败响应缺失，且需你确认"整条分支丢弃 + 改动面 ≤ 3 文件"
