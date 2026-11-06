# .zstack

My agent skill library. Skill files exist once, under `skills/<scene>/<skill-name>/`. Each harness gets a symlink farm built from [`targets.json`](./targets.json), so adding a skill to a harness is one link and no copy.

## Layout

```
skills/<scene>/<skill-name>/SKILL.md    the skill, one copy
skills/archive/<skill-name>/            kept here, published to no harness
skills-pi/<skill-name>                  -> ../skills/<scene>/<skill-name>
skills-claude/<skill-name>              -> ../skills/<scene>/<skill-name>
```

Two levels under `skills/`: a scene, then a skill. `skills/archive/` is a bucket, not a scene, and holds skills no harness is told about. Supporting files (`references/`, `scripts/`, assets) sit beside `SKILL.md` inside the skill directory. `skills-pi/` and `skills-claude/` are never edited by hand; `scripts/link-skills.mjs` builds them from `targets.json`.

## Invocation

Every skill is one of two kinds, and the flag is independent of the harness that gets it:

- **User-invoked**: `disable-model-invocation: true` in the frontmatter, so only `/skill:<name>` reaches it. Its description is read by a human.
- **Model-invoked**: no such flag, so the model can also reach for it on its own. Its description carries trigger phrasing.

This matters most in Pi: every model-invoked description sits in its prompt on every turn, while a user-invoked skill costs nothing until it is called. The two sections below list the 31 skills that at least one harness is told about; skills in `skills/archive/` are listed under `## Archived` instead.

## Targets

[`targets.json`](./targets.json) is the single source of truth. `pi` lists what Pi gets, `claude` lists what Claude Code gets, and a name in both is shared, with the file still existing once. The checker fails when a scene skill is in no list and not archived, when a farm disagrees with the lists, or when the index below disagrees with either.

The split follows the harness. Claude Code carries the long, judgment-heavy workflows, because its harness is built for them. Pi keeps the narrow, self-contained ones and stays cheap.

## User-invoked

- **[correct](./skills/meta/correct/SKILL.md)**: Find the mistakes agents keep repeating in this repo and make each one impossible.
- **[ds-prompting](./skills/meta/ds-prompting/SKILL.md)**: DeepSeek 极限用量提示词的逐字存档，需要原样取用时调用。
- **[grill-me](./skills/plan/grill-me/SKILL.md)**: Get relentlessly interviewed about a plan or design until every branch of the design tree is settled.
- **[grill-with-docs](./skills/plan/grill-with-docs/SKILL.md)**: Grilling session that also builds the project's domain model, writing `GLOSSARY.md` and ADRs inline. Asks at most 3 questions per round.
- **[handoff](./skills/meta/handoff/SKILL.md)**: Compact the current conversation into a handoff document another agent can pick up.
- **[how](./skills/investigate/how/SKILL.md)**: Trace a subsystem’s architecture, runtime flow, ownership, and gotchas from the code.
- **[multi-phase-plan](./skills/plan/multi-phase-plan/SKILL.md)**: Ground changes in code and feasibility evidence, then plan reviewable PRs with strict verification gates and safe parallel boundaries.
- **[no-comments](./skills/build/no-comments/SKILL.md)**: Spawn the comment-sicko subagent, fix accepted findings, offer encodings for claimed constraints.
- **[readme-crafter-skill](./skills/explain/readme-crafter-skill/SKILL.md)**: Write, rewrite, or audit a repository's `README.md` as a landing page and onboarding guide.
- **[skill-creator](./skills/meta/skill-creator/SKILL.md)**: Create or revise a skill, then measure it: test cases, a review viewer, and variance analysis before shipping it.
- **[spike](./skills/plan/spike/SKILL.md)**: Settle design, behavior, timing, and feasibility questions with throwaway prototypes, observed evidence, and a recommendation.
- **[video-transcribe](./skills/documents/video-transcribe/SKILL.md)**: Bilibili 视频或本地音频转成带时间戳的中文转写，并按内容生成阅读报告或笔记。
- **[wait-what](./skills/explain/wait-what/SKILL.md)**: Stop the answer that did not land and re-pitch it: context first, Simplified Technical English, project glossary terms.
- **[why](./skills/investigate/why/SKILL.md)**: Investigate the evidence behind design decisions across git history and available MCP sources, separating facts from inference.

