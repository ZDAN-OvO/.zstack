TOOL bash: {"command": "pwd; ls -la; echo \"---\"; find . -maxdepth 3 -type d -not -path '*/.git/*' | head -50"}

TOOL bash: {"command": "echo \"PI env:\"; env | grep -i '^PI_' | sed 's/=.*/=<set>/'; echo \"---git---\"; git rev-parse --show-toplevel 2>/dev/null; git log --oneline -5 2>/dev/null"}

RESULT: /tmp/pf-15-with_skill-7f_i_41p
total 184
drwxrwxr-x  4 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 64 root root 167936 11月 10 22:35 ..
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 data
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 notes
-rw-rw-r--  1 zdan zdan    131 11月 10 16:17 template.md
---
.
./data
./notes


RESULT: PI env:
PI_COMPUTER_USE_CHROME_EXECUTABLE=<set>
PI_CODING_AGENT=<set>
PI_REASONING_LEVEL=<set>
PI_PROVIDER=<set>
PI_CACHE_RETENTION=<set>
PI_MODEL=<set>
PI_SESSION_ID=<set>
---git---


Command exited with code 128

TOOL bash: {"command": "ls -la data notes; echo \"=== template.md ===\"; cat template.md"}

TOOL bash: {"command": "for f in notes/*; do echo \"=== $f ===\"; cat \"$f\"; echo; done"}

RESULT: data:
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  126 11月 10 16:17 q3-metrics.csv

notes:
total 12
drwxrwxr-x 2 zdan zdan 4096 11月 10 16:17 .
drwxrwxr-x 4 zdan zdan 4096 11月 10 16:17 ..
-rw-rw-r-- 1 zdan zdan  182 11月 10 16:17 worklog.md
=== template.md ===
# Q3 业务回顾

## 收入
本季收入：{{revenue}}

## 客户
新增：{{new}}，流失：{{churn}}

## 下季计划
{{plan}}


RESULT: === notes/worklog.md ===
# 工作日志

- 9 月 8 日起，客服工单里"太难上手"的投诉明显变多。
- 8 月中旬把免费试用从 14 天改为 7 天。
- 老板说 QBR 下周四给 VP 看。



TOOL bash: {"command": "cat data/q3-metrics.csv"}

RESULT: month,revenue_usd,new_customers,churned_customers,nps
2026-07,182000,41,12,38
2026-08,176000,35,19,31
2026-09,171000,30,24,27


TOOL bash: {"command": "date +%F; ls -la local 2>/dev/null; ls /home/zdan/.zstack/skills/plan/preflight/references/ 2>/dev/null"}

TOOL bash: {"command": "sed -n 1,80p /home/zdan/.zstack/skills/plan/preflight/references/ambition.md"}

RESULT: 2026-11-10
ambition.md
task-definition.md


RESULT: # Ambition: distilled

Source of the Requirement axes and the judge in `/preflight`. Distilled from Felix Rieseberg (engineering lead on Claude at Anthropic):

- **[E]** Essay, "How to be more ambitious: A tutorial for humans with models", 2026-10-13. <https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/>
- **[I]** Interview, Silicon Valley Girl, "Claude Engineering Lead: Stop Using Claude Like It's 2024", 2026-10-20. <https://www.youtube.com/watch?v=D-SVFneJ_Nk>. Timestamps are approximate and come from the auto-captions.

## Thesis

- **Best guess.** A task given to the model is the user's best guess at a route to an outcome. The model runs the guess. [E]
- **Four types.** Ambition comes in four types: speed, altitude, depth and range. Speed means the same work done faster. It is well established and needs no new thinking, so the skill leaves it out. [E]
- **Self-efficacy.** People are held back by what they believe is possible. Specific, hard goals beat "do your best" (Locke and Latham, 35 years of studies). Belief, a visible precedent and permission to fail all raise what gets attempted. The studies are on humans; carrying them over to models is Felix's extension. [E]

## Altitude

