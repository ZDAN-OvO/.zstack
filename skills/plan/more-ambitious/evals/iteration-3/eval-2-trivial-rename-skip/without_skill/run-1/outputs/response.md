改好了：`src/login.ts` 里的 `mountLogin` 已改成 `renderLogin`。

- 全仓库只有这一处引用（就是这个定义本身），没有其他调用点或导入需要跟着改；`docs/GLOSSARY.md` 里也没有提到这个名字。
- 没能跑类型检查：项目没装 `typescript`（`npx tsc` 提示需要先安装），所以这次只做了文本层面的确认。

需要的话我可以帮你装 TypeScript，或者继续看看别的命名（比如这个函数叫 "render" 但其实还负责请求 `/api/session`）。
