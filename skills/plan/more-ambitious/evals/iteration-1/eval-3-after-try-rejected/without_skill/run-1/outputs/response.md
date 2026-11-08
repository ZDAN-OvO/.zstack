rung 2 该退——问题出在我写的那层目标上，不是执行不够快。它写的是"整条链路别卡住、别白屏"，这种说法允许"把等待遮盖住"就算交差，骨架屏正好钻这个空子，于是没人去找真正空白的那个分支。

退回 rung 1 重写，同时我把 [src/login.ts](src/login.ts) 看了，白屏有两条明确出口：

- 第 5 行 `root.innerHTML = s.user ? '' : '<form id="login"></form>'`：已登录用户打开登录页时渲染空字符串。这不是"偶尔"，这类会话是必然白屏。
- 第 3–4 行没有 try/catch：`fetch('/api/session')` 网络失败，或拿到非 JSON（比如网关 502 的 HTML 错误页）时 `res.json()` 抛错，`mountLogin` 返回 rejected promise，调用方不接住，root 就一直空着。

所以真正要找的是"哪些分支会让 root 没有内容"，而不是"等的时候给人看什么"。骨架屏对上面两种情况一点用都没有。

新的 rung 1（已写回 [ladders/login-whitescreen.md](ladders/login-whitescreen.md)，rung 2 标为 rejected）：

> 登录页在 /api/session 的任何结果下都不空白：已登录、401、5xx、网络失败、返回非 JSON 五种情况各自渲染出可见界面；后三种给可重试的提示，并把原始错误连同 status 记进日志。
>
> 验收：人为把这五种返回逐一造出来（或 devtools 断网 + 改写响应）刷新页面，每种都能看到界面；只要有一次空白就不通过；日志里能查到当时的 status。

两点需要你定，我给默认：

1. 已登录用户打开登录页——默认直接跳首页（登录页对已登录用户没意义），提示文案是备选。
2. 修法范围——默认连调用方一起收口（`mountLogin` 外层要 catch 并把错误上报），只改 `login.ts` 内部治不住"调用方没人接"的那条。

这两点你确认或改掉之后，我按这一版重写任务稿交给 /to-brief。
