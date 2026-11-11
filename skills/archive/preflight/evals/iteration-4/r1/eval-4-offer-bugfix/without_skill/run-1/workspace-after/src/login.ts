type Session = { user?: { name?: string } | null } | null;

export function mountLogin(root: HTMLElement) {
  const token = localStorage.getItem("token");
  const headers: Record<string, string> = token
    ? { Authorization: `Bearer ${token}` }
    : {};

  fetch("/api/session", { headers })
    .then((r) => (r.ok ? (r.json() as Promise<Session>) : null))
    .then((session) => {
      const name = session?.user?.name;
      // No token / expired session / unexpected payload: fall back to an
      // empty login form instead of throwing and leaving a blank page.
      root.innerHTML = renderForm(typeof name === "string" ? name : "");
    })
    .catch(() => {
      // Network error or invalid JSON must not white-screen the page.
      root.innerHTML = renderForm("");
    });
}

function renderForm(name: string) {
  return `<form><input value="${escapeHtml(name)}"/></form>`;
}

function escapeHtml(value: string) {
  return value.replace(
    /[&<>"']/g,
    (ch) =>
      ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
      })[ch] as string,
  );
}
