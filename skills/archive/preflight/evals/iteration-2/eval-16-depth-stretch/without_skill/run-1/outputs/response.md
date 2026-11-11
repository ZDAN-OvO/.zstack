我先看了项目，结论是：**这个仓库里没有首页代码，也没有任何性能数据，所以现在无法做“5秒→3秒”的优化**——我没有可以基于事实去改的东西。

## 实际情况

整个项目只有 4 个文件、12 行源码：

| 文件 | 内容 |
|---|---|
| `src/login.ts` | 登录挂载逻辑，12 行 |
| `package.json` | 只有 `test` / `build` 脚本 |
| `README.md` | 一句话说明 |
| `logs/crashes-2026-11.csv` | 崩溃日志 |

没有路由、没有首页组件、没有 `index.html`、没有 vite 配置、没有 node_modules，也不是 git 仓库。任何“我帮你加了 code splitting / 懒加载 / 预取”的改动都只能是我凭空编的，改完也无法验证是否真的从 5 秒降到 3 秒。

## 但日志里有两个真实问题，值得先修

```
2026-11-01,2.3.0,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",412
2026-11-01,2.3.0,"ChunkLoadError: Loading chunk 7 failed",88
```

**1. `login.ts:5` 每天都在崩，复现路径明确**

`src/login.ts:5` 是 `renderForm(s.user.name)`。当 `/api/session` 返回 `{user: null}` 或 token 过期返回 401 的 HTML/错误体时，`s.user` 就是 undefined，直接抛错，导致页面白屏。这是一条必然触发路径，不该等到用户报障：

```ts
fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
  .then((r) => {
    if (!r.ok) throw new Error(`session ${r.status}`);
    return r.json();
  })
  .then((s) => {
    if (!s?.user?.name) return root.innerHTML = renderForm("");  // 或跳登录
    root.innerHTML = renderForm(s.user.name);
  })
  .catch(() => { root.innerHTML = renderForm(""); });
```

另外这里还有 XSS 隐患：`name` 未经转义直接拼进 HTML 属性。

**2. `ChunkLoadError: Loading chunk 7 failed`**

这是典型的发版后旧 HTML 引用已删除的 chunk，用户停留页面点导航就炸。和数据里的 88 次吻合。标准解法是给 `index.html` 加 chunk 加载失败自动 reload 一次（`vite-plugin-chunk-reload` 或手写 `window.addEventListener('vite:preloadError', ...)`）。

## 要真正做性能优化，我需要你提供

1. **首页源码**——现在不在这个目录里，是不是另一个仓库/branch？
2. **5 秒的测量口径**——是 LCP、TTFB 还是 `load` 事件？哪台机器/什么网络（4G/有线）？dev 还是 prod build？
3. **一次 Lighthouse 或 DevTools Network+Performance 的导出**——没有这个，我不知道 5 秒里是慢在接口、JS 体积、还是渲染阻塞。

给了这三样，我才能定位到真正的主因，再谈 3 秒目标是否可达。现在贸然改代码，风险是改了一堆地方、数字不动，还引入新 bug。

要不要我先按上面第 1 点把登录崩溃和 XSS 修掉？这个不依赖任何测量数据，是明确的 bug。