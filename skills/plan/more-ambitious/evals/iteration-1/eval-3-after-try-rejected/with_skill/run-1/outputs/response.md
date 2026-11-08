已记进 [ladders/login-whitescreen.md](ladders/login-whitescreen.md) 的 Trials（rung 2 先保持 `handed`，还没退阶）。

我的判断：这次不是台阶选高了，是这一阶缺「诊断」。骨架屏只改「渲染之前显示什么」，对任何一次请求失败或空渲染都无济于事——它能让眼睛看不见白屏，不能证明白屏的原因消失了。

仓库里能看到的两处可疑点（都还没验证）：

- **known**：[src/login.ts](src/login.ts) 的 `fetch('/api/session')` 没有失败分支。请求失败、超时或返回非 JSON 时 `await res.json()` 抛错，`mountLogin` 直接退出，`root` 保持空 → 白屏，且这属于未捕获的 promise 拒绝，页面级错误钩子很可能看不到。
- **known（代码如此）/ unsure（是否就是这次的 bug）**：同一行的 `root.innerHTML = s.user ? '' : '<form id="login"></form>'`。已登录用户访问登录页时写入空字符串，也是白屏；「偶尔」可能与是否存在有效的 Session（Redis，TTL 30 分钟）正好吻合。
- **unsure**：白屏也可能发生在 Shell 阶段（SPA bundle 之前），那样 `login.ts` 根本没执行，登录页里怎么改都没用。

原因没定位属于方法问题而不是台阶问题，所以建议**同阶先跑 `/deeper`**，别急着退阶。它会先 grill 你手上有什么：能不能拿到前端错误日志、白屏时 Network 里 `/api/session` 是什么状态、能不能本地复现、白屏时是全空白还是有 Shell；然后给出这一阶的专家做法——先证明白屏断在哪一层再谈改法，以及「改完凭什么算修好」的证据（例如故意让 `/api/session` 失败一次，看页面是否给出可见反馈）。

两个选择：

- **A. 同阶跑 `/deeper`**（rung 2 不变），把诊断补齐再重跑；
- **B. 退到 rung 1**（「登录页每次都能正常打开」，AI 只负责复现与定位，需要前端错误日志），拿到定位结论后重新往上走。

你选哪个？选 A 我开始 grill 你要哪些材料；选 B 我把 rung 2 标 `rejected`、rung 1 标 `handed`。