- **Goal beyond the goal.** Ask what should happen next, then hand that over. The crash example climbs from "fix this crash" to "keep the apps crash-free". [E]
- **Ceiling.** Keep climbing until the model fails. "Go make money" is past the line today. Work at the ceiling sits at the frontier and gains the most from the next model. [I 39:05]
- **Fit.** Altitude fits work after an ultimate outcome. Work that will be discussed in meetings is a good sign. It fits creative work less well. [E]
- **Workflow cost.** Climbing usually means rebuilding access first. Crash-free needed crash-report fetching, a version-to-commit map, and Windows, macOS and Linux machines to reproduce and verify on. The setup cost is real and worth paying. [E] [I 22:39]
- **Conveyor belt.** A user who carries items to the model one at a time is the bottleneck. Give the model the whole data source and let it choose what to act on. [I 22:39]

Worked ladder, a quarterly business review [E]:

1. Update the template's numbers.
2. What changed this quarter, why, and what to do.
3. The three most urgent decisions, with the case for and against each.
4. Replace the deck with a better way for leadership to catch problems early and move money and people. Prove on past history that it would have caught them sooner, then run it beside the deck for a quarter.

## Depth

- **Instruments, not costume.** A persona switches the vocabulary and keeps the method. Ask which tools the top of the field uses, then require those tools, and get the result explained plainly. The leap in AI 3D and motion work came from using Blender, not from a better grasp of animation. [E] [I 10:28, 25:20]
- **Stretch target.** Set an unreasonable goal and treat it as reasonable: 200 ms, not 5 s. When the model says it is impossible, tell it to keep going. [E]
- **Challenge beliefs.** Give the model the raw data and have it try to reproduce a belief the user holds ("churn is an onboarding problem"). [E]
- **New knowledge.** From inside the data, look for the blind spot: an unknown early signal, shown to predict data it has not seen. [E]
- **Expert questions.** Before the task is rewritten, name four things: (1) what a top professional would do that is not being asked; (2) the rawest material they would start from; (3) their specific methods and tools; (4) what, other than the model or the user, would show the result is right. Then rewrite the task to ask for exactly that. [E]
- **Process.** For work that rests on taste, the gain comes from copying the steps professionals take, since good work comes out of a refined process. [I 8:26–9:52]

## Range

- **Noun to verb.** A deliverable's name hides its job. A quarterly review is not "a deck". It gets busy people to believe a cause-and-effect story and decide under uncertainty in 30 minutes. The verbs show which fields can help. The idea comes from Kelley and Littman, *The Art of Innovation*. [E]
- **Crew.** Ask which team would be assembled if the stakes were extreme. For the review: an analyst, a journalist and an editor; a motion and audio designer if it is presented; a short seller and a forensic accountant as the red team. [E]
- **Do, not write.** Use the crew to find fields and techniques. Ask the model to do the short seller's research, not to write in a short seller's voice. Role play makes the transcript stranger and the output no better. [E]

## Judge

- **Outside session.** The session that did the work is a poor judge of it. Far more tasks are unsafe to trust to a single session than to the model. Prefer a check the model can run and get feedback from at once. [E] [I 26:10]
- **Grade the process.** A correct guess of the temperature fails. A half-degree miss that came from the right location and a reputable source passes. [I 7:35]
- **Adversarial review.** When nothing hard can check the work, spin off sessions whose only job is to prove the output wrong, as red teams and short sellers do. Finding flaws is easier than building, so a cheaper model can do the attacking. Then one more session rules on which objections hold. Valid objections go back to the maker, which can decline them. [I 12:57–15:39]
- **User as client.** When the user can tell good from bad themselves, their judgment of the result is enough. When they cannot, add more AI review. [I 16:15]
- **Fact checks.** Requiring a verified primary source for every number in a document can be trusted to a single session. [I 17:03]

## Access

