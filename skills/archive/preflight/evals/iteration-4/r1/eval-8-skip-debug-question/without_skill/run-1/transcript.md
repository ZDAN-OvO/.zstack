TOOL bash: {"command": "ls -la /tmp/pf-8-without_skill-e0eaaz7s"}

TOOL find: {"pattern": "**/login.ts"}

RESULT: total 188
drwxrwxr-x  4 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 63 root root 167936 11月 10 22:22 ..
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 logs
-rw-rw-r--  1 zdan zdan    206 11月 10 16:17 package.json
-rw-rw-r--  1 zdan zdan    104 11月 10 16:17 README.md
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 src


RESULT: src/login.ts

TOOL read: {"path": "/tmp/pf-8-without_skill-e0eaaz7s/src/login.ts"}

TOOL bash: {"command": "cd /tmp/pf-8-without_skill-e0eaaz7s && ls -la src logs && cat package.json README.md"}

RESULT: export function mountLogin(root: HTMLElement) {
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


RESULT: logs:
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  373 11月 10 16:17 crashes-2026-11.csv

src:
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  441 11月 10 16:17 login.ts
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
# acme-web

React + TypeScript 前端。`npm test` 跑 vitest。
Node 版本见 package.json engines。


TOOL read: {"path": "/tmp/pf-8-without_skill-e0eaaz7s/logs/crashes-2026-11.csv"}

RESULT: date,app_version,error,count
2026-11-01,2.3.0,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",412
2026-11-01,2.3.0,"ChunkLoadError: Loading chunk 7 failed",88
2026-11-03,2.3.1,"TypeError: Cannot read properties of undefined (reading 'name') at login.ts:5",377
2026-11-05,2.3.1,"RangeError: Maximum call stack size exceeded at cart.ts:41",19


TOOL bash: {"command": "cd /tmp/pf-8-without_skill-e0eaaz7s && cat -n src/login.ts"}

RESULT:      1	export function mountLogin(root: HTMLElement) {
     2	  console.log("mount login");
     3	  const token = localStorage.getItem("token");
     4	  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
     5	    .then((r) => r.json())
     6	    .then((s) => { console.log("session", s); root.innerHTML = renderForm(s.user.name); });
     7	}
     8	
     9	function renderForm(name: string) {
    10	  console.log("render", name);
    11	  return `<form><input value="${name}"/></form>`;
    12	}


ASSISTANT: ## 崩溃点

`src/login.ts` 第 5–6 行：

```ts
5   .then((r) => r.json())
6   .then((s) => { console.log("session", s); root.innerHTML = renderForm(s.user.name); });
```

报错文案是 **reading 'name'**，说明 `s` 本身是有值的，**是 `s.user` 为 `undefined`**，于是 `undefined.name` 抛错。（如果响应体为空，报文会是 "reading 'user'"。）线上报的行号是 5 而不是 6，是打包／source map 把链式调用的行号归到了上一行，位置就是这句。

## 为什么 `s.user` 会是 undefined

三条叠加的原因：

1. **第 3 行 `localStorage.getItem("token")` 很可能返回 `null`**（未登录、被清缓存、隐私模式）。于是第 4 行发出的是 `Authorization: Bearer null`。
2. 服务端对非法 token 返回 401，body 类似 `{"error":"unauthorized"}`。**`fetch` 不会因为 4xx/5xx 而 reject，`r.json()` 照样成功解析**，所以第 6 行的 `s` 是一个错误对象，`s.user` 不存在。
3. **没有 `r.ok` 检查、也没有 `.catch()`、也没有 `?.`**，所以第一个真实失败直接变成线上 TypeError。

这也是 `logs/crashes-2026-11.csv` 里 2.3.0/2.3.1 每天 400 次左右、跨版本持续出现的原因——它不是偶发，而是「未登录用户进入登录页」这条必经路径。

顺带一提：TypeScript 没能在编译期拦住这里，是因为 `Response.json()` 返回 `Promise<any>`，`s.user.name` 一路静默通过类型检查。

## 建议的修法

```ts
export function mountLogin(root: HTMLElement) {
  const token = localStorage.getItem("token");
  if (!token) return showLoginForm(root);          // 没有 token 就别请求

  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
    .then(async (r) => {
      if (r.status === 401) { showLoginForm(root); return null; }
      if (!r.ok) throw new Error(`session failed: ${r.status}`);
      return r.json() as Promise<{ user?: { name?: string } }>;
    })
    .then((s) => {
      if (!s?.user?.name) return showLoginForm(root);
      root.innerHTML = renderForm(s.user.name);
    })
    .catch((err) => { console.error(err); showLoginForm(root); });
}
```

要我直接改到文件里吗？另外目前 `src/` 下只有 `login.ts`，没有对应测试，`npm test` 里也没有覆盖这条 401 分支。