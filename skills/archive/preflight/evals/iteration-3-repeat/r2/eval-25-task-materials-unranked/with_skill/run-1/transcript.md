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

Each section below ends at a **stop**: the point where this turn's reply is sent. Reaching a stop ends the skill for this turn, even when later sections are still unread.

## Enter

1. **Cost.** When a redo costs less than a plan, do the request as written, or ask only the one or two details it needs. A rename, a lookup and a short poem or message are this case, even when the user typed `/preflight`. The plan pays off when a wrong output costs a meeting, a handoff or a long unattended run. Stop.
2. **Consent.** The user typed `/preflight`, or accepted an offer: go on to Look. Otherwise offer the plan in one line and stop. Until the user accepts, the workspace stays unchanged, and that includes `local/plans/`: a plan file written before acceptance is a plan the user never asked for.

Accepting the plan is consent to plan, not to execute. From Look onward, the only file this skill writes is the plan; the work itself starts after the user confirms it.

## Look

Read the files, data and history the request touches. Facts you can look up go into the plan as facts. The questions you ask are about intent, which no file holds.

State each finding at the strength the data supports. Two things that change at the same time are a correlation to test. A cause needs evidence that rules the alternatives out.

## Stage

Match the request to the user's stage. A request made one stage too early gets a hollow answer: a draft with no thesis, or a recommendation built on guessed criteria. Only Execute goes on to Requirement and writes a plan. Each earlier stage gives its own result and stops.

- **Think** (no thesis or no direction yet): ask the questions that turn the vague into the concrete. Stop.
- **Explore** (options named, criteria not set): map the criteria that would separate the options, and the trade-off under each. Ask for the few facts that decide between them, and leave the choice open. Stop.
- **Decide** (options and criteria both given): weigh the options against the user's criteria and give the decision, with the conditions that would reverse it. Stop.
- **Execute** (the user wants the work done): continue with this skill.

## Requirement

Look at the task through all three lenses in this turn. Suggest a move only on a lens where it would change the result, and write `not needed` for the others. A deliverable named by its noun (a deck, a homepage, a report) always gets a Range move. Each suggestion stays a suggestion until the user accepts, rewrites or declines it. A declined move is recorded with its reason. When the user has already ruled on the moves offered earlier in the conversation, the Requirement is settled: record their rulings and open no new moves. A risk you notice goes under Open as a question.

- **Altitude**: hand over the outcome, not the step. Ask what should happen after this result, and climb rung by rung. Stop when a rung plainly exceeds what models can own today. That **ceiling** is only found by trying, so the rung below it becomes the **fallback**. Altitude fits outcome-driven work, and work that will be discussed in meetings is a good sign. It fits creative work less well. Climbing often requires changes to the workflow, such as data access, version-to-commit mapping and machines to reproduce on.
- **Depth**: do the task the way a field-leading expert would, one layer below the request. Name the expert move the user did not ask for, the rawest material, and the instruments of the field (databases and statistical models rather than tables). The instruments change the method. A persona only changes the vocabulary. Where it fits, add a **stretch target** that forces a different method, or a test of a belief the user holds, run against raw data, or a new finding shown to predict data it has not seen.
- **Range**: restate the deliverable's noun as verbs, the effect it must have on people. Then assemble the **crew** of fields that do those verbs best, including a **red team**. Ask for what each field *does*, not how it sounds.

Every move needs a **judge** outside the session that did the work. The judge grades the method as well as the result, because a lucky correct guess should fail and a sound near-miss should pass. Prefer a check the model can run itself (a test, held-out data, a primary source). Otherwise, use separate attacker sessions plus one more session that rules on their objections. When the user can judge the result directly, their judgment is enough.

## Task

Ask the five intent questions. Each one has an answer only the user holds:

- **Purpose**: the decision or problem the output serves. An action ("analyse five competitors") is not a purpose.
- **Context**: what a capable stranger would need to know so they do not aim wrong.
- **Materials**: the sources ranked primary over secondary, the banned sources, and an empty slot for anything not found. An unranked or unbounded source list invites fabrication.
- **Boundaries**: the outputs that would make the user say "not what I wanted". These are **walls**, mostly "don'ts". Directions and adjectives do not count.
- **Done**: what appears in front of the user that means stop. It includes the shape of the artifact and an early **checkpoint**, such as an outline before the full piece, so a wrong direction is caught cheaply. Boundaries and Done together give the scope.

The model can ask these questions, and only the user can answer them. Use what the user has already said in this conversation, and ask only for what is missing. Write each answer in the user's words. Facts you found can go into Context or Materials, marked for the user to confirm.

A Purpose or Done the user cannot answer stays empty, and the question goes under Open. The gap itself is the finding. Ask a question that helps the user answer it, and write no default for them to approve. For Materials, you may propose a source ranking, banned sources and a leave-blank rule; they go under Proposed for the user to rule on.

## Write

Write `local/plans/<topic>.md` at the workspace root (the git root, or the current directory). `<topic>` is a short kebab-case English slug of the outcome. Write the plan in the same turn as Requirement and Task, with unanswered slots under Open; Ready tells the user what is still missing.

