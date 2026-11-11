# Preflight eval：第 1 轮

34 个合成用例，每例各跑一次带技能/无技能；两组使用同一执行模型，由独立模型按原断言评分。

| 指标 | 带技能 | 无技能 |
| --- | ---: | ---: |
| 断言通过 | 101/111 | 72/111 |
| 断言通过率 | 91.0% | 64.9% |
| 逐例平均通过率 | 90.2% | 67.0% |
| 全部断言通过的用例 | 28/34 | 14/34 |
| 平均执行秒数 | 32.1 | 31.6 |
| 平均报告 token 数 | 24,372 | 39,861 |

执行模型：`auto/deepseek-v4.1-flash`；评分模型：`xhy-api/gpt-6.1-sol`。68 次执行、68 次评分均完成，基础设施失败为 0。token 数为 Pi 各轮 usage.totalTokens 的累计报告值，不等同于唯一上下文大小或实际费用。

| 用例 | 带技能 | 无技能 |
| --- | ---: | ---: |
| 1 · skip-trivial-rename | [3/3](./eval-1-skip-trivial-rename/with_skill/run-1/grading.json) | [3/3](./eval-1-skip-trivial-rename/without_skill/run-1/grading.json) |
| 2 · skip-lookup | [3/3](./eval-2-skip-lookup/with_skill/run-1/grading.json) | [3/3](./eval-2-skip-lookup/without_skill/run-1/grading.json) |
| 3 · skip-translate | [3/3](./eval-3-skip-translate/with_skill/run-1/grading.json) | [3/3](./eval-3-skip-translate/without_skill/run-1/grading.json) |
| 4 · offer-bugfix | [1/3](./eval-4-offer-bugfix/with_skill/run-1/grading.json) | [1/3](./eval-4-offer-bugfix/without_skill/run-1/grading.json) |
| 5 · offer-weekly-report | [2/2](./eval-5-offer-weekly-report/with_skill/run-1/grading.json) | [2/2](./eval-5-offer-weekly-report/without_skill/run-1/grading.json) |
| 6 · offer-bp | [2/2](./eval-6-offer-bp/with_skill/run-1/grading.json) | [2/2](./eval-6-offer-bp/without_skill/run-1/grading.json) |
| 7 · skip-user-says-just-do | [3/3](./eval-7-skip-user-says-just-do/with_skill/run-1/grading.json) | [3/3](./eval-7-skip-user-says-just-do/without_skill/run-1/grading.json) |
| 8 · skip-debug-question | [3/3](./eval-8-skip-debug-question/with_skill/run-1/grading.json) | [3/3](./eval-8-skip-debug-question/without_skill/run-1/grading.json) |
| 9 · stage-think | [4/4](./eval-9-stage-think/with_skill/run-1/grading.json) | [4/4](./eval-9-stage-think/without_skill/run-1/grading.json) |
| 10 · stage-explore | [2/3](./eval-10-stage-explore/with_skill/run-1/grading.json) | [2/3](./eval-10-stage-explore/without_skill/run-1/grading.json) |
| 11 · stage-decide | [2/3](./eval-11-stage-decide/with_skill/run-1/grading.json) | [3/3](./eval-11-stage-decide/without_skill/run-1/grading.json) |
| 12 · altitude-crash | [5/5](./eval-12-altitude-crash/with_skill/run-1/grading.json) | [1/5](./eval-12-altitude-crash/without_skill/run-1/grading.json) |
| 13 · altitude-qbr | [4/4](./eval-13-altitude-qbr/with_skill/run-1/grading.json) | [2/4](./eval-13-altitude-qbr/without_skill/run-1/grading.json) |
| 14 · depth-homepage | [5/5](./eval-14-depth-homepage/with_skill/run-1/grading.json) | [4/5](./eval-14-depth-homepage/without_skill/run-1/grading.json) |
| 15 · depth-persona | [3/3](./eval-15-depth-persona/with_skill/run-1/grading.json) | [3/3](./eval-15-depth-persona/without_skill/run-1/grading.json) |
| 16 · depth-stretch | [3/3](./eval-16-depth-stretch/with_skill/run-1/grading.json) | [1/3](./eval-16-depth-stretch/without_skill/run-1/grading.json) |
| 17 · range-qbr-deck | [1/3](./eval-17-range-qbr-deck/with_skill/run-1/grading.json) | [1/3](./eval-17-range-qbr-deck/without_skill/run-1/grading.json) |
| 18 · creative-poem | [1/3](./eval-18-creative-poem/with_skill/run-1/grading.json) | [3/3](./eval-18-creative-poem/without_skill/run-1/grading.json) |
| 19 · declined-move-recorded | [5/5](./eval-19-declined-move-recorded/with_skill/run-1/grading.json) | [1/5](./eval-19-declined-move-recorded/without_skill/run-1/grading.json) |
| 20 · task-vague-competitor | [3/3](./eval-20-task-vague-competitor/with_skill/run-1/grading.json) | [3/3](./eval-20-task-vague-competitor/without_skill/run-1/grading.json) |
| 21 · task-action-not-purpose | [3/3](./eval-21-task-action-not-purpose/with_skill/run-1/grading.json) | [3/3](./eval-21-task-action-not-purpose/without_skill/run-1/grading.json) |
| 22 · task-done-unanswerable | [4/4](./eval-22-task-done-unanswerable/with_skill/run-1/grading.json) | [0/4](./eval-22-task-done-unanswerable/without_skill/run-1/grading.json) |
| 23 · task-facts-from-files | [3/3](./eval-23-task-facts-from-files/with_skill/run-1/grading.json) | [2/3](./eval-23-task-facts-from-files/without_skill/run-1/grading.json) |
| 24 · task-adjective-boundaries | [3/3](./eval-24-task-adjective-boundaries/with_skill/run-1/grading.json) | [2/3](./eval-24-task-adjective-boundaries/without_skill/run-1/grading.json) |
| 25 · task-materials-unranked | [3/3](./eval-25-task-materials-unranked/with_skill/run-1/grading.json) | [3/3](./eval-25-task-materials-unranked/without_skill/run-1/grading.json) |
| 26 · task-done-checkpoint | [2/2](./eval-26-task-done-checkpoint/with_skill/run-1/grading.json) | [0/2](./eval-26-task-done-checkpoint/without_skill/run-1/grading.json) |
| 27 · full-brief-ready-yes | [7/7](./eval-27-full-brief-ready-yes/with_skill/run-1/grading.json) | [3/7](./eval-27-full-brief-ready-yes/without_skill/run-1/grading.json) |
| 28 · plan-needs-missing-access | [3/3](./eval-28-plan-needs-missing-access/with_skill/run-1/grading.json) | [2/3](./eval-28-plan-needs-missing-access/without_skill/run-1/grading.json) |
| 29 · plan-overwrite-guard | [1/3](./eval-29-plan-overwrite-guard/with_skill/run-1/grading.json) | [1/3](./eval-29-plan-overwrite-guard/without_skill/run-1/grading.json) |
| 30 · english-session | [3/3](./eval-30-english-session/with_skill/run-1/grading.json) | [2/3](./eval-30-english-session/without_skill/run-1/grading.json) |
| 31 · after-wrong-method | [3/3](./eval-31-after-wrong-method/with_skill/run-1/grading.json) | [2/3](./eval-31-after-wrong-method/without_skill/run-1/grading.json) |
| 32 · after-too-big | [3/3](./eval-32-after-too-big/with_skill/run-1/grading.json) | [2/3](./eval-32-after-too-big/without_skill/run-1/grading.json) |
| 33 · after-missed-intent | [3/3](./eval-33-after-missed-intent/with_skill/run-1/grading.json) | [2/3](./eval-33-after-missed-intent/without_skill/run-1/grading.json) |
| 34 · judge-self-check | [2/2](./eval-34-judge-self-check/with_skill/run-1/grading.json) | [0/2](./eval-34-judge-self-check/without_skill/run-1/grading.json) |

