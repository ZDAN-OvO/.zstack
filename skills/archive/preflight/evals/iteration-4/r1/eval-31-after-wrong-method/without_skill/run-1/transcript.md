TOOL bash: {"command": "ls -la; echo ---; cat local/plans/login-whitescreen.md 2>/dev/null | head -100"}

TOOL find: {"pattern": "**/*.{json,md}", "limit": 40}

RESULT: total 192
drwxrwxr-x  5 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 63 root root 167936 11月 10 22:26 ..
drwxrwxr-x  3 zdan zdan   4096 11月 10 16:17 local
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 logs
-rw-rw-r--  1 zdan zdan    206 11月 10 16:17 package.json
-rw-rw-r--  1 zdan zdan    104 11月 10 16:17 README.md
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 src
---
# Plan: 登录页白屏不再出现

- Asked: 帮我修一下登录页偶尔白屏的 bug
- Stage: execute
- Date: 2026-11-08

## Requirement
Hand over: 登录页白屏不再出现，并有回归测试
Fallback: 只修当前复现的那一个白屏
Depth: 先看崩溃日志
Range: —
Judge: 回归测试通过 + 一周内崩溃日志该错误为 0
Needs: 崩溃日志
Declined: —

## Task
Purpose: 下周演示前登录稳定
Context: React 前端，登录依赖 /api/session
Materials: logs/crashes-2026-11.csv, src/login.ts
Boundaries: 不改后端接口
Done: 一个 PR，含回归测试

Ready: yes


RESULT: README.md
local/plans/login-whitescreen.md
package.json

TOOL bash: {"command": "cat README.md package.json; echo ---; ls -la src logs; echo ---; cat src/login.ts; echo ---; head -40 logs/*.csv; echo ---; wc -l logs/*.csv"}

RESULT: # acme-web

React + TypeScript 前端。`npm test` 跑 vitest。
Node 版本见 package.json engines。
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
---
logs:
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 5 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  373 11月 10 16:17 crashes-2026-11.csv

src:
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 5 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  441 11月 10 16:17 login.ts
---
export function mountLogin(root: HTMLElement) {
  console.log("mount login");
  const token = localStorage.getItem("token");
  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
    .then((r) => r.json())
    .then((s) => { console.log("session", s); root.innerHTML = renderForm(s.user.name); });
}

function renderForm(name: string) {
  console.log("render", name);
  return `<form><input value="${name}"/></form>`;
}
---
date,app_version,error,count
2026-11-01,2.3.0,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",412
2026-11-01,2.3.0,"ChunkLoadError: Loading chunk 7 failed",88
2026-11-03,2.3.1,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",377
2026-11-05,2.3.1,"RangeError: Maximum call stack size exceeded at cart.ts:41",19
---
5 logs/crashes-2026-11.csv


TOOL bash: {"command": "find local -type f | head -50; echo ---; ls -la local local/plans; echo ---; grep -rn \"name\" src logs | head -20"}

RESULT: local/plans/login-whitescreen.md
---
local:
total 12
drwxrwxr-x 3 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 5 zdan zdan 4096 11月 10 16:17 ..
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 plans

