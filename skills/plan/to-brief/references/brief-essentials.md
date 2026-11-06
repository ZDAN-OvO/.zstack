# Brief essentials

Distilled from Gary Chen, "Prompt 再完整也没用：先学会定义任务" (Bilibili BV1fseX6vE2L, 20 min). The reasoning behind `/to-brief`; cite it when a user asks why a question matters.

## Core claims

1. **Prompting ≠ defining the task.** Prompting makes the words clear; defining the task decides what is wanted. Polished words around an empty task yield an empty output. Prompt engineering is the floor, not the ceiling.
2. **Brief a senior, not an intern.** Current models read, revise, verify, and re-plan on their own. Specifying _how_ (clicks, steps, formatting rituals) is micromanaging an intern. Specify _what, why, what not to touch, when to stop_.
3. **The model challenges content, never intent.** It acts on receipt and does not ask "is this deck for the CFO or the client?". Vague in, generic out: it mirrors back whatever you failed to think through. Adding "ask me if unsure" only turns the brief from an essay question into a fill-in-the-blank; the blanks are still yours.
4. **This is management, not an AI trick.** Thinking (what do I want, what decision does it serve, what counts as good) plus communication (translating that for another capable mind). People skip the same step with human reports, who often don't dare ask back. Result is the same: nobody thinks it through for you.

## Stage before slots

Knowledge work runs **think → explore → decide → execute**. Most bad outputs come from issuing a later-stage request at an earlier stage:

| User is at | Asks for | Gets | Should ask for |
|---|---|---|---|
| think (no thesis) | a full draft | the version anyone could write, no point of view | questions back to the user |
| explore | a recommendation | a guess at the user's criteria | options with trade-offs |
| decide | — | — | a recommendation against stated decision logic |
| execute | the artifact | — | the five-slot brief |

The model never warns you you're at the wrong stage. Pausing before the request is the skill.

## The five slots

| Slot | Test question | What the model does without it |
|---|---|---|
| Goal | What decision does this output support? | Executes the action textbook-style: everything covered, nothing decidable. |
| Context | What does a smart stranger need so they don't aim wrong? | Assumes the generic case (big company, free to change price, competing with everyone). Theoretically right, unusable. |
| Materials | What may it be built from; what is banned; what if data is missing? | Treats everything not forbidden as allowed; doesn't rank sources; invents plausible values when it can't find one. |
| Boundaries | What output would make me say "not what I wanted"? | Fills the open space with things you never imagined. Direction without walls is an open brief. |
| Done | What appearing in front of me means I can stop? | Writes the whole thing, so a wrong direction is found at page 30, not at the outline. |

Pairs worth remembering:

- **Goal vs action.** "Analyse 5 competitors: features, pricing, pros/cons" is an action. "Support next quarter's call: should our USP lean easier or cheaper? End with a clear recommendation and reasons" is a goal. The goal lets the model narrow focus by itself.
- **Context sets the angle.** Revenue ~$2M, customers <50-person firms who find the product complex and expensive, last year's price change landed badly. With that, the model stops recommending price cuts and benchmarks similar-sized rivals. (Figures are the video's case setup, not industry data.)
- **Boundaries vs Goal.** "Nordic, minimal, cool tones" is direction; "no tatami, no wood floor, no patterned wallpaper" is walls. Boundaries are mostly "don't".
- **Boundaries + Done = scope.** Boundaries say what not to do; Done says where to stop.

## Rules that carry the most weight

- **Narrow the inputs.** 3 overlapping competitors studied deeply beat 5 scanned broadly. Narrowing is part of defining the task.
- **Ban low-trust sources by name**, with the reason (SEO-farm reviews contaminate the whole report's credibility).
- **"Not found → leave blank, don't invent."** The model's default is to answer whatever was asked. A fabricated price carried into a meeting is not a small error.
- **Forbid fabricated metrics** (ARR, user counts, growth): say "unknown" instead.
- **Separate policy from discussion.** "Don't propose changing the tier structure; pricing positioning is open."
- **Ban adjective-only output**: praise and blame without trade-offs is not analysis.
- **Specifying the artifact is not micromanaging.** Micromanagement governs the _process_; the output's shape (outline, Markdown, 3–4 bullets per section) is a spec you own.
- **Checkpoint first.** "Give me the outline; don't write the full report until I review it." Direction errors get fixed at the cheapest point, and tokens aren't burned on a doomed draft.

## Worked example

```text
Goal:       Next-quarter product direction (easier vs cheaper). End with one clear recommendation + reasons.
Context:    ~$2M ARR marketing-automation SaaS; customers <50 people, often say we're complex and expensive;
            last year's price change landed badly.
Materials:  Three competitors' sites and product docs (links); my compiled user reviews.
            No second-hand review articles. Not found → leave blank, don't invent.
Boundaries: No fabricated ARR/users/growth; don't touch the tier structure (positioning is open);
            no adjective-only, trade-off-free version.
Done:       Outline first (key differences + recommended USP + reasoning); full report after my review.
```

Bad-prompt output: five competitors described almost identically ("friendly UI, a bit pricey"); no direction. Brief output: an outline that already says "lean easier; benchmark B, whose 3-step onboarding hits your customers' top complaint; B costs more, so easier and cheaper conflict, pick easier, because complaints about complexity outnumber complaints about price in your reviews." That outline is meeting-ready.

## Common misdiagnosis

A one-page summary prompt with length, structure, and tone fully specified ("one page, four sections, concise and professional") still fails when **Goal** is missing: is the page to win budget, to warn of a delay, or to get another team's cooperation? Each needs different highlights. "Make the boss happy" is not a Goal; it is an empty criterion. Specs without a Goal are the most common gap.

## When not to brief

Ask one question: **is a redo expensive?** Quick lookups: no brief. Output for a meeting, for someone else, or from a half-hour unattended run: ten minutes of briefing beats three reruns.

## Unverified in the source

- The video gives no tested wording for making the model ask back reliably.
- It paraphrases the Microsoft/LinkedIn 2024 Work Trend Index (heavy AI users "pause before acting") without quoting it; check the report before citing.
