TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/SKILL.md"}

RESULT: ---
name: preflight
description: >-
  Write a one-screen plan the user reads to check their own thinking before AI runs the work: could the requirement aim higher, deeper or wider, and can the user state the task's purpose, context, materials, boundaries and done? Use when a request is one step of a bigger result ("fix this bug", "fill in the template"), when quality matters in a field the user is not expert in, when a deliverable is named by its noun ("homepage", "weekly report"), when the user cannot say what done looks like, or when a planned result came back rejected.
---

# Preflight

A request is the user's guess at one step toward an outcome they have not stated. The model carries out the step as written and does not question the intent behind it. So two gaps go unseen until the output lands:

- **Requirement**: the request undershoots what the model could own today.
- **Task**: the intent is still unformed. The model mirrors vagueness back as a generic output.

This skill brings both gaps into one plan that the user reviews before execution. The user's thinking is the subject. Writing the goal and doing the work come after the plan.

## Enter

Offer the plan in one line, and go on only if the user accepts. When a redo costs less than a plan (a rename, a lookup), do the request as written. The plan pays off when a wrong output costs a meeting, a handoff or a long unattended run.

## Look

Read the files, data and history the request touches. Facts you can look up go into the plan as facts. The questions you ask are about intent, which no file holds.

## Stage

Match the request to the user's stage. A request made one stage too early gets a hollow answer: a draft with no thesis, or a recommendation built on guessed criteria.

- **Think**: ask questions that turn the vague into the concrete.
- **Explore**: map the options and their trade-offs.
- **Decide**: weigh the options against the user's decision logic.
- **Execute**: continue with this skill.

## Requirement

Suggest moves on three axes. The user accepts, rewrites or declines each one, and a declined move is recorded with its reason.

- **Altitude**: hand over the outcome, not the step. Ask what should happen after this result, and climb rung by rung. Stop when a rung plainly exceeds what models can own today. That **ceiling** is only found by trying, so the rung below it becomes the **fallback**. Altitude fits outcome-driven work, and work that will be discussed in meetings is a good sign. It fits creative work less well. Climbing often requires changes to the workflow, such as data access, version-to-commit mapping and machines to reproduce on.
- **Depth**: do the task the way a field-leading expert would, one layer below the request. Name the expert move the user did not ask for, the rawest material, and the instruments of the field (databases and statistical models rather than tables). The instruments change the method. A persona only changes the vocabulary. Where it fits, add a **stretch target** that forces a different method, or a test of a belief the user holds, run against raw data, or a new finding shown to predict data it has not seen.
- **Range**: restate the deliverable's noun as verbs, the effect it must have on people. Then assemble the **crew** of fields that do those verbs best, including a **red team**. Ask for what each field *does*, not how it sounds.

Every axis needs a **judge** outside the session that did the work. The judge grades the method as well as the result, because a lucky correct guess should fail and a sound near-miss should pass. Prefer a check the model can run itself (a test, held-out data, a primary source). Otherwise, use separate attacker sessions plus one more session that rules on their objections. When the user can judge the result directly, their judgment is enough.

## Task

Ask the five intent questions. Each one has an answer only the user holds:

- **Purpose**: the decision or problem the output serves. An action ("analyse five competitors") is not a purpose.
- **Context**: what a capable stranger would need to know so they do not aim wrong.
- **Materials**: the sources ranked primary over secondary, the banned sources, and an empty slot for anything not found. An unranked or unbounded source list invites fabrication.
- **Boundaries**: the outputs that would make the user say "not what I wanted". These are **walls**, mostly "don'ts". Directions and adjectives do not count.
- **Done**: what appears in front of the user that means stop. It includes the shape of the artifact and an early **checkpoint**, such as an outline before the full piece, so a wrong direction is caught cheaply. Boundaries and Done together give the scope.

The model can ask these questions, and only the user can answer them. Write each answer in the user's words. Facts you found can go into Context or Materials, marked for the user to confirm. A slot the user cannot answer goes under Open. The gap itself is the finding, so it is never filled with a plausible guess.

## Write

Write `local/plans/<topic>.md` at the workspace root (the git root, or the current directory). `<topic>` is a short kebab-case English slug of the outcome. Ask before you overwrite a file from another task. Use the user's language and keep the plan to one screen:

```markdown
# Plan: <outcome in a few words>

- Asked: <the request as the user wrote it>
- Stage: execute
- Date: <YYYY-MM-DD>

## Requirement
Hand over: <accepted rung>
Fallback: <rung below>
Depth: <raw material; instruments; stretch target>
Range: <verbs; crew and what each does>
Judge: <the outside check, and what it grades>
Needs: <data, access, machines; mark what is missing>
Declined: <move, reason>

## Task
Purpose:
Context:
Materials:
Boundaries:
Done:

## Open
<what the user has not thought through yet; omit when empty>

Ready: <yes | no, because …>
```

`Ready` is yes when the user has ruled on every Requirement move and answered all five Task slots. The plan is done when the user has read it and confirmed the Ready line. Close with the path, and offer `/define-goal` with the plan as its source.

## After a try

When the user brings back a rejected result, find the cause and act on it:

- **Wrong method** (a missed diagnosis, a missing source): use more Depth on the same rung.
- **Too big**: take the Fallback.
- **Missed intent**: go back to the Task slot that let the miss through.

