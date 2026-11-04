# Fictional PR body example

This is an illustration, not an actual run. Replace the links and observations with real evidence before publishing. The artifact contains exact versions, commands, test output, step-by-step media, and original side-effect assertions; the body gives the reviewer their meaning.

```markdown
## Why
A lost response makes an admin retry issue credit twice. Reuse the first result when the request ID repeats.

## What changed
- Identical retries return the original issuance; conflicting payloads return 409.
- The page keeps the same ID across a failed operation and retry.

## Scope
- Covers the API and admin page, including retry and refresh.
- Does not change quota rules or persist records across process restarts.

## Tradeoffs
Client-only button disabling cannot protect retries after refresh, so deduplication lives in the API.

## Blast Radius
Affects every issuance caller. Existing callers migrate in this PR; replay and conflict checks cover the shared boundary.

## Verification
- Applied an issuance, dropped its response, then retried: one balance change and one issuance record. [API run and state assertions](https://example.org/evidence/credit-retry/api)
- Submitted, retried and refreshed in the browser: the result stayed single and visible. [Action sequence, screenshots and video](https://example.org/evidence/credit-retry/web)
- Measured the actual page-visible completion against the agreed budget. [Measurements and independent verdict](https://example.org/evidence/credit-retry/verdict)
```
