# astack

My agent skill library. Each directory under `skills/` is one Agent Skill, copied byte for byte from upstream and adapted only where Pi needs it, or written for this library. Skills are published by symlinking `~/.agents/skills` at the `skills/` folder itself.

## Layout

```
skills/<skill-name>/SKILL.md
```

Flat, one level, no category folders. [`skills/`](./skills) is the whole library, and this README is its only index. Adding a skill means adding a directory and one line here; there is no bucket to choose and no second index to keep in sync.

Supporting files (`references/`, `scripts/`, assets) sit beside `SKILL.md` inside the skill directory.

## Invocation

Every skill is one of two kinds:

- **User-invoked**: `disable-model-invocation: true` in the frontmatter, so only `/skill:<name>` reaches it. Its description is read by a human.
- **Model-invoked**: no such flag, so the model can also reach for it on its own. Its description carries trigger phrasing.

## User-invoked

- **[arena](./skills/arena/SKILL.md)**: Compare parallel candidates for the same task, select a base, combine their strongest parts, and verify the result.
- **[benchmark-checklist](./skills/benchmark-checklist/SKILL.md)**: Check performance measurements for bottlenecks, fair tuning, errors, repeatability, and user-visible impact.
- **[blast-radius](./skills/blast-radius/SKILL.md)**: Trace what a change could break beyond its diff and run real code to prove the key safety assumptions.
- **[bro](./skills/bro/SKILL.md)**: Say it again in plain human language, without jargon.
- **[correct](./skills/correct/SKILL.md)**: Find the mistakes agents keep repeating in this repo and make each one impossible.
- **[create-verification-skill](./skills/create-verification-skill/SKILL.md)**: Generate and exercise a project-local skill for launching the real app, driving features, and preserving evidence.
- **[ds-prompting](./skills/ds-prompting/SKILL.md)**: DeepSeek 极限用量提示词的逐字存档，需要原样取用时调用。
- **[grill-me](./skills/grill-me/SKILL.md)**: Get relentlessly interviewed about a plan or design until every branch of the design tree is settled.
- **[grill-with-docs](./skills/grill-with-docs/SKILL.md)**: Grilling session that also builds the project's domain model, writing `GLOSSARY.md` and ADRs inline. Asks at most 3 questions per round.
- **[handoff](./skills/handoff/SKILL.md)**: Compact the current conversation into a handoff document another agent can pick up.
- **[how](./skills/how/SKILL.md)**: Trace a subsystem’s architecture, runtime flow, ownership, and gotchas from the code.
- **[improve-codebase-architecture](./skills/improve-codebase-architecture/SKILL.md)**: Find opportunities to deepen modules, compare them in a visual HTML report, and work through a chosen design.
- **[in-your-own-words](./skills/in-your-own-words/SKILL.md)**: Restate your reading of the user's goals and the problem before working on it.
- **[interrogate](./skills/interrogate/SKILL.md)**: Challenge a change with parallel adversaries and retain only findings confirmed by rerunning their reproductions.
- **[learn-tech](./skills/learn-tech/SKILL.md)**: Learn a language, framework or library from official docs and version-matched source, checking understanding through teach-back and small exercises.
- **[maintain-verification-skill](./skills/maintain-verification-skill/SKILL.md)**: Keep a project’s verification skill and feature map accurate through source review and live feature checks.
- **[multi-phase-plan](./skills/multi-phase-plan/SKILL.md)**: Ground changes in code and feasibility evidence, then plan reviewable PRs with strict verification gates and safe parallel boundaries.
- **[no-comments](./skills/no-comments/SKILL.md)**: Spawn the comment-sicko subagent, fix accepted findings, offer encodings for claimed constraints.
- **[readme-crafter-skill](./skills/readme-crafter-skill/SKILL.md)**: Write, rewrite, or audit a repository's `README.md` as a landing page and onboarding guide.
- **[retro](./skills/retro/SKILL.md)**: Retrospective on a coding session, most severe improvement first.
- **[sharpen](./skills/sharpen/SKILL.md)**: Make a task deeper rather than bigger, then rewrite the prompt to ask for that.
- **[show-me](./skills/show-me/SKILL.md)**: Explain the current topic visually with diagrams, code-shape sketches, and focused HTML artifacts.
- **[skill-creator](./skills/skill-creator/SKILL.md)**: Create or revise a skill, then measure it: test cases, a review viewer, and variance analysis before shipping it.
- **[spike](./skills/spike/SKILL.md)**: Settle design, behavior, timing, and feasibility questions with throwaway prototypes, observed evidence, and a recommendation.
- **[to-goal](./skills/to-goal/SKILL.md)**: Compile approved work and the current repo state into a copyable goal another session can execute and verify. Read-only.
- **[unslop](./skills/unslop/SKILL.md)**: Cut AI tells from any writing.
- **[wait-what](./skills/wait-what/SKILL.md)**: Stop the answer that did not land and re-pitch it: context first, Simplified Technical English, project glossary terms.
- **[why](./skills/why/SKILL.md)**: Investigate the evidence behind design decisions across git history and available MCP sources, separating facts from inference.

## Model-invoked

