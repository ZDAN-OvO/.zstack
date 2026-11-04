---
name: verify-pr
description: "Use to independently verify a behavior PR before merge-ready, audit original evidence or changed checks, or renew a verdict after base/head or environment changes."
metadata:
  source: "https://github.com/cursor/plugins/blob/ae5650febf4320793844c12c4adaa937f417f8da/pstack/skills/poteto-mode/playbooks/shipping.md"
  revision: ae5650febf4320793844c12c4adaa937f417f8da
  adaptation: "Locally authored verification workflow. Keeps non-author user-path verification and version-bound verdicts; omits cloud-agent mandates, patch-id reuse, polling and merge automation. Adds explicit blocked outcomes and acceptance/check sensitivity review."
---

# Verify a PR

Own the verdict, not the implementation. Verify the actual behavior against the approved acceptance. Green CI and the PR author's report are inputs, not a verdict. This skill does not merge or authorize publication.

## 1. Establish the review boundary

Read project instructions, the originating requirement/acceptance map, the actual review entity and diff, and the project's verification skill. Record review URL/path, base and head SHAs, dirty state, environment/data/driver versions, implementer, verifier, and evidence destination. On a forge use the real PR. A no-forge persisted review record needs explicit operator acceptance and must contain base/head, diff, briefing, receipts, reviewer and decision.

The Behavior verifier must not have implemented the product or its changed checks. One authorized human or Agent verifier per PR is enough; no fixed swarm. A non-author Agent may act as verifier when the execution grant names that role. Delegation still needs authority. An author running this skill can prepare the audit but must return **BLOCKED — independent verifier pending**, not self-award PASS. A different model reviewing the author's summary without running the path is not independent verification.

When the entity, acceptance or authority for safe driving is missing, return BLOCKED with the concrete next action. Do not start irreversible external operations to obtain proof. Use authorized isolated/test environments and disclose their limits.

## 2. Audit acceptance and the check itself

Map every criterion to the relevant diff, observation surface, pass/fail predicate and evidence. Compare approved criteria with the final checks. Inspect changes to tests, baselines, snapshots, skips, feature flags, mocks, budgets, CI and non-applicability decisions. A weakened assertion or deleted case does not preserve acceptance merely because the suite passes. Operator review is required for criterion changes; retain the previous criterion and decision.

For each critical invariant, run a sensitivity check: the relevant regression on a known-bad version, or a safe controlled defect in an isolated copy, must fail for the intended reason. Then run it on head. Save exact commands, versions and outputs for both. A build/import error in the bad version does not demonstrate detection of the behavioral defect. Do not introduce a defect into a shared instance or alter the reviewed product/checks. If a safe fault is impractical, record why and obtain operator review of a concrete independent observation; unobserved or unaccepted alternatives remain BLOCKED.

A criterion present in prose but absent from executable/observable proof is a coverage gap. Keep it open instead of changing it to match the implementation.

## 3. Run the real paths

Use the project's actual harness and feature map. Confirm the instance is at the claimed version and ready for the journey, then run every affected surface against base and head on comparable isolated data. Capture initial conditions, operations, intermediate state, final state and required refresh/retry/reconnect. Read side effects as well as the visible result. Direct internal setters, test-only shortcuts and synthetic final screens do not prove the user path.

Keep fault injection at the boundary the criterion describes. A request cancelled before execution cannot demonstrate a committed operation whose response was lost. Record stubs, external-system substitutions and safe test-mode exclusions. When base lacks a feature, record that observation and test added behavior and the final state separately. Reproduce old base failures; distinguish them from regressions. A pre-existing defect still blocks if it violates the accepted goal.

Run the applicable automated checks and performance contract. Measure the actual named quantity with a common driver on both versions, base first and interleaved comparable runs. A server/HTTP time does not measure a browser-visible deadline. If there is no matching driver, mark that criterion BLOCKED. Preserve numeric budgets and units; no ratios between unlike scenarios. Docs-only changes receive actual applicable asset/link checks and independent review, with explicit runtime non-applicability.

Inspect original logs, screenshots/video, traces and side-effect assertions; confirm each exists, resolves for its reviewer, and shows the claim at these versions. Do not treat an artifact filename, a hash, or a filled report as authenticity proof. Clean up only instances/state this run owns; evidence survives cleanup. Findings name a reproducible operation, actual result, required result and artifact.

## 4. Issue a bounded verdict

Use [the report format](references/report.md). Classify:

- **PASS.** Every applicable criterion was observed satisfied at the recorded versions; required checks passed; Behavior verification was independent.
- **PASS+NOTES.** The same acceptance bar as PASS, with nonblocking facts outside that bar. Missing proof, failed criteria, missing independence or waived budgets cannot be notes.
- **FAIL.** An observed behavior/check fails an accepted criterion. Include the reproduction. If other coverage is incomplete, record that too.
- **BLOCKED.** Proof cannot finish: missing independence, entity, runnable environment/driver, authority, reviewed criterion change, or required observation. Name what unblocks it.

Record interaction approval as approved or pending separately. Passing behavior evidence does not grant that approval, satisfy every external CI/review gate, or authorize merging. Merge-ready requires a valid PASS/PASS+NOTES, all required project gates, the review entity and applicable operator interaction approval. For a stack, state the verified prerequisite run and any pending parent; only the contiguous verified run can land bottom-up. A child waiting on an unverified/unmerged prerequisite is not ready to land on trunk. After retargeting/rebasing it onto the intended merge destination, recheck integration and renew affected proof. Merge execution still requires explicit authorization.

Re-read current base/head and environment before handing back. Any drift invalidates affected observations and requires their rerun plus a renewed independent verdict. A rebase needs integration rechecking; do not reuse a verdict just because patch text looks similar. If an author fixes a finding, the verifier reruns affected proof at the new head. If the verifier implements a fix or rewrites checks, hand the new verdict to a different non-author verifier.

Save the report and return its path, verdict, verified versions, blocking gaps and remaining operator gates. Post to a PR only with publication authority. Stop before merge; no background polling or automatic merge.
