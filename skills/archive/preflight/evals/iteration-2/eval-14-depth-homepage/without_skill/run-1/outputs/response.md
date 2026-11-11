改动逻辑：

| 问题 | 旧文案 | 新文案 |
|---|---|---|
| 和 Notion 没区别 | “all-in-one platform for modern teams” | 直接点名对手 + 对照表 |
| 全是形容词，无具体 | “seamless, AI-powered” | 写清楚自动化到底做什么（催审批、自己写周报） |
| 价格页找不到 | 页面上没有价格入口 | 导航 + footer 都放 Pricing |
| 怕连日历 | 没有任何承诺 | “no setup / no integrations required to start” |

## 5. 上线前必须处理的（否则会 404）

页面里的 `Acme`、`$` 价格、`/pricing`、`/vs/notion`、`/docs` 都是占位符，这些路径目前都不存在。要么补页面，要么改成真实 URL。

## 6. 怎么验证

别全量发布。按来源分层做 A/B：

- `organic` 50/50 分流，只跟 organic 的 CVR 比
- paid_social **不参与实验**，它现在的 1.9% 是受众问题，不是页面问题，混进来会污染结果
- 先修埋点再加 `source` 维度，拿到干净基线，再跑 2 周（按现在量级，organic 每天约 1,700 访问，能测出 ~0.5pp 的差异）

要不要我先做两件事：给 `weekly.csv` 加来源拆分脚本，以及把「连日历」那步做成可跳过？后者对转化率的影响，会比这版文案大。