我看了一下这个目录，**这里没有首页代码，也没有任何性能数据**，所以现在没法真正做“5 秒 → 3 秒”的优化。

目录里全部内容：

```
package.json      # 只有 bash 脚本，无依赖安装（无 node_modules）
README.md
src/login.ts      # 唯一的源码，登录挂载逻辑
logs/crashes-2026-11.csv
```

缺失的关键东西：

- 没有首页/路由/入口（没有 `index.html`、`App.tsx`、路由配置）
- 没有构建配置（`vite.config.*`、`tsconfig.json`）
- 没有 `node_modules`，`npm run build` / `npm test` 跑不起来
- 没有性能测量：没有 Lighthouse / WebPageTest 报告、没有 bundle 体积数据、没有网络瀑布图
- 不是 git 仓库，无从对比改动

没有基线和代码，任何“优化”都只能靠猜，而且我没法验证是否真的从 5 秒降到 3 秒——所以我不会凭空改。

要继续，请给我其中至少一项：

1. **首页相关源码**（入口文件、路由、首屏组件、`vite.config`、`index.html`）
2. **性能数据**：Lighthouse 报告 / `vite build` 的产物体积 / Network 面板截图或 HAR
3. 说明 5 秒是**哪个指标**：TTFB、FCP、LCP 还是可交互时间？是本地、内网还是公网？

另外顺带提醒（和加载速度无关，但是真 bug）：`logs/crashes-2026-11.csv` 里 2.3.1 有 789 次 `Cannot read properties of undefined (reading 'name') at login.ts:5`，对应 `src/login.ts` 里 `s.user.name` —— 接口返回没有 `user` 时会崩。要不要我先把这个修了？

拿到首页代码后，我通常会按这个顺序查：打包体积（分包/按需加载）→ 首屏关键请求数与瀑布 → 图片/字体 → 阻塞渲染的 JS → 缓存与 CDN。但具体动哪里，得先看数据。