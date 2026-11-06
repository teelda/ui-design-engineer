# UI Design Engineer

A Claude Code / Agent Skill that turns "make it look good" into a checklist of
specific, deliberate design decisions — color, typography, copy, components, motion,
layout, and accessibility — so UI work stops defaulting to generic AI output.

## What's inside

- [`skill/SKILL.md`](skill/SKILL.md) — the skill itself: five up-front design decisions,
  a category-by-category avoid/do checklist, a build workflow, and a pre-ship checklist.

## Install

**Local, right now (this repo):**

```bash
mkdir -p .claude/skills/ui-design-engineer
cp skill/SKILL.md .claude/skills/ui-design-engineer/SKILL.md
```

Claude Code picks up project skills automatically from `.claude/skills/`.

**As a standalone install:**

```bash
npx skills add teelda/ui-design-engineer
```

You can also download or copy `skill/SKILL.md` directly from GitHub and add it to
any AI coding tool that supports reusable project instructions.

## Why this exists

RedPenn AI already runs this same category of check — AI-default palettes, font
monoculture, card overuse, missing alt text, placeholder-as-label, contrast failures,
generic marketing copy — as live DOM audits inside the browser extension
(`apps/extension/src/content/dom-inspector.ts`). This skill is that same design
sense, written as guidance for *writing* UI instead of *scanning* it.

## Product audit coverage

The standalone skill now also reviews existing product journeys, AI results, Web3 flows and search readiness. It ranks findings with evidence and lists untested states. Existing copied installations need to reinstall to receive updates.
