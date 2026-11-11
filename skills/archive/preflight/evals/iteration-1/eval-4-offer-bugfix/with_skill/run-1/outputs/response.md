我已经先查了代码和日志，根因其实基本锁定；但“白屏”有三种可能来源，改法不同，所以先给你一屏计划，你确认后我再动手。

计划：`local/plans/login-white-screen.md`

查到的事实（可直接确认）：
- `src/login.ts:5` 无判空取 `s.user.name`，且 `fetch` 没有 `.catch` → 401/非 JSON 响应时 `s.user` 为 undefined，抛错后 `root.innerHTML` 永不赋值 = 白屏。
- `logs/crashes-2026-11.csv`：该 TypeError 在 2.3.0 + 2.3.1 合计 **789 次**，2.3.1 仍在涨；另有 **ChunkLoadError 88 次**，也是白屏但修法完全不同。
- 仓库无测试文件、非 git 仓库（`npm test` 现在跑不出任何断言）。

需要你裁决的四件事：
1. **Hand over**：只兜底修 TypeError（Fallback），还是升级为“任何后端/网络异常都不白屏 + 回归测试”（建议）。
2. **白屏期间用户看到什么**：loading、错误文案+重试，还是自动重试？
3. **范围**：这 88 次 ChunkLoadError 算不算在内？
4. **完成的样子**：先看“根因对照表+测试清单”当检查点，还是直接看 patch？

你回一句（或直接说“按建议走，范围只修 TypeError，先看 patch”），我就开始改并补 vitest 用例。