## Model-invoked

- **[answer-me-with-html](./skills/explain/answer-me-with-html/SKILL.md)**: Draft an answer as Markdown and let a bundled CLI build it into a one-page visual HTML explainer, with diagrams, charts and a writing check.
- **[archify](./skills/explain/archify/SKILL.md)**: Render architecture, workflow, sequence, ERD and lifecycle diagrams plus one-page explainers as standalone HTML through a JSON-IR CLI.
- **[diagnosing-bugs](./skills/investigate/diagnosing-bugs/SKILL.md)**: Diagnosis loop for hard bugs and perf regressions, built on a tight pass/fail feedback loop.
- **[dispatching-parallel-agents](./skills/build/dispatching-parallel-agents/SKILL.md)**: Split independent work across agents dispatched in one response, then review and integrate what they return.
- **[docx](./skills/documents/docx/SKILL.md)**: Create, read, edit and template Word `.docx`/`.dotx` files.
- **[domain-modeling](./skills/plan/domain-modeling/SKILL.md)**: Build and sharpen the domain model: challenge terms, test edge-case scenarios, keep `GLOSSARY.md` and ADRs current.
- **[find-skills](./skills/meta/find-skills/SKILL.md)**: Discover and install skills from the open agent skills ecosystem.
- **[grilling](./skills/plan/grilling/SKILL.md)**: Interview the user relentlessly about a plan until every branch of the design tree is settled. The engine behind `/grill-me` and `/grill-with-docs`.
- **[pdf](./skills/documents/pdf/SKILL.md)**: Read, merge, split, fill, encrypt and OCR PDFs.
- **[pptx](./skills/documents/pptx/SKILL.md)**: Build, parse and edit `.pptx` decks from templates.
- **[prototype](./skills/plan/prototype/SKILL.md)**: Build a throwaway prototype to answer a design question: one shareable HTML file for a state model, or several switchable UI variations on one route.
- **[shuorenhua](./skills/explain/shuorenhua/SKILL.md)**: Cut packaging and translationese from Chinese or English without dropping facts, terms or who is responsible, or mark the problems without rewriting.
- **[tdd](./skills/build/tdd/SKILL.md)**: Write the failing regression test before fixing a bug with a cheap local test target, and fall back to the closest executable check when a test is impractical.
- **[verification-before-completion](./skills/verify/verification-before-completion/SKILL.md)**: Put every completion claim behind fresh evidence: run the check, read the output, then report.
- **[writing-for-agents](./skills/meta/writing-for-agents/SKILL.md)**: The levers for writing anything an agent consumes: context pointers, skills, `AGENTS.md`, and pointer wording.
- **[xlsx](./skills/documents/xlsx/SKILL.md)**: Read, edit, clean and generate spreadsheets, formulas and charts.
- **[zdan-mode](./skills/meta/zdan-mode/SKILL.md)**: zdan's agent style for plan-gated work, delegated execution, evidence-based verification, small stacked PRs, and terse Chinese reporting.

## Archived

