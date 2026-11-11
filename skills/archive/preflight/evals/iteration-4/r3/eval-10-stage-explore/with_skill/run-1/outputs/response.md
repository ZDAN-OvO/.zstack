已写入 `local/plans/db-choice-postgres-vs-mongodb.md`。

阶段是 **think**，不是 execute：你要的"标准"不在任何文件里 —— 工作区是空的（无 git、无 schema、无代码、无流量数字），标准只能从你的访问模式和不变量里长出来。所以这份计划先不回答选哪个，而是把"怎么选"提到能交付的高度。

我提了三条 Requirement，需要你逐条裁定（接受 / 改写 / 拒绝，拒了也记下理由）：

1. **Altitude**：交一份 ADR + 一次真实量级 spike（前 10 条查询跑 10 倍首年数据量，量 p95、恢复时间、托管价），而不是功能对比表。退一步是"定标准 + 加权打分"。
2. **Depth**：先写查询和读写比，再比引擎；带反向测试（让输的一方也达标 —— 两边都过就说明性能不是决定项）。
3. **Range**：crew 里加红队（专职论证相反的选型 + 攻击你的 benchmark），裁判用留出的 5 条查询，蒙对不算过。

五个 Task 槽（Purpose / Context / Materials / Boundaries / Done）我一个字都没替你填 —— 那是只有你有的答案。Boundaries 和 Done 我列了候选，方便你直接拍。

Ready 现在是 **no**。你裁完三条 + 答完五个槽（或者明确说"某个槽我不知道"），我再把 Ready 改成 yes。

确认之后可以 `/define-goal`，以这份计划为源。