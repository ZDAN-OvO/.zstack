type Session = { user?: { name?: string } | null } | null;

export async function mountLogin(root: HTMLElement) {
  console.log("mount login");
  const token = localStorage.getItem("token");

  try {
    const res = await fetch("/api/session", {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!res.ok) throw new Error(`session request failed: HTTP ${res.status}`);

    const session: Session = await res.json().catch(() => null);
    root.innerHTML = renderForm(session?.user?.name ?? "");
  } catch (err) {
    // 会话获取失败时降级为空白登录表单，避免整页白屏
    console.error("failed to load session", err);
    root.innerHTML = renderForm("");
  }
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
