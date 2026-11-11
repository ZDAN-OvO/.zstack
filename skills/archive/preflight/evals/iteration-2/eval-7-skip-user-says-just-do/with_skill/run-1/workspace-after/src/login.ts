export function mountLogin(root: HTMLElement) {
  const token = localStorage.getItem("token");
  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
    .then((r) => r.json())
    .then((s) => { root.innerHTML = renderForm(s.user.name); });
}

function renderForm(name: string) {
  return `<form><input value="${name}"/></form>`;
}
