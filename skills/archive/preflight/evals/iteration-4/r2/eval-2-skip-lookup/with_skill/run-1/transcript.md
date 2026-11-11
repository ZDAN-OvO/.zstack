TOOL bash: {"command": "cd /tmp/pf-2-with_skill-9_5n4697 && ls -a && echo \"---\" && cat package.json 2>/dev/null | head -60"}

TOOL bash: {"command": "cd /tmp/pf-2-with_skill-9_5n4697 && for f in .nvmrc .node-version .tool-versions package.json; do echo \"== $f ==\"; cat \"$f\" 2>/dev/null | head -40; done"}

RESULT: .
..
logs
package.json
README.md
src
---
{
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


RESULT: == .nvmrc ==
== .node-version ==
== .tool-versions ==
== package.json ==
{
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


TOOL bash: {"command": "cd /tmp/pf-2-with_skill-9_5n4697 && cat README.md && echo \"=== logs ===\" && ls logs && echo \"=== src ===\" && ls src"}

RESULT: # acme-web

React + TypeScript 前端。`npm test` 跑 vitest。
Node 版本见 package.json engines。
=== logs ===
crashes-2026-11.csv
=== src ===
login.ts


TOOL bash: {"command": "cd /tmp/pf-2-with_skill-9_5n4697 && head -5 logs/crashes-2026-11.csv"}

RESULT: date,app_version,error,count
2026-11-01,2.3.0,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",412
2026-11-01,2.3.0,"ChunkLoadError: Loading chunk 7 failed",88
2026-11-03,2.3.1,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",377
2026-11-05,2.3.1,"RangeError: Maximum call stack size exceeded at cart.ts:41",19


ASSISTANT: `>=20`，来自 `package.json` 的 `engines` 字段。

```
/tmp/pf-2-with_skill-9_5n4697/package.json:4
  "engines": { "node": ">=20" }
```

README 也指向这一处，没有别的来源。

另外几点（查过，都是事实）：

- **没有版本固定文件**：`.nvmrc`、`.node-version`、`.tool-versions` 都不存在，所以 `>=20` 是唯一的约束，没有精确到具体小版本。
- **`>=20` 是开区间**：Node 20 / 22 / 24 都算「满足」，CI 和本地各自装什么谁也说不准。如果崩溃日志里出现过只在某个 Node 大版本上才复现的问题，这个约束挡不住。
- **`engines` 默认只是建议**：不加 `engine-strict=true`（`.npmrc`）或 `packageManager` 字段的话，npm 只会警告，不会拒绝安装。

如果你要的是「团队应该在哪个版本上跑」，现在这个仓库回答不了——需要新增一个固定文件（比如 `.nvmrc` 写 `20`）。这属于查不到的东西，我没有替你猜。

要不要顺手把版本钉下来？