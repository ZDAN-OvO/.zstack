import { afterEach, describe, expect, it, vi } from "vitest";
import { mountLogin } from "./login";

function fakeRoot() {
  return { innerHTML: "" } as HTMLElement;
}

function stubSession(status: number, body: unknown) {
  vi.stubGlobal("localStorage", {
    getItem: () => "token",
  });
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({
      ok: status >= 200 && status < 300,
      status,
      json: async () => body,
    }),
  );
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("mountLogin", () => {
  it("renders the form when the session is valid", async () => {
    stubSession(200, { user: { name: "Ada" } });
    const root = fakeRoot();

    mountLogin(root);
    await vi.waitFor(() => expect(root.innerHTML).toContain('value="Ada"'));
  });

  it("still renders a login form on 401 without a user (white-screen regression)", async () => {
    stubSession(401, { error: "unauthorized" });
    const root = fakeRoot();

    mountLogin(root);
    await vi.waitFor(() => expect(root.innerHTML).toContain("<form>"));
  });

  it("still renders a login form when the response has no user", async () => {
    stubSession(200, {});
    const root = fakeRoot();

    mountLogin(root);
    await vi.waitFor(() => expect(root.innerHTML).toContain("<form>"));
  });
});
