# Product quality skills

Three agent skills, one job each:

| Skill | Use it to | Folder |
|---|---|---|
| **ui-design-engineer** | Build or refine a page, component, form, or dashboard with deliberate design decisions, reused tokens, and verified states | [`skills/ui-design-engineer/`](skills/ui-design-engineer/) |
| **senior-product-experience-auditor** | Review an existing screen, journey, or launch — UX, accessibility, Web3 and AI products, and analytics/funnel evidence when supplied | [`skills/senior-product-experience-auditor/`](skills/senior-product-experience-auditor/) |
| **search-answer-readiness** | Check whether public pages can be found, read, and cited by search engines and AI answer engines (SEO and AEO) | [`skills/search-answer-readiness/`](skills/search-answer-readiness/) |

The design skill builds; the auditor grades. A launch review in the auditor calls on the search skill for its discoverability layer.

## Install

```bash
npx skills add teelda/ui-design-engineer --skill ui-design-engineer
```

```bash
npx skills add teelda/ui-design-engineer --skill senior-product-experience-auditor
```

```bash
npx skills add teelda/ui-design-engineer --skill search-answer-readiness
```

For a manual install, copy the **whole** skill folder (for example `skills/ui-design-engineer/`) into your agent's skills directory. Each `SKILL.md` links to its own `references/` and `scripts/`; copying that file alone omits them. Existing manual copies need replacing when you update.

## Source checker

From this repository, run `python3 skills/ui-design-engineer/scripts/ui_lint.py <project-paths>`. After installing, run the installed skill's `scripts/ui_lint.py` by absolute path. See [checker coverage](skills/ui-design-engineer/references/source-checker.md) for supported syntax and exclusions.

## Evaluation

The [evaluation protocol](evals/README.md) includes a fixed design fixture, a search-readiness fixture, a repeated-run procedure, and scoring anchors. [Illustrative examples](evals/examples.md) show how context changes a decision. Paired model results have not been published yet.

Run the checker tests from the repository root:

```bash
python3 -m unittest discover -s evals -p 'test_*.py'
```
