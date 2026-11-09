#!/usr/bin/env python3
"""Mechanical search and answer-engine checks for public URLs.

Fetches each URL once as a plain HTTP client (no JavaScript), reads robots.txt
and sitemaps for its origin, and reports pass / fail / risk / info / not_tested
results with evidence. It does not prove indexing, rankings, or citations:
judgement checks (answer quality, owner intent) are left to the reviewer.
Standard library only.
"""

import argparse
import gzip
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

USER_AGENT = "search-answer-readiness-checker/1.0 (+https://github.com/teelda/ui-design-engineer)"
MAX_BYTES = 5 * 1024 * 1024
RESULTS = ("fail", "risk", "pass", "info", "not_tested")

# (robots.txt token, purpose). Names change; check vendor docs before relying on them.
CRAWLERS = (
    ("Googlebot", "search"),
    ("Bingbot", "search"),
    ("OAI-SearchBot", "ai-search"),
    ("Claude-SearchBot", "ai-search"),
    ("PerplexityBot", "ai-search"),
    ("GPTBot", "training"),
    ("ClaudeBot", "training"),
    ("Google-Extended", "control-token"),
    ("ChatGPT-User", "user-triggered"),
    ("Claude-User", "user-triggered"),
    ("Perplexity-User", "user-triggered"),
)
GENERIC_TITLES = {"home", "homepage", "index", "untitled", "welcome", "page", "document", "react app", "vite app"}
GENERIC_DESCRIPTION = re.compile(r"^\s*(welcome to (our|my|the) (website|site|page)|this is (our|my|the) (website|site))\b", re.I)
CLICK_NAV = re.compile(r"(location\.(href|assign|replace)|window\.open|router\.push|navigate\()", re.I)


# ---------------------------------------------------------------- fetching

class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


class Response:
    def __init__(self, url):
        self.url = url
        self.final_url = url
        self.status = None
        self.headers = {}
        self.body = b""
        self.chain = []
        self.error = None

    @property
    def text(self):
        match = re.search(r"charset=([\w-]+)", self.headers.get("content-type", ""), re.I)
        try:
            return self.body.decode(match.group(1) if match else "utf-8", errors="replace")
        except LookupError:
            return self.body.decode("utf-8", errors="replace")


def fetch(url, timeout, cache, max_redirects=10):
    if url in cache:
        return cache[url]
    response = Response(url)
    current = url
    for _ in range(max_redirects + 1):
        request = urllib.request.Request(current, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "identity"})
        try:
            raw = _OPENER.open(request, timeout=timeout)
            status, headers = raw.status, raw.headers
        except urllib.error.HTTPError as error:
            raw, status, headers = error, error.code, error.headers
        except (urllib.error.URLError, OSError, ValueError) as error:
            response.error = str(getattr(error, "reason", error))
            break
        lowered = {key.lower(): value for key, value in headers.items()}
        if 300 <= status < 400 and lowered.get("location"):
            response.chain.append((status, current))
            current = urllib.parse.urljoin(current, lowered["location"])
            continue
        response.status, response.headers, response.final_url = status, lowered, current
        try:
            response.body = raw.read(MAX_BYTES + 1)[:MAX_BYTES]
        except OSError as error:
            response.error = str(error)
        break
    else:
        response.error = f"more than {max_redirects} redirects"
    cache[url] = response
    return response


# ---------------------------------------------------------------- robots.txt

def parse_robots(text):
    """Return (groups, sitemaps). Each group is (agents, [(allow, pattern)])."""
    groups, sitemaps, current, last_was_agent = [], [], None, False
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        key = key.lower()
        if key == "user-agent":
            if current is None or not last_was_agent:
                current = ([], [])
                groups.append(current)
            current[0].append(value.lower())
            last_was_agent = True
            continue
        last_was_agent = False
        if key == "sitemap" and value:
            sitemaps.append(value)
        elif key in ("allow", "disallow") and current is not None and value:
            current[1].append((key == "allow", value))
    return groups, sitemaps


