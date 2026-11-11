大致情况先对齐：**在那个 PR 上继续审查只会浪费时间，请直接关掉它。** 现在这个工作区是干净的基线版本（没有 git 仓库、没有 node_modules、没有生成任何改动），所以 40 个文件的 diff 不在我这里；但根据 plan 和日志，我能说清它为什么会变成 40 个。

## 真实的 bug 只有一行

`logs/crashes-2026-11.csv` 共 896 次崩溃，其中 **789 次（88%）是同一条**：

```
TypeError: Cannot read properties of undefined (reading 'name')
```

全仓只有一处 `.name` 访问，就是 `src/login.ts:6` 的 `renderForm(s.user.name)`。整条崩溃路径是：

`/api/session` 在 token 过期或无效时返回 401，body 里没有 `user`（或不是 JSON）→ `r.json()` 照样 resolve → `s.user` 是 `undefined` → 取 `.name` 抛出异常 → 这个 `.then` 链**没有 `catch`** → unhandled rejection → `root.innerHTML` 此行从未执行 → 页面元素没有内容，也就是白屏。另外 `localStorage.getItem("token")` 为 null 时还会发出 `Bearer null`。

日志里另外两条是**不同的 bug**：`ChunkLoadError`（88 次，部署和缓存问题）和 `cart.ts:41` 递归爆栈（19 次，购物车）。它们和登录白屏没有任何关系。

## 为什么跑一晚上会改 40 个文件：问题出在 plan，不在 agent

| plan 字段 | 写了什么 | 实际效果 |
|---|---|---|
| `Range:` | `—` | 范围完全没有边界。日志里有三条错误，于是三条都“修”了，40 个文件就是这么来的 |
| `Depth:` | `先看崩溃日志` | 这是一条**调查顺序**说明，不是范围限制。日志看完，自由发挥就开始了 |
| 缺 `不做` | 没有 | 没有排除 ChunkLoadError、cart.ts，它们被当成同一件事 |
| `Done:` | `一个 PR，含回归测试` | 没有文件数量或修改范围的上限。更糟的是：仓库**没有安装 vitest、没有测试目录、没有 tsconfig**，为了满足“含回归测试”，只能搭脚手架并增加 devDeps、config，这是文件数膨胀的主要入口 |
| `Fallback:` | `只修当前复现的那一个白屏` | 这其实**才是正确的范围**，却被放在 fallback 位置，“当前复现的”也没有固定成具体错误签名（`reading 'name'`） |

也就是说，plan 把“什么算完成”写成了开放式要求，agent 于是给出了一个包罗万象的 PR。

## 最小修复：2 个文件，16 行

```ts
// src/login.ts
export async function mountLogin(root: HTMLElement) {
  const token = localStorage.getItem("token");
  try {
    const res = await fetch("/api/session", {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!res.ok) return renderLogin(root);          // 401/500 走登录表单,不再白屏
    const s = await res.json().catch(() => null);
    const name = s?.user?.name;
    if (!name) return renderLogin(root);            // 兜住空 body / 字段缺失
    root.innerHTML = renderForm(name);
  } catch {
    renderLogin(root);                              // 网络失败也不留白屏
  }
}

function renderLogin(root: HTMLElement) {
  root.innerHTML =
    `<form><input name="username"/><input type="password" name="password"/><button>登录</button></form>`;
}
```

不只修改 `s.user.name`，是因为仅加 `?.` 会让页面渲染出 `value="undefined"`，白屏变成了坏页面；真正需要的是“未登录时渲染登录表单”。不修改后端，也不扩大范围。`renderForm` 把 name 直接插入 `innerHTML` 存在 XSS 风险，**这次不改**，只把它记进 plan 的“不做”。

## 重写后的 plan（可直接替换）

```md
## Task
Purpose: 下周演示前登录稳定
Context: React 前端，登录依赖 /api/session
Materials: logs/crashes-2026-11.csv, src/login.ts
Boundaries: 不改后端接口

## Scope  ← 关键
Range: src/login.ts 一个文件（+1 个测试文件）
Target: 错误签名 "Cannot read properties of undefined (reading 'name')"，
        即 /api/session 非 2xx/无 user 时的白屏
Depth: 只修登录挂载路径；不改请求协议、不动 UI 框架
Not doing: ChunkLoadError(chunk 7)、cart.ts:41 爆栈、renderForm 的 innerHTML XSS
           —— 三条都记 issue，本 PR 不碰
Fallback: 同上，范围不再收窄（本来就是最小范围）

## Done
- PR ≤ 2 个文件、≤ 30 行 diff
- 测试只覆盖两个 case：401 无 user → 渲染登录表单；正常 session → 渲染表单
- 演示环境手工点一次过期 token 场景

Ready: yes
```

两个需要你决定的点：

1. **要不要我直接应用上面这个 diff 并改 plan？** 2 个文件，我可以现在就执行。
2. 回归测试有个前置问题：仓库没有安装 vitest（`npm test` 指向它但 devDependencies 是空的）。加 devDeps 和 config 会把 PR 从 2 个文件扩大到 5 个。我倾向**先在 plan 里把测试写成“待补”，本 PR 只修 bug**，测试单独一个 PR，避免重演第一次的规模。

40 个文件那个 PR 里如果混进了别的东西，其中唯一可能值得保留的是 `ChunkLoadError` 的排查，建议单独提 issue，别在登录 PR 里救。