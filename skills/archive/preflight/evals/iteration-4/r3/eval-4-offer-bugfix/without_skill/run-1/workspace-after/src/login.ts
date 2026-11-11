export function mountLogin(root: HTMLElement) {
  console.log("mount login");
  const token = localStorage.getItem("token");

  // 无 token 时直接渲染空表单，避免发起必然失败的请求
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
      // 会话无效/过期时接口可能返回缺少 user 的响应，兜底为空白表单
      root.innerHTML = renderForm(s?.user?.name ?? "");
    })
    .catch((err) => {
      console.error("load session failed", err);
      localStorage.removeItem("token");
      root.innerHTML = renderForm("");
    });
}

function renderForm(name: string) {
  console.log("render", name);
  return `<form><input value="${name}"/></form>`;
}
