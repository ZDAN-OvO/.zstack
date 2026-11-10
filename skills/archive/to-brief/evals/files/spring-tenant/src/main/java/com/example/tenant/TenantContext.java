package com.example.tenant;

// 当前请求的租户 ID，由 TenantFilter 从请求头 X-Tenant-Id 写入
public final class TenantContext {
    private static final ThreadLocal<Long> CURRENT = new ThreadLocal<>();
    public static void set(Long id) { CURRENT.set(id); }
    public static Long get() { return CURRENT.get(); }
    public static void clear() { CURRENT.remove(); }
}
