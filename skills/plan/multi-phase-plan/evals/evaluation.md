# Planning skill evaluation

## Scope

The first standalone Pi planning skill was evaluated on 2026-11-03 through the explicitly invoked `/skill-creator` workflow. Source: `cursor/plugins` revision `ae5650febf4320793844c12c4adaa937f417f8da`; MIT attribution is retained in LICENSE and frontmatter. Source snapshots and comparison documents are not part of the skill.

Three fixture tasks were run with and without the skill, one execution per configuration per iteration, across three iterations (18 child runs). Both configurations used `magpie/auto/deepseek-v4.1-flash` through Pi subagents. The parent graded inline against the same 14 task-level assertions, inspecting original outputs and transcripts. The source fixture is retained under `files/credit-demo/`; it is an isolated in-memory HTTP/Web demo, not a production credit system.

The model scores below describe the earlier iteration-3 snapshot only. The subsequent four-goal revision changes the operational workflow, template, checker, and companion skills; those model scores do not evaluate the current version. The current revision has local checker regression tests and scenario specifications, not a new with/without-skill model benchmark.

## Results

| Final scenario | With skill | Without skill | Independent evidence |
| --- | --- | --- | --- |
| Obvious one-file copy change | 3/3 | 2/3 | Output length/content; absence of a mini-plan; clean source/HEAD |
| API + Web retry plan | 5/7 | 2/7 | Original plan, source caller/route audit, metric and fault-injection review |
| Unresolved delivery choice | 4/4 | 2/4 | Draft/Spike handoff, transcript tool actions, clean source/HEAD |
| Pooled assertions | 12/14 | 6/14 | Per-run grading.json |

The bundled aggregation script reports an unweighted mean across cases: 90.5% with skill and 48.4% without. Those figures differ from the pooled assertion rates because the three cases have different assertion counts. They are neither reliability estimates nor significance tests.

The final small-change response exits in two sentences. The design-blocked response returns a Draft and a concrete unauthorized `/spike` handoff without running an experiment. The full-plan case preserves request-ID replay semantics, migrates callers within the API PR, includes the module's serving route, and defines operator media approval.

## Failures retained

The final with-skill full plan still fails two assertions:

1. It references an external driver and response-drop proxy without a complete scoped creation and launch/port recipe. The intended verification is not fully reproducible as written.
2. It permits HTTP-only timings as a fallback for the 500 ms page-visible latency budget when browser measurement is unavailable. HTTP request completion does not measure rendering/display, so that budget remains unverified. The sample plan must be corrected before execution.

The iteration-3 structure checker accepted that sample plan. This is direct evidence of its limits: it verified declarations and formatting, not semantic adequacy, actual feasibility, or authenticity. The revised schema adds contracts but likewise cannot prove their truth. The skill requires a code/goal review in addition to the checker; it must not be described as a guarantee of a correct plan.

Earlier iterations exposed mini-plan drift after the small-task exit, head-only instrumentation used for a trunk baseline, pre-execution aborts mistaken for post-commit response loss, broken intermediate callers, and an imported module without a server route. General workflow corrections addressed these; failed artifacts remain in the review workspace rather than being overwritten with successes.

## Evaluation limitations

- One run per task/configuration cannot establish stable performance or causality. The baseline varies across iterations.
- Both configurations received a concise/nonduplicated-report instruction from iteration 2 onward. Cross-iteration resource changes cannot be attributed solely to skill edits.
- Boundary-preservation assertions often pass in both configurations and do not distinguish the skill. The small-task skip assertion tests this chosen contract, not the general value of short plans.
- All 18 project source trees/HEADs are checked without relying on child self-reports. Clean source does not prove no runtime state was changed: the final baseline design case started a server and issued fixture credits despite the no-experiment instruction, and was graded down for it.
- The model runs do not cover authorized Spike execution or a full Docs-only planning task. Docs applicability and parsing branches are covered only by checker fixtures.
- Human review is pending. No feedback or approval is assumed, and no description optimization was run because this skill deliberately preserves user invocation.

## Historical checks and review artifacts

The first-version checks were `node --test scripts/*.test.mjs` (then 43 tests, including 23 planning-checker tests), asset/link checks, Pi's native skill loader, source/license comparisons, and the fixture's two existing tests. These are historical results, not proof of the revised workflow.

## Four-goal revision

The current version requires code-flow grounding, observed feasibility for critical assumptions, an acceptance map with change review, sensitivity checks for critical invariants, explicit parallel groups and per-PR base/writes/resources/interface contracts. It routes actual PR briefings to `/opening-a-pr` and non-author Behavior verdicts to `/verify-pr`. A missing independent verifier leaves delivery pending. No fixed swarm, cloud VM, scheduler or merge automation is introduced.

New executable regression cases reject missing feasibility/acceptance/review contracts, self-verification, missing sensitivity plans, unknown or dependent parallel members, and identical write ownership in a parallel group. The PR-body checker rejects log inventories, missing/incorrect sections, missing per-operation links and oversized briefings. These tests prove only those parser behaviors. Glob/alias overlap, shared resource truth, criterion adequacy, driver feasibility and evidence authenticity remain human/independent-verifier responsibilities.

A same-input local sensitivity run on 2026-11-03 removed the new gate/ownership fields from the published format example: the saved previous checker returned `1 PR sections, 0 problems` (exit 0), and the revised checker returned `1 PR sections, 24 problems` (exit 1). The complete revised format example returned zero problems. The PR checker accepted its illustrated body and rejected a paths/command/test-total inventory (exit 1). These observations demonstrate structural rejection only. Local receipts are under `/tmp/astack-plan-revision-20261103/checks/`; that temporary directory may be cleared.

The revised eval specifications add shared DB/port conflicts, old caller incompatibility, false latency/fault proxies, weakened assertions, self-awarded PASS, missing review entities and stale verdicts. They are prepared scenarios, not completed model runs. A future evaluation must inspect actual outputs and original evidence rather than checking whether the report merely contains the right words.

The evaluation workspace is `/tmp/astack-multi-phase-plan-20261103/multi-phase-plan-workspace/`. `review.html` was generated with `/skill-creator`'s `eval-viewer/generate_review.py`; it shows final outputs, previous outputs and quantitative results. `review-iteration-1.html` and `review-iteration-2.html` retain earlier reviews. Each iteration has task metadata, output artifacts, raw transcripts, independent source checks, grading and actual Pi timing/token records.

The skill snapshots live beside that workspace (first version at `/tmp/astack-multi-phase-plan-20261103/multi-phase-plan/`, later versions under `snapshots/`). The temporary workspace can be cleared by the system; durable prompts, fixture, and this bounded interpretation remain in the skill directory.