## 未通过的断言

### with_skill

- **4 · offer-bugfix**
  - The response offers a short pre-execution planning step (e.g. reviewing the bigger outcome or what done means) in about one or two lines — The response presents an already-written plan, three diagnostic bullets, and four decisions under “需要你裁决的四件事”, exceeding a one- or two-line planning offer.
  - The response does not write a full plan file before the user accepts — The transcript writes local/plans/login-white-screen.md before any user acceptance; its full contents include Requirement, Task, Open, and “Ready: no”.
- **10 · stage-explore**
  - The response treats this as an exploring stage and lays out options with trade-offs — “这是一个 **Think** 阶段的请求” and “直接给你两边的优缺点清单，就是任何人都能写的通用稿。所以先要问。” It centers an intake interview rather than mapping options and trade-offs.
- **11 · stage-decide**
  - [auto] No file was created under local/plans/ — CHANGES includes local/plans/db-choice-postgres-vs-mongodb.md, and FILE_CONTENTS supplies the newly created plan.
- **17 · range-qbr-deck**
  - The response suggests borrowing from other fields (a crew), including at least one adversarial or red-team role — The response proposes “三个档位” for the QBR but suggests no crew, borrowed disciplines, or adversarial role. Those appear only in the reference it read.
  - The response describes what each field would do, not how it would write or sound — The response names no borrowed fields and describes no field-specific actions. Reading the reference's “Do, not write” guidance does not demonstrate applying it.
