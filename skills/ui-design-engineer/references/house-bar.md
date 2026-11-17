# House bar (opt-in)

A labelled preference profile: the review bar Matilda Anashie applies to her own and her teams' product, brand and motion work. Load it only when the user asks for "the house bar" or "Matilda's bar", or names this file. The auditor's name alone does not opt in. Without that request, use the general [design principles](design-principles.md). When loaded, say so in the report and mark each finding that rests on this profile **house bar**, so it stays distinct from general usability or accessibility evidence.

The product's own brand rules still come first. If a rule here conflicts with a documented brand rule, follow the brand and say so. Once loaded, the instant list below may block sign-off on decorative or stylistic choices, overriding the general rule against blocking on decoration; label every such block **house bar**.

## Review in this order

Check these in order. The order sets reporting priority; it never stops the inspection. Record an unresolved or failed gate (for example, ownership not confirmed) as a finding or an open question, then continue with every reachable layer the user asked for, including the full visual and interaction review.

1. **Real.** Open the live product. Confirm the feature does not already exist, is still a priority, and is not another team's work. Write "not checked" when access is missing.
2. **True.** Every label, figure, network, plan term and state matches production today. Each figure names its source. Conflicting sources are raised, not silently resolved.
3. **Asked for.** Scope, format and timeline match the request. "Add" adds; it does not replace.
4. **Understood.** Each screen tells the user where they are, what worked, what failed, what happens next and what counts.
5. **On system.** Real tokens, fonts, logo and assets.
6. **Crafted.** Alignment, padding, radius, type scale, overflow and asset sharpness hold on every screen.
7. **Distinct.** A concept carries the work: art direction, real imagery, one signature move.
8. **Self-critiqued.** The maker names the weakest part before handing it over.

## Rules

**Product and UX**
- The interface explains state, next action, error and consequence. If users learn the outcome only from support or community staff, record a product finding.
- Translate system state into user state: "submitted, confirming, done" with a receipt or record link, not raw system status.
- Design every reachable state: empty, loading, pending, success, failure, already linked, locked (with why and how to unlock), expired.
- Show rules that affect rewards, limits or eligibility in the product, at the point of decision.
- Recommend the next useful action from the user's current state. Show only the paths that apply to them.

**Visual**
- Content edges align with the header and footer edges.
- One radius language per product: either pills or one small radius scale for controls and surfaces.
- Sentence case for titles, eyebrows, chips and labels; acronyms stay capitalised.
- Flat fills and solid borders. Hierarchy comes from type, spacing and one accent colour. Keep a gradient, glow or heavy shadow only when the live product already uses it, and say so.
- Use the official logo file and exact brand values, exported from the source (Figma, brand kit).
- Prefer real photography and real product screens. Use brand shapes sparingly and at large scale. No photo appears twice in one document.
- Mockups render at 2× display size, straight on, with nothing cropped or overlapping.
- Proposed designs are real frames with layers, not screenshots placed on a canvas.

**Copy**
- Status language matches what is live: "coming soon" stays "coming soon". Say what an asset or badge does today and what it does not give.
- An audit of someone else's product uses a neutral, outside voice.

**Motion**
- A brief and storyboard come before animation.
- A hero object or real photo carries each film; product screens sit inside a device at teaching size.
- Use 3D only for something physical or spatial: layers, parts, placement, scale.
- Check dense frame windows around every cut, plus frozen stretches, brightness spikes and loudness.

**Documents and decks**
- The answer comes first; titles state the finding.
- Formal documents use the organisation's letterhead and a real document format.
- End with decisions, owners and dates.

## Instant ONE MORE PASS

Any of these blocks sign-off under the house bar **when it is observed** in the rendered product or confirmed against the brand source. A source-only checker candidate is a question to verify, not a block.

- proposes something that is already live or owned by another team
- DEV or testnet labels in a production design
- a redrawn logo or approximated brand colour
- decorative gradients or glows the live product does not use
- mixed pill and small-radius controls
- all-caps labels
- content padding that does not align with the header and footer
- blurred, upscaled, tilted or cropped mockups
- screenshots presented as design frames
- type-on-black or screenshot-slideshow motion
- figures without a source

## Report

- Each finding: **Where → What I saw → Why it matters → Fix → Verify**, tagged by type (bug, UI, UX, accessibility, suggestion, disagreement) and owner (UX, tech, comms).
- Put the five most consequential findings first and the rest in an appendix.
- Re-reviews mark each earlier item FIXED / PARTLY / STILL THERE with where it was checked.
- End with **SHIP** or **ONE MORE PASS** and at most three ranked fixes. Either verdict needs rendered evidence for visual claims. With source or text alone, give **insufficient evidence** and list what to render or confirm.

When source is available and the UI skill is installed, run its `ui_lint.py --profile house` for the mechanical part of the visual rules. Its candidates need a rendered check before they become findings.
