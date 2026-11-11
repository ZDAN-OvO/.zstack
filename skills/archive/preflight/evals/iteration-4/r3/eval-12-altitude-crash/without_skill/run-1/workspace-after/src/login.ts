type Session = { user?: { name?: string } };

export function mountLogin(root: HTMLElement) {
  console.log("mount login");
  const token = localStorage.getItem("token");
  if (!token) {
    root.innerHTML = renderForm("");
    return;
  }
  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
    .then((r) => (r.ok ? (r.json() as Promise<Session>) : null))
    .then((s) => { root.innerHTML = renderForm(s?.user?.name ?? ""); })
    .catch((e) => {
      console.error("failed to load session", e);
      root.innerHTML = renderForm("");
    });
}

function renderForm(name: string) {
  console.log("render", name);
  return `<form><input value="${name}"/></form>`;
}
