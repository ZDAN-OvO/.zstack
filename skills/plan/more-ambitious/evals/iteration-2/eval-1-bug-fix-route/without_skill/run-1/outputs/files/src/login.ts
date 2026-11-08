// Login page entry. Renders after /api/session resolves.
export async function mountLogin(root: HTMLElement) {
  try {
    const res = await fetch('/api/session', { cache: 'no-store' });
    if (!res.ok) throw new Error(`/api/session responded ${res.status}`);
    const s = await res.json();
    if (s.user) return; // already logged in: leave whatever the shell rendered alone
    root.innerHTML = '<form id="login"></form>';
  } catch (err) {
    // Never leave root empty: a thrown fetch/json() used to blank the page forever.
    console.error('[login] mountLogin failed', err);
    root.innerHTML =
      '<p class="login-error">登录状态获取失败，请重试。</p>' +
      '<button type="button" data-login-retry>重试</button>';
    root
      .querySelector('[data-login-retry]')
      ?.addEventListener('click', () => void mountLogin(root));
  }
}
