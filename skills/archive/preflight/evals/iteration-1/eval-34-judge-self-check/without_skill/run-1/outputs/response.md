修好了，自己验过了。

**最多的崩溃**：`TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5` —— 412 + 377 = 789 次，占日志绝大多数（第二位 ChunkLoadError 只有 88 次）。

**原因**：`s.user.name` 没有防护。`/api/session` 返回 401 时 body 是 `{error: ...}`，空 body 时 `r.json()` 直接抛错，两种情况 `s.user` 都是 undefined。

**改动** `src/login.ts`：
- 非 2xx 不再解析 body，直接按会话失效处理
- `s?.user?.name` 判空，缺失则清 token + 渲染「登录已过期」
- 补 `.catch()`，兜住 JSON 解析失败 / 网络错误

**自查**（Node 26 原生跑 TS，stub 掉 localStorage/fetch + 假 DOM，5 个场景）：

```
ok | 401 empty body    | html=登录已过期 | token=已清除
ok | 401 error json    | html=登录已过期 | token=已清除
ok | 200 without user  | html=登录已过期 | token=已清除
ok | 200 null body     | html=登录已过期 | token=已清除
ok | 200 valid user    | html=<form><input value="ada"/></form> | token=保留
```

正常登录路径行为不变；原来必崩的 4 条路径都不再抛异常，且不会留坏 token。

两点说明：`npm test` 跑不了（仓库里没有测试文件，也没装 node_modules），所以上面是临时脚本验证，没往仓库加测试；崩溃日志里的 `cart.ts:41`（RangeError，19 次）是另一个问题，本次没动。