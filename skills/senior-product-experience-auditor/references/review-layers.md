# Review layers

For a journey or launch review, record each layer as tested / partially tested / not tested / not applicable, with evidence, findings and remaining checks. For a single screen, inspect only the layers that apply and skip the table. A missing state is not automatically a defect unless the task needs it.

| Layer | Inspect |
|---|---|
| Task and journey | Entry, orientation, next action, success feedback, back/exit and recovery. Use the four cognitive-walkthrough questions in SKILL.md. |
| Interaction and states | Default, hover, focus, pressed, selected, disabled, loading, empty, partial, success, validation, warning, error, offline, timeout, interrupted and duplicate actions. |
| Visual quality | Container widths, edge/baseline alignment, gutters, nested spacing, type scale, line height, measure, truncation, icons, radius, shadows and density. Claim pixel deviations only with measurement. |
| Design system | Compare with supplied tokens/components and actual variants. If no system is supplied, assess internal consistency; do not invent a compliance standard. |
| Accessibility | WCAG 2.2 AA as review target: semantics, names, error associations, keyboard order, focus visibility/obscuring, modal focus return, announcements, contrast, 200% text scaling, 400% reflow, reduced motion, dragging alternatives and target size. Automated tools are partial evidence. |
| Responsive | 320, 375/390, tablet, laptop and wide layouts where supported. Check text wrapping, horizontal overflow, sticky controls, zoom and orientation. A desktop screenshot cannot prove mobile quality. |
| Content | Labels, terminology, plain language, helper/error copy, first-use comprehension and localization/long text. |
| Cognitive load and IA | Grouping, progressive disclosure, recognition rather than recall, prioritization, discoverability and navigation. |
| Trust and safety | What data leaves the device, permission scope, action previews, confirmations where consequential, undo, deletion, sensitive content and stale/misattributed results. |
| Domain rules | Activate only applicable domain overlays. Separate UX defects from unverified legal or specialist claims. |
| AI UX | Generated versus source data, uncertainty, citations, progress truthfulness, interruption/cancel, retry, incorrect findings, feedback, approval boundaries and score semantics. |
| Implementation | Actual behavior, console/API errors, persistence, refresh, tab switching, races, performance measurements and release parity. Distinguish production, preview and mocks. |
| Discoverability | For public pages: can people and answer engines find, read and cite them? For a launch review, run `search-answer-readiness` and summarise its verdicts here; if it is not installed, record the layer as not tested. |
| Behavioural evidence | Funnel steps and drop-off, success-event tracking, retention or repeat use, and support/feedback themes, from owner-supplied data only. Map each high-drop step to interface findings, or mark it unexplained. Record "not tested" when no data is supplied. |

Useful primary references (check current guidance when citing specific requirements):
- https://www.w3.org/TR/WCAG22/
- https://www.nngroup.com/articles/ten-usability-heuristics/
- https://ethereum.org/en/developers/docs/design-and-ux/heuristics/

WCAG 2.2 AA target size has exceptions and a 24 CSS-pixel minimum criterion; do not call every target below 44px an AA failure. Focus Appearance is AAA; focus visibility and obscuring still need their applicable checks. Cite the actual criterion and tested conditions rather than a generic accessibility label.
