已记到 [ladders/login-whitescreen.md](ladders/login-whitescreen.md) 的 Trials：2026-11-08，rung 2 rejected，理由是你说的"只加了 loading 骨架屏，白屏的真正原因没找到"。表里 rung 2 我先留 `handed`，等你决定是原地重试还是降档。

我的判断：这次落空的不是高度，是方法。你交出去的是"用户从打开 App 到登录成功不再卡住或白屏"，它没做诊断就动手，骨架屏只是把空白盖住。

同档换深度再跑一次比降档划算，也就是 `/deeper`。几个具体线索，能当那一轮的起点：

- [src/login.ts](src/login.ts) 的 `mountLogin` 只有一句 `await fetch('/api/session')`，没有超时也没有 catch。按 [docs/GLOSSARY.md](docs/GLOSSARY.md)，session 存在 Redis、TTL 30 分钟，过期或网关返回非 JSON 时 `res.json()` 会抛错或一直挂着，`root` 就永远不渲染，"偶尔"正好对得上这条失败路径；骨架屏没用，因为它自己也在等同一个 fetch。
- 同一行里 `s.user ? '' : '<form…>'`：已登录时是把 root 清空、靠后续渲染接上，路由没接住也会白屏。这是第二种候选原因，和上面的表现一样。

两条路，你选：

1. 同档重跑 `/deeper`（推荐）：先要求它定位根因——区分"fetch 挂起 / 401 返回非 JSON / mount 之前就报错"各自的表现，靠临时日志跑真实失败场景来验证；复现不出来就先加全局错误捕获和 `/api/session` 的超时监控，拿到证据再改。验收方式我也想好了：人为让 session 过期，看登录页是否还有可操作的出口。
2. 降回 rung 1"登录页每次都能正常打开"：范围小，但如果不先定位，大概率还是打补丁。

选 1 的话，我下一轮先把深度访谈的问题列给你；选 2 我改表里的状态，把 rung 1 标成 handed。
