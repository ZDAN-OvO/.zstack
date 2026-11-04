# Format examples

These examples illustrate the format in a fictional repository. Their commands and artifacts are not evidence of a real implementation or measured performance. Replace them with facts from the target repository.

## Behavior with two surfaces

```markdown
# Credit retry plan

Make admin retries safe across the API and Web page. Preserve valid single-request behavior. PR-01 adds idempotent issuance; PR-02 can later add unrelated reporting, but is outside this plan. Acceptance: repeated submission with one request ID changes the balance once.

## How to read this

Status. Ready.
Blockers. None.
Execution. Sequential PR handoff after explicit go; record each branch base before building.
Roles. Implementer builds; a non-author verifier runs the real paths and checks original receipts; operator reviews interaction evidence and decides merge.
Permissions. No delegation, publishing, or merge grant; request the required authority before those actions.

One box is one unit of work; check it only with its evidence. Tests alone do not verify behavior. Complete applicable checks and justify every non-applicability decision.

## Program checklist

### Start and sequence

PR-01 branches from trunk and owns src/credits.mjs, src/server.mjs, web/admin.html and related tests. No parallel writers. On hold, stop writes and record the current state in artifacts/credit-retry/handoff.md.

Parallel. None. This plan has one PR; run the API and Web integration checks together before handoff.
Feasibility. Reuse the matching process-local request/response and browser submission observations at the base version, with commands and limits recorded in Appendix A.
Acceptance. PR-01 owns same-ID replay, conflicting-payload rejection, independent new issuance and refresh consistency; API state and Web sequence artifacts below record each failure predicate.
Changes. Operator review is required before altering acceptance, budgets, coverage or non-applicability reasons; preserve the old criteria in the decision record.

### Evidence rules

Versions. Record base/head SHAs, dirty state, Node version and fixture seed with every run in artifacts/credit-retry/versions.json.
Invalidation. Rerun affected checks and review after code, base, fixture or environment changes; issue a fresh head-bound verdict.
Input boundary. Drive Web through browser automation and API through HTTP; direct store reads are diagnostics only. This example uses an isolated in-memory fixture, not production data.

### Boot recipe

Install with npm ci. Start npm run dev against a fresh local fixture and wait for GET /health to return 200. Use one isolated process per run. Save logs and recordings under artifacts/credit-retry/. Stop the process after evidence capture.

### Verdict and handoff

Review entity. Open a real project-forge PR with /opening-a-pr after publication authority; record its URL, base/head and evidence links in artifacts/credit-retry/handoff.md before merge-ready.
Verdict. A non-author uses /verify-pr to run real paths and inspect raw tests, request records, screenshot sequence, video and changed checks; self-checks leave independent verification pending.

Reproduce trunk failures before attribution; a failure of acceptance still blocks. Resolve project CI and accepted review blockers. Wait for operator interaction approval and explicit merge authorization. Record PR state and decisions in artifacts/credit-retry/handoff.md.

## PR-01 Make credit issuance retry-safe

**Depends on.** None.

**Files.**

Base. Trunk.
Writes. `src/credits.mjs`, `src/server.mjs`, `web/admin.html`, `tests/credits.test.mjs`.
Resources. A separate worktree/process and empty in-memory store per version; ports 4311 and 4312; no shared database or account.
Contract. PR-01 defines requestId, migrates every caller including Web and probes, and serves every new browser module in the same PR.

- [ ] Edit src/credits.mjs, src/server.mjs, web/admin.html and tests/credits.test.mjs within the issuance boundary. Evidence. `artifacts/credit-retry/diff.patch`.

**Build.**

- [ ] Deduplicate a request ID, preserve the first response, and reuse the ID on Web retry. Evidence. `artifacts/credit-retry/diff.patch`.

**You see.**

Kind. Behavior.
Surfaces. API, Web.
Interaction. Yes.

- [ ] Repeated submission updates the balance once; refresh shows the same result. Evidence. `artifacts/credit-retry/result.png`.

**Verify, unit.** Required.

Sensitivity. In an isolated faulted copy disable replay lookup, then run the same duplicate-ID check: require a balance/record-count assertion failure; restore head and rerun. Independently review any changes to this check.

- [ ] Run `npm test` for new issuance, duplicate retry, conflict and independent IDs. Pass when all cases match the intended balance and response. Evidence. `artifacts/credit-retry/tests.log`.

**Verify, live.** Required.

- [ ] Regression against trunk. Surface. API. Send the same seeded issuance on trunk and head, then repeat its request ID. Record trunk's duplicate behavior; gate the preserved single-request result and corrected retry on head. Pass when the documented difference is reproduced and head balance changes once. Evidence. `artifacts/credit-retry/api.json`.
- [ ] Surface. Web. Submit, retry, and refresh using the browser; save intermediate states. Pass when the visible balance changes once and the request ID is reused. Evidence. `artifacts/credit-retry/web-sequence/`.

**Verify, perf.** Required.

- [ ] Metric. Measure issuance API p95 in ms and Web completion in ms using the same fixture. Evidence. `artifacts/credit-retry/metrics.json`.
- [ ] Probe. Freeze the external driver and its hash in artifacts/credit-retry/driver.mjs before comparing; have it send the same HTTP requests and use an external browser timer on both versions. Run `node artifacts/credit-retry/driver.mjs` with each server URL in trunk/head/trunk/head order after readiness; measure each stage separately. Evidence. `artifacts/credit-retry/probe.log`.
- [ ] Baseline. Run the trunk probe first and save its actual values, without inventing a pre-run result. Evidence. `artifacts/credit-retry/baseline.json`.
- [ ] Rule. Fail when API p95 exceeds 50 ms or visible completion exceeds 500 ms, using the agreed absolute budgets. Limit. 50 ms. Evidence. `artifacts/credit-retry/perf-verdict.json`.

**Review gate.** Required.

- [ ] Present screenshots and video of submit, retry and refresh to the operator; wait for approval before merge. Evidence. `artifacts/credit-retry/operator-review/`.

**Merge.**

Verifier. Independent.

- [ ] Record the actual PR URL and /opening-a-pr body, non-author /verify-pr verdict at exact base/head and original artifacts, clear project checks and interaction review, and stop at merge-ready until explicitly authorized. Evidence. `artifacts/credit-retry/handoff.md`.

## Close the program

After execution, account for applicable boxes with their actual artifacts. Report verified base/head, PR state, whole-change acceptance, outstanding decisions and risks. A blocked acceptance remains blocked rather than complete.

## Appendix A. Spike evidence

In this fictional example, the matching base observation record establishes process-local request handling and the real browser submission path, including the readiness and refresh operations. No new architecture or external dependency is assumed. A real plan must link the actual versioned observations here; a settled request alone does not pass feasibility.

## Appendix B. Alternatives rejected

Client-only button disabling loses protection across retries and refresh; use API idempotency instead.

## Appendix C. Risks

PR-01 owns request-ID conflict handling; verify conflicting payloads do not issue more credit. An unavailable browser driver blocks Web proof until a named alternative exists.

## Appendix D. Links and decisions

Read src/credits.mjs, src/server.mjs and web/admin.html before editing. Use package.json for check and boot commands. Record reasoning and receipt links in artifacts/credit-retry/handoff.md.
```

