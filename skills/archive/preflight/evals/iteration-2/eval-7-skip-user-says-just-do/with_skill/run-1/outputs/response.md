已删除 `src/login.ts` 中全部 3 处 `console.log`：

- `mountLogin` 里的 `console.log("mount login")`
- `.then` 回调里的 `console.log("session", s)`（保留 `root.innerHTML` 赋值）
- `renderForm` 里的 `console.log("render", name)`

其余逻辑未改动。