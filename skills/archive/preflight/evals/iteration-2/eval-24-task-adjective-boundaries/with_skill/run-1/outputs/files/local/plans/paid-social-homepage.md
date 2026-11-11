# Plan: 让付费社媒访客 5 秒看懂我们在做什么

- Asked: 帮我重做首页视觉
- Stage: execute
- Date: 2026-11-10

## Requirement
Hand over: 请求原样（重做首页视觉）
Fallback: 只重做首屏（一屏内的文案 + 构图 + CTA），整页不动
Depth: 素材用 `support/chats-sample.md` 里三条真实异议（和 Notion 有什么区别 / 价格页在哪 / 注册要连日历就放弃），而不是形容词；仪器是一次 5 秒首屏测试 + 转化率前后对比
Range: 动词 = 一眼认出品类、一眼看到与 Notion 的差别、一眼找到价格、不连日历也能开始；crew = 定位策略、转化文案、投放信息一致性、前端视觉、红队（一个刷到广告就划走的付费访客）
Judge: 冷读者 5 秒复述测试（说不出"我们是干嘛的"即失败）+ 投放渠道 2 周转化率对比；同时判方法与结果
Needs: 缺失 —— 正在跑的广告素材与落地页 URL、真实差异化说明、价格页
Proposed:
  - Altitude ↑ 交付物从"首页视觉"升到"付费社媒访客的首屏激活率"（含广告词与首屏的话术对齐）
  - Depth ↑ 首页主张按三条真实异议重写，并加一次 5 秒可复述性测试
  - Range ↑ 加一个红队角色，专门挑"这看起来像不像又一个 Notion"
Declined: —

## Task
Purpose: 让付费社媒来的新访客 5 秒内看懂我们是干嘛的
Context: 近四周 organic→paid_social 切换，访问量 1.2万→2.1万，转化 4.0%→1.9%（`analytics/weekly.csv`）；三条客服记录指向定位与入口问题，不是美术问题（待你确认）
Materials: `index.html`（现首屏"all-in-one platform for modern teams / AI-powered workspace"，正是客服说"和 Notion 没区别"的来源）；`analytics/weekly.csv`；`support/chats-sample.md`。缺：广告素材、落地页 URL
Boundaries: （空）"高级、简洁、有科技感"是方向词，不是墙
Done: （未定）

## Open
- Boundaries 空着，这是本次最大的风险：没有墙，"高级简洁科技感"可以被做成任何样子。你的墙可能是哪些？例如：不许再用"all-in-one / 一体化工作台"这类话术、不用图库素材和渐变紫、首屏不放注册表单、不写还没做出来的功能。
- Done 未定：先看首屏一版（文案 + 构图 + CTA），过了再做整页 —— 这个 checkpoint 你认吗？
- 数据里"注册后要连日历我就放弃了"是注册流程问题，首页重做改不到它。这块要不要单独立项？
- 广告素材缺席时无法做投放词与首屏的对齐；你先给素材，还是先做一版通用首屏？

Ready: no — Boundaries 与 Done 未答，三条 Proposed 待你裁决，广告素材缺失
