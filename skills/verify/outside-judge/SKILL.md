---
name: outside-judge
description: Verify work with something other than your own judgment. Use when about to declare non-trivial work done, when a target or metric was set, when results go to other people, or when the user asks to check, verify, validate or review the work.
---

# Outside judge

Your own reading of your own work is the weakest evidence there is: you approve it too easily. Hold the work to an **outside judge**, something that can say no.

## 1. Pick the judge

Pick it before the work starts whenever you can, so the work cannot bend the check. Strongest first:

1. **A check that runs**: tests, a benchmark, a validator, a compiler, a reproduction on a clean machine.
2. **Held-out data**: part of the data set aside before you looked, opened only after the model or claim is locked.
3. **A primary source**: the original document, dataset or spec to compare against.
4. **A measurement**: a number taken the same way before and after.
5. **A blind reviewer** (below), when the judge has to be judgment.

Use the strongest one the task allows. Write down which one and why.

## 2. Run it as you go

Run the judge after every significant change, and record what it said each time. A judge run once at the end only tells you how far off you drifted.

## 3. Blind reviewer

Start a separate agent with only the original task and the result: no reasoning, no working steps, no account of what you tried. Ask it to find errors, weak spots and claims that are not verified. Fix what it finds, and note what you left unfixed and why.

With no subagents available, write the review instructions for the user instead, so a person can play the reviewer.

## 4. Report in three lists

- **Verified**: each claim with the judge that verified it.
- **Unverified**: claims stated as unverified, plainly.
- **Failed**: what the judge rejected, with what it said.

Done when every claim in the final report sits in exactly one of the three lists.
