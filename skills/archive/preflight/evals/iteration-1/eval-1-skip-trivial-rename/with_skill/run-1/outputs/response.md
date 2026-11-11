已完成 `src/login.ts` 第 1 行的重命名：

- `mountLogin` → `renderLogin`

检查结果：
- 全仓库（排除 `logs/`）已无 `mountLogin` 残留引用，无需同步修改调用方。
- `renderForm`、内部 `console.log("mount login")` 等日志文案未改动 —— 如果你也想让日志字符串跟着改（`"mount login"` → `"render login"`），告诉我一声即可。