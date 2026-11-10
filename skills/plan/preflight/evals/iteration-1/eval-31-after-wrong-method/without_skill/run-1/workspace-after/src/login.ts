// 白屏根因：/api/session 的响应体不保证有 user.name。
// 401/204/代理 HTML 错误页/瞬时空响应都会让 s.user.name 抛 TypeError，
// 异常发生在 .then 里且没有 catch → renderForm 永远不执行，root.innerHTML 一直是空的（白屏）。
// 所以这里必须校验 token、status 和 payload，并且必须有失败分支。

type Root = { innerHTML: string };

export function mountLogin(root: Root) {
  const token = localStorage.getItem("token");
  if (!token) {
    root.innerHTML = renderForm("");
    return;
  }

  return fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
    .then(async (r) => {
      if (r.status === 401 || r.status === 403) {
        localStorage.removeItem("token");
        return { name: "" };
      }
      if (!r.ok) throw new Error(`session request failed: HTTP ${r.status}`);
      const session = await r.json().catch(() => null);
      const name = session?.user?.name;
      if (typeof name !== "string" || name === "") {
        throw new Error("session payload missing user.name");
      }
      return { name };
    })
    .then(({ name }) => {
      root.innerHTML = renderForm(name);
    })
    .catch((err: unknown) => {
      console.error("[login] mount failed", err);
      root.innerHTML = renderRetry();
    });
}

function renderForm(name: string) {
  return `<form><input name="user" value="${escapeAttr(name)}"/></form>`;
}

function renderRetry() {
  return `<div role="alert">会话加载失败，<button type="button" data-action="retry">重试</button></div>`;
}

function escapeAttr(value: string) {
  return value
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}
