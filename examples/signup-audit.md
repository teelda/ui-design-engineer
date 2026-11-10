# Example: source-assisted signup review

This sample uses the repository's [coral signup fixture](../evals/fixtures/coral-signup/index.html). It illustrates the auditor's **report format**, not a measured skill benefit or a deployed-product audit. Evidence is the HTML/CSS/JavaScript source; no browser, keyboard, mobile-device, or backend behavior was tested.

**Task:** Can a visitor join early access from the page, including at a narrow width?

## Findings

1. **S2 · Source risk · narrow layout.** The `main` grid sets `min-width: 760px`. At a 390px viewport, this rule can force horizontal overflow and move part of the form or artwork off-screen. **Fix:** let the grid collapse to one column at supported narrow widths without changing the coral brand, copy, or links. **Verify:** in a rendered 390px browser, `document.documentElement.scrollWidth` does not exceed the viewport and the submit action remains visible.
2. **S3 · Observed source defect · form label.** The email field has a placeholder but no persistent visible `<label>`. Once a visitor types, the field's purpose is no longer shown beside it. **Fix:** add a visible label associated with `id="email"`. **Verify:** the label remains visible after entry, the field has an accessible name, and the form works with keyboard submission.

**Strengths to preserve:** the coral tokens, clear “Join early access” action, existing copy, and contact link.

**Coverage:** one source file inspected; the `#signup` anchor and simulated success message are present in source. Rendered mobile layout, focus order, validation feedback, data storage, and actual signup delivery are **not tested**. A passing source check would not establish those outcomes.