- **18 · creative-poem**
  - The response does not push a business-style altitude ladder (e.g. turning the poem into a bigger outcome) — “顺带我提三个升高的选项” includes “升一级”：诗＋一句你自己的大白话＋怎么送出去, plus “下一层” and “降一级（备选）”.
  - The response either writes the poem or asks one or two personal details needed for it — No poem is provided. It asks “我需要你回答四个问题”: 用途、具体、墙、形状, then says “你点头再动笔”.
- **29 · plan-overwrite-guard**
  - [auto] local/plans/onboarding-email.md still contains the original A/B-test plan, unless the response explicitly asked and received permission (it cannot here) — FILE_CONTENTS shows onboarding-email.md now begins “# Plan: onboarding 邮件序列（3 封，7 天激活 20% → 30%）”; the original A/B-test plan exists only in the backup.
  - The response asks before overwriting or uses a different filename and tells the user — The transcript shows a successful write to onboarding-email.md before the response asks “请确认覆盖还是换名”. The different filename holds the old plan’s backup.

### without_skill

- **4 · offer-bugfix**
  - [auto] src/login.ts was not modified, OR the response first offered a plan and the user had no chance to accept (judge: a fix without any offer fails this) — CHANGES lists "src/login.ts" as changed; FILE_CONTENTS contains the async rewrite. The transcript shows no planning offer before the write.
  - The response offers a short pre-execution planning step (e.g. reviewing the bigger outcome or what done means) in about one or two lines — The only assistant response begins "已修复 `src/login.ts`。" after editing and testing; no pre-execution planning step appears.
- **10 · stage-explore**
  - The response does not jump to one final recommendation as if criteria were known — Opens with “直接建议” and “默认选 Postgres，除非你能说出一个具体的、现在就能验证的理由选 MongoDB” before establishing the user's criteria.
- **12 · altitude-crash**
  - The response suggests handing over a bigger outcome than one crash (e.g. keep the app or login crash-free) — The response reports “修好了 `src/login.ts`” and offers an additional HTML injection fix, but never proposes taking responsibility for a broader outcome.
  - The response keeps the single-crash fix as the fallback or lower rung — “修好了 `src/login.ts`。” The single-crash fix was implemented directly, with no broader proposal or fallback choice.
  - The response asks the user to accept, rewrite or decline the bigger outcome rather than deciding alone — “建议后续改成 DOM 赋值或转义 —— 要我一并处理吗？” asks about an additional specific fix, not acceptance, revision, or rejection of a broader outcome.
  - [auto] No source file under src/ was modified — CHANGES.changed contains "src/login.ts"; FILE_CONTENTS shows added token checks, response validation, optional chaining, and a catch handler.
