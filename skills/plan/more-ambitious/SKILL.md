---
name: more-ambitious
description: Help the user make a request more ambitious with the higher, deeper and wider interviews, record it in docs/reqs/<topic>.md for /to-brief, and step the task back after a rejected result.
disable-model-invocation: true
---

# More Ambitious

What a person gets out of AI is capped by the ambition and understanding they bring to the request. Ambition is the user's own, sharpened over repeated tries. This skill advises: each leaf grills the user on their situation, then gives concrete suggestions. The user keeps, edits or drops every one.

This skill defines the task and stops there. The one file it writes is the requirement file (see Record); the leaves write none. Carrying out the task happens after the skill ends, through `/to-brief` or the user's own request.

Interview the user in their language.

The source idea, its leading words and worked examples live in [references/four-questions.md](references/four-questions.md). Read it when a signal or a suggestion needs grounding, when you need an example, or when the user asks why a question is being asked.

## Route

Read a leaf in full before running it: `/higher`, `/deeper`, `/wider`.

Suggest which leaves to run, each with the signal you saw. The user adds or drops leaves. End the turn there; start the first leaf only after the user confirms the list.

| Signal in the request | Leaf |
|---|---|
| Asks for a step, a fix or a part ("fix this bug", "fill in the template"), and the result it serves is unstated | `/higher` |
| A domain where the user is not the expert, and quality matters | `/deeper` |
| Names a deliverable by its noun ("homepage", "sales deck", "README") | `/wider` |

Run them in this order: higher, deeper, wider. Higher builds the ladder and picks the rung to hand over; deeper and wider work on that rung. Deeper comes first because it checks the premise, and a wrong premise would waste a round of borrowing.

Suggest skipping the whole skill when a redo is cheaper than the interview (a rename, a one-line lookup), and stop. The user then asks for the task as a plain request.

## Loops

- When `/deeper` or `/wider` moves the goal, return to `/higher` with the finding.
- When the user rules a rung out as "AI can't do that" without trying it, point out that a failed attempt costs a few minutes and a few tokens, then ask whether it stays on the ladder. The user decides.

## Done

1. Read back the handed rung and the kept suggestions. The user confirms or edits them.
2. Ask the user to restate the task in their own words. When the restatement leaves out a kept suggestion, ask whether it is dropped; the user decides.
3. Write the requirement file (see Record), with the restatement as the Requirement.
4. The skill is done when the checker exits 0. Close by naming the file and offering `/to-brief` with it as the source.

## Record

Write `docs/reqs/<topic>.md` at the workspace root (the git root, or the current directory if there is none). `<topic>` is a short kebab-case English slug of the handed rung. Create the directory if needed. If the file exists and is not this task's, ask before overwriting; offer a `-2` suffix instead.

The file is the ambitious requirement, not the finished brief. Fill it from the leaves' result blocks, in the user's final words, and leave out the section of a leaf that did not run:

```markdown
# Requirement: <handed rung in a few words>

- Source: <request as the user wrote it>
- Date: <YYYY-MM-DD>

## Requirement

<the user's restatement>

## Ladder

| Rung | Goal | AI owns | Needs | Status |
|---|---|---|---|---|
| 0 | <request as written> | | | |
| 1 | <the user's words> | <what moved to AI> | <data, access, checks> | handed |

Handed over: rung <N>

## Deeper

- Premise: <holds | moved, handed to /higher>
- Kept: <suggestion>
- Dropped: <suggestion, and the user's reason>

## Wider

- Noun → verb: <noun> → <the user's verb>
- Borrowed: <field: technique>
- Dropped: <technique, and the user's reason>

## Trials
```

Trials starts empty. Each later entry is a dated H3 with the rung and the verdict, then bullets on what happened:

```markdown
### 2026-11-08 · rung 2 · rejected
- Fell short: <what the user said fell short>
```

Then validate the file:

```bash
node <this-skill-directory>/scripts/check-req.mjs docs/reqs/<topic>.md
```

Fix every reported line and rerun. It checks format only: title, Source/Date, section order, the ladder table (header, rung numbering, one `handed` rung matching the "Handed over" line), the field bullets in Deeper and Wider, Trials headings, and leftover placeholders. Whether the requirement is ambitious enough stays the user's call.

## After the try

When the user returns with a verdict on the result, read the requirement file and run `/higher`'s Step back on its ladder. Write the outcome back: the updated Status column and a dated entry under Trials, then rerun the checker. On a new handed rung, rerun `/deeper` or `/wider` only where the user wants, update the Requirement and those sections, then offer `/to-brief` again.
