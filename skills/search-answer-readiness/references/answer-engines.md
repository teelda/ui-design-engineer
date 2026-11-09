# Answer-engine (AEO) checks

Answer engines — ChatGPT search, Perplexity, Claude, Gemini, Google AI Overviews and similar — can only cite what they can fetch, read, and attribute. These checks cover those three things. They do not predict whether a page will be cited.

| Check | Evidence required | Failure condition | Fix and verification |
|---|---|---|---|
| **AI crawler access** | The owner's intent per engine and purpose (see below), the effective `robots.txt` rules, and any CDN/WAF bot rules | The effective rules block or allow a crawler **contrary to the owner's stated intent**, or a firewall blocks it regardless of `robots.txt` | Change only the rules that conflict with intent; existing wildcard rules that already match intent need no per-agent group. Refetch `robots.txt`; check firewall logs or settings when available. |
| **Content without JavaScript** | Raw initial HTML (no rendering) compared with the rendered DOM | **Not a universal failure.** Google renders JavaScript for Search, and its AI features have no extra technical requirements. Record content that exists only after rendering as a **risk** for engines whose crawlers are not documented to render it. Record a **failure** only when a specific engine is observed or documented to miss the content. | When the risk matters to the owner, server-render or pre-render the substantive content; refetch raw HTML and recheck the affected engine. |
| **Answer-first structure** | The representative question for the page and where it is answered | The direct answer is buried below marketing copy, inside tabs/accordions only, or split across pages | Put a plain one-to-three-sentence answer near the top under a heading that matches the question; keep detail below it. |
| **Entity clarity** | Product/organisation name, one-line description, and `Organization`/`Product`/`SoftwareApplication` markup where relevant; the same facts on docs and official profiles | Name, description, or key facts differ across the site, docs, and profiles, or markup contradicts visible text | Use one canonical name and description; align markup and profiles; link profiles with `sameAs`. |
| **Freshness and provenance** | Visible published/updated date, author or owner, and sources for factual claims | Undated time-sensitive content, unattributed claims, or stale facts | Add dates and sources; update or retire stale pages. |
| **`llms.txt`** (optional) | Whether `/llms.txt` exists and what it lists | It lists private, outdated, or non-canonical pages | Treat it as an optional proposal ([llmstxt.org](https://llmstxt.org/)), not a standard or ranking factor; keep it consistent with the sitemap if used. |

## Three kinds of bot control

Agent names and their purposes change; check each vendor's current crawler documentation before judging rules. Treat these cases separately:

1. **Training crawlers** (for example OpenAI `GPTBot`, Anthropic `ClaudeBot`) collect content for model training. Blocking them is a legitimate owner choice and does not by itself remove a site from AI search answers.
2. **Search crawlers** (for example OpenAI `OAI-SearchBot`, Anthropic `Claude-SearchBot`, `PerplexityBot`) index pages for an engine's search answers. These are the `robots.txt` controls that matter for being cited. For OpenAI, `OAI-SearchBot` — not `ChatGPT-User` — is the Search control.
3. **User-triggered fetchers** (for example `ChatGPT-User`, `Claude-User`, `Perplexity-User`) visit a page because a person asked. Vendors document that `robots.txt` may not apply to these visits, so do not report a `robots.txt` rule as controlling them; a firewall rule is the only reliable block.

`Google-Extended` is a `robots.txt` control token for Gemini model use, not a separate crawler, and does not change Google Search or AI Overviews eligibility; those follow `Googlebot`.

The check is whether the **effective** rules match the owner's intent for each case — not whether every agent has its own group. References: [OpenAI crawlers](https://developers.openai.com/api/docs/bots).

## Observed visibility (only when requested)

Record the engine, exact query, date, signed-in state/location if known, whether the page was cited, the cited URL, and whether the answer was factually accurate. Repeat each query at least three times; answers vary between runs. A citation on one run is an observation, not a visibility guarantee.

Google says AI Overviews and AI Mode have [no additional technical requirements beyond Search eligibility](https://developers.google.com/search/docs/appearance/ai-features). Do not generalise that policy to other engines. Do not invent AEO scores or promise citations or traffic.
