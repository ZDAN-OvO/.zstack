# Ladder: login white screen

| Rung | Goal | AI owns | Needs | Status |
|---|---|---|---|---|
| 0 | 修一下登录页偶尔白屏的 bug | | | |
| 1 | 登录页每次都能正常打开 | 复现与定位 | 前端错误日志 | |
| 2 | 用户从打开 App 到登录成功不再卡住或白屏 | 整条登录链路的稳定性 | 前端日志、/api/session 监控 | failed → back to 1 |

Handed over: rung 2

## Trials

### Rung 2 — 2026-11-08 — failed
- 交付物：登录页加 loading 骨架屏。
- 为什么不达标：只改变了白屏的表现（白 → 骨架屏），没有定位成因；验收人判定「真正原因根本没找到」。
- 结论：退回 rung 1（登录页每次都能正常打开），先补根因定位，再谈整条链路。骨架屏视为未验证的遮蔽物，待定去留。
