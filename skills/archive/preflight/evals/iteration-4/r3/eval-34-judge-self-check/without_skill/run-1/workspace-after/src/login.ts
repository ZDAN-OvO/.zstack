export function mountLogin(root: HTMLElement) {
  console.log("mount login");
  const token = localStorage.getItem("token");
  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
    .then((r) => (r.ok ? r.json() : null))
    .then((s) => {
      console.log("session", s);
      // 未登录 / token 过期时接口可能返回 401 或没有 user 字段：
      // 之前这里直接读 s.user.name 会抛 TypeError（线上最多的崩溃）。
      root.innerHTML = renderForm(s?.user?.name ?? "");
    })
    .catch((err) => { console.error("session load failed", err); root.innerHTML = renderForm(""); });
}

function renderForm(name: string) {
  console.log("render", name);
  return `<form><input value="${name}"/></form>`;
}