def _pattern_matches(pattern, path):
    anchored = pattern.endswith("$")
    body = pattern[:-1] if anchored else pattern
    regex = "^" + ".*".join(re.escape(part) for part in body.split("*")) + ("$" if anchored else "")
    return re.match(regex, path) is not None


def robots_allows(groups, agent, path):
    """RFC 9309 matching: specific group over '*', longest rule wins, allow wins ties."""
    token = agent.lower()
    rules = [rule for agents, rules_ in groups if token in agents for rule in rules_]
    if not any(token in agents for agents, _ in groups):
        rules = [rule for agents, rules_ in groups if "*" in agents for rule in rules_]
    best = None
    for allow, pattern in rules:
        if _pattern_matches(pattern, path):
            key = (len(pattern), allow)
            if best is None or key > best[0]:
                best = (key, allow, pattern)
    return (True, None) if best is None else (best[1], best[2])


# ---------------------------------------------------------------- HTML

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.lang = None, None
        self.meta = {}
        self.canonicals, self.hreflang, self.links, self.json_ld = [], [], [], []
        self.click_nav = 0
        self.h1 = 0
        self.scripts = 0
        self.words = 0
        self._stack = []
        self._in_title = False
        self._title_parts = []
        self._json_ld = None

    def handle_starttag(self, tag, attrs):
        attrs = {key.lower(): (value or "") for key, value in attrs}
        if tag == "html":
            self.lang = attrs.get("lang") or None
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = (attrs.get("name") or attrs.get("property") or "").lower()
            if name:
                self.meta.setdefault(name, attrs.get("content", ""))
        elif tag == "link":
            rel = attrs.get("rel", "").lower().split()
            if "canonical" in rel:
                self.canonicals.append(attrs.get("href", ""))
            if "alternate" in rel and attrs.get("hreflang"):
                self.hreflang.append((attrs["hreflang"].lower(), attrs.get("href", "")))
        elif tag == "a" and attrs.get("href") and not attrs["href"].lower().startswith(("javascript:", "#")):
            self.links.append(attrs["href"])
        elif tag == "h1":
            self.h1 += 1
        elif tag == "script":
            self.scripts += 1
            if attrs.get("type", "").lower() == "application/ld+json":
                self._json_ld = []
        if any(CLICK_NAV.search(value) for key, value in attrs.items() if key.startswith("on")):
            self.click_nav += 1
        if tag in ("script", "style", "noscript", "template"):
            self._stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
            self.title = " ".join("".join(self._title_parts).split())
        elif tag == "script" and self._json_ld is not None:
            self.json_ld.append("".join(self._json_ld))
            self._json_ld = None
        if self._stack and self._stack[-1] == tag:
            self._stack.pop()

    def handle_data(self, data):
        if self._in_title:
            self._title_parts.append(data)
        elif self._json_ld is not None:
            self._json_ld.append(data)
        elif not self._stack:
            self.words += len(data.split())


def parse_page(text):
    parser = PageParser()
    parser.feed(text)
    parser.close()
    return parser


def robots_directives(response, page):
    """Return noindex/nofollow directives that apply to all crawlers or to Googlebot/Bingbot."""
    values = [response.headers.get("x-robots-tag", "")]
    if page:
        values += [page.meta.get(name, "") for name in ("robots", "googlebot", "bingbot")]
    found = set()
    for value in values:
        for part in value.lower().split(","):
            part = part.strip()
            if ":" in part:
                prefix, rest = (piece.strip() for piece in part.split(":", 1))
                if prefix not in ("googlebot", "bingbot"):
                    continue  # another crawler's rule, or max-snippet / unavailable_after
                part = rest
            if part in ("noindex", "none"):
                found.add("noindex")
            elif part == "nofollow":
                found.add("nofollow")
    return found


def normalise(url):
    parts = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path or "/", parts.query, ""))


def robots_path(url):
    parts = urllib.parse.urlsplit(url)
    return (parts.path or "/") + (f"?{parts.query}" if parts.query else "")


