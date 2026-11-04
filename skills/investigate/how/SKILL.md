---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
disable-model-invocation: true
---

# How

Explore the codebase to answer "how does X work?" questions. Produce architectural explanations at the level of a senior engineer onboarding onto a subsystem, enough to build a working mental model, not so much that it reads like annotated source code.

Every spawn uses Pi's `subagent` tool with `agent: "scout"` for explorers and `agent: "reviewer"` for explainers, and a read-only task brief. Explorers use the `how explorer` line in `~/.pi/agent/pstack-models.md`, and every explainer uses the `how explainer` line. Set `model` to that line's exact Pi `provider/id`; if the file or line is missing, or the value is `auto`, leave `model` unset to use the agent's configured Pi model. For `inherit-parent`, pass the current session's exact `provider/id`. Use `subagent({ action: "models" })` to inspect available models. If a launch fails, stop and report the failure rather than switching runtimes or retrying a rejected model. Read `/pi-subagents` for the native call shape and reasoning overrides. Run dependent exploration and synthesis inside one async scripted workflow; native completion wakes the parent.

## 1. Assess complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (a single module, a small utility, a narrow question such as "how does function X work"): no explorers. Spawn one explainer that explores and explains in one pass, built from `references/explainer-prompt.md` without the explorer-findings section. Go to step 4.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): go to step 2.

When in doubt, take the simple path.

## 2. Explore (complex only)

Decompose the question into 2 to 4 angles, each a distinct slice of the subsystem. Spawn all explorers in a single message, each with `references/explorer-prompt.md` and its angle filled in.

## 3. Synthesize (complex only)

Once all explorers have returned, spawn one explainer with `references/explainer-prompt.md` and every explorer's findings filled in.

## 4. Present

Present the explainer's output. Light edits for clarity or context from the conversation are fine. Do not substantially rewrite it.

## Output format

The explanation uses the sections defined in `references/explainer-prompt.md`, dropping any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.
