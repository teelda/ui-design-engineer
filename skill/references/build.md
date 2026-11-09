# Build and refine guidance

Use the existing design system when one exists. Inspect tokens, components, typography, spacing, breakpoints, states, and a representative screen before changing styles. Keep the product's recognizable rhythm unless the user asks for a new direction.

For new work, choose the smallest coherent system that serves the content. Document the role of each token and reusable component in code. Do not force a single accent color, a fixed headline length, one typeface, or a card-free layout. Compare alternatives against the user's task and brand.

| Candidate default | Better question |
|---|---|
| Gradient headline or button | Does this convey the brand or hierarchy, and does text remain readable across the full gradient? |
| Tiny uppercase kicker on every section | Does it add category or context that the heading lacks? |
| Generic “Get started” action | Can the label name the next action without becoming long or repetitive? |
| Identical icon cards | Is comparison helped by consistency, or would another grouping make the information clearer? |
| Cards nested in cards | Do all boundaries clarify ownership or interaction? |
| Glow, blur, motion, or floating badges | Do they establish identity, feedback, or state without obscuring content? |
| Repeated spacing/radius values | Are they mapped to a deliberate scale and component roles? |

Implement and inspect the states the interface can actually reach: initial, loading, empty, partial, error, success, long content, validation, disabled, and permission denial when relevant. Test narrow and wide layouts, zoom and supported themes. A spinner that rotates off center is an implementation defect; correct its geometry rather than treating it as a style choice.

For accessibility, verify the real task path: keyboard activation and order; visible, unobscured focus; names for icon controls; labels and errors tied to fields; modal entry and focus return; status announcements; meaningful alternatives; reduced motion; and reflow. Automated checks help locate candidates but cannot prove the path works.

Before shipping, run the repository's build and focused tests, inspect the rendered interface, and state the viewport, theme, and interactions actually checked. Keep untested conditions explicit.