- **Model experience.** Picture yourself as the model doing this task. You would want the raw data, a computer, the ability to install software, and room to decide for yourself. [I 22:01]
- **Prerequisite.** Every type of ambition needs a computer that can install software, plus access to the relevant data. [E]
- **Start cheap.** Let the model drive the user's tools in a browser first. Build connectors only after a workflow has proven itself. [I 24:00]
- **Generalists.** Give a generalist model the tools and the data rather than a cast of narrow persona agents with pre-sliced data. Generalist models overtook a purpose-built math system within months. [I 17:37]

## On skills

- **Half-life.** Skills often carry advice meant for the previous model generation, and removing a skill sometimes improves the output. Making that call takes an eval and a clear sense of good and bad output. [I 21:26]


TOOL write: {"path": "/tmp/pf-15-with_skill-7f_i_41p/local/plans/q3-churn-diagnosis.md", "content": "# 计划：Q3 流失上升——归因与决策\n\n- 原始需求：你现在是资深数据分析师，帮我分析 Q3 为什么流失变多\n- 阶段：execute（要的是分析；但\"这份分析服务哪个决定\"未定）\n- 日期：2026-11-10\n\n## Requirement\n交付：不是\"流失原因解释\"，而是下周四 QBR 上 VP 能拍板的三个决定（正反论证＋影响金额），并附一个\"本可在 8 月就发现\"的留存警示信号——用 Q3 数据回测证明。\n后备：只做归因排序 + 决策选项（不含回测与实验设计）。\n深度：\n  最原始材料：客户级明细（注册日、试用/转正、套餐、流失日期、流失原因原文、末次活跃、工单原文），不是 3 行月度汇总。\n  工具：队列留存三角表、hazard/生存模型、率×结构分解、控制图分信号与噪声、工单与流失原因人工编码、试用改动的 DiD。\n  拉伸目标：用 7–8 月数据建提前一个月的流失预警打分，在 9 月留出数据上验证（AUC/命中率进附录）。\n  实测信念：先证伪\"流失变多\"——按可流失口径（剔试用未转化）流失率是否仍涨；涨幅是否只出现在 8/14 试用改动之后的新队列。\n范围：\n  动词：判真假 → 定位（谁/何时/哪类）→ 定量（户数＋金额）→ 归因排序 → 给决策 → 提前拆台。\n  团队：留存/队列分析师（生存分析）；指标审计（专拆口径与数据质量）；实验统计（DiD/holdout）；客服/用户研究员（编码工单、读原话）；财务 BP（流失换算 ARR 与 Q4 重估）；红队（主张\"流失率没涨，是获客掉下来\"）。\n判官：9 月留出数据回测（预警分必须在没见过的数据上有效）+ 一手原文逐条佐证每个归因；另开攻击会话 + 一个裁决会话。评方法：口径是否先查、每条结论是否有证据链；\"猜对了但没验证\"判失败。\n需要：客户级明细 ❌；流失口径定义 ❌；试用改动变更记录 ⚠️仅工作日志一句；工单原文 ❌；去年同期 Q3 ❌；10 月数据能否在周四前拿到 ❓\n已否决：暂无（待你裁决）\n\n## Task\n目的：待你回答。工作日志只说\"下周四 QBR 给 VP 看\"——那是动作。可能的决定：①试用期是否改回 14 天 ②是否给 onboarding 投人/钱 ③Q4 收入是否重估 ④只是让 VP 知道数字难看。选哪个，分析重点完全不同。\n背景（我查到，请确认）：\n  - 只有 2026-07/08/09 三行月度汇总：收入 182k→176k→171k，新增 41→35→30，流失 12→19→24，NPS 38→31→27。\n  - 8 月中旬试用期 14 天改为 7 天；9/8 起工单\"太难上手\"变多。\n  - 三件事同向变动，三个月度点无法分辨因果；\"12→19→24\"很可能是口径/结构效应（试用缩短→新增变少→可流失基数变化）。\n材料（优先级）：\n  一手：CRM/事件导出的客户级明细；工单原文；试用改动变更记录；订阅/账单明细（金额口径流失）；去年 Q3 同期。\n  二手：data/q3-metrics.csv（汇总、已加工，撑不起因果）；notes/worklog.md（同事转述）。\n  禁用：只凭 3 行汇总推因果；拿 NPS 当流失原因代理；编造行业基准；把\"太难上手\"当结论。\n  空位：客户级明细在本工作区完全缺失。\n边界（会让你说\"这不是我要的\"）：\n  - 没有分母/口径的\"三大原因\"清单；用三个点断言因果；把试用改动当既成结论。\n  - 用通用流失框架凑页数，不落到我们的数字。\n  - 把\"没有客户级数据\"藏在自信措辞后面；为数字好看悄悄改流失口径。\n  - 客户名/PII 进 deck。\n  （此栏请你补：哪些输出你绝对不能接受）\n完成：\n  检查点：先给一页\"数据能回答什么/不能回答什么 + 三个候选原因及各自验证方法\"，你点头再往下做。\n  交付物：QBR 用 2 页结论 + 一页\"结论→证据\"附录 + 决策建议（含金额与置信度）。\n  何时停：VP 那句\"那我们做什么\"有答案，且每个数字都能指到来源。\n\n## Open\n- 这份分析服务哪个决定？\n- 流失口径：按户数还是金额？含不含试用未转化？主动/被动怎么算？\n- 客户级明细在哪个系统、谁能给，周四前能否拿到？\n- 试用改动可逆吗？老板是否已预设结论？\n\nReady: no —— 目的、口径、数据可得性三项未定；Requirement 三条动议待你裁决。\n"}

