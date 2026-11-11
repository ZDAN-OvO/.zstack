**Node ≥ 20**（即 Node 20 或更高版本）。

来源：`package.json` 的 `engines` 字段：

```json
"engines": {
  "node": ">=20"
}
```

补充：项目中没有 `.nvmrc` 或 `.node-version` 文件，README 也说明「Node 版本见 package.json engines」，所以 `>=20` 是唯一的版本要求。

注：当前你环境里运行的是 Node v26.13.0（来自 nvm），满足该要求。