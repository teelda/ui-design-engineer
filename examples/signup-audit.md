# Example: source-assisted signup review

This sample uses the repository's [coral signup fixture](../evals/fixtures/coral-signup/index.html). It illustrates the auditor's **report format**, not a measured skill benefit or a deployed-product audit. Evidence is the HTML/CSS/JavaScript source; no browser, keyboard, mobile-device, or backend behavior was tested.

**Task:** Can a visitor join early access from the page, including at a narrow width?

## Findings

1. **S2 · Source risk · narrow layout.** In the page's main content, the grid sets `min-width: 760px`. That constraint is wider than a 390px viewport. If it forces horizontal scrolling in the browser, a visitor may need to pan sideways to reach or understand the signup content. **Change:** let the grid become one column at supported narrow widths; keep the coral palette, wording, links and signup action. **Verify:** render at 390px and confirm `document.documentElement.scrollWidth` does not exceed the viewport, the content reads in the intended order, and the submit control is reachable without sideways panning. The overflow is a source risk until rendered.
2. **S3 · Observed source defect · form label.** The email field uses a placeholder as its only visible cue. After a visitor enters an address, that cue disappears; the source has no persistent visible `<label>`. **Change:** place a concise Email label above the field and associate it with `id="email"` while retaining the existing copy and form behavior. **Verify:** the label remains visible after typing, the field exposes an accessible name, and keyboard submission still reaches the same success or error state. The screen-reader announcement has not been tested.

**Strengths to preserve:** the coral tokens, clear “Join early access” action, existing copy, and contact link.

**Coverage:** one source file inspected; the `#signup` anchor and simulated success message are present in source. Rendered mobile layout, focus order, validation feedback, data storage, and actual signup delivery are **not tested**. A passing source check would not establish those outcomes.
