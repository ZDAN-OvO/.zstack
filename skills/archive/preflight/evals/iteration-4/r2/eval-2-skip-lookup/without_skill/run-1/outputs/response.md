**Node 要求：`>=20`**

依据：
- `package.json` → `"engines": { "node": ">=20" }`
- `README.md` 第 4 行也指向这里：「Node 版本见 package.json engines」

补充：项目里没有 `.nvmrc`、`.node-version`、`.tool-versions` 或 CI 配置，所以没有更精确的版本锁定；`engines` 只是声明，若想让 npm 强制校验，需要 `engine-strict=true` 或加锁文件。