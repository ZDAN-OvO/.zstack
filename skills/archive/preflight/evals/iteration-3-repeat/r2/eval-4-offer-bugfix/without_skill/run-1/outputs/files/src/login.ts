export function mountLogin(root: HTMLElement) {
  console.log("mount login");
  void loadSession(root);
}

async function loadSession(root: HTMLElement) {
  const token = localStorage.getItem("token");

  // 未登录时直接展示空白登录表单，不要带着 "Bearer null" 去请求接口。
  if (!token) {
    root.innerHTML = renderForm("");
    return;
  }

  try {
    const res = await fetch("/api/session", {
      headers: { Authorization: `Bearer ${token}` },
    });

    // token 过期/失效：清掉本地 token，回退到未登录状态。
    if (res.status === 401 || res.status === 403) {
      localStorage.removeItem("token");
      root.innerHTML = renderForm("");
      return;
    }

    if (!res.ok) {
      throw new Error(`session request failed: ${res.status}`);
    }

    const session = await res.json();
    const name = session?.user?.name;

    console.log("session", session);
    root.innerHTML = renderForm(typeof name === "string" ? name : "");
  } catch (err) {
    // 网络错误、响应不是合法 JSON、接口返回结构异常等都不能让页面白屏。
    console.error("failed to load session", err);
    root.innerHTML = renderForm("");
  }
}

function renderForm(name: string) {
  console.log("render", name);
  return `<form><input value="${name}"/></form>`;
}