RESULT: Successfully wrote to /tmp/pf-15-with_skill-7f_i_41p/local/plans/q3-churn-diagnosis.md

ASSISTANT: 看完工作区了，先说三个硬事实，再说计划。

**Look 发现的问题**
- `data/q3-metrics.csv` 只有三行月汇总：收入 182k→176k→171k，新增 41→35→30，**流失 12→19→24**，NPS 38→31→27。
- `notes/worklog.md`：8 月中旬试用期 14 天→7 天；9/8 起工单"太难上手"变多；下周四 QBR 给 VP 看。
- 关键：流失人数翻倍的同时**新增从 41 掉到 30**，而试用期正好在 8 月中被砍半。用三个月度点讲"为什么"，最可能的产出是一个听起来对、但没被检验过的因果故事——而且很可能是错的：如果流失率的分母是"当期活跃账户/转正数"，试用缩短会自己把流失率推上去。

所以计划里我把"先证伪'流失变多'"放在第一层，而不是第四层。

**计划已写到** `local/plans/q3-churn-diagnosis.md`

- 交付：下周四 VP 能拍板的三个决定（含金额、正反论证）+ 一个用 Q3 数据回测过的留存警示信号
- 后备：只做归因排序 + 决策选项
- 深度：客户级明细、队列留存/生存模型、率×结构分解、工单原文编码、试用改动的 DiD；拉伸目标是用 7–8 月建预警分、在 9 月留出数据上验证
- 判官：留出数据回测 + 一手原文逐条佐证，另开攻击会话和裁决会话；猜对了但没验证 → 判失败
- 需要但目前没有：客户级明细、流失口径定义、工单原文、去年 Q3 对比

**只有你能答的四件事**（其余我都不会猜）
1. 这份分析最终服务哪个决定？是"试用期要不要改回 14 天"、"onboarding 要不要投钱"、"Q4 收入要不要重估"，还是只是汇报？
2. 流失口径：按户数还是金额？含不含试用未转化？主动/被动怎么分？
3. 客户级明细在哪个系统、谁能给，周四前拿得到吗？（拿不到就要落到后备方案）
4. 试用改动可逆吗？老板是不是已经预设了结论？

这四项一填，`Ready` 就转 yes。之后可以直接 `/define-goal`，以这份计划为源。