- **[answer-me-with-html](./skills/answer-me-with-html/SKILL.md)**: Draft an answer as Markdown and let a bundled CLI build it into a one-page visual HTML explainer, with diagrams, charts and a writing check.
- **[archify](./skills/archify/SKILL.md)**: Render architecture, workflow, sequence, ERD and lifecycle diagrams plus one-page explainers as standalone HTML through a JSON-IR CLI.
- **[code-review](./skills/code-review/SKILL.md)**: Review the diff since a fixed point on two axes, Standards and Spec, run as parallel sub-agents and reported side by side.
- **[codebase-design](./skills/codebase-design/SKILL.md)**: Shared vocabulary for deep modules: interface, seam, depth, adapter, plus deepening and design-it-twice passes.
- **[diagnosing-bugs](./skills/diagnosing-bugs/SKILL.md)**: Diagnosis loop for hard bugs and perf regressions, built on a tight pass/fail feedback loop.
- **[dispatching-parallel-agents](./skills/dispatching-parallel-agents/SKILL.md)**: Split independent work across agents dispatched in one response, then review and integrate what they return.
- **[domain-modeling](./skills/domain-modeling/SKILL.md)**: Build and sharpen the domain model: challenge terms, test edge-case scenarios, keep `GLOSSARY.md` and ADRs current.
- **[find-skills](./skills/find-skills/SKILL.md)**: Discover and install skills from the open agent skills ecosystem.
- **[grilling](./skills/grilling/SKILL.md)**: Interview the user relentlessly about a plan until every branch of the design tree is settled. The engine behind `/grill-me` and `/grill-with-docs`.
- **[impeccable](./skills/impeccable/SKILL.md)**: Steer and review an existing interface with 24 named design moves, from a scored critique and technical audit to bolder, quieter, polish, or a deliberate rewrite. Ships a rule-based slop detector.
- **[ljg-explain](./skills/ljg-explain/SKILL.md)**: Explain a concept, formula or mechanism in plain Chinese until the reader can recognise it, derive results and transfer the reasoning to a new case.
- **[opening-a-pr](./skills/opening-a-pr/SKILL.md)**: Write a fixed PR briefing on the problem, changes, scope, risk and observed verification, with original evidence linked.
- **[prototype](./skills/prototype/SKILL.md)**: Build a throwaway prototype to answer a design question: one shareable HTML file for a state model, or several switchable UI variations on one route.
- **[shuorenhua](./skills/shuorenhua/SKILL.md)**: Cut packaging and translationese from Chinese or English without dropping facts, terms or who is responsible, or mark the problems without rewriting.
- **[tdd](./skills/tdd/SKILL.md)**: Write the failing regression test before fixing a bug with a cheap local test target, and fall back to the closest executable check when a test is impractical.
- **[verification-before-completion](./skills/verification-before-completion/SKILL.md)**: Put every completion claim behind fresh evidence: run the check, read the output, then report.
- **[verify-pr](./skills/verify-pr/SKILL.md)**: Independently run a PR’s real behavior, audit acceptance and check sensitivity, and issue a verdict bound to its versions.
- **[writing-for-agents](./skills/writing-for-agents/SKILL.md)**: The levers for writing anything an agent consumes: context pointers, skills, `AGENTS.md`, and pointer wording.

## Scoped

`scoped-skills/` holds skills that are real but should not sit in every session's context: one book converter, React/Next performance, video transcription, recording debriefs, and the Word, PDF, Sheets and Slides pipelines. Nothing here is in Pi's skill path, so none of it is advertised or loaded, and that is deliberate: Pi reads only `~/.agents/skills` under `~/.agents/`, so the folder's own link at `~/.agents/scoped-skills` is a stable path to reach it, not a place Pi scans. A project that needs one symlinks it into its own `.agents/skills/`:

```bash
mkdir -p .agents/skills
ln -s ~/.agents/scoped-skills/docx .agents/skills/docx
```

Pi discovers project `.agents/skills/` from the working directory up to the repository root once the project is trusted, and its loader follows directory symlinks, so the skill loads in that project only and disappears from everywhere else.

- **[book-to-skill](./scoped-skills/book-to-skill/SKILL.md)**: Convert a book or document into a structured agent skill holding its frameworks, mental models, and anti-patterns.
- **[docx](./scoped-skills/docx/SKILL.md)**: Create, read, edit and template Word `.docx`/`.dotx` files.
- **[pdf](./scoped-skills/pdf/SKILL.md)**: Read, merge, split, fill, encrypt and OCR PDFs.
- **[pptx](./scoped-skills/pptx/SKILL.md)**: Build, parse and edit `.pptx` decks from templates.
- **[vercel-react-best-practices](./scoped-skills/vercel-react-best-practices/SKILL.md)**: React and Next.js performance rules from Vercel Engineering.
- **[video-transcribe](./scoped-skills/video-transcribe/SKILL.md)**: Bilibili 视频或本地音频转成带时间戳的中文转写，并按内容生成阅读报告或笔记。
- **[voice-debrief](./scoped-skills/voice-debrief/SKILL.md)**: 面试或会议录音转写复盘，可存飞书文档并归档到对应多维表格。
- **[xlsx](./scoped-skills/xlsx/SKILL.md)**: Read, edit, clean and generate spreadsheets, formulas and charts.

`scoped-skills/` is a store, not a second library: it has no loader of its own.

## Install

`~/.agents/skills` is one symlink to this repo's `skills/` folder, and `~/.agents/scoped-skills` one to `scoped-skills/`, so every skill here is a skill Pi can load, the scoped store stays out of Pi's way, and `git pull` keeps both current:

```bash
node scripts/link-skills.mjs          # point both links at this repo, replacing the old per-skill links
node scripts/link-skills.mjs --check  # report a wrong or missing link
```

Then run `/reload` in Pi. Conventions for installing, adapting, and indexing skills live in [`AGENTS.md`](./AGENTS.md).
