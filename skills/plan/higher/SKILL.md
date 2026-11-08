---
name: higher
description: Build a "then what?" ladder with the user, hand over the top rung, and step back one rung when the user rejects the result.
disable-model-invocation: true
---

# Higher

People hand AI the step they already chose ("fix this bug") instead of the result it serves ("the app stops crashing"). The habit dates from weaker models; now it underuses the model, and the chosen steps may point the wrong way. Where AI starts doing badly cannot be guessed, only found by trying: climb until the result is bad, then back off one rung. So the ladder is built before the try, kept, and walked back after the user judges the result.

The agent suggests. The user decides every rung. The agent writes no files: the ladder lives in the conversation, and `/more-ambitious` records it. Carrying out the handed rung happens after this skill ends.

## Grill

Choose the interview by the workspace:

- `/grill-with-docs` when the task is coding work or the workspace keeps a record (`docs/`, `GLOSSARY.md`, ADRs).
- `/grill-me` otherwise.

Scope it to the situation behind the request: what the result is for, who uses it, and what data, access and checks AI would have. Interview in the user's language. The grill is done when you can say in one sentence why the user wants this done. After each round of questions, end the turn and wait for the answers. Suggest no rung until the grill is done.

## Build the ladder

1. **Rung 0** is the request as the user wrote it.
2. **Suggest the next rung**: the result the current rung serves. Give the reason, what AI would newly own, and what it needs to own it: data, access, a way to check its own work. A missing need marks the rung as likely past what AI does reliably today.
3. **The user accepts, rewrites or stops.** End the turn after each suggestion and wait. Keep the rung in the user's final words.
4. **Repeat** until the user stops, or the next rung has no checkable result ("make us a million").

The top rung is the one handed over, uncertain or not. A failed try costs minutes and some tokens, and the rung below is already on record.

Example ladder, a quarterly review: fill last quarter's template with the new numbers → explain what changed, why, and what to do next → pick the three most urgent decisions, each with the case for and against → ask whether a quarterly report is still the right tool, and design daily monitoring that alerts only on significant change.

## Result

When the user stops climbing, close with the ladder:

```markdown
**Higher result**

| Rung | Goal | AI owns | Needs | Status |
|---|---|---|---|---|
| 0 | <request as written> | | | |
| 1 | <the user's words> | <what moved to AI> | <data, access, checks> | |

Handed over: rung <N>
```

Status is one of `handed`, `accepted`, `rejected`. Mark the top rung `handed`.

## Step back

When the user comes back with a verdict on the handed rung's result:

- **Accepted**: mark it `accepted`. The ladder is done.
- **Rejected**: ask what fell short and note it as a trial with the date. When the reason points at method rather than size (a wrong diagnosis, a missing source), suggest running `/deeper` on the same rung before stepping down. The user chooses. Stepping down marks the rung `rejected` and the one below `handed`.

Close with the updated ladder and the trial.

## Done

Building is done when the user has stopped climbing and one rung is marked `handed`. Close with the Higher result block.
