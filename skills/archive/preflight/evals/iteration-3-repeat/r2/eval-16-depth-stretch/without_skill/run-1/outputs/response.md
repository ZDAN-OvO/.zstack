我先看了仓库，结论比较直接：**这个仓库里没有首页，也没有任何可用于定位 5 秒耗时的东西，所以我没法在这里做出并验证“5s → 3s”的优化。**

## 现状

仓库全部内容：

```
package.json      # 只有 react 依赖 + vite build 脚本
README.md
src/login.ts      # 唯一的业务代码
logs/crashes-2026-11.csv
```

具体缺失：

- 没有 `index.html` / `main.tsx` / 路由或首页组件 —— 不知道“首页”是哪段代码
- 没有 `vite.config.*`、依赖未安装、没有构建产物，无法分析 bundle
- 没有任何性能数据（Lighthouse、HAR、资源瀑布、TTFB、首屏接口耗时）
- 除 `login.ts` 外无源码，无法判断 5 秒花在 TTFB、JS 解析、首屏请求还是渲染

在这种情况下给“优化到 3 秒”的方案，只能是猜测；即使改了也无法验证达标。我不会假装做到。

## 唯一有价值的线索：一个真实 Bug，不是性能优化

`logs/crashes-2026-11.csv` 里 2.3.1 版本有 **377 次/月**：

```
TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5
```

对应 `src/login.ts:5`：

```ts
.then((s) => { console.log("session", s); root.innerHTML = renderForm(s.user.name); });
```

`/api/session` 返回里没有 `user` 时直接抛错，结果：**白屏、无兜底、无重试**。这会让用户主观上觉得“页面加载不出来/很慢”，但它是否贡献了那 5 秒，日志证明不了 —— 需要结合上面的性能数据确认。

另外这段代码本身就是阻塞式首屏：`fetch` 完成前什么都不渲染，也没有 timeout / 错误分支。这是可以改的，但收益需要实测。

## 要往下做，我需要你提供其一

1. **首页代码 + 构建配置**（或正确仓库/分支），我直接做剖析和改动；
2. 或者一份基线数据，最小集：
   ```bash
   npx lighthouse <首页URL> --preset=desktop --output=json --output-path=./lh.json
   # 以及首屏关键接口的耗时
   curl -o /dev/null -s -w 'dns:%{time_namelookup} tcp:%{time_connect} ttfb:%{time_starttransfer} total:%{time_total}\n' <API_URL>
   ```
3. 如果只想先止血，我可以立刻把 `login.ts` 改成：先渲染骨架 → 再请求 session → `s.user?.name` 兜底 + `AbortSignal.timeout` + 失败态。这能消掉那 377 次崩溃并改善体感，**但我不承诺它等于 3 秒**。

你倾向哪条？给我首页入口文件和一份 Lighthouse/HAR，我就能指出具体是哪几百毫秒、按收益排序改。