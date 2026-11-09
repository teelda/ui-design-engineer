import functools
import importlib.util
import threading
import unittest
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/search-answer-readiness/scripts/search_check.py"
FIXTURE = ROOT / "evals/fixtures/search-readiness"
spec = importlib.util.spec_from_file_location("search_check", SCRIPT)
search_check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(search_check)


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class RobotsMatchingTests(unittest.TestCase):
    def allowed(self, robots, agent, path):
        groups, _ = search_check.parse_robots(robots)
        return search_check.robots_allows(groups, agent, path)[0]

    def test_specific_group_replaces_wildcard_group(self):
        robots = "User-agent: *\nDisallow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n"
        self.assertTrue(self.allowed(robots, "OAI-SearchBot", "/guide/"))
        self.assertFalse(self.allowed(robots, "GPTBot", "/guide/"))

    def test_longest_rule_wins_and_allow_wins_ties(self):
        robots = "User-agent: *\nDisallow: /docs/\nAllow: /docs/public/\nDisallow: /a\nAllow: /a\n"
        self.assertTrue(self.allowed(robots, "Googlebot", "/docs/public/page"))
        self.assertFalse(self.allowed(robots, "Googlebot", "/docs/private"))
        self.assertTrue(self.allowed(robots, "Googlebot", "/a"))

    def test_wildcards_and_end_anchor(self):
        robots = "User-agent: *\nDisallow: /*.pdf$\nDisallow: /*?session=\n"
        self.assertFalse(self.allowed(robots, "Googlebot", "/files/report.pdf"))
        self.assertTrue(self.allowed(robots, "Googlebot", "/files/report.pdf?v=2"))
        self.assertFalse(self.allowed(robots, "Googlebot", "/cart?session=1"))

    def test_grouped_user_agents_and_empty_disallow(self):
        robots = "User-agent: GPTBot\nUser-agent: ClaudeBot\nDisallow: /\n\nUser-agent: *\nDisallow:\n"
        self.assertFalse(self.allowed(robots, "ClaudeBot", "/"))
        self.assertTrue(self.allowed(robots, "Googlebot", "/"))


class DirectiveTests(unittest.TestCase):
    def directives(self, header="", html=""):
        response = SimpleNamespace(headers={"x-robots-tag": header} if header else {})
        return search_check.robots_directives(response, search_check.parse_page(html))

    def test_meta_and_header_noindex(self):
        self.assertIn("noindex", self.directives(html='<meta name="robots" content="noindex, follow">'))
        self.assertIn("noindex", self.directives(header="googlebot: noindex"))
        self.assertIn("noindex", self.directives(header="none"))

    def test_other_crawler_and_snippet_rules_are_ignored(self):
        self.assertEqual(set(), self.directives(header="otherbot: noindex, max-snippet: 20"))


class FixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        handler = functools.partial(QuietHandler, directory=str(FIXTURE))
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{cls.server.server_address[1]}"
        args = SimpleNamespace(timeout=5, min_words=50, sitemap_sample=25)
        cls.home, cls.guide, cls.dashboard = base + "/", base + "/guide/", base + "/dashboard/"
        cls.findings = search_check.run([cls.home, cls.guide], [cls.dashboard], args).findings

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def results(self, page, check):
        return [f["result"] for f in self.findings if f["page"] == page and f["check"] == check]

    def detail(self, page, check):
        return " ".join(f["detail"] for f in self.findings if f["page"] == page and f["check"] == check)

    def test_guide_is_blocked_and_noindex_cannot_be_read(self):
        self.assertIn("fail", self.results(self.guide, "crawl access"))
        self.assertIn("fail", self.results(self.guide, "indexing"))
        self.assertIn("cannot read the noindex", self.detail(self.guide, "indexing"))

    def test_guide_content_needs_javascript_is_a_risk_not_a_failure(self):
        self.assertEqual(["risk"], self.results(self.guide, "content without JavaScript"))

    def test_guide_is_not_discoverable(self):
        self.assertEqual(["fail"], self.results(self.guide, "discovery"))

    def test_home_canonical_metadata_and_click_navigation(self):
        self.assertEqual(["fail"], self.results(self.home, "canonical"))
        self.assertIn("pricing", self.detail(self.home, "canonical"))
        self.assertIn("risk", self.results(self.home, "metadata"))
        self.assertEqual(["risk"], self.results(self.home, "links"))
        self.assertNotIn("pass", self.results(self.home, "indexing"))

    def test_private_dashboard_is_excluded(self):
        self.assertEqual(["pass"], self.results(self.dashboard, "exclusion"))

    def test_missing_sitemap_is_info_and_indexing_is_not_claimed(self):
        origin = self.home.rstrip("/")
        self.assertEqual(["info"], self.results(origin, "sitemap"))
        self.assertEqual(["not_tested"], self.results("all pages", "Search Console"))


class CrossHostRedirectTests(unittest.TestCase):
    """A redirect to another host must use that host's robots.txt and sitemap."""

    def test_rules_come_from_the_serving_host(self):
        class Target(QuietHandler):
            def do_GET(self):
                bodies = {
                    "/robots.txt": (b"User-agent: *\nDisallow: /\n", "text/plain"),
                    "/": (b"<html lang='en'><title>Target home page</title><h1>Hi</h1></html>", "text/html"),
                }
                body, kind = bodies.get(self.path, (b"", "text/plain"))
                self.send_response(200 if self.path in bodies else 404)
                self.send_header("Content-Type", kind)
                self.end_headers()
                self.wfile.write(body)

        target = ThreadingHTTPServer(("127.0.0.1", 0), Target)
        target_url = f"http://127.0.0.1:{target.server_address[1]}/"

        class Source(QuietHandler):
            def do_GET(self):
                if self.path == "/":
                    self.send_response(301)
                    self.send_header("Location", target_url)
                else:
                    self.send_response(404)
                self.end_headers()

        source = ThreadingHTTPServer(("127.0.0.1", 0), Source)
        for server in (target, source):
            threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            source_url = f"http://127.0.0.1:{source.server_address[1]}/"
            args = SimpleNamespace(timeout=5, min_words=50, sitemap_sample=5)
            findings = search_check.run([source_url], [], args).findings
            crawl = [f["result"] for f in findings if f["page"] == source_url and f["check"] == "crawl access"]
            self.assertIn("fail", crawl)
        finally:
            for server in (target, source):
                server.shutdown()
                server.server_close()


if __name__ == "__main__":
    unittest.main()
