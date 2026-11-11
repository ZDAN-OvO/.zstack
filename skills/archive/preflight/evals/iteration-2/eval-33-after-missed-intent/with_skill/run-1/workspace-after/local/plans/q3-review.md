# Plan: Q3 回顾讲清变化与决策

- Asked: 帮我做 Q3 QBR
- Stage: execute
- Date: 2026-11-06（2026-11-10 修订）

## Requirement
Hand over: 给客户看的季度回顾——本季对他们发生了什么、为什么、对他们意味着什么
Fallback: 按 template.md 填数，不做叙事
Depth: 从原始月度数据出发（收入 182k→176k→171k，流失 12→19→24，NPS 38→31→27）。只有 3 个月，试用期缩短与流失上升只是同向变化，不能当因果写进客户版
Range: 客户成功/账户视角（客户要听到什么、要决定什么）+ 红队（一个挑剔的客户读这份东西）
Judge: 一个独立 session 扮演客户方决策人，只凭这份 deck 判断"我该做什么"；另加一条：每个数字都能回溯到 data/q3-metrics.csv，客户版不出现无法回溯的数字
Needs: data/q3-metrics.csv（只有内部月度聚合，缺客户侧材料：合同、SLA、已对客户的承诺）
Proposed:
- Task·Purpose 补读者与其要做的决定（见下）
- Task·Boundaries 增墙：不出现内部工单细节、不写未经确认的下季承诺、不出现"给 VP 看"式的内部口径
- Task·Done 改为对客户成立的样子，并加一个 outline 检查点
- Requirement·Judge 由"老板审阅"换成上面那条（老板审阅保留为第二道）
- Requirement·Range 增加客户视角 + 红队（客户版需要，内部 deck 不需要）
Declined: —

## Task
Purpose: 给客户看的季度回顾（要服务哪个客户决定：待定）
Context: SaaS，Q3 收入下滑；notes/worklog.md 记 9/8 起"太难上手"投诉增多，8 月中旬试用由 14 天改为 7 天
Materials: data/q3-metrics.csv（内部聚合，已用）；template.md（字段：收入/客户/下季计划）；客户侧材料：未找到
Boundaries: 不编数字；不出现内部口径（本次新增，待确认）
Done: 一份 10 页 deck（客户版页数/形态待确认，先出目录）

## Open
- 这份回顾服务客户的哪个决定：续约、扩容、还是解释 Q3 的下滑？（决定全篇的重心）
- 读者是谁：客户方的业务负责人，还是采购/财务？
- "下季计划"在客户版里是承诺还是说明？写死会变成合同义务。
- 客户侧材料在哪：合同条款、SLA、此前对客户的承诺、客户自己的用量数据？
- 页数 10 页是为内部 deck 定的，客户版是否沿用？

## Tries
- 2026-11-10 否决：交出去的是给老板的内部 deck，不是客户回顾。原因：Task·Purpose 只写了"季度回顾"，读者从 notes/worklog.md 的"给 VP 看"一句推来，没问就定了；Boundaries 没有"客户版不能出现什么"这条墙；Judge 是老板审阅，看不出客户读了会怎么想。已改：Purpose/Context/Boundaries/Done 按客户读者重述，Judge 换成客户方决策人 + 数字回溯，Range 加客户视角与红队。等待你对 Open 与 Proposed 的裁定。

Ready: no——Purpose 的客户与决定、Boundaries 新墙、Done 的形态都还没定；Proposed 里五条等你裁定。
