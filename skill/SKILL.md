---
name: ui-design-engineer
description: "Use when building or reviewing any UI — landing pages, dashboards, forms, components — to make deliberate design decisions instead of shipping generic AI-default output. Covers color, typography, copy, components, motion, layout, accessibility, and a pre-ship checklist."
---

# UI Design Engineer

A design pass, not a vibe check. This skill turns "make it look good" into a sequence
of specific, checkable decisions. Apply it whenever you're building a new UI surface
or reviewing one before ship.

## When to use

- Building a new page, screen, or component from a prompt or brief
- Reviewing UI code before merging or shipping
- Something "looks AI-generated" but the reason is hard to name
- Choosing color, type, or spacing systems for a new surface

Skip it for pure logic/data changes that don't touch markup or styles.

## The five decisions, in order

Make these decisions *before* writing any markup. Everything else in this skill is
detail underneath them.

1. **Name the design in one phrase.** "Quiet and dense" or "confident and spacious" —
   not "modern and clean" (that's not a decision, it's the default everyone types).
   If you can't name it, you'll default to whatever the framework ships with.
2. **Pick exactly one accent color.** Everything else is neutrals (2–3 grays/near-blacks)
   plus that one hue. A second accent needs a specific job (destructive actions, a
   status color) or it doesn't exist.
3. **Build hierarchy with scale and space, not color.** If removing all color still
   leaves the page readable in the right order, the hierarchy is real. If the page
   goes flat without color, you were using color to do layout's job.
4. **Subtract before you add.** For every card, badge, icon tile, or shadow: could
   this be a plain line of text at the right weight and size instead? Default to yes.
5. **Every decorative element must carry meaning.** A colored dot, a border, an icon —
   if you can't say what state or category it represents, delete it.

## Checklist by category

Each row: the generic default vs. the deliberate choice. "Avoid" isn't banned outright —
it's what happens when no one made the decision. It's fine *if it's the actual decision*
(e.g., a status dot that really does indicate live state).

### Color

| Avoid (undecided default) | Do instead |
|---|---|
| Indigo/violet gradient buttons, gradient headline text | One flat accent color; gradients only where they represent something (a live signal, a hero image treatment picked for the brand) |
| Same hue for a status box's border, text, and tinted background | Vary weight/saturation so the element doesn't read as one flat sticker |
| Near-black page with glow/halo effects "for atmosphere" | Dark mode built from a real neutral scale (test each step's contrast), glow reserved for actual focus/active states |

### Typography

| Avoid | Do instead |
|---|---|
| A serif swapped into one word mid-headline for "emphasis" | Weight or size change within the same typeface; reserve a second typeface for a real structural role (headings vs. body) |
| Tiny uppercase kicker line above every heading, restating the heading | Cut it, or make it carry new information (a category, a date) |
| An entire marketing sentence set at display size (text-6xl+) | Split subject from supporting detail — the display size is for 2–5 words |
| All text sizes crammed into 14–18px | A real type scale (e.g. 12/14/16/20/28/36) so size differences are visible at a glance |

### Copy

| Avoid | Do instead |
|---|---|
| "Not just X — it's Y", "Say goodbye to...", stacked em-dashes | State the specific benefit in one sentence, plainly |
| Emoji on every heading, button, and bullet | Reserve emoji (if used at all) for one deliberate spot, or use icons with real meaning |
| Vague buzzwords: "seamlessly," "unlock the power of," "next-gen," "revolutionize" | Say the concrete outcome: what changes for the user, with a number or example if you have one |
| Generic CTA text repeated everywhere: "Get Started," "Learn More" | Name the actual next action: "Start free audit," "See the 12 rules" |

### Components

| Avoid | Do instead |
|---|---|
| Pulsing colored dot next to something that never changes state | Only animate a status indicator if the state actually changes; otherwise a static label |
| Every list item wrapped in a pale card with a 4px colored left border | Plain rows with a divider; reserve the card treatment for content that's genuinely a separate, movable unit |
| Feature grid of interchangeable rounded icon tiles, one per bullet | Icons only where they disambiguate (not decorate); vary layout so items aren't visually identical |
| Max border-radius + backdrop-blur on every panel | Pick one radius scale (e.g. 6/10/16px) tied to element size; blur reserved for actual overlays |
| Nested containers all sharing the same border-radius (corners don't nest correctly) | Inner radius = outer radius minus the padding between them, or drop the inner border entirely |
| "✨ New," "β Beta," "🔥 Popular" badges on everything | One badge, only where it's true and useful right now |

### Motion

| Avoid | Do instead |
|---|---|
| `hover:scale-105` + `transition-all` + bouncy easing on every interactive element | Motion on the elements where it clarifies cause/effect (press feedback, expand/collapse); ease-out on enter, ease-in on exit, 150–300ms |
| Spinner that rotates around an off-center point | Standard centered spinner, or better: a skeleton that mirrors the real layout |

### Layout

| Avoid | Do instead |
|---|---|
| Rows of uppercase-label cards filling the screen | Vary layout rhythm — not everything is the same-size box in a grid |
| Three unverified stats ("10k+ users," "99.9% uptime," "24/7 support") for social proof | Real numbers you can back up, or cut the row entirely |
| Giant faint "01 / 02 / 03" ordinals on unordered feature sections | Only number things that have an actual sequence |
| Cards nested inside cards inside cards | Flatten — most of those layers are one background/border too many |
| One spacing value (`gap-4`, `p-4`) stamped across the whole page regardless of hierarchy | A spacing scale where bigger gaps mean bigger hierarchy jumps (e.g. 4/8/16/24/48px) |

### Accessibility (non-negotiable, not a style choice)

- Every `<img>` that conveys meaning has real `alt` text; decorative images get `alt=""`.
- Labels are real `<label>` elements, not placeholder text that disappears on focus.
- Text contrast meets WCAG AA: 4.5:1 normal text, 3:1 at 18px+/bold 14px+.
- Focus states are visible (`outline` or an equivalent ring) on every interactive element — never `outline: none` with nothing to replace it.
- Heading levels are sequential (no h2 → h4 skips) and there's exactly one h1.

## Workflow

1. **Decide first.** Answer the five decisions above in a sentence or two before touching code.
2. **Build the neutral structure.** Layout, hierarchy, spacing — in grayscale, no accent color yet. If it doesn't read correctly in grayscale, color won't fix it.
3. **Add the one accent color** to the 1–2 places that need emphasis (primary action, active state).
4. **Run the checklist** above against what you built. For every "avoid" pattern present, ask: is this the actual decision, or the default I got for free?
5. **Check contrast and focus states** in both light and dark mode before calling it done.

## Pre-ship checklist

- [ ] Can you name the design in one phrase, and does the accent-color count match that decision (one, or a specifically justified second)?
- [ ] Does the layout still read in the right order with color removed?
- [ ] Every card/badge/shadow/icon tile: is it doing a job a plain line of text couldn't?
- [ ] Every decorative element (dot, border, animation) maps to a real state or category?
- [ ] Copy: any buzzwords or stacked em-dashes to cut? Are CTAs named for the specific action?
- [ ] Alt text, real labels, AA contrast, visible focus rings, sequential headings — all checked?
- [ ] Tested in both light and dark mode, not just the one you designed in?

## Relationship to ReadPenn AI

Use this skill while designing or building. Run a ReadPenn audit afterward to catch
what slipped through on the live page.