local/plans:
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 3 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  607 11月 10 16:17 login-whitescreen.md
---
src/login.ts:6:    .then((s) => { console.log("session", s); root.innerHTML = renderForm(s.user.name); });
src/login.ts:9:function renderForm(name: string) {
src/login.ts:10:  console.log("render", name);
src/login.ts:11:  return `<form><input value="${name}"/></form>`;
logs/crashes-2026-11.csv:2:2026-11-01,2.3.0,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",412
logs/crashes-2026-11.csv:4:2026-11-03,2.3.1,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",377


TOOL bash: {"command": "git status 2>&1 | head -5; ls node_modules 2>&1 | head -3; node -v; ls -a; find / -maxdepth 6 -name \"vitest\" -type d 2>/dev/null | head -3"}

RESULT: fatal: not a git repository (or any of the parent directories): .git
ls: cannot access 'node_modules': No such file or directory
v26.13.0
.
..
local
logs
package.json
README.md
src
/home/zdan/.local/share/vitest


TOOL bash: {"command": "ls /home/zdan/.local/share/vitest 2>/dev/null | head; timeout 10 npm view vitest version 2>&1 | tail -3"}

RESULT: 5.1.0


TOOL write: {"path": "src/login.ts", "content": "type SessionResponse = { user?: { name?: string } | null } | null;\n\nconst escapeHtml = (value: string) =>\n  value.replace(/[&<>\"']/g, (c) =>\n    ({ \"&\": \"&amp;\", \"<\": \"&lt;\", \">\": \"&gt;\", '\"': \"&quot;\", \"'\": \"&#39;\" }[c] as string),\n  );\n\nexport function mountLogin(root: HTMLElement) {\n  // Always render something usable first: a blank login form is a valid\n  // fallback for \"no session\", unlike a permanently empty root.\n  root.innerHTML = renderForm(\"\");\n\n  const token = localStorage.getItem(\"token\");\n  const headers: Record<string, string> = {};\n  if (token) headers.Authorization = `Bearer ${token}`;\n\n  fetch(\"/api/session\", { headers })\n    .then(async (r) => {\n      if (!r.ok) {\n        console.warn(\"session request failed\", r.status);\n        return;\n      }\n      const session = (await r.json().catch(() => null)) as SessionResponse;\n      const name = session?.user?.name;\n      if (typeof name === \"string\") root.innerHTML = renderForm(name);\n    })\n    .catch((err) => {\n      // Network errors must not leave the page blank.\n      console.warn(\"session request error\", err);\n    });\n}\n\nfunction renderForm(name: string) {\n  return `<form><input value=\"${escapeHtml(name)}\"/></form>`;\n}\n"}

TOOL write: {"path": "src/login.test.ts", "content": "import { afterEach, beforeEach, describe, expect, it, vi } from \"vitest\";\nimport { mountLogin } from \"./login\";\n\nconst fakeRoot = () => ({ innerHTML: \"\" }) as unknown as HTMLElement;\nconst flush = () => new Promise((resolve) => setTimeout(resolve, 0));\n\nconst respond = (ok: boolean, status: number, body: unknown) =>\n  vi.fn(async () => ({ ok, status, json: async () => body }));\n\ndescribe(\"mountLogin\", () => {\n  beforeEach(() => {\n    vi.stubGlobal(\"localStorage\", {\n      getItem: vi.fn(() => \"token-123\"),\n      setItem: vi.fn(),\n      removeItem: vi.fn(),\n    });\n    vi.spyOn(console, \"log\").mockImplementation(() => {});\n    vi.spyOn(console, \"warn\").mockImplementation(() => {});\n  });\n\n  afterEach(() => {\n    vi.unstubAllGlobals();\n    vi.restoreAllMocks();\n  });\n\n  it(\"renders the login form when /api/session returns 401\", async () => {\n    // Regression: this used to throw on `session.user.name`, leaving a white page.\n    vi.stubGlobal(\"fetch\", respond(false, 401, { error: \"unauthorized\" }));\n    const root = fakeRoot();\n\n    mountLogin(root);\n    await flush();\n\n    expect(root.innerHTML).toContain(\"<form\");\n  });\n\n  it(\"renders the login form when the session payload has no user\", async () => {\n    // Regression: the crash-log signature (reading 'name' of undefined).\n    vi.stubGlobal(\"fetch\", respond(true, 200, {}));\n    const root = fakeRoot();\n\n    expect(() => mountLogin(root)).not.toThrow();\n    await flush();\n\n    expect(root.innerHTML).toContain(\"<form\");\n  });\n\n  it(\"renders the login form when the request rejects\", async () => {\n    vi.stubGlobal(\"fetch\", vi.fn(async () => { throw new Error(\"offline\"); }));\n    const root = fakeRoot();\n\n    mountLogin(root);\n    await flush();\n\n    expect(root.innerHTML).toContain(\"<form\");\n  });\n\n  it(\"renders the user name when a session exists\", async () => {\n    vi.stubGlobal(\"fetch\", respond(true, 200, { user: { name: \"Ada\" } }));\n    const root = fakeRoot();\n\n    mountLogin(root);\n    await flush();\n\n    expect(root.innerHTML).toContain('value=\"Ada\"');\n  });\n\n  it(\"escapes the user name\", async () => {\n    vi.stubGlobal(\"fetch\", respond(true, 200, { user: { name: 'A\"B<script>' } }));\n    const root = fakeRoot();\n\n    mountLogin(root);\n    await flush();\n\n    expect(root.innerHTML).not.toContain(\"<script>\");\n    expect(root.innerHTML).toContain(\"&quot;\");\n  });\n\n  it(\"does not send a Bearer header when the token is missing\", async () => {\n    vi.stubGlobal(\"localStorage\", { getItem: vi.fn(() => null), setItem: vi.fn(), removeItem: vi.fn() });\n    const fetchMock = respond(true, 200, { user: { name: \"Ada\" } });\n    vi.stubGlobal(\"fetch\", fetchMock);\n\n    mountLogin(fakeRoot());\n    await flush();\n\n    expect(fetchMock.mock.calls[0][1]).toEqual({ headers: {} });\n  });\n});\n"}

RESULT: Successfully wrote to src/login.ts

RESULT: Successfully wrote to src/login.test.ts

TOOL bash: {"command": "cd /tmp/pf-31-without_skill-k1ve3urv && timeout 120 npm i -D vitest@^3 2>&1 | tail -5"}

RESULT: Run `npm audit` for details.
npm warn install-scripts 1 package has install scripts not yet covered by allowScripts:
npm warn install-scripts   esbuild@0.28.2 (postinstall: node install.js)
npm warn install-scripts
npm warn install-scripts Run `npm install-scripts ls` to review, or `npm install-scripts approve <pkg>` to allow.


TOOL bash: {"command": "cd /tmp/pf-31-without_skill-k1ve3urv && timeout 180 npx vitest run 2>&1 | tail -30"}

RESULT: 
 RUN  v3.2.7 /tmp/pf-31-without_skill-k1ve3urv

 ✓ src/login.test.ts (6 tests) 12ms

 Test Files  1 passed (1)
      Tests  6 passed (6)
   Start at  22:27:22
   Duration  230ms (transform 30ms, setup 0ms, collect 26ms, tests 12ms, environment 0ms, prepare 63ms)



TOOL bash: {"command": "cd /tmp && rm -rf ws-oldcheck && cp -r pf-31-without_skill-k1ve3urv ws-oldcheck && cd ws-oldcheck && git -C . status >/dev/null 2>&1; cat > src/login.ts <<'EOF'\nexport function mountLogin(root: HTMLElement) {\n  console.log(\"mount login\");\n  const token = localStorage.getItem(\"token\");\n  fetch(\"/api/session\", { headers: { Authorization: `Bearer ${token}` } })\n    .then((r) => r.json())\n    .then((s) => { console.log(\"session\", s); root.innerHTML = renderForm(s.user.name); });\n}\n\nfunction renderForm(name: string) {\n  console.log(\"render\", name);\n  return `<form><input value=\"${name}\"/></form>`;\n}\nEOF\ntimeout 120 npx vitest run 2>&1 | tail -25"}

RESULT:        |                                                      ^
     50|     const root = fakeRoot();
     51| 
 ❯ mockCall node_modules/@vitest/spy/dist/index.js:96:15
 ❯ spy node_modules/tinyspy/dist/index.js:47:80
 ❯ mountLogin src/login.ts:4:3
 ❯ src/login.test.ts:52:5
 ❯ node_modules/@vitest/runner/dist/chunk-hooks.js:155:11
 ❯ node_modules/@vitest/runner/dist/chunk-hooks.js:752:26
 ❯ node_modules/@vitest/runner/dist/chunk-hooks.js:1897:20
 ❯ runWithTimeout node_modules/@vitest/runner/dist/chunk-hooks.js:1863:10

This error originated in "src/login.test.ts" test file. It doesn't mean the error was thrown inside the file itself, but while it was running.
The latest test that might've caused the error is "renders the login form when the request rejects". It might mean one of the following:
- The error was thrown, while Vitest was running this test.
- If the error occurred after the test had been completed, this was the last documented test before it was thrown.
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯


 Test Files  1 failed (1)
      Tests  5 failed | 1 passed (6)
     Errors  3 errors
   Start at  22:27:26
   Duration  234ms (transform 28ms, setup 0ms, collect 24ms, tests 19ms, environment 0ms, prepare 53ms)



TOOL bash: {"command": "cd /tmp && rm -rf ws-oldcheck; cd pf-31-without_skill-k1ve3urv && cat package.json; ls -a"}

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
  },
  "devDependencies": {
    "vitest": "^3.2.7"
  }
}
.
..
local
logs
node_modules
package.json
package-lock.json
README.md
src


