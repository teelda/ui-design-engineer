# UI Design Engineer

A reusable skill for building and refining web interfaces in their product context. It covers design decisions, component and token reuse, interaction states, responsive checks, and honest verification. Its audit route is for focused UI reviews; the separate [Senior Product Experience Auditor](https://github.com/teelda/ui-design-engineer/tree/main/skills/senior-product-experience-auditor) follows whole journeys across product patterns and surfaces.

## Install

```bash
npx skills add teelda/ui-design-engineer --skill ui-design-engineer
```

For broader product review, install the second skill from the same repository:

```bash
npx skills add teelda/ui-design-engineer --skill senior-product-experience-auditor
```

For a manual install, copy the **whole** [`skill/`](skill/) folder into your agent's skills directory. `SKILL.md` links to `references/` and `scripts/`; copying that file alone omits those capabilities. Existing manual copies need replacing when you update.

## Use

- Build or refine a page, component, form, or dashboard while preserving its existing design system.
- Request a focused UI review with evidence limits stated. Read the Web3 or search reference only when that topic is in scope. Use the separate product-review skill for multi-step workflows and launch decisions.
- From this repository, run `python3 skill/scripts/ui_lint.py <project-paths>`. After installing, locate the installed `SKILL.md` and run its sibling `scripts/ui_lint.py` by absolute path. See [checker coverage](skill/references/source-checker.md) for supported syntax and exclusions.

The [evaluation protocol](evals/README.md) includes a fixed fixture, repeated-run procedure, and scoring anchors. [Illustrative examples](evals/examples.md) show how context changes a decision. Paired model results have not been published yet.

RedPenn's browser extension has its own DOM inspector. This public skill does not require RedPenn or access to its private source. Its guidance is separate from the extension's hosted audit model.