Check the path before the write. When a file there belongs to another task, keep it unchanged. Ask which path to use, or write to a new slug and name it in the reply. A backup copy does not count as permission to overwrite.

Use the user's language and keep the plan to one screen:

```markdown
# Plan: <outcome in a few words>

- Asked: <the request as the user wrote it>
- Stage: execute
- Date: <YYYY-MM-DD>

## Requirement
Hand over: <accepted rung, or the request as asked>
Fallback: <rung below>
Depth: <raw material; instruments; stretch target | not needed>
Range: <verbs; crew and what each does | not needed>
Judge: <the outside check, and what it grades>
Needs: <data, access, machines; mark what is missing>
Proposed: <moves the user has not ruled on yet; omit when the user has ruled on them all>
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

`Ready` is yes when the user has ruled on every proposed move and answered all five Task slots. The plan is done when the user has read it and confirmed the Ready line. Close with the path, and offer `/define-goal` with the plan as its source. Stop.

## After a try

When the user brings back a rejected result, find the cause and act on it:

- **Wrong method** (a missed diagnosis, a missing source): use more Depth on the same rung.
- **Too big**: take the Fallback.
- **Missed intent**: go back to the Task slot that let the miss through.

Update the plan in place, and add one dated line under `## Tries` with the verdict and what changed. Stop.

## References

- [references/ambition.md](references/ambition.md): the source of the Requirement axes and the judge, with a worked ladder and the expert questions. Read it when a Requirement move needs grounding.
- [references/task-definition.md](references/task-definition.md): the source of the stages and the five slots, with a worked brief. Read it when a Task question needs grounding.


TOOL bash: {"command": "ls -a; echo \"---\"; git rev-parse --show-toplevel 2>/dev/null || echo \"no git\""}

TOOL bash: {"command": "timeout 8 curl -sS -o /dev/null -w \"%{http_code}\\n\" https://www.bing.com 2>&1 | tail -2; echo \"---dns---\"; timeout 5 getent hosts trae.ai 2>&1 | head -2"}

RESULT: .
..
.keep
---
no git


RESULT: 200
---dns---
198.18.0.142    trae.ai


ASSISTANT: 这个请求目前不适合直接写成方案，因为它处在 **Explore** 阶段：工具集只给到“国内 AI 编程工具”这个市场，还不是具体名单；选型标准也没有给出。这种情况下，我直接交一份价格表，最可能的结果是一张在计量单位上无法比较、既没法回答“买哪家”、还要你重新做的表格。

先确认两件事：

- 环境有外网（已实测通过），所以“上网找”可行。但官网定价页只能作为二手材料：国内企业版的真实单价基本要走销售报价，公开页面常常只有个人版或“联系销售”。我会为每条价格标注出处，以及抓取日期（报价一周内就会变不同）。
- 定价本身很少是决定因素。同样的席位数量下，结论可能完全相反：

**能区分选项的标准及各自的取舍：**

1. **计费单位**：按席位月付，还是按用量（token、请求数）计费，各有免费额度。团队 10 人和 200 人会倒向不同答案；按用量计费在重度使用者身上成本可能高出数倍，而轻度使用者的平均成本更低。
2. **采购门槛**：支持对公付款、发票、年框合同、SSO/SCIM、审计日志，有没有私有化或专属实例。很多“便宜”的选项在你们采购流程里根本无法走通，它的价格就不是真实成本。
3. **代码出不出境**：这会不会直接决定选项集合？必须境内存储，还是只要厂商在境内即可？如果要考虑 Cursor/Copilot 在国内的可用性与合规问题，选项集合会完全不一样。
4. **能力边界**：只有 IDE 内的补全，还是也覆盖 Agent 式多文件改造、在 CI/终端里运行、对私有代码库检索。相差一个档位，价格就没有可比性。
5. **模型来源**：自研还是套用第三方模型，这关系到明年涨价和断供的风险。这项不属于价格，但会影响“下季买”这个决定的质量。
6. **工具链契合度**：VS Code、JetBrains、终端、自建 GitLab 各支持到什么程度，以及团队要改多少现有工作流。
7. **价格稳定性**：季付还是年付折扣、历史涨价记录、试用和退出成本。

**请你回答以下几个能直接决定结论的事实：**

- 团队人数，其中真正重度写代码的有几人？这一项会决定按席位计费还是按用量计费，哪个更便宜。
- 现在用什么工具、为什么想换？这是为了防止得到一个“换了个更贵的”结论。
- 数据必须在境内或必须私有化吗？
- 预算区间或人均月上限是多少？下季什么时候必须落地？
- 谁签字批准，即是否需要走正式的采购、招标流程？

如果你不想回答这些，也可以直接说“就按公开价格排个表”。我会照做，但在表格里明确标出计量单位不可比的地方，以及哪几格是缺失值，而不是编造数字。

你回答完这几个问题后，就到了 Decide 阶段，我会写方案并直接给出结论（含“什么条件下结论会反转”）。