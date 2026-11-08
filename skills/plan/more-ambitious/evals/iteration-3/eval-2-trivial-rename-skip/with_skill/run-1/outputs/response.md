这个不用走 more-ambitious。

`src/login.ts:2` 里只有一处 `mountLogin`，全仓库没有别的引用，改名的返工成本比访谈一圈低得多。按技能的判断，这种情况建议整套跳过（higher / deeper / wider 都不跑），你直接把任务当普通请求发过来就行。

需要我改的话说一声，我就把这一处 `mountLogin` 改成 `renderLogin`。
