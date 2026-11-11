**`>=20`**（Node 20 或更高）

出处：`package.json` 的 `engines` 字段：

```json
"engines": {
  "node": ">=20"
}
```

`README.md` 也指明「Node 版本见 package.json engines」。注意这不是硬性限制——`engines` 只是一个声明，默认情况下 npm 只会警告不会阻止安装，除非项目启用了 `engine-strict`。