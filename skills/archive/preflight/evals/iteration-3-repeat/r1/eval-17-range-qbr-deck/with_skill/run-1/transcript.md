TOOL bash: {"command": "ls -la; echo \"---\"; ls -R . 2>/dev/null | head -50"}

RESULT: total 184
drwxrwxr-x  4 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 62 root root 167936 11月 10 21:28 ..
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 data
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 notes
-rw-rw-r--  1 zdan zdan    131 11月 10 16:17 template.md
---
.:
data
notes
template.md

./data:
q3-metrics.csv

./notes:
worklog.md


TOOL read: {"path": "template.md"}

TOOL read: {"path": "notes/worklog.md"}

TOOL bash: {"command": "head -5 data/q3-metrics.csv; echo ...; wc -l data/q3-metrics.csv"}

RESULT: # Q3 业务回顾

## 收入
本季收入：{{revenue}}

## 客户
新增：{{new}}，流失：{{churn}}

## 下季计划
{{plan}}


RESULT: # 工作日志

- 9 月 8 日起，客服工单里"太难上手"的投诉明显变多。
- 8 月中旬把免费试用从 14 天改为 7 天。
- 老板说 QBR 下周四给 VP 看。


RESULT: month,revenue_usd,new_customers,churned_customers,nps
2026-07,182000,41,12,38
2026-08,176000,35,19,31
2026-09,171000,30,24,27
...
4 data/q3-metrics.csv


ASSISTANT: 这个 QBR 面向 VP，如果推倒重做，就需要重新约会议，因此不能按便宜任务处理；先花一屏时间确认方向，再开始做。

**建议先写计划，再开始做**：工作区里只有 `template.md`（三格填空模板）、`data/q3-metrics.csv`（7–9 月三个月的收入、新增客户、流失客户、NPS）和 `notes/worklog.md`（其中有两条时间线：8 月中旬试用期 14 天→7 天，9 月 8 日起「太难上手」客诉上升）。所以关键问题在于，**数据里有一件模板装不下的事**：收入连续三月下滑（182k→176k→171k）、流失从 12 升到 24、NPS 从 38 掉到 27，而唯一的时间变量是试用期缩短。按模板填空会做出「本季一般般」的 QBR；真正该交给 VP 的是「试用期改动是嫌疑原因，我们这样验证、这样补救」——这是相关性，还不是已证实的因果。

要不要我按这个思路写一屏计划（含 Purpose / 材料排序 / 边界 / Done 与检查点），你确认后再动手？

- 同意 → 我写 `local/plans/qbr-vp-brief.md`，先给你看计划和 Open 项，不动 PPT
- 不同意 → 直接说「按模板填」，我就照 `template.md` 做
- 或者你先告诉我两件事，我直接进 Requirement/Task：**这场会 VP 要做的决定是什么**（追加预算／认不认这个原因／定下季目标？），**PPT 讲多久、有没有给老板预审过**

也可以接着用 `/define-goal` 把上面的意图补成完整目标。