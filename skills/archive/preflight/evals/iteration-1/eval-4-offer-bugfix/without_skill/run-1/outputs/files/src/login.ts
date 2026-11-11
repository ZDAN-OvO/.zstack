type Session = { user?: { name?: string } | null } | null;

export async function mountLogin(root: HTMLElement) {
  console.log("mount login");

  const token = localStorage.getItem("token");
  // 没有 token 时没必要请求，直接渲染空的登录表单。
  if (!token) {
    render(root, "");
    return;
  }

  try {
    const res = await fetch("/api/session", {
      headers: { Authorization: `Bearer ${token}` },
    });
    // 401/500 等响应体通常不是 session JSON，先判 ok，避免 r.json() 抛错后白屏。
    if (!res.ok) {
      throw new Error(`session request failed: ${res.status}`);
    }
    const session: Session = await res.json();
    // session/user/name 任意一级缺失都不能让渲染失败。
    render(root, session?.user?.name ?? "");
  } catch (err) {
    // 网络错误、超时、JSON 解析失败、token 失效都要兜底渲染，页面不能白屏。
    console.warn("failed to load session, rendering empty login form", err);
    render(root, "");
  }
}

function render(root: HTMLElement, name: string) {
  console.log("render", name);
  root.innerHTML = renderForm(name);
}

function renderForm(name: string) {
  return `<form><input value="${escapeHtml(name)}"/></form>`;
}

function escapeHtml(value: string) {
  return value
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}
