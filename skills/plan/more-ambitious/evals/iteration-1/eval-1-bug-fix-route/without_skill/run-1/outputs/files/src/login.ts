// Login page entry. Renders after /api/session resolves.
const SESSION_TIMEOUT_MS = 8000;

type Session = { user?: unknown };

// /api/session 可能返回 204 或空 body，直接用 res.json() 会抛异常。
async function readSession(res: Response): Promise<Session> {
  const raw = await res.text();
  return raw ? (JSON.parse(raw) as Session) : {};
}

export async function mountLogin(root: HTMLElement) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), SESSION_TIMEOUT_MS);
  try {
    const res = await fetch('/api/session', {
      credentials: 'same-origin',
      signal: controller.signal,
    });
    if (!res.ok) throw new Error(`/api/session responded ${res.status}`);

    const session = await readSession(res);
    root.innerHTML = session.user ? '' : '<form id="login"></form>';
  } catch (err) {
    // 请求失败、超时、502 HTML、坏 JSON 都应降级成登录表单，而不是留下白屏。
    console.error('[login] failed to load session', err);
    root.innerHTML = '<form id="login"></form>';
  } finally {
    clearTimeout(timer);
  }
}
