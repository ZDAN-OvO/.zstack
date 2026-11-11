# Plan: 登录白屏——只修会话字段缺失这一条

- Asked: 帮我修一下登录页偶尔白屏的 bug
- Stage: execute
- Date: 2026-11-10

## Requirement
Hand over: login.ts 对 /api/session 的响应做形状校验：无 token / 过期 token 时 user 缺失或非 200，渲染兜底表单而不是整页崩；附一条在旧代码上会红的测试
Fallback: 只在 .then 里加空值保护 + 一行测试，不重构数据流
Depth: 原始材料是 crashes CSV 按「签名 × 版本 × count」排序，不读叙述；主导项 = login.ts:5 TypeError（412/377，2.3.1 仍在发生），ChunkLoadError 与 cart.ts:41 出本 PR 范围；专家动作 = 先写根因假设（token 失效 → 响应无 user → s.user 崩 → 白屏）再写会红的测试，最后改实现；拉伸 = 把守卫删掉测试必须重新变红，证明测试绑行为不绑实现
Range: 动词是定位→复现→守卫→证伪；班组 = 前端运行时（session 守卫/错误态）、红队（问"这修的是那 377 次，还是只修了演示走的那一条"）、发布视角（ChunkLoadError 单独开票，不进本 PR）
Judge: 自跑——新测试在未改动的 src/login.ts 上必须红、改后绿、删守卫后复红；"一周崩溃日志该签名为 0" 只作事后确认，不作闸门
Needs: logs/crashes-2026-11.csv（已有）、vitest（package.json 有）、**/api/session 失败时的真实响应体（缺）**——用代理抓一次，否则测试只能按假设写
Declined: 上一版 Hand over「白屏不再出现」降级，它是 40 个文件的来源

## Task
Purpose: 下周演示前登录稳定
Context: React 前端，登录依赖 /api/session；2.3.1 线上仍有 377 次 login.ts:5 TypeError；当前 login.ts 没有任何失败分支
Materials: logs/crashes-2026-11.csv（主）、src/login.ts（主）；无次级来源
Boundaries: 不改后端接口；只改 src/login.ts + 新增一个测试文件，不碰 cart.ts、不碰构建/打包配置；不引入新依赖；diff ≤ 60 行
Done: 先贴根因假设 + 3–5 行 diff 计划 + 一条会红的测试，确认后才动实现；最终一个 PR，只含 login.ts 与测试

## Open
- 40 文件那条分支直接废弃？建议关掉、从主分支重切
- 88 次 ChunkLoadError 也落在演示窗口里（部署后旧 index.html 会白屏），占 18%——进不进来你定，我倾向另开票
- /api/session 失败时返回什么：401 空 body、{error}、还是 200 但无 user？这决定测试怎么写

## Tries
- 2026-11-10 驳：40 文件 PR 审不动、bug 未修。判定=Too big + Missed intent。改：原 Fallback 提为 Hand over（单签名）；Depth 加"按计数取主导项 + 先红后绿"；Boundaries 加文件与 diff 上限；Done 加"先确认假设再实现"检查点；Judge 换成自跑的红→绿→删守卫复红

Ready: no — 待你定 Open 三条（尤其 /api/session 的失败响应），并对 Hand over 与 Boundaries 点头
