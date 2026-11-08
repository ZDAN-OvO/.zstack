// Login page entry. Renders after /api/session resolves.
export async function renderLogin(root: HTMLElement) {
  const res = await fetch('/api/session');
  const s = await res.json();
  root.innerHTML = s.user ? '' : '<form id="login"></form>';
}
