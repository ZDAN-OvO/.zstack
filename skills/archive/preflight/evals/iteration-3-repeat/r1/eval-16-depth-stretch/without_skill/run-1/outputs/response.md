## 先说明结论：当前仓库里没有首页代码，无法直接做这个优化

我检查了工作区，全部内容只有 4 个文件：

```
package.json
README.md
src/login.ts
logs/crashes-2026-11.csv
```

没有首页组件/入口、路由、HTML 模板、构建配置（vite config）、依赖锁文件，也没有 `node_modules` 或 git 历史。因此：

- 无法定位首页 5 秒花在哪里（TTFB / 资源下载 / JS 执行 / 接口串行？）
- 无法做有依据的改动，硬改只会是猜测
- 也无法运行 `npm run build` 或 `npm test` 验证效果

## 需要你补充（二选一即可）

1. **首页代码所在路径或仓库/分支**（如果不在这个目录），我直接去看入口、路由和请求链路。
2. **性能数据**：
   - Lighthouse 报告或 Chrome Performance trace
   - Network waterfall（哪些请求慢、大小、TTFB）
   - “5 秒”具体指哪个指标：`load`、LCP、还是白屏到可交互？
   - 目标环境（移动端/桌面、弱网、地区）

这些数据能把优化从“猜”变成“对症”：常见大头是首屏 bundle 过大、LCP 图片/字体阻塞、接口串行瀑布、第三方脚本、或服务端 TTFB。

## 另外发现的两个独立问题（与加载耗时无关，但建议处理）

`src/login.ts:5`：

```ts
fetch("/api/session", ...).then(r => r.json())
  .then(s => { ... s.user.name ... })
```

- `logs/crashes-2026-11.csv` 里 2.3.0/2.3.1 各有 300+ 次 `Cannot read properties of undefined (reading 'name')`，就是这个未校验 `s.user` 导致的；session 失效或接口返回错误时会直接崩。
- 同时日志里有 `ChunkLoadError: Loading chunk 7 failed`，如果首页也用了动态 `import()`，这可能和加载失败/重试有关，值得一起查。

把首页代码或性能报告给我，我就能给出具体改法和预期收益。