# Plan: 修掉最高频的登录崩溃

- Asked: 修一下 logs 里出现最多的那个崩溃
- Stage: execute
- Date: 2026-11-10

## Requirement
排序事实：TypeError reading 'name' @login.ts:5 = 789/896（88%），2.3.0 有 412，2.3.1（当前版本）仍有 377 → 上次发版没修掉，不是老问题的残留。

Hand over: 不只补空值判断，而是「会话不可用时不崩、可识别」：token 缺失 / 401 / 非 JSON / 无 user 都走登出态表单，失败被记一条日志而不是静默消失。发布到 2.3.2 的另一半（无 git、无发布配置）超出本仓库，属天花板。
Fallback: 只在 login.ts:6 加 `s?.user?.name ?? ""` 一行兜底 + 一个测试。
Depth: 原始材料 = 崩溃 CSV + 实际响应；仪器 = 会话类型 + 解析函数（拒绝 `any` 直取 `.name`）+ 用 Node 26 自带 `node --test` 和假 fetch 的用例（零依赖）。专家动作：崩溃报在 :5 而解引用在 :6，说明线上 bundle 与本仓库 src 有偏移 —— 先确认「修的是线上跑的那份代码」再改。Stretch: 用数据证伪「崩溃只因 token 过期」—— CSV 无 UA/接口状态列，此假设在本仓库不可检验，记为发现而非结论。
Range: 动词 = 让用户不再看到白屏 / 让下一次同类失败可认 / 挡住复发。Crew：前端（补丁 + 类型）、可观测性（2.3.1 的 377 说明埋点或发版有问题）、红队（打穿兜底：user 为 null、200 返回 HTML、fetch reject）。
Judge: 先写用例在旧代码上跑出同样的 throw，改完后全绿；红队另出 5 种坏响应作为未调优用例。判方法而非运气：兜底能过而未复现旧错，判失败。
Needs: 有（node 26 / npm 可通）；缺：git 仓库（无法把 2.3.0/2.3.1 对到 commit）、`cart.ts`（另一个崩溃引用的文件不在仓库）、接口真响应与服务端日志、前端埋点。
Declined: —

## Task
Purpose: `<待你回答>` —— 这次是「2.3.2 发版前止血」、「查清 2.3.1 为什么没修掉」，还是「让登录失败可统计」？三者产出不同。
Context: `待确认的事实`：token 可能为 null；401 后的 JSON 无 `user` 字段；`.then` 链无 `.catch`，失败即白屏；线上行号与本仓库差 1 行。
Materials: 主 = `logs/crashes-2026-11.csv`、`src/login.ts`；次 = `package.json`（版本 2.3.1）。禁用 = 凭空假设后端契约。空位 = 接口 schema、服务端日志、UA/浏览器分布。
Boundaries: `<待你回答>` —— 哪些改动会让你说「不是我要的」？（例：不动视觉、不改与后端的接口约定、不加依赖、只碰 login.ts）
Done: 待定形状：`src/login.ts` 的补丁 + 一个 `node --test` 用例文件 + 3 行结论（为什么 2.3.1 仍在崩）。Checkpoint：动手前给诊断和补丁要点，供你否掉方向。

## Open
- 2.3.1 仍在崩 377 次：是修了没发、发的是旧 bundle，还是根本没修？本仓库无 git、无 sourcemap 可查。
- `cart.ts:41` 的栈溢出在仓库里找不到对应文件 —— 这个 logs 目录覆盖的代码范围是否大于本目录？

Ready: no —— Requirement 三轴待你取舍，Purpose / Boundaries / Done 待你回答。
