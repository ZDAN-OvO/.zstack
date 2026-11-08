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

| Slot | Answers | Clear when | Bad examples | Good examples |
|---|---|---|---|---|
| **Goal** | What decision or use does the output serve? | It names the decision or downstream use, not just the action. | 1. "Analyse our 5 main competitors: features, pricing, pros and cons." -- an action; no decision to aim at, so it gets the textbook version.<br>2. "Summarise this 30-page report into one page, four sections, concise." -- format only; nothing says what the page must achieve.<br>3. "Add caching to the search API." -- a solution, not a goal; nothing says what "fast enough" means or why.<br>4. "Write a blog post about our launch." -- a deliverable with no reader or desired effect. | 1. "Support next quarter's call: should our USP lean easier or cheaper? End with one recommendation and reasons." -- names the decision and the axis, so focus narrows by itself.<br>2. "Get management to approve the Q3 budget: make return vs spend clear enough to sign off." -- names the reader's decision, which decides what to highlight.<br>3. "Bring /search p95 under 300 ms so the mobile client stops timing out." -- measurable target plus the reason it matters.<br>4. "Get trial sign-ups from small-agency owners who read our newsletter." -- names audience and desired action, so tone and CTA follow. |
| **Context** | What would a smart stranger need so they don't aim wrong? | It holds the facts that rule out the generic answer: who, scale, constraints, past attempts that failed. | 1. "We're a SaaS company." -- too generic to rule out any default assumption.<br>2. "It's for management." -- which managers, and what do they need from it?<br>3. "Make it fit our system." -- the stranger cannot know what "our system" constrains.<br>4. "Customers have some complaints." -- which complaints, and how widespread? | 1. "~$2M ARR marketing-automation SaaS; customers are firms under 50 people." -- scale and segment rule out enterprise-style advice.<br>2. "Readers are the CFO and two VPs; they skim on a phone for two minutes." -- reader and reading conditions set length and depth.<br>3. "Redis exists but another team owns it; the last cache attempt was rolled back over stale prices." -- ownership and a past failure rule out the obvious fix.<br>4. "Top complaint is setup complexity; last year's price rise landed badly." -- real pain points and a burned option steer the proposal. |
| **Materials** | What may the work be built from, and what is banned? | Sources are named and ranked, excluded sources are named, and the behaviour for missing data is stated (default: leave blank, never invent). | 1. "Use whatever you can find online." -- no ranking and no exclusions; SEO filler gets in.<br>2. "Here's some data." -- no source status: primary, background, or noise?<br>3. "Look at the code." -- the whole repo is in scope, so attention spreads thin.<br>4. "Fill any gaps with reasonable estimates." -- invites fabricated figures. | 1. "Competitors' official sites and docs only; no third-party review articles." -- names the allowed sources and bans the low-trust one.<br>2. "Primary: the attached Q2 report. Secondary: last quarter's deck, for comparison only." -- ranks sources and limits the secondary one's role.<br>3. "Read `order/` and `pricing/`; ignore `legacy/`." -- scopes reading and excludes the misleading part.<br>4. "If a figure isn't in the sources, leave the cell blank and mark it 'not found'." -- states the missing-data behaviour explicitly. |
| **Boundaries** | What output would make the user say "this isn't what I wanted"? | It lists concrete don'ts: what not to touch, assume, fabricate, or recommend. These are walls, not directions. | 1. "Keep it professional." -- a direction, not a wall; nothing is ruled out.<br>2. "Be careful with the code." -- no concrete line to stay behind.<br>3. "Don't make mistakes." -- the default already; changes nothing.<br>4. "Make it insightful, not generic." -- adjectives, not a testable don't. | 1. "No ARR, user counts or growth figures unless sourced." -- a checkable ban on fabricated metrics.<br>2. "Don't change public API signatures or the DB schema." -- names exactly what must not change.<br>3. "Don't propose changing the tier structure; pricing positioning is open." -- separates fixed policy from what is open.<br>4. "No adjective-only comparisons; every claim names a trade-off." -- bans the failure mode and states the replacement. |
| **Done** | What appearing in front of the user means stop? | It names the artifact, its shape, and a checkpoint: for large work, an outline to review before the full thing. | 1. "Write the full report." -- no checkpoint; a wrong direction surfaces at page 30.<br>2. "Finish the feature." -- no observable finish line.<br>3. "Make it better." -- unbounded; there is never a point to stop.<br>4. "Keep going until it's done." -- circular; restates the question. | 1. "A Markdown outline: 3 key differences, recommended USP, reasoning. Full report only after I approve." -- names the artifact and a review gate before the expensive part.<br>2. "`PricingServiceTest` passes and the PR description lists every changed endpoint." -- observable: a test result and a checkable PR.<br>3. "One page, four sections, under 400 words, forwardable as-is." -- shape and size are concrete and checkable.<br>4. "Stop at a design note with two options; no code until I pick one." -- stops at the cheapest decision point. |

