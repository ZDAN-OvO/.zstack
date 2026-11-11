计划写在 `/tmp/pf-34-with_skill-2lvn3z_z/local/plans/fix-top-login-crash.md`。

先说查到的事实（这些不用你回答）：
- 最高频的是 `TypeError ... reading 'name' at login.ts:5`，412+377 = **789/896（88%）**，两个 date、2.3.0 和 2.3.1 都有 → 2.3.1 没修到
- 出错点就在本仓库 `src/login.ts:5`：`.then(s => root.innerHTML = renderForm(s.user.name))`，`s.user` 为空时炸
- `package.json` 写了 `test: vitest run`，但没有 vitest 依赖、也没有测试文件
- `cart.ts:41`（第三条，19 条）的源码不在 `src/` 里

你让我自己检查，我可以跑一个「修复前必须红、修复后绿」的用例来当判据。但有三件事只有你能定：

1. **只加 guard，还是把「session 里没有 user」当作未登录跳登录页？** guard 只是让它不抛错，用户还是卡在空白表单；跳登录才是让这条从 CSV 里消失。
2. **什么不算修好？**（不许改登录跳转？不许动后端契约？）
3. **检查到什么算停？** 测试绿就停，还是要 2.3.1 上线后这条归零的证据——后者这个仓库给不了。

Ready: no。你回这三条我就动手；或者回一句「就加 guard，测试绿即停」，我就按这个做。