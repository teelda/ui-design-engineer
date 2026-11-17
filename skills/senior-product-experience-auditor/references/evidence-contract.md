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

1. Verdict for the requested decision, with evidence limits.
2. Primary journey steps and tested state of each.
3. Highest-impact unique findings in order. A priority table can orient the reader, but it is not the full review: expand the top findings using the five parts above. Make lower-impact details expandable or linked when possible.
4. For a journey or launch review: the review-layer coverage matrix, including untested and inapplicable layers. Skip it for a single-screen review.
5. Regression tests and exit criteria.

For a UI review, add a short **experience walkthrough** before the findings: what a visitor sees first at each tested width, the primary action and where it leads, and the result or interruption observed. Add **what works and should survive** so a proposed redesign does not erase effective brand, content or interaction choices. State exact widths, device/browser, date and evidence mode when available. If only HTML text or a screenshot was available, do not claim mobile fold position, visual contrast, animation behavior, keyboard behavior, or screen-reader announcements as tested.

Never invent user studies, success metrics, score distributions, past failures or fixes. Auditing your own product is useful, but it is not independent validation. Repeatability requires fixed inputs and multiple recorded runs; before/after quality requires checking the actual changes and controlling for run variance.
