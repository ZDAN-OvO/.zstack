---
name: altitude
description: Raise a task to the outcome it serves. Use when the user asks for an artifact that feeds a decision or a meeting (a deck, report, review, memo), keeps repeating the same kind of request, or asks you to "keep", "own" or "make sure" something stays working.
---

# Altitude

A request is the user's best guess at a road to an outcome. **Altitude** climbs from the task to the **goal behind the goal**, then checks whether the requested road is the best one.

## 1. Climb

Write the chain: "this produces X, so that Y happens, so that Z." Keep climbing until you reach an outcome in the world (money moved, a problem caught early, users kept, an app that stays up), not an artifact.

Done when the chain has at least two links and ends at an outcome the user would recognise as the point.

## 2. Test the road

Compare the requested task against the higher roads to the same outcome:

- **Decisions over documents.** An artifact for a meeting exists so someone decides. Find the three most urgent decisions it must serve. For each: the options, the case for and against, and the one fact that would flip your recommendation. Build the artifact around those decisions.
- **Process replacement.** A recurring process (a quarterly review, a weekly report) was designed for people reading data by hand. Design a better way to reach its purpose, show from the user's own history that it would have caught things sooner, and propose running it alongside the old one for one cycle.
- **Standing ownership.** When the same request keeps coming back (fix this crash, then that one), the higher task is the standing state ("the app stays crash-free").

## 3. Raise or keep

If a higher road clearly serves the outcome better, propose it in one or two sentences and confirm before changing the deliverable. If not, keep the task as asked and build it to serve the outcome you found.

Creative work often has no outcome above it to climb to. Keep the task there.

## 4. Equip standing ownership

When the user takes the standing-ownership road, list what you need to hold it without being fed tasks one at a time:

- the data, and how you fetch it (crash reports, metrics, logs)
- the access (environments to reproduce and verify on)
- how you notice on your own that something needs doing
- how you verify your own fix (call `/outside-judge`)
- when you hand a decision back to the human

Build the first missing piece, then report what is still missing.
