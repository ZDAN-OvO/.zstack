type Session = { user?: { name?: string } };

export function mountLogin(root: HTMLElement) {
  const token = localStorage.getItem("token");
  if (!token) {
    root.innerHTML = renderForm("");
    return;
  }

  loadSession(token)
    .then((session) => {
      root.innerHTML = renderForm(session.user?.name ?? "");
    })
    .catch((err) => {
      console.error("mount login failed", err);
      root.innerHTML = renderError();
    });
}

async function loadSession(token: string): Promise<Session> {
  const res = await fetch("/api/session", {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    throw new Error(`session request failed: ${res.status}`);
  }
  const session = (await res.json()) as Session | null;
  if (!session?.user) {
    throw new Error("session response has no user");
  }
  return session;
}

function renderForm(name: string) {
  return `<form><input value="${name}"/></form>`;
}

function renderError() {
  return `<div role="alert">登录失败，请刷新重试</div>`;
}
