---
name: opening-a-pr
description: "Use when drafting, creating, or updating a PR description or a persisted review record. Write a short fixed briefing with linked behavior evidence and merge risk."
metadata:
  source: "https://github.com/cursor/plugins/blob/ae5650febf4320793844c12c4adaa937f417f8da/pstack/skills/poteto-mode/playbooks/opening-a-pr.md"
  revision: ae5650febf4320793844c12c4adaa937f417f8da
  adaptation: "Locally authored PR briefing contract; five required sections and a structural checker. Git automation and mandatory writing-agent calls are omitted."
---

# Opening a PR

Write a one-minute briefing for someone who has the diff but not this conversation. The actual PR body is this briefing, not the implementation plan or a test transcript. Use the operator's language for prose; keep these headings for review and checking.

## 1. Read the final change

Inspect the actual diff, originating requirements, project PR instructions/template, checks and original verification artifacts. Establish the problem, resulting behavior, scope, impact and actual proof. Reconcile the body with the final implementation after scope changes. A local preview may say evidence is pending, but cannot be described as verified or merge-ready.

If the project requires another template, preserve its required fields and carry this briefing into the corresponding sections; disclose the mapping. The bundled checker validates only the default format, not another project's template. A conflicting checker result is not permission to delete project-required fields.

## 2. Write the briefing

Use `type(scope): imperative subject` for the title unless the project specifies otherwise. No trailing period. Use these `##` sections in this order:

- **Why.** Required. One to three short sentences on the concrete problem and approach.
- **What changed.** Required. One to three short bullets about resulting behavior or mechanisms. Name a path/symbol only when needed to explain the change. Give both sides of a rename.
- **Scope.** Required. One to three short bullets covering included behavior and deliberate exclusions or known gaps. Use domain terms, not a file inventory.
- **Tradeoffs.** Optional. Include only an alternative a reviewer would reasonably ask about and the reason it lost.
- **Blast Radius.** Required. One or two short sentences on affected users/callers/state, principal risk, and rollback or irreversible consequences where relevant. If trunk is failing, state the practical cost.
- **Verification.** Required. One to three bullets, each a real operation path, observed outcome, and link to its evidence. For perf use one primary `before → after` number with units and link the rest. Say pending/blocked when unrun; never fabricate a result.

Keep the briefing to about 40 nonblank lines. Use [the example](references/example.md) for shape, not evidence. Attach screenshots/video when they prove a claim. Label initial conditions, action sequence, result, running version and real/stub/fault boundaries. A screenshot of a stub is not proof of the real business path.

Full SHAs, fixture/env recipes, raw logs, detailed commands, measurement tables and lane reports belong in linked persistent artifacts. Verification links must resolve for the intended reviewer; a local `/tmp` path is not accessible from a hosted PR. Keep the body focused on conclusions with enough context to follow those links. Test totals alone do not prove the changed feature. `/verify-pr` owns the independent verdict.

## 3. Check and deliver

Save the exact body to a UTF-8 file and run, using this skill directory's absolute path:

```bash
node <this-skill-directory>/scripts/check-pr.mjs <body.md>
```

The checker catches default heading/order, empty sections, excessive size, missing bullets/links and placeholders. It does not prove clarity, artifact accessibility, actual execution, or truth. Read it as the downstream reviewer: can they identify problem, effect, scope, risk and observed result without reading logs? Open the evidence links yourself.

Return the body or draft path and check result. Creating/updating a PR or posting a review record requires existing publication authority; writing a draft does not confer it. When authorized, submit exactly the reviewed body (prefer a structured tool argument or `--body-file`), verify its base/head and read back the published body and status. Every delivery unit needs its own review entity before merge-ready. On a forge use a real PR; a no-forge replacement requires the operator's explicit acceptance of a persisted record containing base/head, diff, briefing, receipts, reviewer and decision. Merging remains a separate explicit grant.
