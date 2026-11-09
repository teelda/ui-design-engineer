# Evaluation cases

Run each prompt once with the skill folder installed and once without it. Keep the same model, repository, time budget, and tools. Save outputs and screenshots; have a reviewer who did not write the prompt score the behavior below. These are cases and criteria, **not claimed benchmark results**.

| Case | Prompt and fixture | Observable success |
|---|---|---|
| Branded marketing page | “Refine this coral-and-cream landing page without changing its brand, videos, copy, or links.” Use a repository with existing tokens and components. | Reuses tokens and components; checks responsive layout and supported states; does not force one accent or remove purposeful gradient. |
| Dense dashboard | “Improve scanability of this trading dashboard while preserving comparison across rows.” Supply representative long and empty data. | Preserves comparison structure; handles density, loading/empty/error and long values; does not flatten all information into plain text. |
| Accessible form | “Build a signup form with validation and a confirmation step.” | Persistent labels, keyboard path, error association, focus handling, narrow layout, and tested success/error states. |
| Existing-system component | “Add a filter panel using this design system.” Supply tokens, components, and light theme only. | Reuses APIs/tokens, verifies only supported theme, and explains any justified deviation. |
| Screenshot-only review | “Audit this screenshot for launch readiness.” Supply a static image with no code or browser. | Reports visible findings and untested interaction/accessibility/crawl behavior; does not certify launch readiness. |
| Web3 handoff | “Review this swap preview and wallet handoff using safe fixtures.” Supply mock screens. | Distinguishes approval from transfer, labels units and fees, checks rejection/recovery, and does not request signatures or claim contract security. |

Score each run 0–2 for context fit, state coverage, accessibility evidence, verification honesty, and task completion. Record concrete regressions and compare paired outputs. Do not turn this rubric into a product score or claim improvement without running it.
