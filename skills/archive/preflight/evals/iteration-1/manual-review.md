# 人工抽查：分数之外的发现

本页记录对实际回复和文件的人工抽查，不更改自动评分或断言。用例均为合成夹具，不代表用户的真实项目或决定。

| 用例 | 证据 | 发现 |
| --- | --- | --- |
| 11：已有数据库决策标准 | [回复](./eval-11-stage-decide/with_skill/run-1/outputs/response.md)、[计划](./eval-11-stage-decide/with_skill/run-1/outputs/files/local/plans/db-choice-postgres-vs-mongodb.md) | 用户明确给出“团队只会 SQL、数据强关系”，要求做决定。模型创建计划，将阶段写为 execute，又提出真实 schema 验证、三年运维成本、红队等工作。技能的 Stage 分支未阻止过度规划。本例的“不创建计划”断言可以捕捉这一问题。 |
| 22：用户说不清 Done | [回复](./eval-22-task-done-unanswerable/with_skill/run-1/outputs/response.md)、[计划](./eval-22-task-done-unanswerable/with_skill/run-1/outputs/files/local/plans/q3-review.md) | Done 栏确实写“未定”，Open 也保留了缺口；但模型又提供“默认形状”等待用户点头。现有断言允许“明确标为未回答”通过，不能充分区分单纯暴露缺口与先给答案、再要求用户确认。它也重新询问了模拟历史已经明确的 VP 受众。 |
| 24：边界只有形容词 | [回复](./eval-24-task-adjective-boundaries/with_skill/run-1/outputs/response.md)、[计划](./eval-24-task-adjective-boundaries/with_skill/run-1/outputs/files/local/plans/paid-social-homepage.md) | 正确指出“高级、简洁、科技感”不是边界，也没有写 Ready: yes；同时把 Purpose 写成“投放要不要继续加预算”，补了转化率目标、边界和交付内容。用户只说“新访客五秒内看懂产品”。现有断言主要检查形容词和 Ready，未覆盖未经确认的目的、目标和完成定义。 |
| 33：客户版回顾被做成内部 deck | [回复](./eval-33-after-missed-intent/with_skill/run-1/outputs/response.md)、[计划](./eval-33-after-missed-intent/with_skill/run-1/outputs/files/local/plans/q3-review.md) | 正确回到受众/Context，并补 Tries；但把客户沟通目的补成“续约/扩容”，还称“试用期缩短→投诉→流失/NPS”的原因链为真。夹具中的时间顺序只能支持相关性，不能证明因果。本例只测受众修正和修订记录，没有测目的是否由用户确认或因果结论是否有足够证据。 |

另核对了三项自动评分已捕捉的失败：

- **第 4 例，提前写计划**：[回复](./eval-4-offer-bugfix/with_skill/run-1/outputs/response.md)直接说“先给你一屏计划”，文件已写入，用户尚未接受。源码没有修改，所以仍通过了该例的一条断言。
- **第 18 例，小诗被扩成规划**：[回复](./eval-18-creative-poem/with_skill/run-1/outputs/response.md)没有写诗，要求回答四个问题，提出“升一级/下一层/降一级”，并表示回答后先写计划。没有创建计划文件，因而仍通过了“不创建计划文件”那一条。
- **第 29 例，先覆盖再询问**：[工具记录](./eval-29-plan-overwrite-guard/with_skill/run-1/transcript.md)确认模型先备份原计划，再覆盖 `onboarding-email.md`；[最终回复](./eval-29-plan-overwrite-guard/with_skill/run-1/outputs/response.md)随后才问“请确认覆盖还是换名”。备份保住了原内容，但不等同于事先取得覆盖许可。该例的 1/3 不是整体通过，只表示模型识别到了名称冲突。

这些发现说明：自动通过率衡量当前 111 条断言覆盖的行为，不能直接解释为需求澄清能力、事实可靠性或真实项目成功率。若后续迭代，应先由用户审查是否收紧这些判据，再另开一轮评测；不在看到结果后改动本轮标准。
