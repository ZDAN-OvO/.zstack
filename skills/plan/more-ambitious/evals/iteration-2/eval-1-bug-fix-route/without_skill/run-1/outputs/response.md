我看了 `src/login.ts`，一共 5 行：

```ts
export async function mountLogin(root: HTMLElement) {
  const res = await fetch('/api/session');
  const s = await res.json();
  root.innerHTML = s.user ? '' : '<form id="login"></form>';
}
```

白屏的直接机制是清楚的：这个函数是唯一往 `root` 里写内容的地方，而它没有任何错误路径。只要 `fetch` 抛错（断网、请求被取消、部署中 502）或者 `res.json()` 抛错（返回 502 的 HTML 错误页、204 空 body、网关超时页），Promise 就 reject 了，`root.innerHTML` 那行永远不执行，页面就停在空白状态——正好符合"偶尔"而不是"每次"。另外 `res.ok` 也没检查，4xx/5xx 只要 body 是合法 JSON 就会被当成正常响应处理。

我按这两点做了防御性修复（[src/login.ts](src/login.ts)）：

1. 包 `try/catch`，失败时渲染一行错误提示 + 重试按钮，不再留空白；
2. 检查 `res.ok`，非 2xx 直接进 catch；
3. 已登录时改成 `return`，不再写 `innerHTML = ''`。原来这行会把 shell 已经渲染好的内容整体清掉，如果 shell 里有头部/骨架，已登录用户看到的就是空白——这是第二个可疑的白屏来源，和"偶尔"也吻合（取决于会话是否还有效）。
4. `fetch` 加了 `cache: 'no-store'`，避免会话接口被缓存成旧响应。

两点说明：

- 这是防御性修复，不等于已经定位到根因。我看不到 shell HTML、路由或构建配置，也没法在本地跑起来验证（仓库里没装 TypeScript，`npm run build` 跑不了）。所以现在的状态是"不会再静默白屏"，不是"已经证明原来为什么白"。
- 如果白屏时连错误提示都不出现，那说明 `mountLogin` 根本没被调用（模块加载失败、bundle 404、`root` 选择器拿不到元素），问题就在这个文件之外，得换方向查。

要继续往下定，我需要你给我三样东西：

1. 白屏那一刻浏览器 console 的报错（有没有 `Uncaught (in promise)`，指向 fetch 还是 json）；
2. Network 里 `/api/session` 那条请求的状态码和响应体；
3. 白屏是刷新就好、还是刷新也不行——前者偏请求偶发失败，后者偏会话或 bundle 问题。

有这三条我就能从"防御性修复"走到"确认根因 + 加回归测试"。