Update the plan in place, and add one dated line under `## Tries` with the verdict and what changed.

## References

- [references/ambition.md](references/ambition.md): the source of the Requirement axes and the judge, with a worked ladder and the expert questions. Read it when a Requirement move needs grounding.
- [references/task-definition.md](references/task-definition.md): the source of the stages and the five slots, with a worked brief. Read it when a Task question needs grounding.


TOOL bash: {"command": "cd /tmp/pf-5-with_skill-8mgwyr8n && ls -la && git rev-parse --show-toplevel 2>/dev/null"}

RESULT: total 172
drwxrwxr-x   2 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 112 root root 167936 11月 10 18:00 ..
-rw-rw-r--   1 zdan zdan      0 11月 10 16:17 .keep


Command exited with code 128

TOOL bash: {"command": "date +%Y-%m-%d; date +%A"}

RESULT: 2026-11-10
星期二


TOOL write: {"path": "/tmp/pf-5-with_skill-8mgwyr8n/local/plans/weekly-report.md", "content": "# Plan: 本周周报\n\n- Asked: 帮我写本周周报，下午要交给主管\n- Stage: think（工作区是空的：没有任何本周材料，意图也没定）\n- Date: 2026-11-10（星期二）\n\n## Requirement\nHand over: 一份能让主管读完做出一个具体动作的周报（批资源 / 调优先级 / 放行下一步），而不是活动流水账\nFallback: 按公司模板写清楚「做了什么 + 卡在哪 + 下周计划」的一页纸\nDepth: 专家动作是把它写成**论证**不是日志：每条进展对应目标、每个风险带日期和影响、每个请求带成本和替代方案。原始材料＝你自己的痕迹（git log、工单、日历、文档、群聊），不用回忆。拉伸目标：每行都能回答「主管因此知道了什么 / 要做什么」；并检验一个信念——「主管要看工作量」是否成立（看看他上周实际回应了哪条）\nRange: 动词＝告知、要决定、保时间、对齐优先级、提前暴露风险。班子：项目经理（把请求写成成本收益）、编辑（压到一屏、去掉修饰）、红队（用主管的视角逐行问「所以呢？为什么现在？」）\nJudge: 红队一版＋逐条对原始痕迹核对（每个数字有出处）——既判方法（风险有没有日期、请求有没有成本）也判结果；最终以你的判断为准\nNeeds: 本周的提交记录 / 工单 / 日历 / 文档 / 聊天记录；公司周报模板与字数要求。**全部缺失，需你提供或授权我读取**\nDeclined: —\n\n## Task\nPurpose: 〈待你答：主管读完这份周报要做什么决定？〉\nContext: 〈待你答：主管关心什么？团队这季度在追什么目标？「本周」指 11/02–11/06 还是本周一到今天？〉\nMaterials: 〈待你答：上面哪几项能给我（仓库/工单/日历）？公司模板在哪？〉\nBoundaries: 〈待你答：哪些写法你会说「不是我要的」——比如不夸大、不甩锅、不列琐事、不隐瞒延期〉\nDone: 一屏、贴合公司格式的中文周报；**先给你 3–5 条要点提纲过目**，你点头再写全文\n\n## Open\n- 时间口径：「本周」是上周（11/02–11/06）还是本周至今（只有周一周二）\n- 全部原始材料缺失：不给材料我写出来的只会是通用套话\n- 交付时间：现在已 18:00，「下午」是否已过期，需不需要先发一版占位\n\nReady: no —— 五个 Task 槽全空，且没有任何本周材料\n"}

RESULT: Successfully wrote to /tmp/pf-5-with_skill-8mgwyr8n/local/plans/weekly-report.md

ASSISTANT: 我先不直接写，因为两份检查表里最重要的一项现在是空的：**我手上没有任何你这周干了什么的材料**（工作区是空目录）。硬写只会得到一份谁是主管都能套用的周报——那种交上去最伤。

计划已写好，你过一眼：`local/plans/weekly-report.md`

省你时间，直接回这几条（能答几条答几条）：

1. **主管读完要做什么决定？**（批资源／调优先级／只是知情——这决定周报的写法）
2. **「本周」指哪几天？** 今天星期二 18:00，是补上周（11/02–11/06）还是本周一到现在？
3. **材料给我哪几个？** 仓库路径、工单导出、日历、周会文档、群聊——给路径我自己读，比你回忆准。
4. **公司有模板吗？**（格式/字数/是否要下周计划）
5. **哪些写法你会说「不是我要的」？** 比如不夸大、不甩锅、不列琐事、不隐瞒延期。

我建议把目标抬一档：不是「交一份周报」，而是**让主管读完做出一个动作**。所以正文我会写成「进展→对应目标」「风险→带日期和影响」「请求→带成本和替代方案」，而不是罗列我做了啥。认可就这么定；不认可就说一句，我按 Fallback 降回模板式。

另外提醒一句：现在 18:00，「下午交」可能已经过了。要不要我先出一版**只占位、不含虚构内容**的骨架（做了什么留空给你填／或填我读到的材料），先发过去？

材料一到，我先给你 3–5 条要点提纲，你点头我再写全文——不让你在错的方向上等我写完。