看了三份输入（`local/plans/login-whitescreen.md`、`logs/crashes-2026-11.csv`、`src/login.ts`）。先说一句边界：这个工作区没有 `.git`，也没有那 40 个文件的改动，所以我审不到那个 PR，只能从 plan 和仓库现状推断它为什么失控。

## 结论：问题出在 plan，不在执行

**根因 2 分钟就能定，日志里写着：**

`TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5`，2.3.0 有 412 次，2.3.1 有 377 次。`fetch` 对 401/500 **不会 reject**，原代码照样 `r.json()` 再取 `s.user.name`；响应体里没有 `user` 就抛在 `.then` 里，而 `root.innerHTML` 只在那一行被赋值 —— 于是 DOM 从头到尾是空的，就是白屏。一行 `s?.user?.name` 加一个 `!r.ok` 判断的事。同一份日志里的 `ChunkLoadError` 和 `cart.ts:41` 是另外两个 bug，跟登录白屏无关。

## 40 个文件是怎么长出来的

1. **plan 里没有"根因"字段。** 只有 `Depth: 先看崩溃日志` —— 记的是动作，不是结论。于是每次执行都要从零考古，改着改着就往"顺手把这层也重写一下"滑。
2. **验收条件不可验证。** `Judge: 回归测试通过 + 一周内崩溃日志该错误为 0`，当夜无法判定，agent 拿不到"够了"的信号，只能靠继续加防御、加抽象来证明自己在推进。
3. **仓库本身没有测试基建。** `package.json` 的 `test` 指向 vitest，但 vitest 不在依赖里、没有 `tsconfig`、没有 `*.test.ts`、没有 `node_modules`：

   ```
   $ npm test  →  sh: 1: vitest: not found
   ```

   要满足 `Done: 一个 PR，含回归测试`，它必须先铺脚手架。这大概就吃掉了十几个文件。
4. **没有改动预算和停止条件。** `Boundaries` 只写了"不改后端接口"，没写"最多动 N 个文件 / 不许碰 X 目录"。

## 我这边已经做的（只动 2 个文件）

- `src/login.ts`：进入时先渲染空表单兜底，`!r.ok` 直接返回，`s?.user?.name` 取值，`try/catch` 兜住网络和非 JSON 响应。任何分支下 `root.innerHTML` 都不为空 —— 白屏这个失败模式被结构性地消除了。
- `src/login.test.ts`：3 个用例，覆盖 401 空体、缺 `user` 字段（就是 2.3.1 的崩溃现场）、正常渲染。

但 **测试还没跑起来**：`npm test` 依然 `vitest: not found`，这个坑得先补（装 vitest + 一个 `tsconfig.json`），否则"回归测试通过"这条验收永远是空头支票。

## plan 该补的字段

```
Root cause: login.ts:5 取 s.user.name，401/无 user 体时抛错 → root 未渲染(白屏)
Repro:     fetch 返回 401 或 {} → 页面空白
Budget:    ≤ 3 个文件(login.ts + login.test.ts + tsconfig)；其余一律不动
Non-goals: 不碰 cart.ts(独立 bug)、不碰 ChunkLoadError、不重构 fetch 层
Done:      npm test 绿 + 401 场景下 DOM 非空(可本地复现，不依赖一周日志)
Stop:      上述通过即停，不再改任何文件
```

## 下一步，二选一

- **A**：我把 vitest + tsconfig 补上，让 `npm test` 真跑绿，然后你只审这 3 个文件。
- **B**：你先看上面 `src/login.ts` 的 patch，认可了我再补测试基建。

那个 40 文件的 PR 建议直接丢，别去救 —— 里面真正需要的只有一个 `login.ts`。