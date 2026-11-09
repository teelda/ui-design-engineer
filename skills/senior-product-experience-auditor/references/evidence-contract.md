# Evidence and output contract

## Severity

- S0 Blocker: core task cannot complete, or evidenced security/money-loss risk requiring immediate hold.
- S1 Critical: major task failure, accessibility blocker or irreversible-action risk.
- S2 High: significant confusion or likely errors.
- S3 Medium: degraded usability or meaningful polish issue.
- S4 Low: small refinement.

Severity describes impact, not confidence. An inferred S0 risk stays inferred until tested. Do not mechanically translate all model “high priority” findings into critical defects.

## Finding

ID; screen/URL; component; severity; confidence (high / medium / low); category/layer; classification (observed defect / inferred risk / subjective preference); observed issue; user consequence or plausible concern; evidence and its source; expected behavior; recommended fix; measurable acceptance criterion; screenshot/locator or source reference. Use exact source references only when inspected. State what would raise confidence for inferred risks. Deduplicate by root cause without merging unrelated controls just because they share a word such as “label.”

## Report

1. Verdict for the requested decision, with evidence limits.
2. Primary journey steps and tested state of each.
3. Highest-impact unique findings in order; make remaining details expandable or linked when possible.
4. For a journey or launch review: the review-layer coverage matrix, including untested and inapplicable layers. Skip it for a single-screen review.
5. Regression tests and exit criteria.

Never invent user studies, success metrics, score distributions, past failures or fixes. Auditing your own product is useful, but it is not independent validation. Repeatability requires fixed inputs and multiple recorded runs; before/after quality requires checking the actual changes and controlling for run variance.
