改名完成。

- `src/login.ts:1`：`mountLogin` → `renderLogin`
- 全仓库仅此一处引用，无其他调用点需要同步

未写 plan：按 preflight 的 Enter 条款，比起一份 plan 更便宜的请求（改名、查文件）照原样执行。

如果你其实想动的是更上游的东西（比如 `mountXxx` 这类命名在一个模块里统一成 `renderXxx`，或者有外部消费者通过 `import { mountLogin }` 引用、rename 属于破坏性变更），告诉我，那才需要一份 plan。