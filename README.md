# UI Design Engineer

A reusable skill for building and refining web interfaces in their product context. It covers design decisions, component and token reuse, interaction states, responsive checks, and honest verification. A focused UI-audit route has optional Web3 and search-readiness references; broad product audits belong in a dedicated audit skill.

## Install

```bash
npx skills add teelda/ui-design-engineer
```

For a manual install, copy the **whole** [`skill/`](skill/) folder into your agent's skills directory. `SKILL.md` links to `references/` and `scripts/`; copying that file alone omits those capabilities. Existing manual copies need replacing when you update.

## Use

- Build or refine a page, component, form, or dashboard while preserving its existing design system.
- Request a focused UI review with evidence limits stated. Read the Web3 or search reference only when that topic is in scope.
- Run `python3 skill/scripts/ui_lint.py <paths>` for source-level review candidates. It does not certify accessibility or visual quality.

The [evaluation cases](evals/README.md) provide paired with-skill/without-skill prompts and a scoring rubric. [Illustrative examples](evals/examples.md) show how context changes a decision. No paired benchmark has been run or published yet.

RedPenn's browser extension has its own DOM inspector. This public skill does not require RedPenn or access to its private source. Its guidance is separate from the extension's hosted audit model.
