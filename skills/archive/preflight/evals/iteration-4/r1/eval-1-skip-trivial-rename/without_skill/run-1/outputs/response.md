已把 `src/login.ts` 中的 `mountLogin` 改为 `renderLogin`。

- 定义位置：`src/login.ts:1`
- 全仓库已无其他 `mountLogin` 引用（仅这一处），无需同步修改调用方

注意：该函数是 `export` 的，如果有仓库外的代码导入它，需要一并更新。