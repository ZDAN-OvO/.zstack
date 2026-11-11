`src/login.ts` 已改完，3 处 `console.log` 全部删除：

- 第 2 行 `console.log("mount login");` — 整句删除
- 第 6 行 `.then` 回调里的 `console.log("session", s);` — 只删该调用，保留 `root.innerHTML = renderForm(...)`（回调体拆成多行以保持可读）
- 原第 10 行 `console.log("render", name);` — 整句删除

`grep console` 已无匹配。