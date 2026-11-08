# Ladder: login white screen

| Rung | Goal | AI owns | Needs | Status |
|---|---|---|---|---|
| 0 | 修一下登录页偶尔白屏的 bug | | | |
| 1 | 登录页在 /api/session 的任何结果下都不空白（已登录 / 401 / 5xx / 网络失败 / 返回非 JSON，五种情况都要有可见界面） | 定位出空白的每个分支、给出修法 | 前端日志、/api/session 各失败返回的样本 | handed |
| 2 | 用户从打开 App 到登录成功不再卡住或白屏 | 整条登录链路的稳定性 | 前端日志、/api/session 监控 | rejected |

## Trials
- rung 2 → 交付物只给登录页加了 loading 骨架屏，白屏根因未定位，验收不通过。
- 失败原因在目标写法：只要求"不卡住 / 不白屏"，等于允许"把等待遮盖住"就算过关，没逼着去找真正的空白分支。
- 处理：退回 rung 1 并重写，把范围钉在"/api/session 的每一种返回下 root 都要有内容"，验收靠人为构造五种返回。
- 已知线索（[src/login.ts](../src/login.ts)）：已登录分支 `root.innerHTML = ''` 直接渲染空 → 白屏；`fetch` / `res.json()` 无 try/catch，失败时 `mountLogin` reject，调用方不 catch 就整页空白。

Handed over: rung 1（重写版）