Each example is followed by ` -- ` and the reason it fails or works. Examples are paired by number: each good example repairs the bad one beside it. Use them to calibrate grades and to phrase recommended answers, not as text to copy into a brief.

## Workflow

### 1. Check the stage

Place the request on the ladder **think → explore → decide → execute**. A brief commissions execution; the other stages need a different Done:

- **think**: the user has no thesis yet. Done is "questions for the user", not a draft.
- **explore**: Done is "options with trade-offs", not a recommendation. Goal is clear once it names the options to compare and the open decision they feed; the user's decision criteria are not needed yet, since finding them is what exploring is for.
- **decide**: Done is "a recommendation against the user's stated criteria"; those criteria must be in Goal or Context.
- **execute**: the normal brief.

If the request asks for a later-stage artifact than the user is at (a full draft while still thinking), say so and propose the earlier-stage Done. Record the stage in the brief.

### 2. Grade each slot

Map the user's words onto the five slots and grade each one **clear**, **thin**, **ambiguous**, or **missing**:

- **thin**: present, but too little for the request's size. A large or high-stakes request with a one-phrase slot means the user hasn't thought it through yet.
- **ambiguous**: two reasonable readings lead to different outputs. An adjective standing in for a criterion ("high-end tone", "more stable") or an unnamed audience ("old customers" when tiers or segments differ) is ambiguous, not thin.

Grade against the stated words: a slot the user stated concretely is **clear**, even if you would phrase it differently or could add sub-questions under it. "Give me a plan to review before changing anything" is a clear Done; its exact shape is yours to propose in the brief, not a question.

Facts you can look up yourself (repo layout, existing docs, file contents, tooling) are never gaps: look them up and fill them in. Only the user's intent, preferences, and decisions count as gaps.

### 3. Decide: format or grill

**Ready** when Goal and Done are clear and at least three slots in total are clear, with every remaining slot safe to default (see Defaults). Then go to step 5.

Otherwise rank the non-clear slots by **impact**: how much a wrong guess there would change the output. Goal and Done usually rank highest; a missing slot on a large request outranks a thin slot on a small one. Pick the top 3–5 to question. Every **ambiguous** slot is on that list: a default would pick one reading for the user. Only **thin** or **missing** low-impact slots may be defaulted (see Defaults); list them as assumptions.

### 4. Grill the selected slots

Choose the interview:

- **`/grill-with-docs`** when the task is coding work, or the workspace keeps a record of past work (`docs/`, `GLOSSARY.md`, ADRs). Its glossary and ADR writes keep the brief's terms consistent with the project.
- **`/grill-me`** when the task is non-coding and the workspace has no such record.

Hand the chosen interview its scope: the selected slots are the open decisions; clear slots, defaulted slots and facts you looked up are already settled. How it asks, how many questions per round and when it is done belong to that skill; follow it as written.

When the interview ends, regrade the selected slots and recheck the stage (step 1) against the answers. If the stage moved, update Stage and Done before step 5.

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

Then validate the file:

```bash
node <this-skill-directory>/scripts/check-brief.mjs docs/briefs/<topic>.md
```

Fix every reported line and rerun. The step is done when the checker exits 0 (`1 brief(s) ok`). It checks format only: title, Stage/Source, slot order, bullets-only bodies, 1–5 bullets per slot, no leftover placeholders or empty optional sections. Whether each slot is clear stays your judgment from step 2.

### 6. Confirm

Show the user the path and a one-line summary per slot. Ask them to confirm or correct. Apply corrections to the file and rerun the checker; the step is done when the user confirms the brief and the checker exits 0.

## Defaults

Use these only for a **thin** or **missing** low-impact slot, never for an ambiguous one, and list each one under Assumptions:

- **Materials**: the files and links the user named; no unsourced figures; leave gaps blank and mark them.
- **Boundaries**: no fabricated numbers, names or sources; no changes outside the named scope; trade-offs over adjectives.
- **Done**: for output a reader will take longer than a few minutes to review, an outline first, full version after approval.

Goal has no default. If it cannot be stated, the request is not briefable yet: report that and stay in step 4.

## When not to brief

The test is the cost of a redo. A quick lookup or a one-line edit is cheaper to redo than to brief: tell the user the request is ready as-is and stop. Brief when the output goes to a meeting, to someone else, or into a long unattended run.
