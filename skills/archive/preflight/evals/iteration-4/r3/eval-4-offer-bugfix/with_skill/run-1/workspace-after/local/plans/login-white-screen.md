# Plan: 登录页不再白屏（含原因可观测）

- Asked: 「帮我修一下登录页偶尔白屏的 bug，代码在 src/login.ts」
- Stage: execute
- Date: 2026-11-10

## Requirement

**Hand over（建议直接交给结果的层级）**
`mountLogin` 的每条失败路径都渲染出可恢复的界面（或用整页跳转离开），并且把失败按原因打点；附一组测试：在原始代码上必红（复现同一个 TypeError）、修复后必绿。

**Fallback（上一层够不到时退到）**
只管 `null` token 与 401 两条路径：判空 + 检查 `r.ok` + 兜底 UI + `.catch`。不做打点、不写测试（不算完成，只算止血）。

**Ceiling（试过、超出模型可自主承担）**
「登录页任何原因都不白屏，含 ChunkLoadError、部署缓存策略与线上白屏率 SLO」——需要 `/api/session` 契约、CDN/`index.html` 缓存配置、监控账号，模型无法自行验证。

**Depth**
- 专家动作（你没要求的那一层）：先分离因果再改代码。日志里是**两种**白屏，不是一种。
- 最原始材料：`logs/crashes-2026-11.csv` 逐行（2.3.0 的 412 次与 2.3.1 的 377 次都是 `reading 'name' at login.ts:5`，说明 2.3.1 没修掉它，是主因；另有 88 次 `ChunkLoadError: Loading chunk 7 failed` 是**另一个**白屏来源，`cart.ts:41` 的 19 次与登录页无关）。
- 器械：登录页状态机 `loading → ready | recoverable-error`，加失败注入测试矩阵；而不是重新排一遍 `try/catch`。
- 拉伸目标：先写红队矩阵（token 缺失 / token 过期→401 JSON / 500 返回 HTML / 网络中断 / `/api/session` 返回非 JSON / chunk 加载失败），**修复前全部红**；修复后仅靠 `?.` 判空必须仍有红项。

**Range（把交付物还原成动词）**
定位（两种白屏分开）· 兜住（contain：可恢复 UI 或跳转）· 预防（prevent：契约边界判空 + 测试锁定）· 观测（observe：按原因打点，能在下次日志里区分）。
拼队：前端排障（根因链）· 接口契约负责人（401/无 token 时 `/api/session` 到底返回什么）· 发布/SRE（chunk 与 `index.html` 缓存）· 红队（补矩阵之外的失败）。要各自**做什么**，不要风格。

**Judge**
外部判据：新增测试在原始 `login.ts` 上必须失败（复现同一 TypeError）、修复后通过；另开一个独立红队会话注入矩阵外的失败，再由一个会话裁定其反对意见。评分看方法（是否先复现、是否有对照），**只加 `?.` 的"侥幸正确"必须判不合格**，理由正当但漏一格的近似解可通过。

**Needs**
- vitest + jsdom 依赖（仓库当前**未安装**，`npm test` 现在跑不起来；无测试目录、无 vitest 配置）
- `/api/session` 在无 token / 过期 token 时的真实响应体（**缺失**，仓库内无后端）
- 跳转目标（前端路由登录页还是整页重定向）（**缺失**）
- 错误打点 sink（**缺失**）
- ChunkLoadError 的部署/缓存上下文（**缺失**）
- 事实供确认：`login.ts:3-6` 中 `localStorage.getItem("token")` 可为 `null` → 请求头 `Bearer null` → 非 2xx 时响应体无 `user` → `s.user.name` 抛错，且无 `.catch`，`root.innerHTML` 永不执行，页面即白屏；该文件是裸 DOM 操作，尽管 README 写的是 React。

**Declined**
（等你逐条接受/改写/拒绝）

## Task

**Purpose**：这次修复服务哪个决定/问题？——是"止血上线"（默认走 Fallback），还是"让下次再白屏能一眼看出原因"（走 Hand over）？（动作不是目的。）

**Context**：一个有能力的外人需要知道什么才不跑偏？例如：登录页在什么场景被挂载、token 是否由别处刷新、白屏是否只出现在移动端/弱网？（事实部分见上，请确认）

**Materials**：主源 = `logs/crashes-2026-11.csv` 与真实 401 响应体；次源 = 现有 `login.ts`；禁用源 = ？（尚未给出），"未找到"槽位 = `/api/session` 契约、跳转目标、sink。

**Boundaries**（会让你说"不是我要的"）：
- 只做 `?.` 判空、把报错藏起来而不改变用户所见？
- 401 时静默跳转导致用户丢草稿/丢当前操作？
- 顺手重构整个文件或引入新依赖？
- 把 `ChunkLoadError` 一并处理（跨出 `src/login.ts`）？

**Done**：出现什么你就能停？建议形状 = 状态机实现 + 失败注入测试 + 一行修前/修后对照（同一 CSV 口径）。检查点：先交"病因分离结论 + 测试矩阵清单"给你确认，再动实现。

## Open

- CSV 里 88 次 `ChunkLoadError` 也是白屏来源，但不在 `src/login.ts`。要一起修、单开一条、还是明确不管？
- 你说的"偶尔"指哪一类：token 过期后的 377 次，还是首次访问/发版后的 chunk 失败？
- 2.3.1 已发版但错误数几乎不减（412 → 377），是否意味着这个文件根本没被改过、或另有版本号错配？

Ready: no —— Requirement 三条轴尚未裁决，Task 五问尚未由你回答（Purpose/Boundaries 最关键）。
