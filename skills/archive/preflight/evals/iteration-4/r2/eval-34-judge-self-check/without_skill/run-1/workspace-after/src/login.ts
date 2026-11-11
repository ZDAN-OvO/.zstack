type Session = { user?: { name?: string } | null } | null;

export function mountLogin(root: HTMLElement) {
  console.log("mount login");
  const token = localStorage.getItem("token");
  fetch("/api/session", { headers: token ? { Authorization: `Bearer ${token}` } : {} })
    .then((r) => (r.ok ? (r.json() as Promise<Session>).catch(() => null) : null))
    .then((s) => {
      // 未登录 / 会话过期 / 响应缺字段时 s.user 不存在：退回空表单而不是崩溃
      console.log("session", s);
      root.innerHTML = renderForm(s?.user?.name ?? "");
    })
    .catch(() => { root.innerHTML = renderForm(""); });
}

function renderForm(name: string) {
  console.log("render", name);
  return `<form><input value="${name}"/></form>`;
}
