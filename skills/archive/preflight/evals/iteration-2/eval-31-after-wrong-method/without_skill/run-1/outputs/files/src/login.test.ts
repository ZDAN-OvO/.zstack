import { afterEach, describe, expect, it, vi } from "vitest";
import { fetchSession, mountLogin } from "./login";

/** Minimal stand-in for the app's mount point; no DOM implementation needed. */
class FakeRoot {
  innerHTML = "";
  private clickHandlers: Array<(event: unknown) => void> = [];

  addEventListener(type: string, handler: (event: unknown) => void) {
    if (type === "click") this.clickHandlers.push(handler);
  }

  clickRetry() {
    const target = { closest: (selector: string) => (selector === '[data-action="retry"]' ? {} : null) };
    for (const handler of this.clickHandlers) handler({ target });
  }
}

const root = () => new FakeRoot() as unknown as HTMLElement & FakeRoot;
const flush = () => new Promise((resolve) => setTimeout(resolve, 0));

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

describe("mountLogin", () => {
  it("renders the form when /api/session omits user (the crash from login.ts:5)", async () => {
    const r = root();
    mountLogin(r, async () => ({}));
    await flush();

    expect(r.innerHTML).toContain("login-form");
    expect(r.innerHTML).not.toContain("undefined");
  });

  it("renders the form for an explicitly logged-out session", async () => {
    const r = root();
    mountLogin(r, async () => ({ user: null }));
    await flush();

    expect(r.innerHTML).toContain("login-form");
  });

  it("renders the form for a non-object session payload", async () => {
    const r = root();
    mountLogin(r, async () => null);
    await flush();

    expect(r.innerHTML).toContain("login-form");
  });

  it("keeps the user name when the session is valid", async () => {
    const r = root();
    mountLogin(r, async () => ({ user: { name: "Ada" } }));
    await flush();

    expect(r.innerHTML).toContain('value="Ada"');
  });

  it("escapes the user name instead of injecting markup", async () => {
    const r = root();
    mountLogin(r, async () => ({ user: { name: '<img src=x onerror="alert(1)">' } }));
    await flush();

    expect(r.innerHTML).not.toContain("<img");
    expect(r.innerHTML).toContain("&lt;img");
  });

  it("shows a retry state instead of a blank page when the request fails", async () => {
    const r = root();
    vi.spyOn(console, "error").mockImplementation(() => {});
    mountLogin(r, async () => {
      throw new Error("network down");
    });
    await flush();

    expect(r.innerHTML).toContain("login-error");
    expect(r.innerHTML).toContain('data-action="retry"');
  });

  it("shows a retry state when the loader throws synchronously", async () => {
    const r = root();
    vi.spyOn(console, "error").mockImplementation(() => {});
    mountLogin(r, (() => {
      throw new Error("boom");
    }) as never);
    await flush();

    expect(r.innerHTML).toContain("login-error");
  });

  it("recovers after clicking retry", async () => {
    const r = root();
    vi.spyOn(console, "error").mockImplementation(() => {});
    const load = vi
      .fn<() => Promise<{ user: { name: string } }>>()
      .mockRejectedValueOnce(new Error("network down"))
      .mockResolvedValueOnce({ user: { name: "Ada" } });

    mountLogin(r, load);
    await flush();
    expect(r.innerHTML).toContain("login-error");

    r.clickRetry();
    await flush();

    expect(r.innerHTML).toContain('value="Ada"');
  });

  it("ignores a late response from a superseded attempt", async () => {
    const r = root();
    vi.spyOn(console, "error").mockImplementation(() => {});
    let resolveFirst: (value: { user: { name: string } }) => void = () => {};
    const load = vi
      .fn<() => Promise<{ user: { name: string } }>>()
      .mockImplementationOnce(() => new Promise((resolve) => (resolveFirst = resolve)))
      .mockResolvedValueOnce({ user: { name: "Ada" } });

    mountLogin(r, load);
    r.clickRetry();
    await flush();
    resolveFirst({ user: { name: "stale" } });
    await flush();

    expect(r.innerHTML).toContain('value="Ada"');
    expect(r.innerHTML).not.toContain("stale");
  });
});

describe("fetchSession", () => {
  it("treats 401 as logged out and does not send a Bearer null token", async () => {
    vi.stubGlobal("localStorage", { getItem: () => null });
    const fetchMock = vi.fn().mockResolvedValue({ status: 401, ok: false, json: async () => ({}) });
    vi.stubGlobal("fetch", fetchMock);

    await expect(fetchSession()).resolves.toBeNull();
    const init = fetchMock.mock.calls[0][1] as { headers: Record<string, string> };
    expect(init.headers.Authorization).toBeUndefined();
  });

  it("sends the token when one is stored", async () => {
    vi.stubGlobal("localStorage", { getItem: () => "t0ken" });
    const fetchMock = vi.fn().mockResolvedValue({ status: 200, ok: true, json: async () => ({ user: { name: "Ada" } }) });
    vi.stubGlobal("fetch", fetchMock);

    await fetchSession();
    const init = fetchMock.mock.calls[0][1] as { headers: Record<string, string> };
    expect(init.headers.Authorization).toBe("Bearer t0ken");
  });

  it("rejects on a server error so the UI can offer retry", async () => {
    vi.stubGlobal("localStorage", { getItem: () => null });
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ status: 500, ok: false, json: async () => ({}) }));

    await expect(fetchSession()).rejects.toThrow("500");
  });

  it("aborts a hung request instead of leaving the skeleton forever", async () => {
    vi.stubGlobal("localStorage", { getItem: () => null });
    vi.stubGlobal(
      "fetch",
      vi.fn((_url: string, init: { signal: AbortSignal }) => {
        return new Promise((_resolve, reject) => {
          init.signal.addEventListener("abort", () => reject(new Error("aborted")));
        });
      }),
    );

    await expect(fetchSession(10)).rejects.toThrow("aborted");
  });
});
