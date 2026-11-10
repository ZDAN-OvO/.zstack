---
name: wider
description: Grill the user on what a deliverable is for, then suggest its job as a verb and the fields best at that job, for the user to keep or drop.
disable-model-invocation: true
---

# Wider

A deliverable's noun ("homepage", "sales deck") carries an industry label. Say it, and AI searches that one industry's playbook. The job the deliverable does is shared across fields. Swap the noun for a verb ("stop a stranger within five seconds and make them curious") and the search opens up to trailer editors, short-video creators and shop-window designers.

The agent suggests. The user decides the verb and what to borrow. The agent writes no files; writing the deliverable happens after this skill ends.

## Grill

Choose the interview by the workspace:

- `/grill-with-docs` when the task is coding work or the workspace keeps a record (`docs/`, `GLOSSARY.md`, ADRs).
- `/grill-me` otherwise.

Scope it to the deliverable: who meets it, in what moment, and what they should do or feel after it works. Interview in the user's language. The grill is done when you can describe a reader or user meeting the deliverable without using its noun.

## Suggest

1. **Noun → verb.** Quote the deliverable's noun and suggest two or three verbs for its job. Each names an effect you could check, and leaves the noun out. The user picks one or rewrites it. When the chosen verb changes the result itself rather than restating the noun's job, hand the new result to `/higher`. End the turn here: the fields depend on the verb the user picks.
2. **Fields.** For the chosen verb, suggest 3–5 fields whose practitioners are best at it. For each, give one concrete technique that would transfer to this deliverable, and mark the ones you are unsure of.

The user keeps, edits or drops each technique.

## Done

The step is done when the user has chosen a verb and ruled on every technique. Close with the block below:

```markdown
**Wider result**
- Noun → verb: <noun> → <the user's verb>
- Borrowed: <field: technique>, one per kept technique
- Dropped: <technique, and the user's reason>
```
