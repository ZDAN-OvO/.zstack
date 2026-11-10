# 2026-10-12 orders 表锁等待

给 orders 加索引时未用 CONCURRENTLY，高峰期锁表 11 分钟，checkout 全部超时。
