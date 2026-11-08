已改好：[login.ts:2](src/login.ts) 的 `mountLogin` 现在是 `renderLogin`。

全仓库只有这一处出现 `mountLogin`，`src/` 里也没有其他文件 import 它，所以没有别的地方需要跟着改。`docs/GLOSSARY.md` 里没提到这两个名字，不用同步。

一点说明：`package.json` 的 build 是 `tsc`，但项目里没装 typescript，`npx tsc` 只能跑到占位提示，所以我没法用类型检查验证这次改名，只做了全文搜索确认没有遗漏的引用。

另外这个名字现在和函数实际做的事更贴了——它每次调用都会重新请求 `/api/session` 再重写 `root.innerHTML`，是渲染而不是挂载。如果后面真要拆成「挂载一次 + 后续更新」，那才是 `mount` 语义。
