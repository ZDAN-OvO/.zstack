项目（`/tmp/pf-2-with_skill-6299k4qg`）要求 **Node.js >= 20**。

来源：`package.json` 中的 `engines` 字段：

```json
"engines": {
  "node": ">=20"
}
```

README 也写明「Node 版本见 package.json engines」，但没有指定更精确的版本，也没有 `.nvmrc` 或 `.node-version` 文件。注意 `engines` 默认只是声明，npm 不会强制拦截（除非开启 `engine-strict`）；实际跑起来可能受 React 19 / Vite / vitest 的隐式要求影响，建议用 Node 20 LTS 或更高。