TOOL ls: {"path": "."}

TOOL find: {"pattern": "**/*.md"}

RESULT: analytics/
index.html
support/

RESULT: support/chats-sample.md

TOOL ls: {"path": "analytics"}

TOOL read: {"path": "support/chats-sample.md"}

RESULT: weekly.csv

RESULT: - "我还是没搞懂你们和 Notion 有什么区别"
- "价格页在哪？"
- "注册后要连日历，我就放弃了"


TOOL read: {"path": "analytics/weekly.csv"}

TOOL read: {"path": "index.html"}

RESULT: week,visits,signups,conversion,top_source
2026-10-06,12000,480,4.0%,organic
2026-10-13,11800,460,3.9%,organic
2026-10-20,19500,390,2.0%,paid_social
2026-10-27,21000,399,1.9%,paid_social


RESULT: <h1>The all-in-one platform for modern teams</h1>
<p>Boost productivity with our seamless, AI-powered workspace.</p>
<a href="/signup">Get started</a>


ASSISTANT: 看完 `analytics/weekly.csv`、`support/chats-sample.md` 和当前 `index.html`，下面是计划。

## 结论先行

转化从 4.0% 掉到 2.0%，同期来源从 organic 变成 paid_social，这更像是**流量构成变了**，而不是文案变差了。当前首屏是通用套话（“all-in-one platform / Boost productivity / AI-powered”），对“我们和 Notion 有什么区别”零回答，所以付费社媒来的新访客会直接流失。文案能修的是这个认知缺口。

## 目标与判定

- 主指标：paid_social 新访客注册率 2.0% → 3.5%
- 中间指标：首屏 CTA 点击率、注册页到达率（用来看是文案没说服，还是注册流程劝退）
- 只对比 `top_source = paid_social` 的同期人群，不看全站混合值

## 证据与假设

| 证据 | 来源 | 文案含义 |
|---|---|---|
| 访客翻倍、注册数反降 | weekly.csv | 付费流量意图弱，首屏必须自解释 |
| “和 Notion 有什么区别” | chats-sample | 需要明确的定位对比句，不能只讲功能罗列 |
| “价格页在哪” | chats-sample | 首屏要有定价入口，但不改定价 |
| “注册后要连日历就放弃” | chats-sample | **文案改不了**，最多提前说明期望 |

## 范围

做：首屏标题 + 副标题，3 版备选；CTA 文案如与标题强绑定可同步提。
不做：定价、弹窗、未验证的功能承诺（当前“AI-powered”本身就需要产品确认是否可对外说）、注册流程改动。

## 执行步骤

1. **核事实**（0.5 天）：确认可对外宣称的功能边界，尤其是 AI 能力和与 Notion 的真实差异点。所有标题里的差异主张都要有据可查。
2. **出 3 版**（1 天）：每版 = 标题 + 副标题 + 一句它针对的聊天/数据证据 + 一句它放弃了什么。方向建议：
   - A｜差异化直给：一句话说清“不是又一个 Notion”
   - B｜场景切入：付费社媒人群的具体使用场景，降低理解成本
   - C｜流程预期管理：把“连接日历”等步骤前置说明，筛掉必然流失的人
3. **你选 1 版**，我做像素级文案定稿（含字数与移动端断行检查）。
4. **A/B 上线**：对照组 = 现首页，实验组 = 新首屏，50/50，只投 paid_social。
5. **读结果**（见下）。

## A/B 设计

- 基线 2.0%，目标 3.5%，α=0.05、power=0.8 → 每组约 **1,900 访客**，合计约 3,700
- 按当前 ~21,000/周，两天就能攒够；但**跑满 7 天**以覆盖周内波动，中途不偷看
- 决策规则：达到 3.5% 且中间指标同向 → 保留；落在 2.0–3.5% → 看 CTA 点击率决定是继续迭代文案还是转去修注册流程；低于 2.0% → 回滚，结论写进复盘

## 风险（需要你知情）

- **3.5% 是当前付费流量基准的 1.75 倍**。文案能提升首屏说服力，但“注册要连日历”这个流失点在注册流程里，不在首屏。如果 A/B 显示 CTA 点击率明显上升而注册率不动，问题就不在文案——那需要单独开一轮讨论，不在本次边界内。
- 样本量小（每周约 400 注册），单周结果波动大，别用第一天数据下结论。

## 完成定义

3 版标题+副标题交付、你选定 1 版、A/B 跑满 7 天、出一份含中间指标的结果判定。

**下一步**：我先去核功能边界，然后交 3 版。需要我现在开始第 1 步吗？