ASSISTANT: 问题不在骨架屏；真正原因就在 `logs/crashes-2026-11.csv` 中，执行时没有读取该文件。

## 真正原因

崩溃日志中占绝对多数（412 + 377 = 789 次）的错误是：

```
TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5
```

这对应 `src/login.ts` 第 6 行：

```ts
.then((s) => { console.log("session", s); root.innerHTML = renderForm(s.user.name); });
```

当 `/api/session` 返回 401 JSON，例如 `{"error":"unauthorized"}`，或者返回空对象时，`s.user` 实际上是 `undefined`，于是读取 `.name` 会直接抛出异常。这个异常发生在 promise 链中，导致：

1. `root.innerHTML = renderForm(...)` 永远不会执行，页面因此保持空白；
2. 代码没有 `r.ok` 判断，也没有 `.catch`，网络失败或非 2xx 响应会产生未处理的 rejection，表现同样是白屏；
3. token 不存在时还会发送 `Authorization: Bearer null`，更容易得到 401。

加载骨架屏会在请求发出前让页面不空白，但请求返回后仍然抛出异常，骨架屏之后照样白屏，所以“结果不行”。而且当前工作区的 `src/login.ts` 还是原始有 bug 的版本，没有骨架屏改动，估计那边改动没有同步过来。

