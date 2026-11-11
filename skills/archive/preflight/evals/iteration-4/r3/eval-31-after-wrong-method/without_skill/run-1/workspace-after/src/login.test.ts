import { afterEach, describe, expect, it, vi } from "vitest";
import { mountLogin } from "./login";

const mkRoot = () => ({ innerHTML: "" }) as unknown as HTMLElement;
const flush = () => new Promise((resolve) => setTimeout(resolve, 0));

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

describe("mountLogin", () => {
  it("200 + user 时渲染表单", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ user: { name: "Ada" } }),
    });
    vi.stubGlobal("fetch", fetchMock);
    vi.stubGlobal("localStorage", { getItem: () => "valid-token" });

    const root = mkRoot();
    mountLogin(root);
    await flush();

    expect(root.innerHTML).toContain('<input value="Ada"/>');
    expect(fetchMock).toHaveBeenCalledWith("/api/session", {
      headers: { Authorization: "Bearer valid-token" },
    });
  });

  it("401 + error body 时不崩溃，渲染错误提示", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        status: 401,
        json: async () => ({ error: "unauthorized" }),
      }),
    );
    vi.stubGlobal("localStorage", { getItem: () => "expired-token" });
    vi.spyOn(console, "error").mockImplementation(() => {});

    const root = mkRoot();
    expect(() => mountLogin(root)).not.toThrow();
    await flush();

    expect(root.innerHTML).toContain('role="alert"');
  });

  it("200 但响应没有 user 时不崩溃", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({ ok: true, status: 200, json: async () => ({}) }),
    );
    vi.stubGlobal("localStorage", { getItem: () => "valid-token" });
    vi.spyOn(console, "error").mockImplementation(() => {});

    const root = mkRoot();
    mountLogin(root);
    await flush();

    expect(root.innerHTML).toContain('role="alert"');
  });

  it("网络失败时渲染错误提示", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("Failed to fetch")));
    vi.stubGlobal("localStorage", { getItem: () => "valid-token" });
    vi.spyOn(console, "error").mockImplementation(() => {});

    const root = mkRoot();
    mountLogin(root);
    await flush();

    expect(root.innerHTML).toContain('role="alert"');
  });

  it("没有 token 时直接渲染空表单，不发请求", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    vi.stubGlobal("localStorage", { getItem: () => null });

    const root = mkRoot();
    mountLogin(root);

    expect(fetchMock).not.toHaveBeenCalled();
    expect(root.innerHTML).toContain("<form>");
  });
});
