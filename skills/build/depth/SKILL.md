---
name: depth
description: Do a task the way the field's best practitioner would. Use when the user wants something done really well, "properly" or "deeper", at expert level, or sets a hard target (a load time, an accuracy, a metric to hit).
---

# Depth

Deeper, not bigger. The bar is work that a field-leading practitioner could learn something from.

## 1. Name the practitioner

Who is best in the world at this kind of work, and what do they do here that an average practitioner skips? Write it as actions, not adjectives.

## 2. Start from raw material

Work from the rawest source available: raw data, logs, primary sources, the code itself. A summary someone already digested carries their conclusions with it. If only the summary is in reach, name the raw material that would change the answer and fetch it, or ask for it.

## 3. Use the instruments

Use the practitioner's **instruments**, by name: a database, a statistical model, a profiler, a test harness, a simulation, a proper renderer. **Instruments, not vocabulary**: sounding like a statistician changes nothing, fitting the model does. When you reach for a markdown table or a paragraph where the practitioner would run something, run the thing and show the code, the run and the result.

## 4. Challenge the belief

Name the assumption the task rests on ("churn is an onboarding problem"). Try to reproduce it from raw material, working as if to disprove it: what would the data show if the belief holds, and does it show that? Report the strongest alternative explanation and what the data says about it.

## 5. Work a target in rounds

When there is a target, treat it as solvable: the question is how, never whether. Work in **rounds**: measure, name the biggest remaining obstacle, remove it, measure again. Log the measured number for every round.

Falling short is a legitimate ending. Report how far you got and the next obstacle by name. A partial result reported honestly beats a success nobody measured.

## 6. Produce new knowledge (when deep in data)

Once you are inside the data, look for something nobody knows yet (the earliest signal of churn, the real driver of a cost). Set part of the data aside **before** looking at it, build and lock the model or simulation, then test the finding on the held-out part.

## 7. Judge

Call `/outside-judge` before calling the work done.

Done when every "works", "faster" or "true" in your report carries a measurement or a check from the judge.
