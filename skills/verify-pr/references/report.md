# Verification report format

Fill actual observations. This format is a review record, not an automatic attestation. Store original artifacts beside it or at stable reviewer-accessible links.

```markdown
# PR verification

Verdict: PASS | PASS+NOTES | FAIL | BLOCKED
Review entity: URL or explicitly operator-accepted persisted record
Base/head: exact SHAs; include dirty state and snapshot/hash if applicable
Environment: app/build, runtime, driver, fixture/data versions; test/stub/fault boundaries
Implementer: identity and product/check responsibility
Verifier: identity, non-author basis, driving/delegation authority
Acceptance source: approved requirement/map and any separately reviewed changes

## Criterion results

| Criterion | Required observation and predicate | Operation/version | Actual result | Original evidence |
| --- | --- | --- | --- | --- |

Include automated, live, side-effect, compatibility and perf criteria. Mark failed and unobserved criteria explicitly. State a specific reason for each non-applicable check.

## Check sensitivity

For each critical invariant: known bad version or isolated fault, exact rejecting check, expected failure, observed failure, head passing run, raw artifacts. If the alternative is an independent observation: limitation, operator's review, actual observation and evidence. Preserve changed checks and acceptance decisions for review.

## Findings and limitations

For each failure: command/operation, actual vs required result, artifact and owning criterion. Separate reproduced base defects from introduced regressions. Describe stubs and what remains unproven. Notes cannot contain unmet criteria.

## Delivery gates

- Entity exists and binds the current base/head/diff/body/receipts/reviewer/decision.
- Prerequisites and destination: verified parent run, pending parents, intended merge base, and integration recheck after retargeting/rebase.
- Required CI/reviews: actual status and evidence, or pending.
- Interaction approval: actual operator decision, pending, or concrete non-applicability reason.
- Drift check: versions and environment re-read before verdict; affected checks rerun if changed.
- Evidence retention and cleanup: proof survives; owned instances are stopped.
- Merge-ready: yes only if every gate is met; otherwise blockers.
- Merge authorization: grant reference or pending; a verdict does not grant it.
```
