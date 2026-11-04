# Full planning workflow

Read this after the size check requires a full plan. This workflow ends with a plan, not production implementation.

## 2. Ground the change

Inspect the project instructions and real code. Explain the affected request/command flow, state owners, public contracts, existing callers, module loading, and check/launch entry points. Identify the user goal, scope, exclusions, and whole-change acceptance. Return code pointers and runnable commands; distinguish observations from assumptions. A file list alone does not establish understanding.

Investigate directly by default. For a cross-module ownership question, propose `/how`; for a safety assumption across a boundary, propose `/blast-radius`. These are user-invoked: use them only when invoked or explicitly authorized, otherwise do the bounded investigation yourself. Delegate exploration only with authority, using available models and read-only scopes.

Finish when every affected surface and shared dependency has an owner, the current flow is explained, and the assumptions that could change the design are listed.

## 3. Pass the feasibility gate

For each load-bearing assumption, name the decision, alternatives, observation that settles it, source version/conditions, conclusion, and artifact or reproduction command. Reuse observations only when the question, version, and conditions match. A settled product direction is not proof of technical feasibility.

For an unproven architecture, interaction, integration, or timing assumption, prepare a `/spike` task for the smallest experiment that can falsify it. `/spike` is user-invoked; execute it only with explicit authority. Otherwise return the task and pause dependent planning, continuing independent investigation if useful. Do not replace it with an unapproved experiment. Ask the operator about product or preference choices that observation cannot settle, with grounded options.

Observe the actual property: a browser-visible deadline needs a browser observation; a server timer measures server work. Record failed and inconclusive experiments. Preserve the source/prototype revision or content hash and needed artifacts outside disposable scratch, or provide working reproduction instructions. A report's explanation is supported only as far as its observations show.

Finish only when the load-bearing assumptions have applicable observed evidence. Existing verified behavior can satisfy this gate without a redundant prototype. If evidence, authorization, or a consequential decision is missing, return Draft, the blocker, and next action. Do not mark the plan Ready.

## 4. Divide into deliverable PRs

Read [the template](plan-template.md). Use its structural labels and nine PR blocks; write prose in the operator's language. Use the project path convention, otherwise `docs/plans/<topic>.md`.

One section is one PR that leaves an independently usable, verifiable state. List each dependency and branch base. When making a contract required, migrate all existing callers in the same PR, including pages and probes. Trace new imports/assets to a loader, build output, or serving route. A temporarily broken caller or unloadable module is not an acceptable PR boundary.

For each PR, fill the delivery fields under Files: branch base, exact write ownership, shared resource isolation, and interface producer/consumers. Include schema migrations, fixtures, generated files, lockfiles, ports, accounts and external state, not only source files. Put the parallel schedule in Start and sequence. Use separate worktrees and data/ports for independent writers. A shared file or migration has one owner; factor a prerequisite contract PR or serialize it. Different files with a shared mutable resource are not automatically independent. Start dependent work after its parent merges, or explicitly use its parent branch. Every parallel wave ends with an integration check of its combined state.

Finish when each intermediate PR can ship, every shared write has one owner or enforced serialization, and the schedule names its integration check. Do not add a tracker, separate spec, or tickets unless requested.

## 5. Freeze the acceptance and review contract

Map each whole-change criterion to its owning PR, observation surface, failure predicate, and evidence destination. Keep this acceptance map authoritative. Changes to a criterion, budget, coverage, or non-applicability reason need explicit review by the operator; a passing run after weakening a check does not preserve acceptance. State the execution roles, delegation/publication grants, review entity, and merge authority. Planning approval is not execution or merge approval.

Specify these evidence requirements in the plan:

