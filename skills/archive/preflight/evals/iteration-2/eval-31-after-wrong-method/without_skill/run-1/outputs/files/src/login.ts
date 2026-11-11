export type SessionUser = { name?: unknown };
export type Session = { user?: SessionUser | null } | null | undefined;
export type SessionLoader = () => Promise<Session>;

const TOKEN_KEY = "token";
const SESSION_TIMEOUT_MS = 10_000;

/**
 * /api/session answers with `{}` / `{ user: null }` when there is no valid
 * session, and may answer with a non-JSON error page. Neither is a reason to
 * blank the page, so logged-out states are normalised to `null` and transport
 * failures are rejected (the caller shows a retry UI).
 */
export async function fetchSession(timeoutMs: number = SESSION_TIMEOUT_MS): Promise<Session> {
  const token = localStorage.getItem(TOKEN_KEY);
  const headers: Record<string, string> = { Accept: "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch("/api/session", { headers, signal: controller.signal });
    if (res.status === 401 || res.status === 403) return null;
    if (!res.ok) throw new Error(`GET /api/session -> ${res.status}`);
    return (await res.json()) as Session;
  } finally {
    clearTimeout(timer);
  }
}

function displayName(session: Session): string {
  const name = session?.user?.name;
  return typeof name === "string" ? name : "";
}

const escapeHtml = (value: string): string =>
  value.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c] as string);

export function renderForm(name: string): string {
  return `<form data-testid="login-form"><input name="username" value="${escapeHtml(name)}" autocomplete="username"/></form>`;
}

export function renderLoading(): string {
  return `<div data-testid="login-loading" aria-busy="true">加载中…</div>`;
}

export function renderError(): string {
  return `<div data-testid="login-error" role="alert">登录信息加载失败 <button type="button" data-action="retry">重试</button></div>`;
}

/**
 * Always paints one of three states (form / error+retry), so a bad session
 * payload or a failed request can never leave the login page blank.
 */
export function mountLogin(root: HTMLElement, load: SessionLoader = fetchSession): void {
  let attempt = 0;

  const paint = (current: number, html: string) => {
    if (current === attempt) root.innerHTML = html;
  };

  const start = () => {
    const current = ++attempt;
    root.innerHTML = renderLoading();
    // Promise.resolve().then() also turns a synchronously throwing loader into a rejection.
    Promise.resolve()
      .then(load)
      .then(
        (session) => paint(current, renderForm(displayName(session))),
        (err) => {
          console.error("login: session load failed", err);
          paint(current, renderError());
        },
      );
  };

  root.addEventListener("click", (event) => {
    const target = event.target as Element | null;
    if (target?.closest?.('[data-action="retry"]')) start();
  });

  start();
}
