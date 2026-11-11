export function mountLogin(root: HTMLElement) {
  console.log("mount login");
  const token = localStorage.getItem("token");
  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
    .then((r) => {
      if (!r.ok) throw new Error(`session request failed: ${r.status}`);
      return r.json();
    })
    .then((s) => {
      // 未登录 / 会话失效时接口不会返回 user，不能直接读 s.user.name
      const name = s?.user?.name;
      if (!name) {
        root.innerHTML = renderLoginPrompt();
        return;
      }
      root.innerHTML = renderForm(name);
    })
    .catch(() => {
      root.innerHTML = renderLoginPrompt();
    });
}

function renderLoginPrompt() {
  return `<form><input name="username"/><input type="password" name="password"/></form>`;
}

function renderForm(name: string) {
  console.log("render", name);
  return `<form><input value="${name}"/></form>`;
}