# ---------------------------------------------------------------- checks

class Report:
    def __init__(self):
        self.findings = []

    def add(self, page, check, result, detail):
        self.findings.append({"page": page, "check": check, "result": result, "detail": detail})


def load_robots(origin, timeout, cache, report):
    response = fetch(origin + "/robots.txt", timeout, cache)
    if response.error:
        report.add(origin, "robots.txt", "not_tested", f"could not fetch robots.txt: {response.error}")
        return [], [], "unreachable"
    if response.status >= 500:
        report.add(origin, "robots.txt", "fail", f"robots.txt returned {response.status}; Google treats a server error as a full block until it recovers")
        return [(["*"], [(False, "/")])], [], "error"
    if response.status >= 400:
        report.add(origin, "robots.txt", "info", f"no robots.txt ({response.status}); every crawler is allowed by default")
        return [], [], "missing"
    groups, sitemaps = parse_robots(response.text)
    report.add(origin, "robots.txt", "pass", f"fetched ({len(groups)} group(s), {len(sitemaps)} sitemap line(s))")
    return groups, sitemaps, "ok"


def load_sitemaps(origin, declared, timeout, cache, report, limit=5):
    candidates = declared or [origin + "/sitemap.xml"]
    urls, found, queue, seen = set(), [], list(candidates), set()
    while queue and len(seen) < limit:
        location = queue.pop(0)
        if location in seen:
            continue
        seen.add(location)
        response = fetch(location, timeout, cache)
        if response.error or response.status != 200:
            if declared:
                report.add(origin, "sitemap", "fail", f"declared sitemap {location} returned {response.status or response.error}")
            continue
        body = response.body
        if body[:2] == b"\x1f\x8b":
            try:
                body = gzip.decompress(body)[:MAX_BYTES * 4]
            except OSError:
                report.add(origin, "sitemap", "fail", f"{location} is not valid gzip")
                continue
        try:
            root = ET.fromstring(body)
        except ET.ParseError as error:
            report.add(origin, "sitemap", "fail", f"{location} is not valid XML: {error}")
            continue
        found.append(location)
        locs = [el.text.strip() for el in root.iter() if el.tag.endswith("loc") and el.text]
        if root.tag.endswith("sitemapindex"):
            queue.extend(locs)
        else:
            urls.update(normalise(loc) for loc in locs)
    return found, urls


