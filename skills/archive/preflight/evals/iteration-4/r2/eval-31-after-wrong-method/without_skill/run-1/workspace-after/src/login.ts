type SessionResponse = { user?: { name?: string } };

export function mountLogin(root: HTMLElement) {
  console.log("mount login");
  const token = localStorage.getItem("token");
  fetch("/api/session", { headers: token ? { Authorization: `Bearer ${token}` } : {} })
    .then(async (r) => {
      if (!r.ok) throw new Error(`/api/session returned ${r.status}`);
      return (await r.json()) as SessionResponse;
    })
    .then((s) => {
      root.innerHTML = renderForm(s.user?.name ?? "");
    })
    .catch((err) => {
      console.error("mountLogin failed", err);
      root.innerHTML = renderForm("");
    });
}

function renderForm(name: string) {
  console.log("render", name);
  return `<form><input value="${name}"/></form>`;
}
