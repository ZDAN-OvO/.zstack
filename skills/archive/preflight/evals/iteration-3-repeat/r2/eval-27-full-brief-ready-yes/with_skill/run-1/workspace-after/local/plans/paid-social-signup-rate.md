# Plan: 付费社媒新访客注册率回到 3.5%

- Asked: 首页转化率掉了一半，帮我重写首页文案
- Stage: execute
- Date: 2026-11-10

## Requirement
Hand over: 3 版首屏标题+副标题（用户先挑一版），再上 A/B，目标付费社媒新访客注册率 3.5%
Fallback: 只改首屏标题（已接受）
Depth: 已接受——逐条引用 support/chats-sample.md 原话，按来源拆 analytics/weekly.csv 漏斗，不凭感觉写
Range: 已由用户裁决——不新增；素材限定在 support 聊天与 analytics
Judge: A/B 结果本身（分来源看注册率）；上线前由用户挑版
Needs: 3.5% 目标对应的每臂样本量（见 Open）；paid_social 落地页来源参数与注册漏斗埋点是否可拆到首屏来源
Declined: 用网上竞品文案（用户：不用）；改定价、加弹窗、承诺没有的功能（用户：不改）

## Task
Purpose: 让付费社媒带来的新访客看懂“我们和 Notion 的区别”并完成注册，注册率从 1.9–2.0% 回到 3.5%
Context: B2B 协作工具；新访客多不懂我们和 Notion 的区别；降价那周起 top_source 从 organic 变为 paid_social（10-06/13 约 3.9–4.0%，10-20/27 约 1.9–2.0%）
Materials: 一手——support/chats-sample.md（3 条原话）、analytics/weekly.csv、现首页 index.html；禁用——网上竞品文案
Boundaries: 不改定价；不加弹窗；不承诺没有的功能
Done: 3 组“标题+副标题”交到用户手上，附各自对应的聊天原话与取舍理由；用户挑定一版后才进入 A/B

## Open
- 转化腰斩与来源切换同时发生，目前只是相关：先确认 paid_social 访客的注册率是否同样低，文案才能算主因
- 3.5% 需要每臂约 3.8k 访客（2.0%→3.5%，80% 功效）；按 20k/周约 2 周可读出结果，用户是否接受这个周期
- 聊天里“注册后要连日历，我就放弃了”指向注册流程而非首屏文案，且“价格页在哪”指向导航；边界内无法处理，是否记为已知限制
- paid_social 新访客意图可能低于 organic，3.5% 是否仍为合理目标

Ready: no —— 需确认上述 4 个 Open 项（尤其第 1 项与第 3 项）
