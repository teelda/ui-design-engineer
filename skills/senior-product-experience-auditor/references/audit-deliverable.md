# Full audit deliverable

Read before inspecting and use before finalizing a UI/UX or product audit. A request to “audit this site” asks for the supporting review as well as the verdict. Use a summary-only response only when the user requests one. Match the inspected scope to the task; do not expand a component review into an entire product audit.

## Evidence first

Record evidence as you inspect: capture ID or exact locator, URL/component, viewport dimensions, state/action, observed result, and evidence mode. Retain screenshots or recordings for consequential visual/interaction claims when the tool permits. Reference actual artifacts; if no capture can be saved, give a precise locator and say what was observed. A URL alone is not evidence of a font size, contrast ratio, breakpoint behavior or an interaction result.

Follow the main action through every reachable, authorized state relevant to the task. Inventory alternate primary paths rather than stopping after finding a few copy inconsistencies. Test permitted validation, feedback and recovery. At access gates, offer the user a supported handoff; mark remaining states untested if access is unavailable. Stop before actions requiring authorization. A task is not complete just because five findings have been collected.

## Deliver the review

Use these content requirements, with headings and length adapted to the task. A table of priorities is an opening summary, not a substitute for the supporting sections.

1. **Verdict and scope.** State the user task, decision, inspected surfaces and evidence limits in a few sentences. Name the loaded skill source/revision when known. Avoid unverified version claims.
2. **Visual design assessment.** Explain the actual composition and reading order at the tested widths. Cover the applicable design principles: typography, alignment/spacing, color/contrast, component relationships, imagery/motion, density, consistency and responsive behavior. Use section-specific observations to support both strengths and weaknesses. Separate distinctive product subject matter from distinctive visual execution. If no rendered evidence exists, state that visual quality is unassessed; do not replace inspection with praise or a guessed visual verdict.
3. **User journey and product assessment.** Show entry → action → destination → feedback/result or gate. Explain what the user expects and what actually happens. Check the agreement between audience, product promise, availability, pricing and onboarding where relevant. Include reachable error/recovery states, and identify specific untested steps rather than a vague final disclaimer.
4. **Detailed findings.** Rank distinct root problems by impact. Each finding gives **Where → What I saw → Why it matters → Fix → Verify**, with evidence references. Distinguish observed defects, plausible risks and preferences. A designer should be able to locate the element and understand the proposed change without another audit. “Improve hierarchy,” “reduce clutter” or “increase legibility” needs a specific relationship, concrete change and acceptance condition. Show the most consequential findings first; preserve other actionable findings in the full report rather than imposing a five-finding limit.
5. **Preserve, coverage and next decision.** Identify effective decisions to preserve with evidence. Summarize checked / partial / not checked / not applicable coverage and the reason for each important gap. End with the prioritized action and acceptance conditions for the requested decision. Do not announce a future “second pass” to perform available work that belongs in this audit.

When a file/artifact tool is available and the review is substantial, write the complete report there and link it from a concise chat summary. Otherwise provide the supporting review in chat. Do not create a file merely to hide missing inspection. Open or read the saved report to verify its contents before linking it. Use accessible paths for the user's environment, not invented URLs or local paths on another machine.

## Example of depth, not an assertion about a real site

Given a captured 390px layout showing three equal-weight buttons before a signup form, an actionable finding could be:

**UX/UI · concern · medium confidence. Where:** signup panel, narrow capture E2. **What I saw:** the trial, documentation and contact buttons share the same filled treatment and occupy a row above the email field. **Why it matters:** the intended task is starting a trial; the equal treatment gives no visible ordering between that action and two exits. This is a hierarchy concern, not a measured conversion loss. **Fix:** keep the trial action adjacent to the form, make documentation a text link, and move contact to the supporting help text while preserving both destinations. **Verify:** at the captured width and desktop, the trial action remains visibly associated with the form, the secondary links remain reachable, and keyboard order follows the displayed order.

The report would still need its visual assessment, path observations and coverage. Expanding one finding alone does not establish a full review.

## Completion check

Before returning, verify against the evidence you collected:

- Does the output include supporting visual and interaction assessments, not only a short issue list?
- Could a teammate locate and act on each top finding from its evidence, fix and acceptance check?
- Are claims of strong visual design grounded in actual visual relationships? Are generic-design criticisms equally specific?
- Did you follow the requested journey as far as tools, access and authorization permit, recording the rest?
- Did you preserve distinct actionable findings, rather than stop at an arbitrary count?
- Are measurements, tests, citations and artifact links real, and is uncertainty attached to the relevant claim?

If an available check or report section is missing, complete it now. If evidence is unavailable, narrow the verdict and explain the exact limit. Never fill a section with invented findings or claim completed testing to satisfy this format.
