export function mountLogin(root: HTMLElement) {
  console.log("mount login");
  const token = localStorage.getItem("token");
  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
    .then((r) => r.json())
    .then((s) => {
      console.log("session", s);
      // 会话无效/过期时接口可能返回空 body 或没有 user 字段
      const name = s?.user?.name;
      root.innerHTML = renderForm(typeof name === "string" ? name : "");
    })
    .catch((err) => {
      console.error("failed to load session", err);
      root.innerHTML = renderForm("");
    });
}

function renderForm(name: string) {
  console.log("render", name);
  return `<form><input value="${escapeAttr(name)}"/></form>`;
}

function escapeAttr(value: string) {
  return value
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}
