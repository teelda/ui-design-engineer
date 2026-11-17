# Design principles audit

Use for a full UI/UX review. Inspect every applicable dimension below; report findings where evidence supports them. Coverage is not a quota of defects. Use observed / concern / not checked / not applicable to show scope. A full review needs rendered evidence and interaction checks; a text-only review has a narrower verdict.

## Establish reality and scope

Identify the intended user, task, product stage, requested deliverable and current live version. Check whether a proposed feature already exists, and whether the reported problem persists when using it. Compare live behavior with source only when both are available. If ownership or another team's work affects a proposed change, confirm it from supplied project evidence. Do not invent organizational context or delay a visual review for irrelevant ownership questions.

Use actual production names, plan terms, networks and states in proposed production screens. Identify intentional prototypes as prototypes. An unexplained DEV label can misrepresent a production design, but a clearly labelled staging screenshot is not automatically a defect.

## Inspect the design, not just its claims

| Principle | What to inspect and how to judge it |
|---|---|
| Hierarchy and emphasis | Identify the first three attention targets, reading order and intended primary action. Compare size, weight, placement, contrast and whitespace. Explain when competing emphasis obscures the task; do not require every CTA above the fold. |
| Composition, balance and proportion | Examine how text, media and controls occupy the viewport, their relative scale and visual weight. Identify awkward empty regions, crowding or weak relationships using actual sections and captures. Symmetry is not mandatory. |
| Alignment and grid | Compare containers, gutters, baselines and repeated edges across header, content and footer. Distinguish deliberate breakout sections from accidental drift. Measure deviations when claiming pixel differences. |
| Proximity and grouping | Check whether related labels, controls, explanations and errors appear related. Inspect spacing within groups versus between groups, shared boundaries and continuity. Flag a specific mistaken association rather than demanding cards everywhere. |
| Typography | Inspect display, heading, body and label roles; actual family, size, weight, line height, line length, wrapping, tracking and truncation. Explain the role that fails. An unusual font or uppercase label is not inherently wrong. |
| Color and contrast | Map colors to brand, actions, information and states. Test relevant rendered pairs when tools permit; account for overlays and gradients. Separate measured contrast failure from weak emphasis or personal taste. |
| Spacing, rhythm and density | Check consistent spacing relationships, breathing room, scanability and repeated section rhythm. Identify where repetition removes useful emphasis or where sparse content is surrounded by excessive UI. Page length alone is not a defect. |
| Components and consistency | Compare controls with the same purpose across states and screens: shape, radius, height, icon treatment, label and behavior. Several radius tokens can form a coherent system; a pill next to a rectangular card is not enough to prove inconsistency. |
| Affordance and signifiers | Check whether interactive elements look actionable, labels describe consequences, selected states are clear, and disabled states explain what is required. Test the actual target and response. |
| Imagery and assets | Verify the real logo and supplied brand assets, crop, aspect ratio, resolution, and relationship to the content. Prefer real product evidence when demonstrating capabilities. Judge generated art by purpose and accuracy; do not ban a medium. |
| Motion and time | Observe transitions, loading and feedback. Assess continuity, pacing, interruption, layout stability, comprehension and reduced-motion behavior. Distinguish observed playback from still-image inference. For a dedicated motion deliverable, inspect sequence and key cuts, not just a poster frame. |
| Responsive behavior | Inspect representative narrow and wide widths, plus breakpoints where layout changes. Check ordering, wrapping, overflow, sticky controls, touch targets and zoom. Record exact tested widths rather than calling a single arbitrary width all mobile devices. |
| Accessibility and inclusion | Inspect keyboard access, focus, names, semantics, errors, announcements, contrast and reflow where applicable. Use the actual criterion and evidence for compliance claims. Include supported language expansion and RTL where relevant. |
| Cognitive load and information architecture | Trace how users locate and compare information. Check navigation, terminology, progressive disclosure, recognition, redundant content and decision burden. Explain which task a proposed removal would help and what information must remain. |
| Feedback, control and recovery | Follow the primary action through pending, result and relevant error/empty/locked states. Inspect cancel, back, retry, persistence and prevention of duplicate or destructive actions. A backend status must translate into a useful user state and next action. |
| Product and content integrity | Compare audience, promise, availability, prices, entitlements, plan choices and onboarding requirements across the journey. Check claims against available evidence; label unverified claims without declaring them false. |
| Performance and resilience | Observe loading, image/font shifts and input response; measure when available. Check relevant slow or failed requests safely. Keep a visual impression separate from measured performance. |
| Concept and distinctiveness | Identify the design idea and how composition, imagery, type and interaction express it. Specific market copy does not prove distinctive visual execution. Explain when interchangeable cards, ornamental glows or repeated patterns overwhelm content, rather than calling them AI-made on appearance alone. |

## Synthesize a judgment

Give a supported assessment of visual craft and a supported assessment of interaction/product fit. Neither substitutes for the other. Praise should name the decision and its useful effect. Criticism should identify the relationship that fails and the evidence behind it. Before recommending a change, consider a smaller correction and the tradeoff of the proposed solution.

Use the product's documented design system and user-supplied preferences as constraints. Defaults such as one accent, sentence case or a restrained radius scale are choices for an unbranded design, not universal audit rules. A brand-specific preference should be labelled as such. Do not infer how the interface was generated or classify a decorative choice as a blocker without a relevant impact.

## Deliver a usable review

Lead with the decision supported by the inspected scope. Use ready / needs changes / insufficient evidence when readiness was requested; otherwise give the design judgment. Show the most consequential findings first, with additional distinct findings in a linked report or appendix if necessary. Keep inspection depth even when the summary is short.

Each finding uses five compact parts: **Where → What I saw → Why it matters → Fix → Verify**. Add type (bug, UI, UX, accessibility, suggestion or disagreement), likely owner role and severity/confidence where useful. Severity follows impact; state observed facts directly and label causal hypotheses once. Preserve supporting screenshots, recordings or exact source references when available.

Include a compact coverage record for a full audit, useful decisions to preserve, and unresolved access limits together. On a re-review, revisit each previous item and mark fixed / partly fixed / still present / not rechecked with fresh evidence. Complete the requested review before finalizing; “first pass” is appropriate only when the user agreed to staged work. Do not promise a later pass to cover checks available now.
