已改好 `src/login.ts:1`：

```ts
export function renderLogin(root: HTMLElement) {
```

仓库中 `mountLogin` 没有其他引用。注意函数内的 `console.log("mount login")` 是日志文本，非函数名，保持不变；如也想改可告诉我。