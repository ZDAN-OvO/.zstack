type Session = { user?: { name?: string } };

export function mountLogin(root: HTMLElement) {
  console.log("mount login");
  const token = localStorage.getItem("token");
  if (!token) {
    // 未登录：直接展示空白登录表单，避免带着无效 token 请求 session
    root.innerHTML = renderForm("");
    return;
  }

  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
    .then((r) => {
      if (!r.ok) throw new Error(`session request failed: ${r.status}`);
      return r.json() as Promise<Session>;
    })
    .then((s) => {
      console.log("session", s);
      // session 过期/无效时后端不返回 user，此时回退到空白登录表单
      root.innerHTML = renderForm(s?.user?.name ?? "");
    })
    .catch((err) => {
      console.error("mount login failed", err);
      root.innerHTML = renderForm("");
    });
}

function renderForm(name: string) {
  console.log("render", name);
  return `<form><input value="${name}"/></form>`;
}
