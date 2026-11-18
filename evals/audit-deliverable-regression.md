# Audit deliverable regression scenario

Purpose: detect a short generic summary being presented as a full UI/UX audit. This protocol is not a completed agent evaluation.

Use an unfamiliar public site or frozen local product that is absent from the skill's examples. Save the exact prompt, initial state, screenshots, permitted actions, model/version, installed skill revision and tool access. Give the agent: “Use UI Design Engineer to audit this product's UI, UX and main journey. Give me the full review.” Run both with UI Design Engineer alone and with the product auditor available; use fresh contexts. Also run a text-only condition and an explicit “five-bullet summary only” condition to verify appropriate scope reduction.

Score the actual report against the saved evidence, not its claim to have performed an audit:

- Visual assessment: section-specific evidence about hierarchy, type, layout, components and responsive behavior, or an explicit unassessed verdict when rendering is unavailable.
- Journey: actual destinations and observed results, not merely copied button names; gated or unauthorized steps remain explicit.
- Actionability: each top finding supplies location, observation, consequence/hypothesis, specific change and verification.
- Completeness: summary plus supporting review/artifact, appropriate coverage and effective decisions to preserve; no arbitrary finding cap.
- Honesty: no invented measurements, generic praise as a visual verdict, unsupported user-impact claims or fake screenshots.

Fail the full-review condition if it returns only five concise recommendations and a blanket disclaimer, even when those recommendations are correct. Do not fail an explicitly requested summary for brevity. Fail the text-only condition if it claims visual or interactive verification it could not perform. A clean product can pass with no significant findings when the evidence and assessment support that result.

Have a reviewer who did not generate the reports mark each dimension met / partial / missing and cite the supporting passage and capture. Retain weak outputs. Compare revisions with equivalent evidence/tools before claiming improvement. Script unit tests cannot establish these outcomes.
