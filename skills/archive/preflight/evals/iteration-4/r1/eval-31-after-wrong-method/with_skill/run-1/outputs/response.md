已按「方法错误」而不是「目标太大」处理，原地更新了 `local/plans/login-whitescreen.md`。

**上次为什么走偏**：Depth 只写了「先看崩溃日志」，等于把诊断当成了动作，没有落到栈上。实际日志已经能定位：

- `src/login.ts:5` 是 `root.innerHTML = renderForm(s.user.name)`
- `Cannot read properties of undefined (reading 'name')` 共 789 次（2.3.0 412 + 2.3.1 377），跨版本未消失
- 即 `/api/session` 有时返回没有 `user` 的 body（无效/过期 token），代码不查 `r.ok`、不校验 body 形状，`.then` 内抛错，`root` 保持空 → 白屏

骨架屏正好让「空 root」看起来像正常加载，遮住了症状。

**本版改动**

- Depth：枚举 token 状态下的响应，把失败响应当测试夹具；`catch` 后渲染登录表单兜底；stretch 是用 `login.ts:5` 原始栈做断言的测试，必须在当前代码上先失败
- Judge：只断言骨架屏出现的测试判失败；修复前测试必须红
- Done：加了检查点，先给根因结论 + 失败测试，再动代码
- Boundaries：记录「只加骨架屏、根因未定位」为已拒绝
- Tries：2026-11-10 一行，判为方法错误，故加 Depth

**Ready: no，需要你定两件事**

1. 失败响应样本从哪取：后端 access log，还是你手动用过期 token 触发一次并给我 Network 记录？
2. `ChunkLoadError` 88 次是否算这次的白屏，进不进本 PR？

确认后我可以按检查点先产出根因结论和那条红测试；需要的话再用 `/define-goal` 以这份计划为源。