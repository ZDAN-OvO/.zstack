import { describe, expect, it, vi, afterEach } from "vitest";
import { mountLogin } from "./login";

function root() {
  return document.createElement("div");
}

afterEach(() => vi.unstubAllGlobals());

describe("mountLogin 白屏回归", () => {
  it("session 返回 401 空体时不抛错、不留空白", async () => {
    vi.stubGlobal("fetch", () =>
      Promise.resolve({ ok: false, status: 401, json: () => Promise.resolve({}) })
    );
    const el = root();
    await mountLogin(el);
    expect(el.innerHTML).not.toBe("");
  });

  it("session 缺 user 字段时不留空白(2.3.1 崩溃现场)", async () => {
    vi.stubGlobal("fetch", () =>
      Promise.resolve({ ok: true, status: 200, json: () => Promise.resolve({}) })
    );
    const el = root();
    await mountLogin(el);
    expect(el.innerHTML).toContain("<form");
  });

  it("正常响应渲染出用户名", async () => {
    vi.stubGlobal("fetch", () =>
      Promise.resolve({
        ok: true,
        status: 200,
        json: () => Promise.resolve({ user: { name: "ada" } }),
      })
    );
    const el = root();
    await mountLogin(el);
    expect(el.innerHTML).toContain('value="ada"');
  });
});
