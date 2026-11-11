type SessionResponse = { user?: { name?: string } | null } | null;

const escapeHtml = (value: string) =>
  value.replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c] as string),
  );

export function mountLogin(root: HTMLElement) {
  // Always render something usable first: a blank login form is a valid
  // fallback for "no session", unlike a permanently empty root.
  root.innerHTML = renderForm("");

  const token = localStorage.getItem("token");
  const headers: Record<string, string> = {};
  if (token) headers.Authorization = `Bearer ${token}`;

  fetch("/api/session", { headers })
    .then(async (r) => {
      if (!r.ok) {
        console.warn("session request failed", r.status);
        return;
      }
      const session = (await r.json().catch(() => null)) as SessionResponse;
      const name = session?.user?.name;
      if (typeof name === "string") root.innerHTML = renderForm(name);
    })
    .catch((err) => {
      // Network errors must not leave the page blank.
      console.warn("session request error", err);
    });
}

function renderForm(name: string) {
  return `<form><input value="${escapeHtml(name)}"/></form>`;
}
