# Product quality skills

Three early skills for autonomous agents building and reviewing web products. They give experienced builders and reviewers decision and verification discipline while preserving existing design systems. They are instructions and small checkers for AI coding tools, **not** the RedPenn browser extension or a substitute for product research.

| Skill | Use it when | What it returns |
|---|---|---|
| [UI Design Engineer](skills/ui-design-engineer/SKILL.md) | Building or refining a page, form, component, or dashboard | A context-aware implementation with relevant states and verification notes. |
| [Senior Product Experience Auditor](skills/senior-product-experience-auditor/SKILL.md) | Reviewing a screen, journey, gated web app, or launch | Ranked findings with evidence, route coverage, and explicit untested steps. |
| [Search and Answer Readiness](skills/search-answer-readiness/SKILL.md) | Checking public-page SEO/AEO prerequisites | Crawl, rendering, content, and answer-readiness checks with evidence and limits; no visibility score. |

Use one skill for the task. The UI skill routes review requests to the auditor; the auditor can use the search skill for public-page discoverability. A wallet or sign-up gate is a handoff point: the auditor should ask for safe test access before claiming to have reviewed protected steps.

## Try the product auditor

Requires Node.js **22.20.0 or newer** for the current `skills` installer. Install the skill, then start a new agent chat:

```bash
npx skills add teelda/ui-design-engineer --skill senior-product-experience-auditor
```

Example request:

> Audit the main user journey at this web app. Follow its visible navigation and primary CTAs. At a sign-up or wallet gate, ask me for a safe test handoff before finishing. Show which routes and states you opened, which remain untested, and the three most consequential findings.

The agent's browser, repository access, and authorization determine what it can verify. If it cannot enter a protected flow, expect an **entry-and-gate review**, not a full product verdict. See this [source-assisted sample report](examples/signup-audit.md) for the evidence and limits a report should show.

## Install the other skills

```bash
npx skills add teelda/ui-design-engineer --skill ui-design-engineer
npx skills add teelda/ui-design-engineer --skill search-answer-readiness
```

For manual installation, copy the **whole** skill folder into your agent's skills directory. Each `SKILL.md` links to its own `references/` and `scripts/`. Installed copies do not update when this repository changes; rerun the install command to pick up new instructions, then start a new chat.

## Checkers and evidence

Both scripts use the Python standard library. Run an installed script by its absolute path.

- **UI source checker:** `python3 skills/ui-design-engineer/scripts/ui_lint.py <project-paths>` flags design and accessibility candidates in HTML/CSS/JSX/TSX. Read its [coverage and limits](skills/ui-design-engineer/references/source-checker.md).
- **Search checker:** `python3 skills/search-answer-readiness/scripts/search_check.py <urls> --exclude <private-urls>` checks HTTP status, crawler access, index directives, canonical URLs, metadata, raw HTML, links, social tags, structured data, language alternates, and sitemaps. Add `--crawl 50` to follow internal links or `--psi` with `PSI_API_KEY` for PageSpeed Insights data. Read its [coverage and limits](skills/search-answer-readiness/references/checker.md). It cannot establish actual indexing, rankings, or AI citations.

Run the checker tests with `python3 -m unittest discover -s evals -p 'test_*.py'`. The [evaluation protocol](evals/README.md) describes paired agent tests. One [exploratory paired pilot](evals/results/quiet-pilot/README.md) found nearly identical small edits with and without the UI skill; it does not demonstrate a quality benefit. Repeated, blinded results have not been published, and effects on design quality and user outcomes are **not yet measured**. Reports should label observation, inference, and untested scope rather than promise accuracy, accessibility certification, search rankings, or AI citations.

Found a wrong or missing finding? Open a GitHub issue with the skill name, agent/tool, exact request, reachable states, and the relevant output. Remove private URLs, credentials, and user data before posting.

Released under the [MIT License](LICENSE). Copyright © 2026 Matilda Anashie.
