已更新 `local/plans/login-whitescreen.md`（原地改，加了一条 Tries）。

判断的原因是两条，不是一条：

**范围没封口（→ 收到 Fallback）。** 计划写的是"白屏不再出现"，但日志里是 4 条互不相干的错误：`login.ts:5` 的 `s.user` 为 undefined（2.3.1 上 377 次，11-03 后没新行，是真凶）、`ChunkLoadError`（只在 2.3.0，已经随发版消失）、`cart.ts:41` 栈溢出（另一个 bug，19 次）。材料只列了"崩溃日志"没有排序，Boundaries 只有"不改后端接口"一条墙，于是顺手把 cart、chunk 都改了 —— 40 个文件大概就是这么长出来的。

**一夜没有刹车（→ Done 加了检查点）。** Done 只有"一个 PR，含回归测试"这个终点，没有中途交付物，所以跑偏了也没人知道。原计划的 Judge 还带了"一周内崩溃日志为 0"，演示前根本判不了，已经删掉。

改动要点：Hand over 收到 fallback（只修 `login.ts:5`，diff ≤ 2 文件）；Done 改成先交一条在旧代码上会红的测试、再看实现；新增"不碰 cart.ts / 不处理 ChunkLoadError / 不做顺手重构"三条墙；Materials 标明只看 2.3.1 的行。

一个限制：这里不是 git 仓库，我看不到那 40 个文件的 diff，所以没法替你判断里面有没有值得留的东西。

Open 里留了一条要你定的：**那个分支整滚还是只挑测试留下？** 定了我就把 Ready 改成 yes。