def check_page(url, args, cache, report, robots, page_data):
    response = fetch(url, args.timeout, cache)
    if response.error:
        report.add(url, "fetch", "fail", f"could not fetch: {response.error}")
        return
    chain = " -> ".join(f"{s} {u}" for s, u in response.chain)
    if response.chain:
        def site(u):
            host = urllib.parse.urlsplit(u).netloc.lower()
            return host[4:] if host.startswith("www.") else host
        same = site(response.final_url) == site(url)
        result = "info" if same and len(response.chain) == 1 else "risk"
        report.add(url, "redirects", result, f"{chain} -> {response.status} {response.final_url}")
    if response.status != 200:
        report.add(url, "status", "fail", f"intended page returned {response.status}")
        return
    report.add(url, "status", "pass", f"200 at {response.final_url}")

    groups = robots.get(origin_of(response.final_url), [])
    path = robots_path(response.final_url)
    blocked_for = {}
    for agent, purpose in CRAWLERS:
        allowed, rule = robots_allows(groups, agent, path)
        if not allowed:
            blocked_for[agent] = (purpose, rule)
    for agent in ("Googlebot", "Bingbot"):
        if agent in blocked_for:
            report.add(url, "crawl access", "fail", f"robots.txt blocks {agent} (rule: Disallow {blocked_for[agent][1]})")
    if not any(a in blocked_for for a in ("Googlebot", "Bingbot")):
        report.add(url, "crawl access", "pass", "Googlebot and Bingbot are allowed by robots.txt")
    by_purpose = {}
    for agent, (purpose, _) in blocked_for.items():
        by_purpose.setdefault(purpose, []).append(agent)
    if by_purpose.get("ai-search"):
        report.add(url, "AI crawler access", "risk", f"blocked for AI search crawlers {', '.join(by_purpose['ai-search'])}; fine only if the owner intends it")
    if by_purpose.get("training"):
        report.add(url, "AI crawler access", "info", f"blocked for training crawlers {', '.join(by_purpose['training'])}; an owner choice that does not remove the page from AI search")
    if by_purpose.get("control-token"):
        report.add(url, "AI crawler access", "info", "Google-Extended is disallowed: limits Gemini model use, not Google Search or AI Overviews")
    if by_purpose.get("user-triggered"):
        report.add(url, "AI crawler access", "info", f"robots.txt disallows {', '.join(by_purpose['user-triggered'])}, but vendors say robots.txt may not apply to user-triggered visits")
    if not by_purpose.get("ai-search"):
        report.add(url, "AI crawler access", "pass", "AI search crawlers in the checked list are allowed by robots.txt (firewall rules not tested)")

    is_html = "html" in response.headers.get("content-type", "html")
    page = parse_page(response.text) if is_html else None
    directives = robots_directives(response, page)
    if "noindex" in directives:
        message = "page is marked noindex (meta robots or X-Robots-Tag)"
        if "Googlebot" in blocked_for:
            message += "; robots.txt also blocks it, so crawlers cannot read the noindex — allow crawling or drop the noindex, not both"
        report.add(url, "indexing", "fail", message)
    if page is None:
        report.add(url, "content", "info", f"not HTML ({response.headers.get('content-type')}); HTML checks skipped")
        return

    page_data[normalise(response.final_url)] = page
    final = normalise(response.final_url)
    canonicals = [normalise(urllib.parse.urljoin(response.final_url, c)) for c in page.canonicals if c]
    if len(set(canonicals)) > 1:
        report.add(url, "canonical", "fail", f"conflicting canonicals: {', '.join(sorted(set(canonicals)))}")
    elif canonicals and canonicals[0] != final:
        report.add(url, "canonical", "fail", f"canonical points to {canonicals[0]}, so this page asks to be replaced by it")
    elif canonicals:
        report.add(url, "canonical", "pass", "self-referencing canonical")
    else:
        report.add(url, "canonical", "info", "no canonical link; search engines will choose one")
    if "noindex" not in directives and "Googlebot" not in blocked_for and (not canonicals or canonicals[0] == final):
        report.add(url, "indexing", "pass", "eligible to be indexed (status, robots and canonical); actual indexing not tested without Search Console")

    title = page.title or ""
    if not title:
        report.add(url, "metadata", "fail", "missing <title>")
    elif title.lower() in GENERIC_TITLES or len(title) < 5:
        report.add(url, "metadata", "risk", f"generic or very short title: \"{title}\"")
    else:
        report.add(url, "metadata", "pass", f"title: \"{title}\"")
    description = page.meta.get("description", "").strip()
    if not description:
        report.add(url, "metadata", "risk", "no meta description; engines will write their own snippet")
    elif GENERIC_DESCRIPTION.search(description) or len(description) < 50:
        report.add(url, "metadata", "risk", f"generic or very short description: \"{description}\"")
    if page.h1 == 0:
        report.add(url, "headings", "risk", "no <h1> in the raw HTML")
    if not page.lang:
        report.add(url, "language", "info", "no lang attribute on <html>")

    if page.words < args.min_words and page.scripts:
        report.add(url, "content without JavaScript", "risk", f"{page.words} words of visible text in the raw HTML and {page.scripts} script(s): main content may need JavaScript. Google renders JavaScript; other engines may not. Compare with the rendered page")
    elif page.words < args.min_words:
        report.add(url, "content without JavaScript", "info", f"only {page.words} words of visible text and no scripts: a short page, not a rendering problem")
    else:
        report.add(url, "content without JavaScript", "pass", f"{page.words} words of visible text in the raw HTML")
    if page.click_nav:
        report.add(url, "links", "risk", f"{page.click_nav} element(s) navigate with a click handler instead of <a href>; crawlers cannot follow them")

    og = {key: page.meta.get(key, "").strip() for key in ("og:title", "og:description", "og:image", "og:url", "twitter:card")}
    missing = [key for key, value in og.items() if not value]
    if missing:
        report.add(url, "social previews", "risk", f"missing {', '.join(missing)}")
    if og["og:image"]:
        image_url = urllib.parse.urljoin(response.final_url, og["og:image"])
        if not urllib.parse.urlsplit(og["og:image"]).scheme:
            report.add(url, "social previews", "risk", "og:image is a relative URL; most platforms need an absolute one")
        image = fetch(image_url, args.timeout, cache)
        if image.error or image.status != 200:
            report.add(url, "social previews", "fail", f"og:image {image_url} returned {image.status or image.error}")
    if not missing and og["og:image"]:
        report.add(url, "social previews", "pass", "Open Graph and Twitter card tags present")

    for block in page.json_ld:
        try:
            data = json.loads(block)
        except ValueError as error:
            report.add(url, "structured data", "fail", f"invalid JSON-LD: {error}")
            continue
        items = data if isinstance(data, list) else data.get("@graph", [data]) if isinstance(data, dict) else []
        types = sorted({str(item.get("@type")) for item in items if isinstance(item, dict) and item.get("@type")})
        report.add(url, "structured data", "info", f"JSON-LD types: {', '.join(types) or 'none declared'}; check it matches visible content")

    if page.hreflang:
        for lang, href in page.hreflang:
            target = normalise(urllib.parse.urljoin(response.final_url, href))
            alternate = fetch(target, args.timeout, cache)
            if alternate.status != 200:
                report.add(url, "hreflang", "fail", f"{lang} alternate {target} returned {alternate.status or alternate.error}")
                continue
            back = parse_page(alternate.text).hreflang
            if final not in {normalise(urllib.parse.urljoin(alternate.final_url, h)) for _, h in back}:
                report.add(url, "hreflang", "fail", f"{lang} alternate {target} does not link back to this page")


