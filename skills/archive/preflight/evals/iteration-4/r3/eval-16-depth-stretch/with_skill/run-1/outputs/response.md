计划已写到 `/tmp/pf-16-with_skill-hm1oxx06/local/plans/homepage-load-time.md`

两点值得先看：

1. **仓库里没有首页代码**，也没有任何性能数据——只有 `src/login.ts` 和一个崩溃日志。所以现在动手改，是猜的。
2. `login.ts` 里的 `/api/session` 没有超时、没有错误分支，而崩溃日志记录了 789 次 `session.user.name` 空指针。**你的"5 秒"里可能有一部分是请求挂住的白屏，不是资源太大。** 先做诊断再削 bundle，比直接改代码省一轮。

要我把它接成正式目标吗：`/define-goal`，以这份计划为源。