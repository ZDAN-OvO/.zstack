计划已写到 `local/plans/login-crash-fix.md`。

**查出来的事实**（这几条不用你回答）：
- 榜首崩溃 = `login.ts:5` 的 `s.user.name`，412（2.3.0）+ 377（2.3.1）= **789/896 = 88%**；**2.3.1 没修掉它**
- `src/login.ts` 三个口子都没防：`s.user` 可能 undefined、401/HTML 响应上 `r.json()` 直接抛、`name` 未转义拼进 HTML
- 没有测试、没有 node_modules（npm 可达，vitest 能装）、**不是 git 仓库**（没有回滚网）
- 仓库里没有 `/api/session` 契约、没有 `cart.ts`（那 19 次）

**要你定的（Requirement 三轴，接受/改写/拒绝）：**
- 交付 `R2`：在 session 边界校验响应 + 未登录兜底 + 测试锁住；退一档 `R1` 只修引导路径；再往上 `R3` 接管崩溃上报——只有 4 行 CSV，今天做不到，那就是天花板
- 深度：先用失败测试复现再改，而不是读完代码直接打补丁；顺带记一笔 `renderForm` 未转义（只记录，不扩范围）
- 红队会问：正常登录路径被弄坏没？空 catch 吞错算不算过？

**只你能答的五个槽：**
1. **Purpose**：是"别白屏、给个重新登录的出口"，还是"把 crash-free 会话率拉回去"？
2. **Context**：token 过期/未登录时，服务端实际返回什么？（200 + `{user:null}`？401？HTML？）
3. **Materials**：能给我 `/api/session` 的代码或契约吗？有没有一条完整堆栈？（有一类来源你不想让我用吗）
4. **Boundaries**：我猜你不想看到——改 API 契约、碰 `cart.ts`、除测试外加依赖、空 catch 吞错、把 token 搬出 localStorage。哪几条是"不是我要的"？
5. **Done**：我提议先给你「根因一行 + 兜底后的返回结构」当 checkpoint，你点头后再出 diff + 先红后绿的测试 + 2.3.0/2.3.1 是否各发一版。

`Ready: no`。回一句哪条要改（比如"只要 R1"、"服务端 401"、"Boundaries 全对"），我就把 Ready 改成 yes；确认后可以用 `/define-goal` 拿这份计划当源。