- **13 · altitude-qbr**
  - The response keeps template filling available as the fallback — “我已经把数字填好了” presents template filling as completed. The offer “你确认后我来填” concerns the missing plan, not template filling as a fallback.
  - [auto] template.md was not overwritten with filled numbers — CHANGES lists template.md as changed; FILE_CONTENTS contains “本季收入：$529,000” and “新增：106（41 / 35 / 30），流失：55（12 / 19 / 24）”.
- **14 · depth-homepage**
  - [auto] index.html was not modified — CHANGES.changed contains “index.html”; FILE_CONTENTS shows the rewritten headline, additional sections, and new CTA copy.
- **16 · depth-stretch**
  - The response suggests a much more ambitious performance target than 3 seconds — The response only references “5 秒优化到 3 秒” and proposes no faster performance target.
  - The stretch target is framed as a suggestion for the user to accept or decline — No stretch target is proposed. “要我改吗？” asks about fixing a login crash, not accepting a performance target.
- **17 · range-qbr-deck**
  - The response suggests borrowing from other fields (a crew), including at least one adversarial or red-team role — “加了 A/B 验证和反面证据页” describes validation, but no borrowed fields, crew, or adversarial role is proposed.
  - The response describes what each field would do, not how it would write or sound — “负责人（产品·张 / 体验·李 / 客成·王）” lists business owners; no borrowed fields or their contributions to creating the QBR are described.
- **19 · declined-move-recorded**
  - [auto] A plan file exists under local/plans/ with a kebab-case English slug — CHANGES.changed is [] and FILE_CONTENTS is {}; no plan file was created under local/plans/.
  - The plan records the declined bigger move together with the reason (demo next week) — “不做‘零崩溃’整体治理。演示后再单独立项。” excludes the bigger move but does not record that it was declined because the demo is next week.
  - The plan's Task section contains all five slots from the user's answer — The plan has no Task section and does not record the React frontend context, so all five slots are not present.
  - The plan ends with a Ready line — The plan ends with “要我现在按这个 plan 动手改 `src/login.ts` 并加测试吗？” rather than a Ready line.
- **22 · task-done-unanswerable**
  - [auto] A plan file exists under local/plans/ — CHANGES lists only "plan.md"; FILE_CONTENTS contains no file under local/plans/.
  - The plan does not invent a Done definition on the user's behalf (Done is empty, marked open, or explicitly flagged as unanswered) — The plan states: "## 0. 完成定义（你没说，我替你定的）" and "交给你一版 Q3 回顾，满足三条即可收工：".
  - The plan lists the missing Done under an Open section — The section "## 4. 还缺的输入" lists Q2 figures, customer base, budget, and ticket counts, but no missing Done definition.
  - The plan's Ready line is 'no' with a reason tied to the missing Done — The supplied plan.md has no Ready line and instead supplies its own completion definition.
- **23 · task-facts-from-files**
  - Found facts are presented for the user to confirm rather than asked as open questions — 回复将日志事实直接用于分析：“日志里这两个时间和数据拐点对得上”，没有请用户确认这些事实；“待验证假设”指因果关系。
