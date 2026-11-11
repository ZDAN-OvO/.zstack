# Plan: 恢复首页转化率

- Asked: 首页转化率掉了一半，帮我重写首页文案
- Stage: execute
- Date: 2026-11-10

## Requirement
Hand over: 诊断转化率下滑的真实来源并修复，把首页转化拉回 4%；文案只是手段之一
Fallback: 拿不到分来源数据和广告素材 → 只做文案假设 + 上线测量方案
Depth: 原始材料 = `analytics/weekly.csv`、`support/chats-sample.md`、`index.html`、paid_social 广告素材（缺）；工具 = 分来源/分设备漏斗拆解、mention→landing 的 message-match 矩阵；stretch = 用未参与诊断的周数据回测，必须解释 2.0% 由哪些来源构成，而不只是描述现象
Range: 动词 = 归因、对齐广告承诺与落地页、消除注册阻力；crew = 增长分析师（拆 mix 效应）、CRO/落地页专家（异议与 message-match）、投放优化师（读素材与受众意图）、UX 研究者（读会话记录）；red team = 统计/取证角色，只负责证明"不是文案的问题"
Judge: 独立红队会话反驳 + 第三个会话裁决；评判方法而非结论——必须能复现 4.0%→2.0% 的来源算术，并能预测未使用的周。最终文案由你直接裁决。
Needs: 分来源 visits/signups（CSV 只有 top_source，缺）、paid_social 广告素材与受众、价格页、注册漏斗埋点、日历授权步骤数据；缺则诊断只能到假设级
Declined: 暂无（待你确认）

## Task
Purpose: （待你回答）这次输出服务哪个决定：改文案、改投放，还是改注册流程？
Context: 事实：10-20 起 top_source 由 organic 变 paid_social，visits 12k→21k（+75%），signups 480→399（−17%），转化 4.0%→1.9%。`index.html` 仅 3 行：无价格入口、无差异化、无社会证明。会话样本（3 条，非随机）显示三类异议：与 Notion 的区别、找不到价格页、注册后要连日历就放弃。
Materials: 一手 = 分析后台分来源/分设备数据、广告素材、注册漏斗埋点；二手 = 会话样本；禁止 = 编造客户数、评价、定价；缺失 = 广告素材、分来源数据
Boundaries: （待你回答）例如：只换形容词的文案、编造社会证明、未经同意改投放或 /signup 结构
Done: 先交一页诊断备忘（来源拆解 + 归因 + 优先级），你确认后再出文案：hero + 三个异议模块 + 价格入口 + 测量方案

## Open
- Purpose 未定，五问中其余四问也需你用自己的话回答
- 本周 visits 与 signups 无法按来源拆分：CSV 只记录 top_source，因此"文案变差"与"流量结构变化"目前不可区分
- 若 organic 维持 3.9%、其量级不变，10-20 周仅 organic 就该有 ≈460 个注册，已超过当周实际 390，说明 organic 的量或转化同时变了；需要后台明细
- 是否允许改注册流程（连日历那一步）尚未确认

Ready: no, because 五个 Task 槽待你回答，且分来源数据与广告素材缺失
