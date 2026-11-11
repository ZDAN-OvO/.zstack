export function mountLogin(root: HTMLElement) {
  console.log("mount login");
  const token = localStorage.getItem("token");
  if (!token) {
    root.innerHTML = renderForm("");
    return;
  }
  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
    .then((r) => {
      if (!r.ok) throw new Error(`session request failed: ${r.status}`);
      return r.json();
    })
    .then((s) => {
      console.log("session", s);
      root.innerHTML = renderForm(s?.user?.name ?? "");
    })
    .catch((err) => {
      console.error("mountLogin failed", err);
      localStorage.removeItem("token");
      root.innerHTML = renderForm("");
    });
}

function renderForm(name: string) {
  console.log("render", name);
  return `<form><input value="${name}"/></form>`;
}
