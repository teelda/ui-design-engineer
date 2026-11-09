# Answer-engine (AEO) checks

Answer engines — ChatGPT search, Perplexity, Claude, Gemini, Google AI Overviews and similar — can only cite what they can fetch, read, and attribute. These checks cover those three things. They do not predict whether a page will be cited.

| Check | Evidence required | Failure condition | Fix and verification |
|---|---|---|---|
| **AI crawler access** | `robots.txt` groups for the agents the owner cares about, plus any CDN/WAF bot rules | An agent is blocked or allowed **contrary to the owner's stated intent**, or a firewall blocks it regardless of `robots.txt` | Write explicit groups per agent; refetch `robots.txt`; check firewall logs or settings when available. |
| **Readable without JavaScript** | Raw initial HTML (no rendering) of each intended page | The answer, headings, or product name appear only after client-side rendering | Server-render or pre-render the substantive content; refetch raw HTML. |
| **Answer-first structure** | The representative question for the page and where it is answered | The direct answer is buried below marketing copy, inside tabs/accordions only, or split across pages | Put a plain one-to-three-sentence answer near the top under a heading that matches the question; keep detail below it. |
| **Entity clarity** | Product/organisation name, one-line description, and `Organization`/`Product`/`SoftwareApplication` markup where relevant; the same facts on docs and official profiles | Name, description, or key facts differ across the site, docs, and profiles, or markup contradicts visible text | Use one canonical name and description; align markup and profiles; link profiles with `sameAs`. |
| **Freshness and provenance** | Visible published/updated date, author or owner, and sources for factual claims | Undated time-sensitive content, unattributed claims, or stale facts | Add dates and sources; update or retire stale pages. |
| **`llms.txt`** (optional) | Whether `/llms.txt` exists and what it lists | It lists private, outdated, or non-canonical pages | Treat it as an optional proposal ([llmstxt.org](https://llmstxt.org/)), not a standard or ranking factor; keep it consistent with the sitemap if used. |

## AI crawler names

Agent names and their purposes change; check each vendor's current crawler documentation before writing rules. As a starting point, vendors separate **training** crawlers from **search/retrieval** and **user-triggered** fetchers — for example OpenAI (`GPTBot`, `OAI-SearchBot`, `ChatGPT-User`), Anthropic (`ClaudeBot`, `Claude-SearchBot`, `Claude-User`), and Perplexity (`PerplexityBot`, `Perplexity-User`). `Google-Extended` is a `robots.txt` control token for Gemini model use, not a separate crawler, and does not change Google Search or AI Overviews eligibility. Blocking a training crawler and allowing a search crawler is a legitimate owner choice; the check is whether the rules match intent.

Several AI crawlers have been reported not to execute JavaScript. Do not assume either way: the raw-HTML check above is the evidence.

## Observed visibility (only when requested)

Record the engine, exact query, date, signed-in state/location if known, whether the page was cited, the cited URL, and whether the answer was factually accurate. Repeat each query at least three times; answers vary between runs. A citation on one run is an observation, not a visibility guarantee.

Google says AI Overviews and AI Mode have [no additional technical requirements beyond Search eligibility](https://developers.google.com/search/docs/appearance/ai-features). Do not generalise that policy to other engines. Do not invent AEO scores or promise citations or traffic.
