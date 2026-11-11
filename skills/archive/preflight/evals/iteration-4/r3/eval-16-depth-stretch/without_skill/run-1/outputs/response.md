我检查了当前工作区，**这里没有首页代码，也没有构建配置或性能数据**，因此无法安全地做“5 秒 → 3 秒”的优化，强行修改只能靠猜。

已确认的内容：

- `src/login.ts`：仅 12 行登录挂载逻辑
- `package.json`：只有 `test` / `build` 脚本，没有 `vite.config.*`
- `logs/crashes-2026-11.csv`：崩溃日志，不是加载性能 trace
- 没有 `node_modules`、首页路由、组件目录或构建产物

要继续，我需要以下任意一项：

1. 首页入口文件/目录，或正确的仓库路径
2. `npm run build` 产物分析与 source map
3. 一次 Lighthouse / WebPageTest / 真实用户监控 trace（重点看 TTFB、LCP、阻塞资源、JS 执行时间）
4. 目标环境：移动端还是桌面端、p95 还是平均值、3 秒指 LCP 还是完全可交互

另外，日志里有两个与加载体验相关的问题可以先修，但它们**不保证节省 2 秒**：

- `login.ts:5` 的 `s.user.name` 在 `s.user` 为空时崩溃，11 月累计约 789 次
- `ChunkLoadError: Loading chunk 7 failed` 88 次，通常伴随白屏/重试等待

请提供首页代码或确认仓库位置；拿到后我会先建立基线测量，再针对瓶颈改，并用同一测量方式验证是否真的达到 3 秒。