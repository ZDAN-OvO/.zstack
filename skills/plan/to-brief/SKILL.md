---
name: to-brief
description: Turn a raw request into a five-slot brief (Goal, Context, Materials, Boundaries, Done) at docs/briefs/<topic>.md, grilling the user only on the gaps that would change the output.
disable-model-invocation: true
---

# To Brief

Turn the user's request into a brief that a capable agent with zero knowledge of this user can execute on the first try. The agent will not ask back: it acts on whatever it gets and fills every gap with generic defaults. Your job is to close the gaps that matter before that happens.

This skill ends at a written, confirmed brief. Executing the task is out of scope.

The reasoning behind every rule here lives in [references/brief-essentials.md](references/brief-essentials.md). Read it when a slot's grade is unclear, or when the user pushes back on a question.

## The five slots

| Slot | Answers | Clear when |
|---|---|---|
| **Goal** | What decision or use does the output serve? | It names the decision or downstream use, not just the action ("analyse competitors" is an action; "decide between easier vs cheaper next quarter" is a goal). |
| **Context** | What would a smart stranger need so they don't aim wrong? | It holds the facts that rule out the generic answer: who, scale, constraints, past attempts that failed. |
| **Materials** | What may the work be built from, and what is banned? | Sources are named and ranked, excluded sources are named, and the behaviour for missing data is stated (default: leave blank, never invent). |
| **Boundaries** | What output would make the user say "this isn't what I wanted"? | It lists concrete don'ts: what not to touch, assume, fabricate, or recommend. These are walls, not directions. |
| **Done** | What appearing in front of the user means stop? | It names the artifact, its shape, and a checkpoint: for large work, an outline to review before the full thing. |

## Workflow

### 1. Check the stage

Place the request on the ladder **think → explore → decide → execute**. A brief commissions execution; the other stages need a different Done:

- **think**: the user has no thesis yet. Done is "questions for the user", not a draft.
- **explore**: Done is "options with trade-offs", not a recommendation.
- **decide**: Done is "a recommendation against the user's stated criteria"; those criteria must be in Goal or Context.
- **execute**: the normal brief.

If the request asks for a later-stage artifact than the user is at (a full draft while still thinking), say so and propose the earlier-stage Done. Record the stage in the brief.

### 2. Grade each slot

Map the user's words onto the five slots and grade each one **clear**, **thin**, **ambiguous**, or **missing**:

- **thin**: present, but too little for the request's size. A large or high-stakes request with a one-phrase slot means the user hasn't thought it through yet.
- **ambiguous**: two reasonable readings lead to different outputs.

Facts you can look up yourself (repo layout, existing docs, file contents, tooling) are never gaps: look them up and fill them in. Only the user's intent, preferences, and decisions count as gaps.

### 3. Decide: format or grill

**Ready** when Goal and Done are clear and at least three slots in total are clear, with every remaining slot safe to default (see Defaults). Then go to step 5.

Otherwise rank the non-clear slots by **impact**: how much a wrong guess there would change the output. Goal and Done usually rank highest; a missing slot on a large request outranks a thin slot on a small one. Pick the top 3–5 to question. Default the rest and list them as assumptions.

### 4. Grill the selected slots

Choose the interview:

- **`/grill-with-docs`** when the task is coding work, or the workspace keeps a record of past work (`docs/`, `GLOSSARY.md`, ADRs). Its glossary and ADR writes keep the brief's terms consistent with the project.
- **`/grill-me`** when the task is non-coding and the workspace has no such record.

Run the chosen interview scoped to the selected slots only: each question targets one slot, carries your recommended answer, and is worded so "yes" accepts it. Highest-impact slots go first. Stop when every selected slot grades clear; the user saying "just use your recommendation" also settles a slot.

Grilling may reveal the stage was wrong (step 1). Then update the stage and Done, rather than pressing on with the old frame.

### 5. Write the brief

Write `docs/briefs/<topic>.md` at the workspace root (the git root, or the current directory if there is none). `<topic>` is a short kebab-case English slug of the outcome, e.g. `competitor-usp-direction`. Create the directory if needed. If the file exists, ask before overwriting; offer a `-2` suffix instead.

Write the slot contents in the user's language; keep the headings below in English so other agents can parse the file. Each slot is 1–5 bullets of concrete statements, no adjectives standing in for criteria.

```markdown
# Brief: <one-line outcome>

- Stage: <think | explore | decide | execute>
- Source: <the user's original request, quoted or condensed>

## Goal
## Context
## Materials
## Boundaries
## Done

## Assumptions
<!-- Defaulted slots and agent-filled facts, each marked so the user can veto it. Omit if empty. -->

## Open questions
<!-- Only questions the user chose to defer. Omit if empty. -->
```

### 6. Confirm

Show the user the path and a one-line summary per slot. Ask them to confirm or correct. Apply corrections to the file; the step is done when the user confirms the brief.

## Defaults

Use these when a low-impact slot stays unfilled, and list each one under Assumptions:

- **Materials**: the files and links the user named; no unsourced figures; leave gaps blank and mark them.
- **Boundaries**: no fabricated numbers, names or sources; no changes outside the named scope; trade-offs over adjectives.
- **Done**: for output a reader will take longer than a few minutes to review, an outline first, full version after approval.

Goal has no default. If it cannot be stated, the request is not briefable yet: report that and stay in step 4.

## When not to brief

The test is the cost of a redo. A quick lookup or a one-line edit is cheaper to redo than to brief: tell the user the request is ready as-is and stop. Brief when the output goes to a meeting, to someone else, or into a long unattended run.
