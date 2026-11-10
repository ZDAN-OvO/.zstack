export function mountLogin(root: HTMLElement) {
  console.log("mount login");
  const token = localStorage.getItem("token");
  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
    .then((r) => (r.ok ? r.json() : null))
    .then((s) => {
      // 会话失效（401/空 body）时 s 可能是 null 或错误对象，s.user 不存在
      const name = s?.user?.name;
      if (!name) {
        localStorage.removeItem("token");
        root.innerHTML = renderSessionExpired();
        return;
      }
      root.innerHTML = renderForm(name);
    })
    .catch(() => { root.innerHTML = renderSessionExpired(); });
}

function renderSessionExpired() {
  return `<form><p>登录已过期，请重新登录</p></form>`;
}

function renderForm(name: string) {
  console.log("render", name);
  return `<form><input value="${name}"/></form>`;
}