## 已修

`src/login.ts`
- 先渲染空白登录表单，保证任何路径都有内容；
- 增加 `!r.ok` 判断：401 等直接视为无会话；
- 改用 `session?.user?.name`，并校验类型，不再假定 `user` 存在；
- 增加 `.catch` 处理网络失败；
- 没有 token 时不发 `Bearer null`；
- 对用户名做 HTML 转义，因为原来会直接拼进 `value="..."`。

`src/login.test.ts`（新增 6 个用例）
- 401 → 渲染表单，不留下白屏；
- 200 但 `{}`（崩溃日志签名）→ 不抛出异常、渲染表单；
- fetch 抛出异常 → 渲染表单；
- 正常会话 → 渲染用户名；
- 用户名转义；
- 无 token 时不发 Authorization 头。

`package.json` 加了 `vitest` devDependency。

## 验证

```
npm test  →  6 passed
```

我还用原始 `login.ts` 跑了一遍这套测试：5 个用例失败（含未处理 rejection），说明测试确实能拦住这个回归，不是只覆盖了正常路径。

## 计划本身的问题

计划里 `Depth: 先看崩溃日志`、`Materials: logs/crashes-2026-11.csv` 都写对了，但执行跳过了这一步，直接进入 UI 空态处理。另外 `Judge` 要求“一周内崩溃日志该错误为 0”，这只能在发布后验证；建议在 `Done` 里补上“无会话、空 payload、网络失败三种路径都不白屏”的可测条件，否则下次还会优先做骨架屏这类表面修法。