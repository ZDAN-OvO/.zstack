项目里没有装 `typescript`（无 `node_modules`），所以没法跑类型检查；逻辑上已逐行核对。

## 改动 `src/login.ts`

1. **消除白屏根因**：先同步渲染空表单，后续任何失败都不会让 `root` 保持空白。

2. **`s.user.name` 崩溃**（日志里那 789 次）：
   - `res.ok` 为 false 时不再解析 body，401/403 视为未登录，直接停在空表单；
   - 用 `session?.user?.name ?? ""` 兜底；
   - `res.json()` 解析失败（比如返回 HTML 错误页）也降级为 `null`。

3. **`token` 为 `null`**：不再发 `Bearer null` 的请求，直接渲染空表单。

4. **网络异常**：`try/catch` 包住，只 `console.error`，不再产生未处理的 Promise rejection。

5. **竞态**：`WeakMap` 记录每个 `root` 的 mount 序号，慢的旧请求回来时不会覆盖新内容。

6. **转义**：`name` 会被插进 `value="..."`，加了属性转义，避免名字里带 `"` 把标签结构打断（顺带堵了 XSS）。

7. 去掉了调试用的 `console.log("mount login"/"session"/"render")`。

## 还需要你确认的两点

- `mountLogin` 现在是 `async`，返回类型从 `void` 变为 `Promise<void>`。忽略返回值的调用方无影响，但如果有地方 `await` 或检查返回类型需要注意。
- 崩溃日志里的 `ChunkLoadError`（88 次）是构建产物加载失败，跟这个文件无关，属于发布/缓存问题，需要另外看。