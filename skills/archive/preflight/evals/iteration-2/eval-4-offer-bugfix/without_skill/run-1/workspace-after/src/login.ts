export function mountLogin(root: HTMLElement) {
  console.log("mount login");

  // 先渲染兜底表单，保证无论接口成功/失败/慢，页面都不会白屏。
  root.innerHTML = renderForm("");

  const token = localStorage.getItem("token");

  fetch("/api/session", { headers: { Authorization: `Bearer ${token}` } })
    .then((r) => {
      // 401/403 等会返回非 JSON 响应，直接 .json() 会抛错。
      if (!r.ok) throw new Error(`session request failed: ${r.status}`);
      return r.json();
    })
    .then((s) => {
      console.log("session", s);
      const name = s?.user?.name;
      if (typeof name === "string" && name) {
        root.innerHTML = renderForm(name);
      }
    })
    .catch((err) => {
      // 网络异常或响应结构不符合预期时保留兜底表单，而不是留下白屏。
      console.error("load session failed", err);
    });
}

function escapeHtml(value: string) {
  return value
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function renderForm(name: string) {
  console.log("render", name);
  return `<form><input value="${escapeHtml(name)}"/></form>`;
}
