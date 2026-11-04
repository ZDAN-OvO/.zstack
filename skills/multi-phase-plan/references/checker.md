# Plan checker

Run `node scripts/check-plan.mjs <plan.md>` from the skill directory. Exit codes: 0 structurally Ready, 1 invalid/Draft, 2 usage/read error. It is read-only, has no dependencies, and never executes the target project's commands.

It checks:

- one H1 and required H2/H3 order, Ready status and no declared blockers
- execution, role, permission, feasibility, acceptance, criterion-change, review-entity and verdict fields
- PR IDs and dependency references, self-dependencies and cycles
- nine PR blocks and unchecked future boxes with evidence destinations
- `Base. Trunk.` or `Base. PR-01.` where that PR is a prerequisite
- `Writes.` with backticked owned paths/globs, plus `Resources.` and `Contract.` descriptions
- `Parallel. None. <reason>` or groups such as `Parallel. PR-02, PR-03; PR-04, PR-05.`
- known, unique members in each parallel group, no direct/transitive dependency between members, and no identical declared write paths between them
- named surfaces and interaction, automated/live coverage for Behavior, trunk comparison and pass predicates
- a `Sensitivity.` contract for Behavior automated checks and `Verifier. Independent.` under Merge; Docs can use `Verifier. Review only.`
- perf applicability, four fields and numeric failure limit, interaction media/approval, nonempty appendices and unfilled placeholders

The checker validates declarations, not whether they are true. In particular, it cannot resolve glob overlap, symlinks/aliases, real branch/DB/port ownership, shared external state, adequacy of acceptance, feasibility evidence, driver existence, fault location, or the metric actually measured. Even disjoint files can conflict at runtime. Review these against the actual repository and run environment.

It does not inspect PRs, independently run behavior, enforce forge protection, authenticate media, or issue a verdict. `/opening-a-pr` checks the actual default PR briefing separately; `/verify-pr` owns independent behavior proof. Required CI/branch protection must be installed in each target project with authorization; having this library does not install it.

A plan with unresolved feasibility or decisions remains Draft; do not weaken readiness requirements to obtain zero problems. A Ready plan is permission-neutral. This checker is for the plan before implementation; a progress copy with completed boxes is not accepted as a new unchecked plan.