## Docs-only PR

Retain all nine PR blocks. Use `Kind. Docs.`, `Surfaces. None.`, and `Interaction. No.` in You see. Keep concrete Files, Build, You see, and Merge boxes with evidence destinations. For example:

- `**Verify, unit.** Required.` followed by the real documentation/link checker, its pass predicate and evidence destination; or a specific reason if there is no automated check.
- `**Verify, live.** Not applicable. Only reference wording changes; no runtime behavior or interaction changes.`
- `**Verify, perf.** Not applicable. No executable source, build inputs, or dependencies change.`
- `**Review gate.** Not applicable. No user interaction changes; prose review remains part of the normal review.`

Non-applicable blocks have no checkboxes. Use `Verifier. Review only.` or `Verifier. Independent.` under Merge; preserve a real review entity and ordinary independent review. Keep Base, Writes, Resources and Contract even for Docs, with concrete reasons where relevant. The global feasibility field can cite observed existing documentation checks and link resolution. The boot section explains why no app startup is needed. Do not classify an executable behavior change as Docs just to skip gates.

## A design-blocked draft

When delivery choice is unproven, return a Draft with the question, alternatives, required observations and Spike task. For example, compare streaming and polling with disconnect/reconnect under the project's actual proxy limits. State what is already known, what depends on the result, and whether Spike is authorized. Do not publish a Ready plan or claim experiment success before observing it.
