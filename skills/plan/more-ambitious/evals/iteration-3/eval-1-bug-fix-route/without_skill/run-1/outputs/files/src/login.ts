// Login page entry. Renders after /api/session resolves.
export async function mountLogin(root: HTMLElement) {
  try {
    const res = await fetch('/api/session');
    if (!res.ok) throw new Error(`/api/session returned ${res.status}`);
    const s = await res.json();
    root.innerHTML = s?.user ? '' : '<form id="login"></form>';
  } catch (err) {
    // Network error / 5xx / non-JSON body used to reject the promise before
    // anything was written to the DOM, leaving the page blank. Fall back to
    // the login form so the user can still sign in.
    console.error('[login] session check failed', err);
    root.innerHTML = '<form id="login"></form>';
  }
}
