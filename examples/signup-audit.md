# Example: source-assisted signup review

This sample uses the repository's [coral signup fixture](../evals/fixtures/coral-signup/index.html). It illustrates the auditor's **report format**, not a measured skill benefit or a deployed-product audit.

**Task:** Can a visitor join early access from the page, including at a narrow width?
**Evidence mode:** source-assisted. One HTML file was read, plus `ui_lint.py` and `ui_lint.py --profile house`. No browser, keyboard, device or backend behaviour was tested.

## Verdict: needs changes

The signup path is present and the action is clearly named. The fixed grid width is the main risk at narrow widths. Confirm it in a rendered browser before shipping.

## Findings

**1 · S2 · UX · source risk · owner: front end**
- **Where:** `main` grid, `index.html` line 15, 390px viewport.
- **What I saw:** The grid sets `min-width: 760px`, which is wider than the viewport.
- **Why it matters:** If the browser applies it as written, a visitor pans sideways to reach the form and the submit button. This is not reproduced yet.
- **Fix:** Collapse the grid to one column at narrow widths. Keep the coral palette, copy, links and signup action.
- **Verify:** At 390px, `document.documentElement.scrollWidth` equals the viewport width, the content reads in order, and the submit button is reachable without panning.

**2 · S3 · Accessibility · observed in source · owner: front end**
- **Where:** email field `#email`, line 37, every width.
- **What I saw:** The placeholder "Email address" is the only visible cue. There is no `<label>`.
- **Why it matters:** The cue disappears as soon as the visitor types, so the field's purpose is no longer shown beside it.
- **Fix:** Put a short "Email" label above the field, tied to `id="email"`. Keep the existing copy and behaviour.
- **Verify:** The label stays visible after typing, the field exposes an accessible name, and keyboard submission reaches the same success or error state. The screen-reader announcement remains untested.

## House bar (opt-in, labelled preference)

This section shows the report when the owner asks for the house bar. These findings rest on that profile, not on general usability evidence, and come from source and `--profile house` only, so they are candidates to verify, not confirmed visual defects. The brief protects the coral gradient, so it is not flagged.

**3 · House bar · UI · observed in source · owner: design**
- **Where:** `.eyebrow`, line 16.
- **What I saw:** `text-transform: uppercase` on "A calmer place to plan".
- **Why it matters:** The house bar uses sentence case for eyebrows and labels.
- **Fix:** Remove the transform and reduce the `.15em` letter-spacing to suit mixed-case text.
- **Verify:** `ui_lint.py --profile house` no longer reports `uppercase` on line 16.

**4 · House bar · UI · source candidate · owner: design**
- **Where:** `.art`, line 19.
- **What I saw:** `box-shadow: 0 30px 70px` under the gradient panel.
- **Why it matters:** If the rendered panel reads as a glow, it is decoration the house bar avoids unless the live product already uses it.
- **Fix:** Remove the shadow, or record it as a brand decision with `/* ui-lint: ok glow -- reason */`.
- **Verify:** The panel still separates from the cream background at both widths.

**5 · House bar · UI · source candidate · owner: design**
- **Where:** `header`, `nav`, `main` and `form` spacing (lines 11, 13, 15, 21); hard-coded colours (lines 19, 22, 23, 25).
- **What I saw:** `--profile house` reports 22px, 25px, 45px and 75px spacing off the 4px grid, and five hard-coded hex uses (four distinct colours) that are not among the page's `--` colour tokens (including `#b7aaa2` on the input border and `#e8dcd3` on the footer rule).
- **Why it matters:** The fixture defines no spacing scale, so the 4px grid is the checker's default, not this page's system. These values may be deliberate.
- **Fix:** None prescribed yet. Confirm the product's spacing scale and palette with its owner first.
- **Verify:** Render at 390px and desktop and check whether these gaps and colours break a visible relationship (alignment with the header, uneven rhythm, a colour that reads off-brand). Only those become findings.

**House bar verdict: insufficient evidence.** The review is source-only. Render the page at 390px and desktop, and confirm the spacing scale, before giving SHIP or ONE MORE PASS. Finding 1 still comes first.

## What works and should stay
The coral tokens, the clear "Join early access" action, the existing copy and the contact link.

## Coverage
One source file inspected. The `#signup` anchor and simulated success message exist in source. Rendered mobile layout, focus order, validation feedback, data storage and signup delivery are **not tested**.
