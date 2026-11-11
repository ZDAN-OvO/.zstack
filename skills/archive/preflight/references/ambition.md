# Ambition: distilled

Source of the Requirement axes and the judge in `/preflight`. Distilled from Felix Rieseberg (engineering lead on Claude at Anthropic):

- **[E]** Essay, "How to be more ambitious: A tutorial for humans with models", 2026-10-13. <https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/>
- **[I]** Interview, Silicon Valley Girl, "Claude Engineering Lead: Stop Using Claude Like It's 2024", 2026-10-20. <https://www.youtube.com/watch?v=D-SVFneJ_Nk>. Timestamps are approximate and come from the auto-captions.

## Thesis

- **Best guess.** A task given to the model is the user's best guess at a route to an outcome. The model runs the guess. [E]
- **Four types.** Ambition comes in four types: speed, altitude, depth and range. Speed means the same work done faster. It is well established and needs no new thinking, so the skill leaves it out. [E]
- **Self-efficacy.** People are held back by what they believe is possible. Specific, hard goals beat "do your best" (Locke and Latham, 35 years of studies). Belief, a visible precedent and permission to fail all raise what gets attempted. The studies are on humans; carrying them over to models is Felix's extension. [E]

## Altitude

- **Goal beyond the goal.** Ask what should happen next, then hand that over. The crash example climbs from "fix this crash" to "keep the apps crash-free". [E]
- **Ceiling.** Keep climbing until the model fails. "Go make money" is past the line today. Work at the ceiling sits at the frontier and gains the most from the next model. [I 39:05]
- **Fit.** Altitude fits work after an ultimate outcome. Work that will be discussed in meetings is a good sign. It fits creative work less well. [E]
- **Workflow cost.** Climbing usually means rebuilding access first. Crash-free needed crash-report fetching, a version-to-commit map, and Windows, macOS and Linux machines to reproduce and verify on. The setup cost is real and worth paying. [E] [I 22:39]
- **Conveyor belt.** A user who carries items to the model one at a time is the bottleneck. Give the model the whole data source and let it choose what to act on. [I 22:39]

Worked ladder, a quarterly business review [E]:

1. Update the template's numbers.
2. What changed this quarter, why, and what to do.
3. The three most urgent decisions, with the case for and against each.
4. Replace the deck with a better way for leadership to catch problems early and move money and people. Prove on past history that it would have caught them sooner, then run it beside the deck for a quarter.

## Depth

- **Instruments, not costume.** A persona switches the vocabulary and keeps the method. Ask which tools the top of the field uses, then require those tools, and get the result explained plainly. The leap in AI 3D and motion work came from using Blender, not from a better grasp of animation. [E] [I 10:28, 25:20]
- **Stretch target.** Set an unreasonable goal and treat it as reasonable: 200 ms, not 5 s. When the model says it is impossible, tell it to keep going. [E]
- **Challenge beliefs.** Give the model the raw data and have it try to reproduce a belief the user holds ("churn is an onboarding problem"). [E]
- **New knowledge.** From inside the data, look for the blind spot: an unknown early signal, shown to predict data it has not seen. [E]
- **Expert questions.** Before the task is rewritten, name four things: (1) what a top professional would do that is not being asked; (2) the rawest material they would start from; (3) their specific methods and tools; (4) what, other than the model or the user, would show the result is right. Then rewrite the task to ask for exactly that. [E]
- **Process.** For work that rests on taste, the gain comes from copying the steps professionals take, since good work comes out of a refined process. [I 8:26–9:52]

## Range

- **Noun to verb.** A deliverable's name hides its job. A quarterly review is not "a deck". It gets busy people to believe a cause-and-effect story and decide under uncertainty in 30 minutes. The verbs show which fields can help. The idea comes from Kelley and Littman, *The Art of Innovation*. [E]
- **Crew.** Ask which team would be assembled if the stakes were extreme. For the review: an analyst, a journalist and an editor; a motion and audio designer if it is presented; a short seller and a forensic accountant as the red team. [E]
- **Do, not write.** Use the crew to find fields and techniques. Ask the model to do the short seller's research, not to write in a short seller's voice. Role play makes the transcript stranger and the output no better. [E]

## Judge

- **Outside session.** The session that did the work is a poor judge of it. Far more tasks are unsafe to trust to a single session than to the model. Prefer a check the model can run and get feedback from at once. [E] [I 26:10]
- **Grade the process.** A correct guess of the temperature fails. A half-degree miss that came from the right location and a reputable source passes. [I 7:35]
- **Adversarial review.** When nothing hard can check the work, spin off sessions whose only job is to prove the output wrong, as red teams and short sellers do. Finding flaws is easier than building, so a cheaper model can do the attacking. Then one more session rules on which objections hold. Valid objections go back to the maker, which can decline them. [I 12:57–15:39]
- **User as client.** When the user can tell good from bad themselves, their judgment of the result is enough. When they cannot, add more AI review. [I 16:15]
- **Fact checks.** Requiring a verified primary source for every number in a document can be trusted to a single session. [I 17:03]

## Access

- **Model experience.** Picture yourself as the model doing this task. You would want the raw data, a computer, the ability to install software, and room to decide for yourself. [I 22:01]
- **Prerequisite.** Every type of ambition needs a computer that can install software, plus access to the relevant data. [E]
- **Start cheap.** Let the model drive the user's tools in a browser first. Build connectors only after a workflow has proven itself. [I 24:00]
- **Generalists.** Give a generalist model the tools and the data rather than a cast of narrow persona agents with pre-sliced data. Generalist models overtook a purpose-built math system within months. [I 17:37]

## On skills

- **Half-life.** Skills often carry advice meant for the previous model generation, and removing a skill sometimes improves the output. Making that call takes an eval and a clear sense of good and bad output. [I 21:26]
