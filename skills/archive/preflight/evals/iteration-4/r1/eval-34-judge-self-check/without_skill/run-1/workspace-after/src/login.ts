type Session = { user?: { name?: string } };

export function mountLogin(root: HTMLElement) {
  const token = localStorage.getItem("token");
  if (!token) {
    root.innerHTML = renderLoginPrompt();
    return;
  }
  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
    .then((r) => {
      if (!r.ok) return null;
      return r.json() as Promise<Session>;
    })
    .then((s) => {
      const name = s?.user?.name;
      root.innerHTML = name ? renderForm(name) : renderLoginPrompt();
    })
    .catch((err) => {
      console.error("failed to load session", err);
      root.innerHTML = renderLoginPrompt();
    });
}

function renderForm(name: string) {
  return `<form><input value="${name}"/></form>`;
}

function renderLoginPrompt() {
  return `<a href="/login">登录</a>`;
}
