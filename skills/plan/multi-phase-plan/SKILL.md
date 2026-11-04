---
name: multi-phase-plan
description: "Ground a substantial change in code and feasibility evidence, then plan independently reviewable PRs with strict verification gates and safe parallel boundaries."
metadata:
  source: "https://github.com/cursor/plugins/blob/ae5650febf4320793844c12c4adaa937f417f8da/pstack/skills/poteto-mode/playbooks/multi-phase-plan.md"
  revision: ae5650febf4320793844c12c4adaa937f417f8da
  adaptation: "Locally authored workflow and checker; direct grounding, authorized Spike, feasibility and parallel contracts, companion PR briefing and independent verifier. No scheduler or fixed swarm."
disable-model-invocation: true
---

# Multi-phase plan

**You own the plan, not the code.** Deliver a checklist an implementer can execute and the operator can audit from evidence. Production implementation starts in a separate task after the operator's explicit go.

## Check the size

When the change is one or two files with an obvious approach, skip the plan. Say so and stop.

For that branch, return only the decision and its brief reason in at most two sentences, in the operator's language. Produce no plan file, mini-plan, implementation instructions, or validation checklist. Once the scope is clear, end here rather than reading the full workflow.

## Plan a substantial change

For any other change, read [the full workflow](references/workflow.md) and follow it through investigation, `/spike` handoff when needed, PR planning, evidence design, readiness checking, and operator handback. The workflow links the template, examples, and checker reference.

Use the project's path convention, otherwise `docs/plans/<topic>.md`. The deliverable is one plan, with exact check output and outstanding decisions. Execution waits for the operator's explicit go.

Execution uses `/opening-a-pr` for the actual PR body and `/verify-pr` for independent behavior verification. The plan's nine PR blocks are the implementer's checklist, not the PR description.
