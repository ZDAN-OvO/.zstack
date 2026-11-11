已改名：`src/login.ts:1` 的 `mountLogin` → `renderLogin`。

几点说明：
- 全仓库只有这一处引用 `mountLogin`，无 import/调用点需要同步。
- 函数体里还有一行 `console.log("mount login")`（字符串，不是标识符），保持原样；要一起改成 `"render login"` 说一声。
- 文件里已有 `renderForm`，改名后 `renderLogin` / `renderForm` 命名风格一致了。