def origin_of(url):
    parts = urllib.parse.urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}"


def check_excluded(url, args, cache, report, robots):
    response = fetch(url, args.timeout, cache)
    if response.error:
        report.add(url, "exclusion", "not_tested", f"could not fetch: {response.error}")
        return
    if response.status in (401, 403, 404, 410):
        report.add(url, "exclusion", "pass", f"returns {response.status}")
        return
    page = parse_page(response.text) if "html" in response.headers.get("content-type", "html") else None
    if "noindex" in robots_directives(response, page):
        allowed, _ = robots_allows(robots.get(origin_of(response.final_url), []), "Googlebot", robots_path(response.final_url))
        if not allowed:
            report.add(url, "exclusion", "fail", "noindex is set but robots.txt blocks crawling, so the noindex cannot be read")
        else:
            report.add(url, "exclusion", "pass", "noindex is set and crawlable")
        return
    allowed, _ = robots_allows(robots.get(origin_of(response.final_url), []), "Googlebot", robots_path(response.final_url))
    if not allowed:
        report.add(url, "exclusion", "risk", "blocked by robots.txt only; the URL can still be indexed without its content. Use noindex or authentication")
    else:
        report.add(url, "exclusion", "fail", f"returns {response.status}, is crawlable and has no noindex: it can be indexed")


