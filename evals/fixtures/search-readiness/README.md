# Search-readiness fixture

Assume `/` and `/guide/` are intended public, indexable pages. `/dashboard/` is private and should stay out of search. Serve this folder from its root with `python3 -m http.server 8765`, then review `http://localhost:8765/` using the search reference. No Search Console access is supplied, so actual indexing must be marked **not tested**.

Known issues to find: the guide is blocked by `robots.txt` and marked `noindex`; the homepage uses generic metadata and an unrelated canonical; its guide navigation has no crawlable `href`; the guide's primary text is added only by JavaScript. Rendering that text in a browser does not establish indexing. Keep private dashboard exclusion intentional. Record evidence and fixes rather than a score.
