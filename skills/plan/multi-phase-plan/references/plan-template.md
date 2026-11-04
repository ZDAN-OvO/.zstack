# {{Program}} plan

{{Under ten lines: problem, users, goal, scope, exclusions, whole-change acceptance, and PR order.}}

## How to read this

Status. Ready.
Blockers. None.
Execution. {{Project workflow or sequential PR handoff; implementation starts only after explicit go.}}
Roles. {{Implementer; non-author verifier for every Behavior PR; interaction reviewer; merge authority. Author self-checks do not grant a verdict.}}
Permissions. {{Delegation and publication grants, or none; merging requires explicit authorization.}}

One box is one unit of work. Check a box only when its evidence exists. Each box names an evidence destination. Keep future implementation boxes unchecked. Tests alone do not verify behavior; complete applicable automated, live, and perf checks and justify every non-applicability decision.

## Program checklist

### Start and sequence

{{PR dependency graph, parallel groups and prerequisite interfaces; branch/stack rules, integration command after each wave, operator gates and pause/stop behavior.}}

Parallel. {{None. followed by a reason, or semicolon-separated groups of comma-separated PR IDs that can run together.}}
Feasibility. {{Load-bearing assumptions and their observed evidence, versions and limits; reference Appendix A. Unproven assumptions block Ready.}}
Acceptance. {{Map each whole-change criterion to its owning PR, observation surface, failure predicate and evidence destination.}}
Changes. {{Operator review required for changes to acceptance, budgets, coverage or non-applicability; preserve previous criteria and explain the change.}}

### Evidence rules

Versions. {{Record trunk/base and exact head SHA, working-tree state, environment, and fixture versions with each run.}}
Invalidation. {{Rerun affected checks after code, base, data, or environment changes; bind each renewed verdict to the new versions.}}
Input boundary. {{Actual UI/CLI/API driver, allowed read-only diagnostics, and stub or fault-injection disclosure.}}

### Boot recipe

{{Commands to prepare isolated data, start each affected surface, detect readiness, and save outputs. Docs-only plans explain why no app boot is needed.}}

### Verdict and handoff

Review entity. {{Real PR on the project forge, using /opening-a-pr; or an operator-accepted persisted review record when no forge exists. Record URL/path before merge-ready.}}
Verdict. {{Non-author Behavior verifier uses /verify-pr to run the actual user path, audit changed checks and original evidence. Missing independence means pending; failed or unproven acceptance blocks PASS+NOTES.}}

{{CI/review gates, interaction approval, explicit merge authorization, head/base invalidation, and handoff report destination. Reproduced trunk defects still block if they violate acceptance.}}

## PR-01 {{Task as a verb phrase}}

**Depends on.** None.

**Files.**

Base. {{Trunk. or a prerequisite PR ID followed by a period; resolve the real branch and SHA at execution.}}
Writes. {{Backticked exclusive write paths/globs, including migrations, generated files, lockfiles and fixtures.}}
Resources. {{Isolated worktree, data/store/account, ports and external state; real sharing has one writer or enforced serialization.}}
Contract. {{Interface producer, consumers, prerequisite version and compatibility; or a specific no-interface-change reason.}}

- [ ] {{Edit/create/delete real paths; define the boundary.}} Evidence. `{{diff path}}`.

**Build.**

- [ ] {{One specific change and implementation entry.}} Evidence. `{{diff or artifact}}`.

**You see.**

Kind. Behavior.
Surfaces. {{Comma-separated names such as Web, CLI, API. Use None for Docs.}}
Interaction. Yes.

- [ ] {{Observable output or screen state.}} Evidence. `{{artifact}}`.

**Verify, unit.** Required.

Sensitivity. {{Known bad version or safe controlled fault for each critical invariant, exact rejecting check and expected failure; or an operator-reviewed limitation with concrete independent proof.}}

- [ ] Run `{{real command}}` for {{named behavior/case}}. Pass when {{predicate}}. Evidence. `{{log}}`.

**Verify, live.** Required.

- [ ] Regression against trunk. Surface. {{Surface name}}. {{Run the same load-bearing scenario on trunk and head; if absent on trunk, record the absence and check the new behavior plus final state.}} Pass when {{predicate}}. Evidence. `{{artifact}}`.
- [ ] Surface. {{Surface name}}. {{Additional scenario needed for coverage or risk.}} Pass when {{predicate}}. Evidence. `{{artifact}}`.

**Verify, perf.** Required.

- [ ] Metric. {{Comparable metric and unit; include added-work and end-state metrics for a feature absent on trunk.}} Evidence. `{{measurement record}}`.
- [ ] Probe. {{Exact common driver/procedure runnable against both trees, independent of head-only files/flags/instrumentation; interleaved trunk/head order.}} Evidence. `{{raw measurements}}`.
- [ ] Baseline. {{Capture trunk first using the named command; cite measured values only if actually observed.}} Evidence. `{{baseline record}}`.
- [ ] Rule. {{Numeric threshold and unit; absolute budgets for added work and end state if scenarios differ.}} Limit. {{number}} {{unit}}. Evidence. `{{verdict record}}`.

**Review gate.** Required.

- [ ] Present screenshots and video of the changed interaction to the operator; wait for approval before merge. Evidence. `{{media and approval record}}`.

**Merge.**

Verifier. Independent.

- [ ] {{Record actual review entity URL/path and /opening-a-pr body, valid non-author /verify-pr verdict for Behavior, required checks/reviews and applicable interaction approval at exact base/head. Stop at merge-ready until explicitly authorized.}} Evidence. `{{handoff and authorization record}}`.

## Close the program

{{After explicit execution approval: account for every applicable box with actual evidence; list PR state, exact verified versions, remaining risks, operator decisions, and links. Finish only when whole-change acceptance is met or report the blocked state.}}

## Appendix A. Spike evidence

{{Every load-bearing assumption: question, alternatives, actual observations, decision, limits, source/prototype version and persistent artifacts or reproduction commands. If no new Spike was needed, show matching existing observed evidence. A direction choice alone is not feasibility evidence.}}

## Appendix B. Alternatives rejected

{{Alternatives and reasons. State None and why if there was no meaningful fork.}}

## Appendix C. Risks

{{Risk, owning PR, mitigation, and observable failure condition. Include data migration, rollback, or unavailable drivers when relevant.}}

## Appendix D. Links and decisions

{{Code pointers, conventions, test commands, entry points, prerequisite reading by PR, and decision record location.}}