def run(urls, excluded, args):
    report, cache, robots, sitemap_urls, page_data = Report(), {}, {}, {}, {}
    # robots.txt and sitemaps belong to the host that actually serves each page,
    # which may differ from the requested one (for example apex -> www).
    origins = {origin_of(u) for u in urls + excluded}
    origins |= {origin_of(fetch(u, args.timeout, cache).final_url) for u in urls + excluded}
    for origin in sorted(origins):
        groups, declared, _ = load_robots(origin, args.timeout, cache, report)
        robots[origin] = groups
        found, listed = load_sitemaps(origin, declared, args.timeout, cache, report)
        sitemap_urls[origin] = listed
        if found:
            report.add(origin, "sitemap", "pass", f"{len(listed)} URL(s) in {', '.join(found)}")
        else:
            report.add(origin, "sitemap", "info", "no sitemap found; only a problem if intended pages are not reachable through links")
    for url in urls:
        check_page(url, args, cache, report, robots, page_data)
    for url in excluded:
        check_excluded(url, args, cache, report, robots)

    linked = set()
    for source, page in page_data.items():
        for href in page.links:
            target = normalise(urllib.parse.urljoin(source, href))
            if target != source:
                linked.add(target)
    all_listed = set().union(*sitemap_urls.values()) if sitemap_urls else set()
    for url in urls:
        target = normalise(fetch(url, args.timeout, cache).final_url)
        in_sitemap = target in all_listed
        is_root = urllib.parse.urlsplit(target).path == "/"
        if is_root or target in linked:
            report.add(url, "discovery", "pass", "linked with <a href> from a checked page" if target in linked else "site root")
        elif in_sitemap:
            report.add(url, "discovery", "pass", "listed in the sitemap (no <a href> link found among checked pages)")
        else:
            report.add(url, "discovery", "fail", "not linked with <a href> from any checked page and not in a sitemap; crawlers may never find it")
    for origin, listed in sitemap_urls.items():
        for url in excluded:
            if normalise(url) in listed:
                report.add(url, "sitemap", "fail", "excluded URL is listed in the sitemap")
        for url in sorted(listed)[: args.sitemap_sample]:
            response = fetch(url, args.timeout, cache)
            if response.error or response.status != 200 or response.chain:
                report.add(url, "sitemap entry", "fail", f"listed in sitemap but returns {response.status or response.error}" + (" after a redirect" if response.chain else ""))
            elif "noindex" in robots_directives(response, parse_page(response.text)):
                report.add(url, "sitemap entry", "fail", "listed in sitemap but marked noindex")
    report.add("all pages", "Search Console", "not_tested", "actual indexing, Core Web Vitals field data and AI citations need owner access or repeated observation")
    return report


def print_text(report):
    order = {result: index for index, result in enumerate(RESULTS)}
    current = None
    for item in sorted(report.findings, key=lambda f: (f["page"], order[f["result"]])):
        if item["page"] != current:
            current = item["page"]
            print(f"\n{current}")
        print(f"  {item['result'].upper():<10} {item['check']}: {item['detail']}")
    counts = {r: sum(1 for f in report.findings if f["result"] == r) for r in RESULTS}
    print("\n" + ", ".join(f"{n} {r}" for r, n in counts.items() if n) + ". Raw-HTML checks only; review judgement items and owner intent separately.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("urls", nargs="+", help="intended public, indexable URLs")
    parser.add_argument("--exclude", nargs="*", default=[], help="URLs that should stay out of search")
    parser.add_argument("--json", action="store_true", help="print findings as JSON")
    parser.add_argument("--strict", action="store_true", help="exit 1 when any check fails")
    parser.add_argument("--timeout", type=float, default=15)
    parser.add_argument("--min-words", type=int, default=50, help="raw-HTML word count below which content may need JavaScript")
    parser.add_argument("--sitemap-sample", type=int, default=25, help="how many sitemap entries to fetch and check")
    args = parser.parse_args(argv)
    for url in args.urls + args.exclude:
        if urllib.parse.urlsplit(url).scheme not in ("http", "https"):
            parser.error(f"not an http(s) URL: {url}")
    report = run(args.urls, args.exclude, args)
    if args.json:
        print(json.dumps(report.findings, indent=2))
    else:
        print_text(report)
    return 1 if args.strict and any(f["result"] == "fail" for f in report.findings) else 0


if __name__ == "__main__":
    sys.exit(main())
