已完成重命名（rename）：`src/login.ts:1` 中 `mountLogin` → `renderLogin`。

- 仓库内只有这一处引用，没有其他文件或测试需要同步。
- 函数内 `console.log("mount login")` 是日志文案，不属于标识符，未改动；如需一并改成 `render login` 请说一声。
- 未运行 `npm test`：当前目录没有 `node_modules`，也没有测试文件。