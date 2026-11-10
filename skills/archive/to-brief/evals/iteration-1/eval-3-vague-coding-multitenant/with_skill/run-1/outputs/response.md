## 结论

这是一次「跨全库的权限改造」类请求，五个槽位里 **Goal、Boundaries、Done 全缺，Context、Materials 只有薄线索**。按 /to-brief：不写 brief，先 grill；Stage 记 **execute**，但 Done 必须带设计闸门。

编码任务 + 仓库已有 `docs/adr/` 与 `GLOSSARY.md` → 走 **/grill-with-docs**（/grilling 提问 + /domain-modeling 现场固化术语）。

## 我已查证的事实（不再问你）

- 项目是 Spring Boot 3.3.4，但 [pom.xml](pom.xml) 里**没有任何依赖**：没有 `spring-boot-starter-security`，也没有 MyBatis/JPA。也就是说认证、持久化、控制器都不在这份代码里。
- [docs/adr/0001-shared-schema-tenancy.md](docs/adr/0001-shared-schema-tenancy.md) 已 accepted：所有租户共享一套 schema，每张业务表带 `tenant_id`，**隔离在服务层强制，不用独立库**。这条已经定了，我不会再问。
- [GLOSSARY.md](GLOSSARY.md) 只有两个词：**Tenant**（学校/培训机构，用 `tenant_id` 标识）、**Teacher enrollment**（`tp_user_course_enrollment` 中 role=TEACHER 的行）。**没有**「角色」「权限」「平台超管」的定义——所以「权限体系」目前是个没被定义过的词。
- [TenantContext.java:4](src/main/java/com/example/tenant/TenantContext.java) 的租户来自请求头 `X-Tenant-Id`，由 `TenantFilter` 写入 ThreadLocal。→ 谁签发这个头、客户端能否伪造，直接决定隔离是否成立。
- [CourseService.java:8](src/main/java/com/example/course/CourseService.java) 的 `pageTeachingCourses` **只按 `createBy` 过滤，没有 `tenant_id` 条件**。这与 ADR「隔离在服务层强制」直接矛盾：ADR 描述的现状并不成立，代码里已有一个可复现的跨租户读取口子。

## 槽位评分

| 槽 | 现状 | 为什么 |
|---|---|---|
| Goal | **missing** | 「加一个完整的多租户权限体系」是动作，不是要支撑的决定 |
| Boundaries | **missing** | 没有一条「不许动」的墙 |
| Done | **missing** | 「完整」没有可观察的终点，也没说要不要先出设计 |
| Context | **thin** | 有 ADR/租户上下文，但规模、角色清单、现有认证、平台超管全未知 |
| Materials | **thin** | 只有 2 个 Java 文件 + ADR + 词汇表；这显然不是完整仓库，也没说能否引入上游框架 |

影响排序：**Goal > Boundaries > Done > Context > Materials**。

> 说明：/grill-with-docs 默认每轮最多两问。这是单轮、不会有第二轮，所以我把第三高影响的 Done 并入本轮（三个问题各对应一个槽位，按影响排序）；Context 与 Materials 留到下一轮，先给出我的默认值供你否决。

---

❓ **Q1** - **「权限体系」指哪一件事？**：这个词现在有三种读法，各自产出的是三个不同的系统：
(a) **堵住跨租户泄漏**（客户/合规驱动）——重点是租户解析可信、强制点覆盖所有查询、回归测试与审计，角色可以做到最小；
(b) **支撑一批学校自助上线**（增长驱动）——重点是租户内角色模型（校管理员/老师/学生）、租户初始化、平台超管的跨租户运维；
(c) **过安全评审或投标资质**（合规驱动）——重点是可证明的访问控制矩阵、文档、审计日志。

➡️ 建议以 **(a) 为主、(b) 的「租户管理员最小可用」为辅**。理由：代码里已经有隔离缺口（`CourseService` 缺 `tenant_id`），而 ADR 声称隔离已在服务层强制——先让 ADR 成立，再谈角色；反过来做，等于在一个漏的容器里加锁。如果你的真实动机是 (b) 或 (c)，直接说，Done 会随之改写。

---

❓ **Q2** - **这几条墙，我默认全部保留，你要动哪条？**：
1. 不改 ADR 0001 的结论——仍是共享 schema + `tenant_id`，不引入分库/独立 schema；
2. 不改现有公开 API 的路径、入参、返回结构，鉴权失败只**新增** 401/403 语义；
3. 不删改已有租户数据；schema 变更只允许加表/加列，且迁移可回滚；
4. 不引入新中间件（Redis、网关、独立鉴权服务）除非你点头；
5. 不重写登录/会话机制，只在现有认证之上加租户与权限判定。

➡️ 建议全部接受，尤其是第 1 条：换隔离模型的代价是数据迁移 + 重写所有查询，而 ADR 已经 accepted。如果你其实想借这次改成独立 schema，或者现有登录本来就要换掉，现在说，比设计文档写完再说便宜得多。

---

❓ **Q3** - **什么出现在你面前，算这件事做完了？**：建议分两段，第一段就是闸门：
1. 先交**设计说明（≤2 页）**：租户来源是否可信（`X-Tenant-Id` 由谁签发、如何防伪造）、角色与权限模型（租户内角色 vs 平台超管）、强制点位置（拦截器 / MyBatis 插件 / 服务层显式条件）、现有查询改造清单（以 `CourseService` 为样板，列出所有缺 `tenant_id` 的点）、迁移与回滚、验收用例清单。**不写实现代码，等你看过再动。**
2. 批准后按切片实现，每片自带测试：① 隔离强制点 + 回归测试（含 `CourseService` 泄漏用例）→ ② 角色与权限判定 → ③ 租户管理员自助。

➡️ 建议接受。理由是这是跨全库改造，方向错了的返工成本是重写所有查询；设计说明是最便宜的纠错点。如果你要的是「一次给完整实现」，我会按通用 RBAC 默认值去猜，猜错概率很高。

---

## 本轮没问、下一轮的 frontier

- **Context**（默认值待你否决）：租户数量在几十量级；角色至少是 平台超管 / 校管理员 / 老师 / 学生；现有认证方式未知，按「已有登录，只在其上加判定」处理。
- **Materials**（默认值待你否决）：只用本仓库这 2 个 Java 文件 + ADR + GLOSSARY，不参考外部框架实现，不引入 `spring-boot-starter-security` 以外的依赖；查不到的（如 DDL、真实表结构）留空标注，不臆造。
- **术语**（/domain-modeling）：等你回答 Q1，我会把定下来的词写进 [GLOSSARY.md](GLOSSARY.md)——目前需要区分的是 **tenant isolation（租户隔离）**、**role-based authorization（角色权限）**、**platform super-admin（平台超管）**，三个词现在被「权限体系」一个词盖住了。

**没有写 brief**（`docs/briefs/` 下未创建任何文件）。等你回答 Q1–Q3，我写 `docs/briefs/tenant-isolation-and-rbac.md` 并跑 `check-brief.mjs` 校验。