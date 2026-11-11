# Plan: 登录页白屏不再出现

- Asked: 帮我修一下登录页偶尔白屏的 bug
- Stage: execute
- Date: 2026-11-08（2026-11-10 修订）

## Requirement
Hand over: 登录页白屏不再出现，并有回归测试
Fallback: 只修当前复现的那一个白屏
Depth: 按量级排序崩溃日志，先定因再改码；覆盖 `/api/session` 的真实异常返回（401/403、HTML 502 页、空 body）；用 app_version→commit 对应表把 2.3.0 与 2.3.1 的同一错误对齐；stretch：一条在修复前代码上失败的渲染测试，并解释 2.3.1 发布为何没让该错误下降（412→377）
Range: 诊断者（日志分诊）× 前端工程师（防御性渲染）× 红队（造出能让修复再次白屏的响应）
Judge: 修复前的 commit 上跑新测试必须红、修复后必须绿；外加用日志里的原始响应样本回放，不看"有没有骨架屏"
Needs: 已有 logs/crashes-2026-11.csv、src/login.ts。缺：app_version→commit 对应表；一份真实的 `/api/session` 非 200 响应样本；能在本地复现的浏览器或 jsdom 跑法
Declined: 加 loading 骨架屏（用户 2026-11-10 判定：遮住白屏，未触根因，错误计数不变）

## Task
Purpose: 下周演示前登录稳定
Context: React 前端，登录依赖 /api/session
Materials: logs/crashes-2026-11.csv（主）, src/login.ts（主）
Boundaries: 不改后端接口
Done: 一个 PR，含回归测试

## 已查明（事实，不用再猜）
- 主因：`s.user` 为 undefined → `renderForm(s.user.name)` 抛 TypeError，login.ts:5。11-01 412 次、11-03 377 次，是最大头，且 2.3.1 未修掉。
- `.then()` 链无 catch，也未检查 `r.ok`：token 缺失/过期或网关返回 HTML 时，`r.json()` 同样抛错，整页无渲染 = 白屏。
- 次因：`ChunkLoadError` 88 次（发版后旧 chunk），是另一条白屏路径，是否纳入见 Open。
- 干扰项：`cart.ts:41` 栈溢出 19 次，属购物车，不是登录白屏。

## Open
- ChunkLoadError 算不算这次要一并处理？（要动构建/缓存策略，可能撞 Boundaries）
- 401 时预期行为是跳转登录还是渲染空表单？这决定修复写法。
- 缺 version→commit 表：2.3.1 的 377 次是否与 2.3.0 同一行代码，需确认后才能下"发布未生效"的结论。

## Tries
- 2026-11-10 驳回：产出仅加载骨架屏。判为方法错（漏诊断），在同一条 Hand over 上加 Depth，不降 Fallback。

Ready: no — Depth 的修复前红测试与真实响应样本未落实；Open 前两条待你裁定。
