自查我按**能自己判的检查**来定，不按「我觉得改好了」：

- 最多的那条是 `login.ts:5` 的 `TypeError ... reading 'name'`，412+377 = 789 次，而且当前 2.3.1 还在报 → 活的崩溃。
- 根因在源码就看得见：`r.json()` 对 401/过期 token 也照解，`s.user` 为 undefined 直接白屏。
- 判据落地：对着日志里的失败形态先写测试，**修复前必须红、修复后必须绿**。没有红这一步，我写的测试只是自我盖章。
- 另外两条顺带查清：`ChunkLoadError` 是发版残留；`RangeError at cart.ts:41` 的源文件不在本仓库，这里修不了。
- 一个前提：这目录不是 git 仓库、也没装 vitest → 改前备份 `.bak`，装 vitest 需联网。

计划已写到 `/tmp/pf-34-with_skill-zl8nmlml/local/plans/top-crash-login-undefined-user.md`。

Ready: no——Purpose（修完要出 2.3.2 还是先止血）、Boundaries（最要紧：别把「不白屏」做成「静默吞 401」）、Done（单测绿够了，还是要浏览器/真机验证）这三个槽还只有我的提议。你回这三行，或直接说「按你提议的执行」即可。

确认后可用 `/define-goal`，以这份计划为源。