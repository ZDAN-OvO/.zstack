type Session = { user?: { name?: string } };

export async function mountLogin(root: HTMLElement) {
  const token = localStorage.getItem("token");
  // 兜底先画:任何分支下 root 都不会是空的(白屏)
  root.innerHTML = renderForm("");

  try {
    const r = await fetch("/api/session", {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!r.ok) return; // 401/500:留登录表单,不打 .user
    const s: Session = await r.json();
    const name = s?.user?.name;
    if (name) root.innerHTML = renderForm(name);
  } catch {
    // 网络错误/非 JSON 响应:同上,保持可用的登录表单
  }
}

function renderForm(name: string) {
  return `<form><input value="${name}"/></form>`;
}
