读完技能与工作区了。这个请求**不够格直接写 brief**：Goal 有三四种读法，Done 的「完整」没有边界。我先说排查到的事实，再问 2 个问题。

## 我查到的（不用你回答）

| 事实 | 来源 | 对请求的含义 |
|---|---|---|
| 依赖里只有 `spring-boot-starter-parent` 3.3.4，**没有** security、web、JDBC/ORM 任何 starter | `pom.xml` | 认证/鉴权栈是零，不是「加一层」，是从零搭 |
| 已接受 ADR：共享 schema + 每表 `tenant_id`，隔离靠 service 层，不用独立库 | `docs/adr/0001-shared-schema-tenancy.md` | 租户方案已定，改动它等于推翻这条 ADR |
| `TenantContext` 是 `ThreadLocal<Long>`，注释说由 `TenantFilter` 从请求头 `X-Tenant-Id` 写入 | `src/main/java/com/example/tenant/TenantContext.java` | **`TenantFilter` 不在仓库里**；且从请求头取租户 ID 意味着租户身份可被客户端伪造 |
| `CourseService.pageTeachingCourses` **只按 `createBy` 过滤，没有 `tenant_id` 条件** | `src/main/java/com/example/course/CourseService.java` | 与 ADR 0001 直接矛盾 —— 已是跨租户数据泄露 |
| 词汇表里只有 `Tenant` 和 `Teacher enrollment`（`tp_user_course_enrollment` 中 role=TEACHER） | `GLOSSARY.md` | 已有「角色」概念的雏形，但只有 TEACHER 一个值，没有权限模型 |

两个术语问题顺带指出：「权限体系」在这里混了三件事 —— **认证**（你是谁）、**租户隔离**（看哪个租户的数据）、**授权**（你能做什么）。你现在要的是哪几件，决定了输出。等 Q1 定了我把这三个词分开写进 `GLOSSARY.md`；现在写等于替你决定，所以没动。

**Stage**：暂定 `decide`（若 Q1 选「直接写代码」则为 `execute`）。`Materials` 是 missing 但低影响，按默认处理（仅限本仓库文件、缺失实现留空标注），会记进 brief 的 Assumptions，你可以否决。

---

❓ **Q1** — **这次到底要解决哪个问题**：把你原话拆开，有四个读法，产出差别很大：

- **(a) 只堵泄露**：补 `TenantFilter`、租户身份改为从登录态/token 取而非请求头，所有查询强制带 `tenant_id`。范围是修现有 service + 数据访问层，**不新建 RBAC**。这是安全修补，`CourseService` 就是现成证据。
- **(b) 只建 RBAC**：租户内的 用户-角色-权限（接口级/菜单级）模型，租户隔离只是其中一个维度。这是新功能，要新建表、新建鉴权入口。
- **(c) 两者都要，但分先后**：先把隔离基线补上并加回归测试，再在隔离之上做租户内 RBAC。
- **(d) 换隔离方案**：独立库/独立 schema，即推翻 ADR 0001。

➡️ 建议 **(c)**：先补隔离、再叠 RBAC。理由：仓库里已有活跃的跨租户泄露（`CourseService` 只按 `createBy` 过滤），而 ADR 0001 把隔离责任放在 service 层，RBAC 如果建在这条已经有洞的基线上，后面每个角色校验都要重写一遍。如果你认同，回「是」即可；选别的就写字母。

---

❓ **Q2** — **第一个交到我手上的东西是什么**：请求说「完整」，但没有可观测的完成线。三种收口方式：

- **(a) 先一份设计说明**：租户隔离 + RBAC 的领域模型、表结构变更、鉴权切入点（filter/interceptor/AOP）、历史数据迁移与回滚、2 个备选方案加推荐。你批了再动代码。
- **(b) 直接给最小垂直切片**：一套表 + 一条端到端链路能跑通，不做前置评审。
- **(c) 先只交隔离修复的 PR**（含测试），RBAC 另开一轮。

➡️ 建议 **(a)，且这份设计说明里就写明分阶段计划**，第一阶段即 Q1 选的隔离修复。理由：表结构和鉴权切入点一旦落地就很难回退（正好满足 ADR 的三条判据：难逆、未来读者会问为什么、有真实取舍），而当前仓库连 `CourseMapper`、`TenantFilter` 都不在，直接写代码只能靠猜。同意回「是」。

---

**下一轮要问**（本轮只问 2 个）：`Boundaries`（能否改 `tp_` 现有表结构、能否回填历史数据、ADR 0001 是否可推翻、现有接口签名能否改）与 `Context`（真实租户数量与数据量、是否已有生产数据、前端是否依赖菜单/按钮权限、这套东西以后谁维护）。

`docs/briefs/` 还没建、brief 还没写 —— Goal 目前有四种读法，按技能规则不能靠默认值填。Q1、Q2 答完我写 `docs/briefs/` 下的 brief 并跑 checker。