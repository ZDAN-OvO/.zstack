**Node 要求：`>=20`**

依据：`package.json` 的 `engines` 字段（README 也指向这一处）：

```json
"engines": { "node": ">=20" }
```

项目中没有任何额外约束来源——没有 `.nvmrc`、`.node-version`、Dockerfile 或 CI 配置覆盖这个声明。所以 `>=20` 是唯一权威版本约束（React 19 也要求 Node 18+，与之一致）。

顺带两点观察（与问题无关，未展开）：
- `src/login.ts:5` 的空指针崩溃（`s.user.name`）与 `logs/crashes-2026-11.csv` 中 2.3.1 版本 377 次崩溃吻合，属线上真实故障，值得单独处理。
- `engines` 只是声明，npm 默认不强制，缺 `engine-strict` 时低版本 Node 仍会装上并可能在运行时炸。

这次是查找类问题，直接答即可，未生成 preflight 计划。若你想把上面的崩溃线索推进成一次有边界的排查，可以 `/preflight` 走一遍。