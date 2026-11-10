TOOL ls: {"path": "/tmp/pf-2-without_skill-lyzvia5m"}

TOOL find: {"pattern": "**/{package.json,.nvmrc,.node-version,.tool-versions,*.md}", "path": "/tmp/pf-2-without_skill-lyzvia5m"}

RESULT: logs/
package.json
README.md
src/

RESULT: README.md
package.json

TOOL read: {"path": "/tmp/pf-2-without_skill-lyzvia5m/package.json"}

TOOL read: {"path": "/tmp/pf-2-without_skill-lyzvia5m/README.md"}

RESULT: {
  "name": "acme-web",
  "version": "2.3.1",
  "engines": {
    "node": ">=20"
  },
  "scripts": {
    "test": "vitest run",
    "build": "vite build"
  },
  "dependencies": {
    "react": "^19.2.0"
  }
}


RESULT: # acme-web

React + TypeScript 前端。`npm test` 跑 vitest。
Node 版本见 package.json engines。


ASSISTANT: **Node 版本要求：`>=20`**

来源：`/tmp/pf-2-without_skill-lyzvia5m/package.json` 中的 `engines.node` 字段：

```json
"engines": {
  "node": ">=20"
}
```

README 里没有写具体版本号，只说明"Node 版本见 package.json engines"。项目中也没有 `.nvmrc` 或 `.node-version` 文件。