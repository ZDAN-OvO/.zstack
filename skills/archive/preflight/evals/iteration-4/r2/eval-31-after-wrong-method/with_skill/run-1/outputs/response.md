我先去核对了一遍原始数据，发现这次失败的根源在方法，不在执行：第 1 版的 Depth 只写了“先看崩溃日志”，结果看完后仍停在一条堆栈上，于是下一步的动作就自然变成了“给个骨架屏先把白屏盖住”。

从 `logs/crashes-2026-11.csv` 和 `src/login.ts` 里直接查出来的事实（不是猜的）：

- **`login.ts:5` 的 `s.user.name`**：`.then(r=>r.json())` 不判断 `r.ok`，导致 401/500 返回的 JSON 错误体直接被当成正常响应使用，于是 `s.user` 是 undefined，抛出 TypeError；同时没有 catch，`root.innerHTML` 从未被赋值，最终白屏。**2.3.0 有 412 次，2.3.1 有 377 次**，两个版本都有，说明不是版本引入的，问题出在接口约定。
- **`ChunkLoadError: chunk 7`**（88 次，只在 11-01）：部署后，旧 tab 仍在请求已经删除的 hash 文件，动态 import 失败，同样导致白屏。这条才更像你说的“偶尔”。
- `RangeError` 出在 `cart.ts:41`，不在登录页，而且源码缺失。
- 骨架屏这两条路径一条都修不了：路径 1 会永远停在骨架屏上，路径 2 照样白屏。

已就地更新 `local/plans/login-whitescreen.md`：Hand over 改成“先交归因表 + 每条路径一个修前失败的测试”，Depth 换成按（版本×错误×次数）拆解，并加一条检验你“版本 bug”这一假设的 stretch，Range 补上部署缓存和 API 约定两个视角与红队，Declined 记下原来那句“先看崩溃日志”，并在 `## Tries` 增加了一行 2026-11-10 的否决记录。

还缺的材料（不会拿猜测填）：2.3.0 和 2.3.1 的部署与 chunk hash 记录、`/api/session` 401 和 500 的实际响应、`cart.ts`，以及 vitest 不在 devDependencies、也没有测试目录。

Ready 是 no，三条 Open 需要你定：①“偶尔”指的是 ChunkLoadError 还是 `s.user` 那条（我判是前者）；②修路径 2 若要动 index.html 缓存头或部署流程，算不算“改后端接口”；③后端能否把 user 缺失改成 401。定完之后，可以 `/define-goal` 以这份 plan 为源。