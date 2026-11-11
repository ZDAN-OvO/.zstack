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
2. **Consent.** The user typed `/preflight`, or accepted an offer: go on to Look. Otherwise offer the plan in one line and stop. The workspace stays unchanged until the user accepts.

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

Look at the task through three lenses. Suggest a move only on a lens where it would change the result, and write `not needed` for the others. Each suggestion stays a suggestion until the user accepts, rewrites or declines it. A declined move is recorded with its reason.

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

A slot the user cannot answer stays empty, and the question goes under Open. The gap itself is the finding. Ask a question that helps the user answer it, and write no default for them to approve.

## Write

Write `local/plans/<topic>.md` at the workspace root (the git root, or the current directory). `<topic>` is a short kebab-case English slug of the outcome. The plan may carry Open items; Ready tells the user what is still missing.

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
Proposed: <moves awaiting the user's ruling; omit when empty>
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


TOOL bash: {"command": "cd /tmp/pf-26-with_skill-y7hjtora && ls -la && git rev-parse --show-toplevel 2>/dev/null; find . -maxdepth 3 -type f | head -50"}

RESULT: total 172
drwxrwxr-x  2 zdan zdan   4096 11月 10 16:17 .
drwxrwxrwt 59 root root 167936 11月 10 20:54 ..
-rw-rw-r--  1 zdan zdan      0 11月 10 16:17 .keep
./.keep


TOOL bash: {"command": "date +%F"}

RESULT: 2026-11-10


TOOL write: {"path": "/tmp/pf-26-with_skill-y7hjtora/local/plans/saas-usp-competitor-analysis.md", "content": "# Plan: 竞品分析支撑下季 USP 方向（易用 vs 便宜）\n\n- Asked: 「写一份我们 SaaS 的竞品分析报告」，支撑下季 USP 往易用还是便宜走，完成即交付完整报告\n- Stage: execute（但决策判据未定，见 Open）\n- Date: 2026-11-10\n\n## Requirement\n\nHand over: 按原样交付报告；但真正要交的是**一个能扛住反问的判据 + 据此得出的方向**，报告只是它的外壳。\nFallback: 若拿不到自有赢单/流失数据，退为一页决策简报（判据、证据强度、在什么情况下结论反转），不出完整报告。\nDepth:\n- 原始材料：不是竞品官网，而是①你们的赢单/丢单记录与丢单理由②流失与降级原因③客服工单主题分布④销售被反问的原话⑤竞品**定价页结构**的时间快照（席位/计量/额度/免费额度）。\n- 工具：投诉语料按时序编码（把 G2/Capterra 差评按「太贵」vs「难用」分类做趋势），定价页 diff，赢单表交叉编码——不是功能对比矩阵。\n- Stretch: 先立一个可被证伪的断言（例：本客群「贵」的反对集中在多席位采购者，「难用」集中在单人试用者），再用你方未参与建模的那段管道数据去验证它。\nRange: 报告要做的动作是①判定哪个 USP 对买家有决定权②让证据可被复核③经得起反向攻击。Crew：竞品情报（定价与包装取证）、定价经济（支付意愿与捆绑）、定位策略（品类框架）、买家研究（赢单/丢失编码）、红队（用同一批数据论证相反结论）。\nJudge: 你本人能直接判（你认识买家）；方法层面加一个红队会话，专门攻击「便宜」与「易用」两个结论的证据链，命中即返工。\nNeeds: 你方赢单/流失/工单数据（缺，需授权）、竞品名单与客群定义（缺）、评价站点取样范围（缺）。\nProposed:\n1. 交付物从「报告」抬到「方向 + 反转条件」——报告结构不变，结论必须可被证伪。\n2. 把「易用 vs 便宜」当成买家**切换成本**的函数而不是二选一：先答「本客群里哪一项在触发比价」，方向自明。\n3. Done 加一个 1 页论点+目录的 checkpoint，再展开全文（你在上一条里明确拒绝过中间稿，等你裁定）。\nDeclined: —\n\n## Task\n\nPurpose: 「支撑下季 USP 往易用还是便宜走」——待确认：报告是**给出推荐**，还是**只摆证据、由团队拍板**？\nContext: 缺买家画像与客群、现用 USP 表述、真正让我们丢单的对手是谁、「易用」具体指上手/集成/自动化中的哪一个。\nMaterials: 缺，需你定名单与排序。建议主源=自有赢单丢单表、流失原因、工单标签、竞品定价页存档、客户访谈原话；次源=评价站点差评、竞品文档与 changelog；禁源=「2026 十大 SaaS 榜单」类聚合文与二手市场报告 PDF。\nBoundaries: 你未给。需要「哪些产出会让你说这不是我要的」（例：不接受功能对比大表 / 不接受只靠公开资料）。\nDone: 你说了「直接给我完整报告」——但「完整」未定义（几家竞品、多长、是否必须落到一个方向）。已列为待裁定。\n\n## Open\n\n- 判据缺失：没有决策规则，任何报告都会变成「两边都有道理」。要定的是：在什么条件下「便宜」该赢、「易用」该赢（谁的切换成本高、谁在比价）。\n- 竞品集合与客群边界：分析谁、针对哪个细分，直接决定结论；不划就是泛泛而谈。\n- 自有数据能否取用：这是唯一能把「易用/便宜」从猜测变成结论的材料。拿不到就要走 Fallback。\n- 「完整报告」的形状与篇幅：不定，交付后必然返工。\n\nReady: no —— 需你裁定 3 条 Proposed，并补齐 Purpose 歧义、Context、Materials、Boundaries、Done 的形状。\n"}

RESULT: Successfully wrote to /tmp/pf-26-with_skill-y7hjtora/local/plans/saas-usp-competitor-analysis.md

ASSISTANT: 计划已写到 `local/plans/saas-usp-competitor-analysis.md`。

先说我看到的核心问题：「易用还是便宜」目前没有判据。没有判据时，任何竞品分析都会得出「两边都有道理」，报告会写得像样，但下季度 USP 还是定不下来。所以关键不在于写得全不全，而在于拿什么材料把「便宜」和「易用」分出胜负。

两条要点：

- **材料是空的**：工作区里没有你们的赢单、丢单表、流失原因、工单标签，也没有竞品定价页存档。这些是唯一能验证结论的材料。竞品官网和「十大 SaaS」聚合文只能罗列功能，不能说明买家为什么又选了别人。拿不到自有数据，建议退成一页决策简报，而不是完整报告。
- **你的「完整报告」把中间检查点去掉了**：我不反对直接出全文，只是需要你把「完成」定义清楚：几家竞品、多长、是否必须落到一个方向。不定义，交付后大概率返工。

需要你裁定的三件事，已列在计划里：交付物是否从「报告」抬高到「方向 + 反转条件」；是否把这个问题改写成「在本客群里哪项在触发比价」；是否加一个 1 页论点+目录的检查点。另外 Purpose 那里有个歧义：报告是给推荐，还是只摆证据由团队拍板？

你确认 Ready 那行后，可以用 `/define-goal` 以这份计划为源头推进。