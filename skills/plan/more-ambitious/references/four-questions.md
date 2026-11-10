# Four questions: source distilled

Source: Gary_Chen, 《Anthropic 工程主管教你打破 AI 的上限》, Bilibili BV1Tm4E6MEXp, 13:34. A retelling of an X article by Felix Rieseberg (engineering lead on Claude at Anthropic; the video puts it at over 5M views). Everything below is the video's claim unless tagged **[inference]**. Quotes are from the auto transcript, lightly corrected.

## Thesis

- **Ceiling.** Same model, same subscription: what you get out depends on your *ambition* and *understanding*. 「野心决定你敢把多大的问题交给 AI，而认知决定你能让 AI 发挥出多深多广的实力。」
- **Habit, not IQ.** Felix sees a split: a few people do remarkable work with Claude, most use it as a search engine or typewriter. The limit stopped being model intelligence a year or more ago. It is old working habits that keep big problems from ever being handed over.
- **The human is the subject.** The four questions are asked *of yourself* (「你可以问自己四个问题」), whether you hand the work to AI or decide to do it by hand. The payoff compounds in the person: 「每一次 AI 的回答都会把你的认知跟野心再往上推一层。」

## Leading words

| Word | Meaning | Anchor example | Failure it names |
|---|---|---|---|
| **speed** | Do it faster | 2-hour code in 5 minutes; automation | None. Everyone does this, so it doesn't separate people |
| **height** | Hand over the *result*, not the *step* | Felix: "fix this crash bug" → "make the app stop crashing"; AI then pulls crash reports, fixes and tests on its own | **Ground view**: pre-chopping steps. It underuses the model, and your chosen steps may point the wrong way |
| **then what?** | The one question that climbs height, a rung at a time | Quarterly review ladder (below) | Jumping straight to an unbounded goal: 「帮我搞个 100 万来花花」 |
| **back off one rung** | Stop rule. Climb until AI starts doing badly, then step down. That rung is the largest goal you can hand over today | — | Treating the ceiling as known instead of found by trying |
| **depth** | Expert-grade method and tools, not intuition | Painkiller for a headache vs a specialist who runs blood work and X-rays before prescribing | **Painkiller**: AI defaults to the mediocre answer unless asked otherwise |
| **cognition ceiling** | Why depth is hard: you are not the expert, so you can't ask for expert depth | — | Asking only what you already know to ask |
| **persona trap** | "You are a 10-year senior marketer" changes tone and vocabulary, not method | Homepage copy rewrite | 「用专家的口气讲外行话」 |
| **four questions (depth)** | Ask AI *before* it acts: what would a top expert do that I didn't think of; which first-hand sources would they read instead of digested reports; which specific methods and tools; how to prove it works beyond "you and I feel it's good" | Homepage conversion (below) | Skipping diagnosis |
| **raw material** | Primary evidence over summaries | Support chats, reviews, session recordings, heatmaps; best headlines are often lifted from customers' own words | Starting from the dashboard |
| **stretch target** | State an unreasonable goal and insist it is reasonable | Page loads in 10 s, you want 5 s: ask for 0.2 s. When AI says impossible, reply "it can be done, keep going" | A modest target only buys patches; 200 ms forces a different approach |
| **breadth** | Borrow the best weapons from *other* fields | — | Staying inside one industry's playbook |
| **noun label** | A deliverable's name ("homepage", "sales deck") carries an industry tag and locks AI's search to that field | "Build a homepage" → AI reads only web-design knowledge, since that is usually efficient | Asking for the thing by its name |
| **noun → verb** | Drop the deliverable's name; state the function it must perform, which is shared across fields. From the book 《创新的艺术》 (English title not given in the video) | Homepage → "make a stranger stop within 5 seconds and get curious" → ask who is best at that: trailer editors, short-video creators, department-store window designers | — |
| **before asking** | The real block is upstream: deciding "AI can't do that" without ever asking | — | **Self-limiting** |
| **proof by others** | Look at what others already did | 4-minute mile broken by Roger Bannister in 1954, again 46 days later; a 28-year-old Spanish product manager with no astronomy training or telescope used Claude Code on public data for 120k+ stars and found a potential new planet | — |
| **near-zero cost** | A wrong real-world call loses money; asking AI something it can't do costs minutes and some tokens. You don't need to believe it can, just try once | Sam Altman, "How to be successful": most people overestimate risk and underestimate reward | Fear |

## Worked examples

**Quarterly review: the height ladder.**
1. Paste numbers into last quarter's template. The deck is done, but on page 3 the boss asks why the number fell.
2. Give AI all the data. Ask what changed this quarter, why, and what to do next. Output becomes an analysis.
3. Ask AI for the three most urgent decisions, each with the case for and against. The meeting discusses next steps, not numbers.
4. Ask whether the quarterly report is a relic. It existed because human analysis was slow; its purpose is to spot problems early and move money and people. Design daily monitoring that stays quiet and alerts the boss only on significant change. Prove on historical data that it catches problems earlier, then run it beside the current report for one quarter and compare.

Same AI throughout. The difference is how many times "then what?" was asked.

**Homepage conversion: depth's four questions, as the author ran them on Claude.**
- Expert move: don't touch the copy first. Confirm the copy is the problem. The ads may have changed audience, the page may have slowed, the tracking may be broken.
- Raw material: support conversations, customer reviews, session recordings, heatmaps. See where visitors stop and leave.
- Methods: the LIFT model, checking the page block by block on value proposition, relevance, clarity, anxiety, urgency, plus one more dimension the transcript renders as 「分析」 (possibly *distraction*; unverified). Also the 5-second test: a stranger sees the page for 5 seconds, then says what it is, who it's for, and why to choose it. If they can't, the page isn't doing its job.
- Proof: not your opinion or AI's. Real customers, via an A/B test of old vs new copy.

## Evidence status

- **Anecdotes**: Felix's crash example, the Berkeley student (1939, saw two unsolved statistics problems on the board, took them for homework, solved them; the video gives no name), the Spanish PM. Illustrative, not data.
- **Research**: Locke & Latham, 35 years of goal-setting studies: specific, hard goals beat "do your best". The subjects are **humans**; applying it to LLM prompting is the video's extrapolation.
- **Transcript artefacts**: "1600 公尺" is the mile; the LIFT dimension list above has one uncertain item; the 5M-view figure is the video's claim.

## How the dimensions relate **[inference]**

The video presents four separate questions. Its own examples show dependencies:

- **Speed enables height.** Rung 4 of the quarterly ladder exists because AI reads data fast; near-zero cost is also a speed claim.
- **Depth reopens height.** Depth's first expert move ("is the copy really the problem?") questions the task itself, which is a height move.
- **Depth before breadth.** The video's order. Depth first confirms the problem and exhausts the home field's expert methods; breadth borrows from other fields where those fall short. The homepage example runs this way: diagnose the copy and run the 5-second test, then restate the page as "stop a stranger in 5 seconds" and look to trailer editors.
- **Stretch pushes depth into breadth.** Once one field's patches can't reach 200 ms, the remaining options lie elsewhere.
- **Breadth can reopen height.** Noun → verb usually restates the deliverable's job; when it changes the result itself, that is a height move.
