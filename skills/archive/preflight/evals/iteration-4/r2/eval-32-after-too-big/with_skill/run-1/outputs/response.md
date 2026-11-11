## 判定：不是执行不到位，是计划给了它 40 个文件的空间

用 `logs/crashes-2026-11.csv` 一聚合，范围本来只有一行：

| error | 次数 |
|---|---|
| `TypeError: ... reading 'name' at login.ts:5` | **789**（412+377） |
| `ChunkLoadError: Loading chunk 7 failed` | 88（另一个根因，部署后旧 chunk） |
| `RangeError ... cart.ts:41` | 19（无关） |

`src/login.ts:5` 在 `/api/session` 返回没有 `user`（未登录 / token 过期 / 401 非 JSON）时读 `s.user.name` → 整页白屏。2.3.1 里 377 次还在，说明这行没被碰过。

计划里的两处漏，让它整夜都在猜：

1. **Too big** — `Hand over: 白屏不再出现，并有回归测试` 这一步把 ChunkLoadError 也算进"白屏"，于是它去改 chunk 加载、路由、请求层……40 个文件。`Fallback: 只修当前复现的那一个白屏` 本来就在计划里，但没被执行。
2. **Missed intent** — `Boundaries` 只有"不改后端接口"，没有规模墙；`Done` 直接是"一个 PR"，没有改前 checkpoint，所以 40 文件的 PR 也算交了卷。

## 已改的（`local/plans/login-whitescreen.md`）

- Hand over 降到 Fallback 那一级：**只修 login.ts:5**，1 file / ~6 行
- Boundaries 加墙：单 PR 文件数 ≤2、不重构、不顺手修 ChunkLoadError
- Done 加 checkpoint：**动手前先出「根因一行 + diff 预览」**
- Depth 换成专家动作：先按 error+行号聚合、算清 896→1，再动手
- Judge 加一条可自查的：diff 只碰 1 个文件、审阅 ≤5 分钟

目标改法（等你点头再落盘）：

```ts
export function mountLogin(root: HTMLElement) {
  const token = localStorage.getItem("token");
  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
    .then((r) => (r.ok ? r.json() : null))
    .then((s) => { root.innerHTML = renderForm(s?.user?.name ?? ""); })
    .catch(() => { root.innerHTML = renderForm(""); });   // 401 / 非 JSON 也不白屏
}
```

红队会问的那句先摆出来：这样吞掉后，token 过期的人看到空表单，以为是"没登录过"而不是"请重新登录"——演示前够用，但不是终态。

## 需要你两个东西（`Ready: no`）

1. 那 40 个文件的**分支 diff**——不给的话整支丢弃重开，免得有人把噪音当修复继承下来
2. **vitest 环境**：`package.json` 没有测试依赖，`src` 下没有测试文件，"回归测试通过"这条现在没人能执行

计划在 `local/plans/login-whitescreen.md`。确认降级 + 两道墙后 `Ready: yes`，可以接着用 `/define-goal` 把它当来源。