我看了一下仓库，有个发现值得先说：崩溃日志里 `login.ts:5` 的 `TypeError: Cannot read properties of undefined (reading 'name')` 在 2.3.0 和 2.3.1 上分别报了 412 / 377 次，同期的 `ChunkLoadError` 只有 88 次——也就是说"偶尔白屏"至少有两个不同的成因，直接按其中一条改很可能只修到一半。

要我先把修复方案写成一份一屏的计划（确认目标和边界再动手）吗？回一句"好"我就开始写计划，代码先不动。