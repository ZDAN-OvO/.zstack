# Spike extraction and upstream comparison

## Source

- Repository: https://github.com/cursor/plugins
- Revision: `ae5650febf4320793844c12c4adaa937f417f8da`.
- Playbook: `pstack/skills/poteto-mode/playbooks/prototype.md`.
- Parent invocation mode: `pstack/skills/poteto-mode/SKILL.md` sets `disable-model-invocation: true`; this extraction preserves it.
- Supporting principle: `pstack/skills/principle-exhaust-the-design-space/SKILL.md`.
- License: MIT, copyright (c) 2026 Lauren Tan. The upstream license is included in `../LICENSE`.
- `upstream-prototype.md` is an unchanged, byte-for-byte snapshot of the pinned playbook, retained for comparison rather than execution.

## Extraction boundary

This skill preserves the complete Prototype playbook: visual exploration, reference gathering, empirical behavior and timing probes, competing variants, observation, recommendations, and the handoff to implementation. It is not narrowed to backend feasibility. The surrounding Poteto mode's global rules and other playbooks are not imported.

The six steps remain in their original order. The original restrictions on scratch directories, production frameworks, tests, abstractions, and production readiness remain. No extra process, persistence requirement, test suite, or evidence threshold is added.

## All adaptations

The new frontmatter supplies the standalone name and human-facing description, and retains the parent skill's user-invoked mode. The complete set of changed body lines follows. All other body lines are unchanged.

1. Original: ### Prototype

   Standalone: # Spike

2. Original: The real build follows Feature.

   Standalone: The real build follows a separate implementation task.

3. Original: The one playbook where the Laziness Protocol's "smallest change" and the verification bar invert.

   Standalone: The workflow where the production defaults of the "smallest change" and the verification bar invert.

4. Original: No decision means no prototype. Route to Feature.

   Standalone: No decision means no prototype. Return the work to the implementation workflow.

5. Original: This is the **exhaust-the-design-space** principle skill made cheap.

   Standalone: For a novel UI interaction or architectural decision with no precedent in the codebase, build 2-3 competing prototypes and compare side by side before committing. This also applies to product design decisions where user experience depends on feel, not logic.

6. Original: screenshot each variant via the control skill and drive the interaction.

   Standalone: screenshot each variant via the available browser or UI automation tools and drive the interaction.

7. Original: Hand the chosen direction to **Feature** (or `architect` for the shape) for the real build.

   Standalone: Hand the chosen direction to a separate implementation task (or an architecture-design task for the shape) for the real build.

The Laziness Protocol reference becomes its production-default meaning. Feature and architect become explicit implementation and architecture handoffs, without inventing installed skills. The control-skill binding becomes the host's available browser or UI automation tools. The design-space principle's trigger and 2-3 prototype guidance are inlined from its own frontmatter, followed by its unchanged body sentence, so no missing principle skill is required.

## Capability coverage

| Upstream requirement | Standalone location |
| --- | --- |
| Own the decision; keep the artifact throwaway | Opening paragraph |
| Speed over polish; explore unrequested alternatives | Opening instructions |
| Identify a visual or empirical decision; route away without one | Step 1 |
| Research references and let the user select open visual directions | Step 2 |
| Use an isolated scratch directory and the lightest runnable instrument | Step 3 |
| Keep production frameworks, tests, and abstractions out | Step 3 |
| Label alternatives and compare through a switcher | Step 4 |
| Operate the visual artifact and capture each variant | Step 5 |
| Observe actual behavior, output, or timing | Step 5 |
| Present alternatives, tradeoffs, and a recommendation | Step 6 |
| Hand off the decision for a separate real build | Opening paragraph and step 6 |
| Report evidence, scratch path, and throwaway status | Reply contract |

## Deliberately unchanged limitations

The upstream playbook does not define a general SDK/database compatibility protocol, performance statistics, numeric pass thresholds, or automated prototype tests. This extraction does not add them. A lightweight probe still needs to observe the actual question to support its conclusion.
