已写入 `local/plans/daily-anomaly-detection.md`。

看过素材后的两个硬事实（决定这份 plan 的形状）：

- `data/q3-metrics.csv` **只有 3 行月度汇总**，`notes/worklog.md` 里却写着 9/8 起"太难上手"投诉变多、8 月中试用期 14→7 天。你要的"用历史数据证明更早发现"用这份数据做不到——只能证明"月度看得到下滑"，证不了"日级能更早看到"。
- worklog 里那条工单投诉，是现成的候选领先指标。拿它去做前置期回测，比新造一套指标更可能一次就中。

待你裁决的三条动作：Hand over / Fallback、Depth、Range+红队。裁完并把 Open 里的"早发现之后谁做什么"和"每月几条不算垃圾"补上，Ready 才能变 yes。

下一步可以 `/define-goal`，把这个 plan 当输入。