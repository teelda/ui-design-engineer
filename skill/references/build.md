# Build and refine guidance

Use the existing design system when one exists. Inspect tokens, components, typography, spacing, breakpoints, states, and a representative screen before changing styles. Keep the product's recognizable rhythm unless the user asks for a new direction.

For new work without a brand, start with one action accent, neutrals, a type scale (for example 14/16/20/28/40px), a spacing scale (4/8/16/24/48px), and radii for controls and surfaces (for example 8/16px). Establish hierarchy in grayscale. Add colors, typefaces, and visual effects only when their role is clear. These are starting values, not a limit on an expressive or data-dense product.

| Candidate default | Better question |
|---|---|
| Gradient headline or button | Does this convey the brand or hierarchy, and does text remain readable across the full gradient? |
| Tiny uppercase kicker on every section | Does it add category or context that the heading lacks? |
| Generic “Get started” action | Can the label name the next action without becoming long or repetitive? |
| Identical icon cards | Is comparison helped by consistency, or would another grouping make the information clearer? |
| Cards nested in cards | Do all boundaries clarify ownership or interaction? |
| Glow, blur, motion, or floating badges | Do they establish identity, feedback, or state without obscuring content? |
| Repeated spacing/radius values | Are they mapped to a deliberate scale and component roles? |

## Worked tradeoffs

| Situation | Competing choices | Evidence and decision | Rendered check |
|---|---|---|---|
| Existing coral marketing page; the primary action is buried below a large headline and video | Remove the video and gradient, or keep the brand while moving the action | The brief protects both assets; the task is to start an audit. Keep them, shorten the hero's text measure, increase action contrast and place the action before the video at narrow widths. | At 390px, the action is visible without horizontal scroll; the video does not obscure it; text is readable over every gradient stop. |
| New dense operations dashboard; users compare six metrics across many rows | Cards per record, or a table with fixed columns | Cross-row comparison is the primary task, so use a table at wide widths. On narrow widths, keep key columns visible and move secondary values into a labelled detail view rather than making every row an unrelated card. | Long names, empty values, loading rows, and keyboard focus remain aligned and readable at both widths. |
| Signup form with an illustrative image | Keep the image, or use the space for form guidance | If the image does not explain the task or brand, give the form more width and place help/error text next to fields. Keep imagery when it teaches the offer or provides necessary identity. | The label, help, error, and submit action stay visible at narrow width and 200% zoom. |

Implement and inspect the states the interface can actually reach: initial, loading, empty, partial, error, success, long content, validation, disabled, and permission denial when relevant. Test narrow and wide layouts, zoom and supported themes. A spinner that rotates off center is an implementation defect; correct its geometry rather than treating it as a style choice.

For accessibility, verify the real task path: keyboard activation and order; visible, unobscured focus; names for icon controls; labels and errors tied to fields; modal entry and focus return; status announcements; meaningful alternatives; reduced motion; and reflow. Automated checks help locate candidates but cannot prove the path works.

Before shipping, run the repository's build and focused tests, inspect the rendered interface, and state the viewport, theme, and interactions actually checked. Keep untested conditions explicit.
