先别在 rung 2 上继续加东西。骨架屏只是把白屏换成了转圈：现象变了，成因没变。按阶梯规则退一层，回到 rung 1（登录页每次都能正常打开），先把根因定位补上，再谈整条登录链路。我已经把这次试跑记为 failed 写进 [ladders/login-whitescreen.md](ladders/login-whitescreen.md) 的 Trials。

翻了 [src/login.ts](src/login.ts)，能直接产生白屏的路径有三条，都不是"加载慢"：

1. `await fetch('/api/session')` 和 `res.json()` 都没有 catch（[login.ts:5-6](src/login.ts)）。接口超时、5xx、返回非 JSON 时 mountLogin 直接 reject，后面那行 `root.innerHTML` 根本不执行，页面就是全白。这条最对得上"偶尔"。
2. 请求没有超时控制。`/api/session` 挂住（Redis 慢、session TTL 边界、连接池耗尽）就一直等，等的时候也是白屏——骨架屏只让等待变得可见，没减少一次白屏。
3. `s.user ? '' : '<form id="login"></form>'`（[login.ts:8](src/login.ts)）。已登录的用户拿到的是空字符串，登录页什么都渲染。如果这条线上生效，"偶尔白屏"的一部分就是"已登录的人打开登录页"。

下一步我建议先只做定位、不改产品代码：给 mountLogin 包一层 try/catch 记日志（error name/message + HTTP status），并记录 `/api/session` 耗时和返回体，跑一两天，看白屏对应的是上面哪一条。那个骨架屏先回滚，别让它盖住症状。

动手之前想跟你确认两件事，免得我又猜错方向：

- 反馈白屏的用户里，已登录的占多数吗？—— 是，就优先查第 3 条；不是，重点在第 1、2 条。
- 出问题时刷新能恢复吗？刷新就好偏第 1、3 条；刷新还是白或还要转很久偏第 2 条。

你回这两条，我再按定下来的那条给具体改法（含超时与失败兜底），而不是再换一层遮罩。