- **[arena](./skills/archive/arena/SKILL.md)**: Compare parallel candidates for the same task, select a base, combine their strongest parts, and verify the result.
- **[automate-me](./skills/archive/automate-me/SKILL.md)**: Turn recurring working preferences and conversation evidence into a personal mode skill, or update an existing one.
- **[benchmark-checklist](./skills/archive/benchmark-checklist/SKILL.md)**: Check performance measurements for bottlenecks, fair tuning, errors, repeatability, and user-visible impact.
- **[blast-radius](./skills/archive/blast-radius/SKILL.md)**: Trace what a change could break beyond its diff and run real code to prove the key safety assumptions.
- **[book-to-skill](./skills/archive/book-to-skill/SKILL.md)**: Convert a book or document into a structured agent skill holding its frameworks, mental models, and anti-patterns.
- **[bro](./skills/archive/bro/SKILL.md)**: Say it again in plain human language, without jargon.
- **[code-review](./skills/archive/code-review/SKILL.md)**: Review the diff since a fixed point on two axes, Standards and Spec, run as parallel sub-agents and reported side by side.
- **[codebase-design](./skills/archive/codebase-design/SKILL.md)**: Shared vocabulary for deep modules: interface, seam, depth, adapter, plus deepening and design-it-twice passes.
- **[create-verification-skill](./skills/archive/create-verification-skill/SKILL.md)**: Generate and exercise a project-local skill for launching the real app, driving features, and preserving evidence.
- **[impeccable](./skills/archive/impeccable/SKILL.md)**: Steer and review an existing interface with 24 named design moves, from a scored critique and technical audit to bolder, quieter, polish, or a deliberate rewrite. Ships a rule-based slop detector.
- **[improve-codebase-architecture](./skills/archive/improve-codebase-architecture/SKILL.md)**: Find opportunities to deepen modules, compare them in a visual HTML report, and work through a chosen design.
- **[in-your-own-words](./skills/archive/in-your-own-words/SKILL.md)**: Restate your reading of the user's goals and the problem before working on it.
- **[interrogate](./skills/archive/interrogate/SKILL.md)**: Challenge a change with parallel adversaries and retain only findings confirmed by rerunning their reproductions.
- **[maintain-verification-skill](./skills/archive/maintain-verification-skill/SKILL.md)**: Keep a project’s verification skill and feature map accurate through source review and live feature checks.
- **[opening-a-pr](./skills/archive/opening-a-pr/SKILL.md)**: Write a fixed PR briefing on the problem, changes, scope, risk and observed verification, with original evidence linked.
- **[retro](./skills/archive/retro/SKILL.md)**: Retrospective on a coding session, most severe improvement first.
- **[sharpen](./skills/archive/sharpen/SKILL.md)**: Make a task deeper rather than bigger, then rewrite the prompt to ask for that.
- **[show-me](./skills/archive/show-me/SKILL.md)**: Explain the current topic visually with diagrams, code-shape sketches, and focused HTML artifacts.
- **[to-goal](./skills/archive/to-goal/SKILL.md)**: Compile approved work and the current repo state into a copyable goal another session can execute and verify. Read-only.
- **[unslop](./skills/archive/unslop/SKILL.md)**: Cut AI tells from any writing.
- **[vercel-react-best-practices](./skills/archive/vercel-react-best-practices/SKILL.md)**: React and Next.js performance rules from Vercel Engineering.
- **[verify-pr](./skills/archive/verify-pr/SKILL.md)**: Independently run a PR’s real behavior, audit acceptance and check sensitivity, and issue a verdict bound to its versions.
- **[voice-debrief](./skills/archive/voice-debrief/SKILL.md)**: 面试或会议录音转写复盘，可存飞书文档并归档到对应多维表格。

## Install

Each harness needs one directory symlink, pointing at its farm:

```bash
node scripts/link-skills.mjs          # rebuild both farms from targets.json, then point the two links at them
node scripts/link-skills.mjs --check  # report a missing, stale, or wrong link
```

| Harness | Link | Farm |
| --- | --- | --- |
| Pi | `~/.pi/agent/skills` | `skills-pi/` |
| Claude Code | `~/.claude/skills` | `skills-claude/` |

Because each farm is one symlink per skill, a `git pull` keeps both harnesses current and no skill file is ever copied. Then run `/reload` in Pi. Conventions for installing, adapting, and indexing skills live in [`AGENTS.md`](./AGENTS.md).
