---
name: deeper
description: Grill the user on the task, then suggest how a top expert would approach it, for the user to keep or drop.
disable-model-invocation: true
---

# Deeper

Ask AI for something without a standard and it gives the painkiller: a plausible fix to the surface symptom. A top expert starts from a diagnosis, raw evidence and named methods. The user is often not that expert, so they cannot ask for that depth. "You are a senior X" changes the voice and leaves the method untouched. So the agent learns the user's situation first, then lays out the expert's playbook as concrete suggestions fitted to it.

The agent suggests. The user decides what to keep. The agent writes no files; carrying out the task happens after this skill ends.

## Grill

Choose the interview by the workspace:

- `/grill-with-docs` when the task is coding work or the workspace keeps a record (`docs/`, `GLOSSARY.md`, ADRs).
- `/grill-me` otherwise.

Scope it to the task (the handed rung, when a ladder exists) and what bounds it: the user's time and access, the material they already hold, what they have tried. Interview in the user's language. The grill is done when the suggestions below can name the user's real sources and constraints rather than generic ones.

## Suggest

Answer the four expert questions as suggestions for this task. Mark each claim as known or unsure, and name a method only together with when it applies.

1. **Premise.** Would a top expert first check whether the problem is really where the task points? Name the other likely causes.
2. **Raw material.** Which first-hand sources they would start from, instead of digested reports, and which of them the user has.
3. **Methods.** Which named methods and tools they would use.
4. **Proof.** Beyond the user's or AI's own judgment, what evidence would show the result worked, and when it can be observed.
5. **Stretch** (optional). A target well past the obvious one, to force a different approach, paired with an honest report of the gap when it is missed.

The user keeps, edits or drops each suggestion. When the user decides the premise does not hold, hand the finding to `/higher`.

## Done

The step is done when the user has ruled on every suggestion. Close with the block below:

```markdown
**Deeper result**
- Premise: <holds | moved, handed to /higher>
- Kept: <suggestion, in the user's final words>, one per kept suggestion
- Dropped: <suggestion, and the user's reason>
```
