# Search checker coverage

`scripts/search_check.py` uses the Python standard library only. It sends plain GET requests with its own user agent, follows up to ten redirects, reads up to 5 MB per response, and never runs JavaScript.

```text
search_check.py URL [URL ...] [--exclude URL ...] [--json] [--strict]
                [--timeout 15] [--min-words 50] [--sitemap-sample 25]
                [--crawl N] [--psi] [--psi-strategy mobile desktop] [--psi-key KEY]
```

`--strict` exits 1 when any check fails. `--json` prints a list of `{page, check, result, detail}`.

- `--crawl N` follows same-host `<a href>` links from the given URLs to up to N more pages, skipping assets and anything `robots.txt` blocks for Googlebot. It fetches one page at a time. Use a small N on sites you do not own.
- `--psi` asks Google PageSpeed Insights for Core Web Vitals. **This sends each URL to Google.** The keyless quota is shared and often exhausted (HTTP 429), so set `PSI_API_KEY` or pass `--psi-key`; a free key comes from the Google Cloud console. A request can take up to a minute per URL and strategy.

| Check | What it does | Does not establish |
|---|---|---|
| Status and redirects | Final status, redirect chain, cross-host or multi-hop redirects as a risk | Behaviour for other user agents or regions |
| Crawl access | RFC 9309 matching per crawler: the specific group replaces `*`, the longest rule wins, `allow` wins ties, `*` and `$` wildcards. A `robots.txt` server error is reported as a full block. | CDN or firewall bot rules; what the owner intends |
| AI crawler access | Groups results by purpose: search, AI search, training, Google-Extended, user-triggered. Only a block of Googlebot or Bingbot on an intended page is a failure; AI search blocks are a risk; the rest is information. | Whether vendors honour the rules; current crawler names (see vendor docs) |
| Indexing | `noindex`/`none` in meta robots, `googlebot`/`bingbot` meta, or `X-Robots-Tag`; flags a `noindex` that `robots.txt` hides from crawlers | Actual indexing, which needs Search Console |
| Canonical | Missing, conflicting, or pointing to another URL | Which canonical Google selected |
| Metadata and headings | Missing or generic title and description, missing `<h1>`, missing `lang` | Whether the copy is accurate or persuasive |
| Content without JavaScript | Visible raw-HTML word count; with scripts present and few words, a **risk** | The rendered page; compare it in a browser |
| Links and discovery | `<a href>` links among the checked pages, click-handler navigation, sitemap listing. An intended page that is neither linked nor in a sitemap fails. | Links from pages you did not pass in |
| Social previews | `og:title`, `og:description`, `og:image` (fetched), `og:url`, `twitter:card` | How each platform renders the card |
| Structured data | JSON-LD parses; lists declared types | Eligibility for rich results, or match with visible content |
| `hreflang` | Each alternate returns 200 and links back | Correct language/region codes |
| Sitemap | Declared or `/sitemap.xml`, gzip and one level of index; samples entries for non-200, redirects and `noindex`; excluded URLs listed | Every entry on a large site; a missing sitemap is information, not a failure |
| Exclusions | Excluded URLs return 401/403/404/410 or a readable `noindex`; `robots.txt`-only blocks are a risk | Access control strength |
| Crawl (`--crawl`) | Broken internal links (fail), internal links that redirect, pages without a title, duplicate titles among indexable pages, linked `noindex` and canonical-elsewhere pages, indexable pages missing from their host's sitemap, and orphan sitemap URLs (only when the crawl reached every linked page) | Pages not linked from the start URLs; JavaScript-only links |
| Core Web Vitals (`--psi`) | Chrome UX Report p75 for LCP, INP and CLS, rated good / needs improvement / poor (any poor fails, any needs-improvement is a risk), falling back to origin data and saying so; plus one Lighthouse lab run as information | Lab numbers are not field data; no field data is `not_tested` |

Results are `fail`, `risk`, `pass`, `info`, or `not_tested`. Search Console data and AI citations are always `not_tested`; Core Web Vitals are `not_tested` unless `--psi` returns field data.
