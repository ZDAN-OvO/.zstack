type SessionResponse = {
  user?: { name?: unknown };
};

export function mountLogin(root: HTMLElement) {
  const token = localStorage.getItem("token");

  // 未登录时不要发一个 "Bearer null" 的请求，直接渲染空表单。
  if (!token) {
    root.innerHTML = renderForm("");
    return;
  }

  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
    .then((r) => {
      if (!r.ok) {
        throw new Error(`session request failed: ${r.status}`);
      }
      return r.json() as Promise<SessionResponse | null>;
    })
    .then((session) => {
      // session/user/name 都可能缺失（token 过期时后端返回空对象）。
      const name = session?.user?.name;
      root.innerHTML = renderForm(typeof name === "string" ? name : "");
    })
    .catch((err) => {
      // 网络错误、非 JSON 响应等也不能让页面停在白屏。
      console.error("failed to load session", err);
      root.innerHTML = renderForm("");
    });
}

function renderForm(name: string) {
  return `<form><input value="${escapeHtml(name)}"/></form>`;
}

function escapeHtml(value: string) {
  return value.replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]!,
  );
}
