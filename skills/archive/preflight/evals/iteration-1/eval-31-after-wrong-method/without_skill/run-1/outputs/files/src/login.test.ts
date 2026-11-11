import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { mountLogin } from "./login";

function fakeRoot() {
  return { innerHTML: "" };
}

function jsonResponse(body: unknown, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
    text: async () => JSON.stringify(body),
  } as unknown as Response;
}

describe("mountLogin 白屏回归", () => {
  beforeEach(() => {
    vi.spyOn(console, "error").mockImplementation(() => {});
    vi.spyOn(console, "log").mockImplementation(() => {});
    const store = new Map<string, string>([["token", "t-1"]]);
    vi.stubGlobal("localStorage", {
      getItem: (k: string) => store.get(k) ?? null,
      setItem: (k: string, v: string) => void store.set(k, v),
      removeItem: (k: string) => void store.delete(k),
    });
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("200 + user.name 正常渲染表单", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => jsonResponse({ user: { name: "amy" } })));
    const root = fakeRoot();
    await mountLogin(root);
    expect(root.innerHTML).toContain('value="amy"');
  });

  it("401 不抛错，并且能渲染出可操作界面（不是白屏）", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => jsonResponse({ error: "unauthorized" }, 401)));
    const root = fakeRoot();
    await expect(mountLogin(root)).resolves.toBeUndefined();
    expect(root.innerHTML).toContain("<form");
    expect(localStorage.getItem("token")).toBeNull();
  });

  it("200 但缺少 user（历史崩溃点 login.ts:5 s.user.name）不再崩溃", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => jsonResponse({})));
    const root = fakeRoot();
    await mountLogin(root);
    expect(root.innerHTML).toContain('role="alert"');
  });

  it("响应不是 JSON（网关 HTML 错误页 / 204 空响应）不再崩溃", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(
        async () =>
          ({
            ok: true,
            status: 200,
            json: async () => {
              throw new SyntaxError("Unexpected token <");
            },
          }) as unknown as Response,
      ),
    );
    const root = fakeRoot();
    await mountLogin(root);
    expect(root.innerHTML).toContain('role="alert"');
  });

  it("5xx 渲染重试提示，而不是留下空 DOM", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => jsonResponse({ error: "boom" }, 500)));
    const root = fakeRoot();
    await mountLogin(root);
    expect(root.innerHTML).toContain('data-action="retry"');
  });

  it("没有 token 时直接渲染登录表单，不再发 Bearer null 请求", async () => {
    localStorage.removeItem("token");
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const root = fakeRoot();
    await mountLogin(root);
    expect(fetchMock).not.toHaveBeenCalled();
    expect(root.innerHTML).toContain("<form");
  });

  it("user.name 中的引号不会破坏属性（顺带修掉注入）", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => jsonResponse({ user: { name: '"x" onfocus=alert(1)' } })));
    const root = fakeRoot();
    await mountLogin(root);
    // 引号被转义后整段仍在同一个 value 属性里，不会逃逸出属性
    expect(root.innerHTML).not.toContain('"x"');
    expect(root.innerHTML).toContain("&quot;");
  });
});
