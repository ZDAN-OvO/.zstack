type Session = { user?: { name?: string } };

// 同一 root 上多次 mount 时，只有最后一次请求的结果可以写 DOM，
// 避免慢请求覆盖新请求导致内容错乱/空白。
const mountSeq = new WeakMap<HTMLElement, number>();

export async function mountLogin(root: HTMLElement) {
  const seq = (mountSeq.get(root) ?? 0) + 1;
  mountSeq.set(root, seq);

  // 先渲染空表单：任何后续失败都不会留下白屏
  root.innerHTML = renderForm("");

  const token = localStorage.getItem("token");
  if (!token) return; // 未登录，保持空表单即可

  try {
    const res = await fetch("/api/session", {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!res.ok) {
      // 401/403 属于正常的"未登录"，其余状态记一笔日志方便排查
      if (res.status !== 401 && res.status !== 403) {
        console.warn("session request failed", res.status);
      }
      return;
    }

    const session: Session | null = await res.json().catch(() => null);
    if (mountSeq.get(root) !== seq) return; // 已被更新的 mount 取代

    root.innerHTML = renderForm(session?.user?.name ?? "");
  } catch (err) {
    // 网络错误 / 请求被中断等：保留空表单，不再向上抛
    console.error("load session failed", err);
  }
}

function escapeAttr(value: string) {
  return value
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function renderForm(name: string) {
  return `<form><input value="${escapeAttr(name)}"/></form>`;
}
