TOOL read: {"path": "/home/zdan/.zstack/skills/plan/preflight/SKILL.md"}

TOOL ls: {"path": "/tmp/pf-25-with_skill-3vx2clp1"}

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


RESULT: .keep

TOOL bash: {"command": "date -u +%F; timeout 8 curl -sS -o /dev/null -w '%{http_code}\\n' https://www.aliyun.com 2>&1 | tail -2"}

RESULT: 2026-11-10
403


TOOL bash: {"command": "for u in https://example.com https://www.bing.com https://lingma.aliyun.com; do printf '%s -> ' \"$u\"; timeout 8 curl -sS -o /dev/null -w '%{http_code}\\n' \"$u\" 2>&1 | tail -1; done"}

RESULT: https://example.com -> 200
https://www.bing.com -> 200
https://lingma.aliyun.com -> 200


TOOL write: {"path": "/tmp/pf-25-with_skill-3vx2clp1/local/plans/ai-coding-tool-purchase.md", "content": "# Plan: 选出下季度团队要采购的 AI 编程工具\n\n- Asked: 调研一下国内 AI 编程工具的定价（要决定下季度买哪家；资料随便上网找）\n- Stage: decide\n- Date: 2026-11-10\n\n## Requirement\nHand over: 一份「按你们真实席位数和用量算出的年费」对比 + 2 家入围 + 1 个月试点与该买的建议（不是价目表）\nFallback: 各厂官方定价对比表（含抓取日期、版本口径、隐藏门槛）\nDepth: 专家会做的不是收集标价，而是把不同计价单位（每人月 / 积分 / 请求数 / 企业版最低席位）折算成同口径的月度账单；最原始材料是官方定价页 + 企业版/私有化报价单 + 采购与合规文档；工具是一个小的成本模型表；伸展目标：用 3 档用量（轻/中/重）算账，并用 1 个试点席位的真实账单验证模型偏差\nRange: 动作是「折算口径、压测用量、拆穿营销话术、卡合规」。需要的人：采购/财务（发票、对公、年框折扣）、安全合规（代码是否出内网、数据驻留）、一线工程师（实际额度消耗与体验）、红队（专挑促销价、试用期、最低席位、涨价条款）\nJudge: 你 + 1 名工程师用试点账单判；模型账与官方页可复核（每格标来源与日期），营销话术由红队专项反驳\nNeeds: 团队席位与角色、现有工具与预算上限、是否要求代码不出内网、决策截止日；我已确认本机可访问外网（curl 可达厂商站点），可直接取官方定价页并标日期\nDeclined: —\n\n## Task\nPurpose: 决定下季度团队买哪家 —— 待补：只选 1 家还是可混用？预算上限与要买的席位数？\nContext: 待补：团队人数与角色构成、现在用什么、是否强制合规/私有化、要发票或年框、什么时候要拍板\nMaterials: 你给的是「随便上网找」——我按主次排：① 厂商官方定价页与企业版说明（一手，标抓取日期）② 官方文档里的额度/限流规则 ③ 采购与合规声明 ④ 媒体评测只作旁证；禁用：二手「XX 元起」聚合文与无日期的比价博客；找不到的格子留空并注明\nBoundaries: 待补 —— 例如「不要只抄官网标价」「不要推荐没有对公发票的」「不要 eval 式打分表」\nDone: 待补 —— 交付形状（一页结论 + 成本模型表 + 来源清单），先给结论骨架和 2 家入围名单作 checkpoint，再展开算账\n\n## Open\n- 用哪个数字拍板：席位月费、还是按积分/请求折算的实际月账单？两者差距通常是 2–5 倍，口径不定这份调研会白做\n- 「国内」是否含 Cursor/Copilot 中国区可用性，还是只要境内厂商\n- 定价页 2026 年变动频繁（促销价、企业版最低席位），需要谁去拿报价单\n\nReady: no —— Requirement 的 3 个动作待你裁决；Context / Boundaries / Done 未答\n"}

RESULT: Successfully wrote to /tmp/pf-25-with_skill-3vx2clp1/local/plans/ai-coding-tool-purchase.md

ASSISTANT: 方案写到 `local/plans/ai-coding-tool-purchase.md`，还没定稿。下面是要点，**你只需就几个我无法替你决定的地方作决定**。

**1. 把要求提高一档（三处，逐条接受或否决）**

| 动作 | 我要交的东西 | 否决的话会怎样 |
|---|---|---|
| 提高目标层级 | 「按你们真实席位数和用量算的年费」+ 2 家入围 + 试点建议 | 退回成一份官方价目表，你上会还得自己算 |
| 加深一层 | 把「每人月 / 积分 / 请求数 / 企业版最低席位」折成同口径月账单，用轻中重 3 档用量压测，再用 1 个试点席位真实账单核对模型 | 各家标价单位不同，直接比会得出错误结论 |
| 扩展范围 | 至少加：采购（年框/发票）、安全合规（代码出不出内网）、红队（促销价、试用期、隐藏最低席位） | 只有价，选完卡在采购或合规上 |

评判不放我自己手里：每格标来源和抓取日期你可复核，结论由你和 1 名工程师用试点账单判。

**2. 五个只有你知道的答案（现在空着 3 个）**
- 目的：✓ 定下季买哪家 —— 但「买 1 家还是可混用」「预算上限」「几个席位」还没说
- 背景：团队人数与角色、现在用什么、是否强制私有化/合规、何时需要作决定 —— **空**
- 资料：你说随便上网找，我按主次排了：官方定价页（标日期）→ 官方额度文档 → 采购合规声明 → 评测只作旁证；**禁用**无日期的比价博客和「XX 元起」聚合文。已验证本机 curl 可达厂商站点
- 边界：**空** —— 什么样的结论你会说「不是我要的」？
- 完成：**空** —— 形状 + 一个早期检查点（先出结论骨架和 2 家入围名单，你点头我再展开算账）

**3. 最可能使这次调研白做的问题**
以哪个数字为准：席位月费，还是按额度折算的实际月账单？国内这几家两者常差 2–5 倍。还有，「国内」是否含 Cursor/Copilot 中国区，还是只要境内厂商。

回我三件事就能开工：① 三个动作哪些接受、哪些否决 ② 席位与预算 ③ 「国内」的口径。Ready 目前是 **no**。