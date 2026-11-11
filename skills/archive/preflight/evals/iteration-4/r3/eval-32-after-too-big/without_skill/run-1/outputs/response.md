抱歉，这份 plan 是我写的，跑偏成这样有我的责任。

两点先说清楚：

**1. 这个工作区里看不到那 40 个文件的改动。** `local/plans/` 之外只有 `src/login.ts`、`logs/`、`package.json`，没有 `.git`，也没有测试目录。所以要看 diff 得回到你真正的仓库，先跑 `git diff --stat main...HEAD`，别直接开 review。

**2. 一个很可能的原因：仓库里根本没有测试脚手架。** `package.json` 写着 `"test": "vitest run"`，但 devDependencies 里没有 vitest，`src/` 下也没有任何测试。plan 的 Done 写的是「含回归测试」，于是这一晚大概把大半时间花在装 vite/vitest、配 tsconfig、补路径别名上——40 个文件是这么来的，跟白屏本身关系不大。

**真正的问题只在 `src/login.ts:5`：**

```ts
.then((s) => { root.innerHTML = renderForm(s.user.name); });
```

崩溃日志里 412 + 377 次全是同一个错：`Cannot read properties of undefined (reading 'name')`。`localStorage` 里没 token 时会发 `Bearer undefined`，`/api/session` 返回 401/错误体，`s.user` 就是 `undefined`，然后 render 抛异常 → 白屏。修它需要：`r.ok` 判断、`s?.user` 兜底、缺 token 直接渲染登录表单。一个文件，十几行。这也符合 plan 的 Boundaries（不动后端）。

**建议的处理顺序：**

1. 先不 review 那 40 个文件。把分支砍掉，只挑真正落在 session/login 路径上的 commit；一个都没有就更省事。
2. 重新出一版收紧的 plan：`Done: 一个 PR，≤3 个文件，只改 src/login* + 一个 test`，并写明「不得引入/升级依赖」，装测试工具单独一个 PR。
3. 修完用 `logs/crashes-2026-11.csv` 里那条 error 字符串做断言——测试要能复现「`s.user` 为 undefined 时不白屏」，这才对得上 plan 里那个 Judge。

要我现在按第 3 步写出这个最小 patch（`src/login.ts` + 一个不依赖新装的 vitest 也能跑的测试骨架）吗？还是你先给我那个分支的 `git diff --stat`，我帮你判断哪些该留？