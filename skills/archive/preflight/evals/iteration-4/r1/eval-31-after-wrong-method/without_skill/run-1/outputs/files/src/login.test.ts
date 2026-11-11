import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { mountLogin } from "./login";

const fakeRoot = () => ({ innerHTML: "" }) as unknown as HTMLElement;
const flush = () => new Promise((resolve) => setTimeout(resolve, 0));

const respond = (ok: boolean, status: number, body: unknown) =>
  vi.fn(async () => ({ ok, status, json: async () => body }));

describe("mountLogin", () => {
  beforeEach(() => {
    vi.stubGlobal("localStorage", {
      getItem: vi.fn(() => "token-123"),
      setItem: vi.fn(),
      removeItem: vi.fn(),
    });
    vi.spyOn(console, "log").mockImplementation(() => {});
    vi.spyOn(console, "warn").mockImplementation(() => {});
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("renders the login form when /api/session returns 401", async () => {
    // Regression: this used to throw on `session.user.name`, leaving a white page.
    vi.stubGlobal("fetch", respond(false, 401, { error: "unauthorized" }));
    const root = fakeRoot();

    mountLogin(root);
    await flush();

    expect(root.innerHTML).toContain("<form");
  });

  it("renders the login form when the session payload has no user", async () => {
    // Regression: the crash-log signature (reading 'name' of undefined).
    vi.stubGlobal("fetch", respond(true, 200, {}));
    const root = fakeRoot();

    expect(() => mountLogin(root)).not.toThrow();
    await flush();

    expect(root.innerHTML).toContain("<form");
  });

  it("renders the login form when the request rejects", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => { throw new Error("offline"); }));
    const root = fakeRoot();

    mountLogin(root);
    await flush();

    expect(root.innerHTML).toContain("<form");
  });

  it("renders the user name when a session exists", async () => {
    vi.stubGlobal("fetch", respond(true, 200, { user: { name: "Ada" } }));
    const root = fakeRoot();

    mountLogin(root);
    await flush();

    expect(root.innerHTML).toContain('value="Ada"');
  });

  it("escapes the user name", async () => {
    vi.stubGlobal("fetch", respond(true, 200, { user: { name: 'A"B<script>' } }));
    const root = fakeRoot();

    mountLogin(root);
    await flush();

    expect(root.innerHTML).not.toContain("<script>");
    expect(root.innerHTML).toContain("&quot;");
  });

  it("does not send a Bearer header when the token is missing", async () => {
    vi.stubGlobal("localStorage", { getItem: vi.fn(() => null), setItem: vi.fn(), removeItem: vi.fn() });
    const fetchMock = respond(true, 200, { user: { name: "Ada" } });
    vi.stubGlobal("fetch", fetchMock);

    mountLogin(fakeRoot());
    await flush();

    expect(fetchMock.mock.calls[0][1]).toEqual({ headers: {} });
  });
});
