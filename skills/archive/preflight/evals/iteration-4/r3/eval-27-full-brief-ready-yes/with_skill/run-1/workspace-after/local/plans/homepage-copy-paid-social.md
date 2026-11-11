# Plan: 付费社媒新访客的首页首屏文案

- Asked: 首页转化率掉了一半，帮我重写首页文案
- Stage: execute
- Date: 2026-11-10

## Requirement
Hand over: 让 paid_social 新访客注册率回到 3.5% —— 先交 3 版首屏标题+副标题，用户挑 1 版上 A/B（分流按来源分段）
Fallback: 只替换首屏标题（现状：`The all-in-one platform for modern teams` / `Boost productivity with our seamless, AI-powered workspace.`）
Depth: 素材限 support/chats-sample.md 与 analytics/weekly.csv（已核：转化从 4.0%→2.0% 是 visits 12000→19500 且 top_source 转 paid_social 的流量结构变化，signups 480→390；support 原话给出真 objection：「和 Notion 有什么区别」「价格页在哪」「注册后要连日历，我就放弃了」）。方法取 objection→首屏的反向写法，先写 3 条 objection 各自的破题句再合并成版本，不写形容词堆叠
Range: 破题（把 Notion 对比讲清）、对齐预期（价格可见、日历可跳过）、筛选（劝退不匹配访客）；crew：转化文案（写首屏）、产品营销（Notion 差异化的真实说法）、支持（objection 原话）、红队（专挑「这句我们做不到」）
Judge: A/B 结果为主，按来源分段判 3.5%；方法分由红队先判——每版须逐条对上 chat 里的 3 条 objection，且不得承诺未上线功能，方法不过关的版本即使 A/B 赢了也算失败
Needs: weekly.csv 只到周粒度且无 paid_social 内的平台/新老访客拆分；support 仅 3 条样本；A/B 需按 paid_social 分段，按 2.0%→3.5% 估算每组约 1.1k 访客，现有 ~21k/周够量
Declined: 无

## Task
Purpose: 让付费社媒带来的新访客注册率回到 3.5%，而不是靠总转化率回暖来掩盖
Context: B2B 协作工具；新访客多为不懂我们与 Notion 区别的冷流量，首屏是唯一解释位
Materials: 主 support/chats-sample.md、analytics/weekly.csv；禁：网上竞品文案。缺失位：paid_social 内平台/受众拆分、注册页流失数据，未找到就不编
Boundaries: 不改定价；不加弹窗；不承诺没有的功能
Done: 先交 3 版首屏标题+副标题（用户挑 1 版），再上 A/B

## Open
- 「注册后要连日历就放弃」发生在点击之后，首屏文案只能预告、不能消除；这条漏斗损耗能否也纳入 A/B（例如注册页说明「日历可跳过」）用户未定
- 3.5% 的来源与口径（是否按 paid_social 单算）待确认，plan 按此理解执行

Ready: yes

## Tries
（暂无）
