export function mountLogin(root: HTMLElement) {
  console.log("mount login");
  const token = localStorage.getItem("token");
  if (!token) {
    root.innerHTML = renderLogin();
    return;
  }
  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
    .then((r) => {
      if (!r.ok) throw new Error(`session request failed: ${r.status}`);
      return r.json();
    })
    .then((s) => {
      console.log("session", s);
      if (!s?.user?.name) {
        localStorage.removeItem("token");
        root.innerHTML = renderLogin();
        return;
      }
      root.innerHTML = renderForm(s.user.name);
    })
    .catch((err) => {
      console.error("mountLogin failed", err);
      root.innerHTML = renderLogin();
    });
}

function renderLogin() {
  return `<form><input name="username" placeholder="用户名"/><button type="submit">登录</button></form>`;
}

function renderForm(name: string) {
  console.log("render", name);
  return `<form><input value="${name}"/></form>`;
}
