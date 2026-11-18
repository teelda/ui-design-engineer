# Evidence and output contract

## Severity

- S0 Blocker: core task cannot complete, or evidenced security/money-loss risk requiring immediate hold.
- S1 Critical: major task failure, accessibility blocker or irreversible-action risk.
- S2 High: significant confusion or likely errors.
- S3 Medium: degraded usability or meaningful polish issue.
- S4 Low: small refinement.

Severity describes impact, not confidence. An inferred S0 risk stays inferred until tested. Do not mechanically translate all model “high priority” findings into critical defects.

## Finding

Use five compact parts: **Where → What I saw → Why it matters → Fix → Verify**. Include the element, tested state and viewport in Where, and the actual evidence or capture in What I saw. Label type (bug, UI, UX, accessibility, suggestion or disagreement), likely owner role, severity and confidence when relevant. Separate the observed behavior from a causal hypothesis. State the missing test once when confidence is limited.

Explain the concrete visual relationship or interaction that fails. Give a change within the product's system and an observable acceptance check. Keep additional evidence in the linked report or ticket; do not turn every finding into fourteen labelled fields. Deduplicate root causes, preserve distinct issues and allow a review with no significant findings.

## Report

Use [the shared full audit deliverable](audit-deliverable.md) for the report structure, evidence record and completion check. Apply the severity and finding rules above within that structure.

Never invent user studies, success metrics, score distributions, past failures or fixes. Auditing your own product is useful, but it is not independent validation. Repeatability requires fixed inputs and multiple recorded runs; before/after quality requires checking the actual changes and controlling for run variance.