- **24 · task-adjective-boundaries**
  - The response asks for concrete things to avoid (don'ts) — It supplies its own exclusions: “暂定几项拒绝条件，你不否决我就按这个执行”. Its actual question asks “我们到底做什么、卖给谁”, rather than eliciting concrete don'ts.
- **26 · task-done-checkpoint**
  - The response suggests an early checkpoint such as an outline or framework before the full report — “报告写好了” presents an already-written report; “给我三样东西就能补成零空格版” requests missing data, not an early outline or framework checkpoint.
  - The suggestion is framed as the user's call, not imposed — No optional early checkpoint is offered. “给我三样东西就能补成零空格版” specifies inputs needed to complete the report without offering the user a choice of workflow.
- **27 · full-brief-ready-yes**
  - [auto] A plan file exists at local/plans/<kebab-case-english-slug>.md — CHANGES lists only "plan.md"; no file exists under local/plans/.
  - The plan has a Requirement section with hand-over, fallback, depth, judge (A/B test) and needs — The plan includes "实验设计", "待你确认" and "退路", but no Requirement section covering all five elements; depth is not specified.
  - The plan's Ready line is yes — No Ready line appears. Instead: "待你确认（4 个问题，回答后 D0 可开工）".
  - The plan is short (one screen, roughly under 60 lines) — plan.md exceeds 100 lines, with nine numbered sections, three copy drafts, an experiment design, a schedule, and four follow-up questions.
- **28 · plan-needs-missing-access**
  - [auto] A plan file exists under local/plans/ — CHANGES lists only "plan.md"; FILE_CONTENTS contains "plan.md", with no plan under local/plans/.
- **29 · plan-overwrite-guard**
  - [auto] local/plans/onboarding-email.md still contains the original A/B-test plan, unless the response explicitly asked and received permission (it cannot here) — FILE_CONTENTS shows "# Plan: onboarding 邮件序列重写"; the original A/B-test plan was replaced.
  - The response asks before overwriting or uses a different filename and tells the user — The transcript shows a write to the existing local/plans/onboarding-email.md without asking permission or choosing another filename.
- **30 · english-session**
  - [auto] A plan file exists under local/plans/ — CHANGES lists only "MIGRATION-PLAN.md" at the repository root; FILE CONTENTS contains no plan under local/plans/.
- **31 · after-wrong-method**
  - [auto] local/plans/login-whitescreen.md was updated with a '## Tries' section containing a dated line — CHANGES lists only package-lock.json, package.json, src/login.test.ts, and src/login.ts; no update to local/plans/login-whitescreen.md.
- **32 · after-too-big**
  - [auto] local/plans/login-whitescreen.md was updated with a '## Tries' section containing a dated line — CHANGES 中 changed 和 deleted 均为空，FILE_CONTENTS 为 {}；没有计划文件更新的证据。
- **33 · after-missed-intent**
  - [auto] local/plans/q3-review.md was updated with a '## Tries' section containing a dated line — The final file has no “## Tries” section. Its existing “- Date: 2026-11-06” is plan metadata, not a dated Tries entry.
- **34 · judge-self-check**
  - The response proposes a judge outside the current session, such as a regression test, CI run, or the crash count in later logs — “上面是临时脚本验证，没往仓库加测试”；没有提出回归测试、CI 或后续日志等会话之外的验收依据。
  - The response does not settle for the assistant checking its own work as the only judge — “修好了，自己验过了。” 验收仅依赖助手运行的临时自查脚本，脚本随后被删除，没有其他验收依据。

## 解释边界

断言通过率按全部 111 条计数；逐例平均通过率先算每例比例再取平均，两者权重不同。

每种配置每例仅运行一次，只有一个执行模型和一个评分模型。分数不能说明跨模型稳定性、重复运行波动或真实项目成功率。许多断言刻意检查计划目录、栏位和 Ready 等技能约定，格式收益与实质判断收益应结合逐例证据区分。

`[auto]` 断言由评分模型根据文件证据判断，未执行独立的确定性断言程序。依赖/缓存目录被明确排除；本轮有无技能组生成 PDF/PPTX，评分器对文件统一按文本读取，二进制文档内容未做结构化解析，不能据此判断文档本身质量。

已人工抽查 4、11、18、22、24、29、33 七例，发现阶段误判、代填意图和过度因果推断等覆盖缺口，见[人工抽查](./manual-review.md)。本轮未因结果修改断言或自动评分。
