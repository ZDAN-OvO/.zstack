改好了。

`src/login.ts:2`：`mountLogin` → `renderLogin`。全仓只有这一处（没有调用方、没有 re-export），改完不留旧名字。

```ts
export async function renderLogin(root: HTMLElement) {
```

没跑 `/more-ambitious`：这种改名重做一遍比访谈便宜，技能里也写明该跳过。如果改名其实是想说"它的职责变了"（现在它是先取 session 再决定渲染什么），那再单独说一声，我们再走一遍。
