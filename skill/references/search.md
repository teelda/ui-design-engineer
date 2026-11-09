# Basic technical and on-page search readiness

Use only for public pages the owner intends people to find in search. First list the intended indexable URLs and the intended exclusions (for example sign-in, private dashboards, and drafts). Record **pass / fail / not tested / not applicable** for each applicable check. Keep crawling, rendering, indexing, content usefulness, and observed answer-engine visibility separate.

| Check and applicable pages | Evidence required | Failure condition | Fix and verification |
|---|---|---|---|
| **Crawl access:** intended public URLs | HTTP status, redirects, `robots.txt`, `X-Robots-Tag`, and page robots meta | Intended page is blocked, errors, or redirects to an unrelated page | Correct the rule or route; fetch the URL again as an unauthenticated client. |
| **Indexing:** intended public URLs | Canonical URL, robots directives, and Search Console URL Inspection when the owner has access | `noindex`, conflicting canonical, or Search Console reports an unexpected exclusion | Align directives and canonical with intent; request/recheck inspection. A fetch alone does not prove indexing. |
| **Rendering and routes:** JavaScript pages | Compare initial response HTML with rendered DOM; inspect route status and substantive text | Main content or metadata disappears, route returns an app shell/error status, or links are only click handlers | Provide stable URL responses and discoverable `<a href>` links; inspect rendered HTML and destination responses again. |
| **Metadata:** intended public URLs | Page-specific title, description, heading, and canonical target in initial/rendered HTML | Generic, duplicated, misleading, or conflicting metadata | Write accurate page-specific metadata; verify each target URL and rendered output. |
| **Content intent:** intended public URLs | Audience question/task, visible answer, supporting evidence, authorship/source where relevant | Page omits the answer, hides key facts, or makes unsupported claims | Complete and substantiate the answer; reread as the intended user. |
| **Structured data:** only relevant supported page types | Markup, visible content, and applicable search documentation | Markup misrepresents the page or contradicts visible content | Correct/remove markup; validate syntax and visible correspondence. |

For a local check, fetch the public URL and `robots.txt`, inspect response headers, compare source HTML with a browser-rendered DOM, and follow representative internal links. Use Search Console only when available to the owner. A browser rendering correctly does not establish crawling or indexing. Google describes separate [crawling, rendering, and indexing](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) stages.

## Answer-engine observations

1. **Discoverability:** record whether each intended page is eligible and accessible under the checks above.
2. **Answer usefulness:** name a representative user question and check whether the page answers it clearly and accurately with appropriate evidence.
3. **Observed visibility:** only when requested and permitted, record the engine, exact query, date, repeated observations, cited URL, and factual accuracy. A mention or citation on one run is an observation, not a visibility guarantee.

Google says its AI Overviews and AI Mode have [no additional technical requirements beyond established Search eligibility](https://developers.google.com/search/docs/appearance/ai-features). Do not generalize that policy to every answer engine. Do not invent SEO/AEO scores or promise rankings, citations, or traffic.