- **Automated.** Name relevant commands and behavior cases. For each critical invariant, plan a sensitivity check against a known bad version or a controlled fault in an isolated copy: show that the same check rejects the intended error before trusting its passing result. Do not mutate production/shared state. For a property that cannot safely be faulted, name the limitation and a concrete independent observation for operator review; it remains unproven until that alternative is accepted and run. A Docs PR can explain why no automated check applies.
- **Live.** Run the real affected surfaces and observe both the operation and its side effects. Cover every surface in You see. Include the same load-bearing scenario on trunk/base and head; if the feature is absent on trunk, record absence and gate added behavior plus the user's end state. Locate fault injection relative to the side effect: aborting before execution cannot prove recovery after a committed operation loses its response. Choose scenarios from failure risks, not a fixed lane count. Docs may justify non-applicability.
- **Boot and drivers.** Name exact base/head versions to record, isolated data/ports, startup and readiness commands, input drivers, allowed read-only diagnostics, teardown, and stub/fault boundaries. Reuse the project's verified harness. A new driver/proxy must have an owning PR/file, creation/build and launch commands, ports, readiness, teardown, and limits. A nonexistent driver with only a future invocation is not reproducible. If the project has no runnable path, propose `/create-verification-skill` with its required authority or keep the affected part Draft.
- **Perf.** When runtime, queries, concurrency, startup, build output, or latency can change, name Metric, Probe, Baseline, Rule. Use one runnable common probe or a concrete equivalent procedure on both trees, trunk first and comparable interleaved runs. Head-only files/flags cannot measure trunk. Set numeric failure limits with units. If trunk lacks the feature, use absolute added-work and user-end-state budgets rather than a ratio between unlike scenarios. Observe the named property; HTTP completion cannot substitute for a visible-state budget. Otherwise give a change-specific non-applicability reason.
- **Interaction review.** Changed interactions require operator review of screenshots and video before merge; duration follows the proof. Include initial conditions, actions, intermediate states, final result and required refresh/retry. Label versions, real paths, and stubs/faults. Posting media is not approval. No-interaction PRs give a reason.
- **Independent verdict.** Every Behavior PR requires a verifier who did not implement its product or check changes. Plan `/verify-pr` and one authorized verifier per PR, human or Agent, rather than a fixed swarm. The verifier runs the user path and inspects original artifacts, including changed checks and non-applicability reasons. Author self-checks are preparation; without independent verification leave the PR pending. Docs still receive normal independent review and actual asset checks where applicable.
- **Review entity and merge.** Require a real PR on the project's forge, with the `/opening-a-pr` body. If no forge is available, the operator must explicitly accept a persisted review record binding base/head, diff, body, receipts, reviewer and decision before it can substitute. A chat summary is not that record. Record the entity's URL/path before declaring merge-ready. Actual creation or posting needs authority. Hold merge until independent PASS/PASS+NOTES for Behavior, required CI/review, interaction approval where applicable, and explicit merge authorization. Any unmet acceptance criterion blocks PASS+NOTES too. Land dependent PRs bottom-up only after their prerequisites are verified and merged; retarget to the intended destination and recheck integration against the current base before landing. An independently verified child cannot bypass an unverified parent.
- **Invalidation.** Bind observations and verdicts to exact base/head, dirty state, data and environment. After changes, rerun affected checks and independent verification before a renewed verdict; explain unaffected coverage. A rebase changes the base and requires checking integration again. Reproduce and disclose old trunk defects rather than calling them new regressions; an old defect still blocks if it violates this change's acceptance.

Keep the plan a how-to. Appendices hold evidence, alternatives, risks and reading/decisions. Fill real paths/commands; future runs stay unchecked and no measured value is invented. Source pointers alone do not prove experiments ran.

Finish when a reviewer can trace every criterion to a runnable check, a failure predicate, and original evidence, and every PR has a concrete delivery/review contract. Use [examples](examples.md) for format; its fictional commands are not reusable proof.

## 6. Check and hand back

Run the checker using this skill's absolute directory:

```bash
node <this-skill-directory>/scripts/check-plan.mjs <plan.md>
```

It checks declared structure, not semantic truth, artifact authenticity, safe commands, or feasibility. Review the plan against the actual code: run paths, all callers/loaders, fault location, matching metrics, intermediate compatibility, shared resources, and review handoff. See [checker limits](checker.md). Keep blocked work Draft; report readiness errors rather than weakening the gate.

Return the plan link, PR dependency/parallel groups, review-gated set, proven/unproven feasibility questions, execution/merge boundaries, and exact check result. Stop. Opening PRs, production implementation, publishing and merging are separate authorized actions.
