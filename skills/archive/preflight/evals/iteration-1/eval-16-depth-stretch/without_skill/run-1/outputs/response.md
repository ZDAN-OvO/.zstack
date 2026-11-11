我先看了仓库，**不建议现在直接动手改**（除非你想让我盲改）。原因如下：

## 现状

```
src/login.ts    ← 只有这一个组件（登录页，不是首页）
package.json    ← scripts 里有 vite build，但 devDependencies 里没有 vite
logs/           ← 崩溃日志
```

- 没有首页代码（无路由、无 `Home`/`index` 组件）
- 没有构建配置、没有代码分割、没有图片/字体资源
- 没有性能数据：不知道 5 秒是 **LCP / TTI / 首屏可见**，也不知道是本地还是线上、什么网络、什么设备
- 不是 git 仓库，看不到改动历史

所以“5 秒优化到 3 秒”目前**无法验证**：没有测量手段，改完也没有基线可比。盲改常见动作（懒加载、拆包、预取）在这个空仓库里无处落地。

## 我需要的信息吧（按重要性）

1. **指标定义**：5 秒是哪个数？LCP？`load` 事件？还是“白屏到有内容”？用 Lighthouse / WebPageTest 跑一次，给我 report JSON 或截图。
2. **首页代码在哪**：是另一个仓库？还是需要我从零建？如果是别的仓库，把路径/仓库地址给我。
3. **打包产物分析**：`dist/` 或 `vite build --mode production` 后的 bundle 分析（`rollup-plugin-visualizer` 输出）。
4. **线上资源瀑布图**：Network 面板 HAR 导出最能定位瓶颈（多半是某个阻塞请求或大 chunk）。

## 顺带：日志里有个真 bug，比性能更急

`logs/crashes-2026-11.csv` 里 2.3.1 版本仍有 **377 次** 同一条崩溃：

```
TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5
```

对应 `src/login.ts:5` `s.user.name` —— 接口返回里没有 `user` 时直接解引用。这是**登录页白屏**的直接原因，用户看到的大概率就是“一直转圈/空白”，体验上很像“页面慢”。同一文件还有：

- 没判 `token` 为空就发请求
- 没处理 `!r.ok`（401 也照样 `r.json()`）
- 没 try/catch，失败后不渲染任何错误态

这个我可以马上修（加 token 校验 + `r.ok` 检查 + fallback 错误 UI，顺带消掉 line 5 的崩溃）。要我改吗？

---

**下一步建议**：先给我一份 Lighthouse 报告或 HAR，我按真实瓶颈出方案；同时我可以先把登录页这个崩溃修掉。你选哪个先？