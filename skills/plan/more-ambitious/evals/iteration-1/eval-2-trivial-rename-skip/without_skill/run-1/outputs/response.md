已改：`src/login.ts:2` 的 `mountLogin` → `renderLogin`。

- 全仓库 grep 只有这一处定义，没有其他文件引用（`docs/GLOSSARY.md` 只提到 login 状态，与函数名无关），所以没有连带改动。
- 未跑类型检查：`package.json` 里只有 `tsc` 脚本，但仓库没有 `node_modules`，本机 npx 取到的不是编译器（提示 "This is not the tsc command you are looking for"）。需要我装依赖后跑一次 `npm run build` 吗？
- 一个小提示：这个函数是 `async` 且要等 `/api/session` 返回后才写 `innerHTML`，语义上更接近「加载后渲染/挂载」。如果以后想区分「立即挂载」和「异步渲染」，现在这个名字倒是留了空间；要保持 `renderLogin` 也可以。
