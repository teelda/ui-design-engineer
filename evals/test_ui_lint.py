import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "skill/scripts/ui_lint.py"
spec = importlib.util.spec_from_file_location("ui_lint", SCRIPT)
ui_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ui_lint)


class UiLintTests(unittest.TestCase):
    def inspect(self, filename, source):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / filename
            path.write_text(source, encoding="utf-8")
            return [kind for _, kind, _ in ui_lint.inspect(path)]

    def test_flags_review_candidates(self):
        kinds = self.inspect("page.html", """<style>
          .cta { color: #777; background-color: #fff; font-size: 18px; font-weight: 700;
                 background-image: linear-gradient(red, blue); transition: all .2s; outline: none; }
        </style><input placeholder="Email">""")
        self.assertEqual(set(kinds), {"contrast", "gradient", "transition-all", "outline-removed", "placeholder-label"})

    def test_large_text_threshold_and_real_label(self):
        kinds = self.inspect("page.html", """<style>
          .title { color: #777; background-color: #fff; font-size: 24px; }
        </style><label for="email">Email</label><input id="email" placeholder="name@example.com">""")
        self.assertNotIn("contrast", kinds)
        self.assertNotIn("placeholder-label", kinds)

    def test_unresolved_colors_are_not_claimed_as_failures(self):
        kinds = self.inspect("theme.css", ".body { color: var(--text); background-color: var(--surface); }")
        self.assertNotIn("contrast", kinds)


if __name__ == "__main__":
    unittest.main()
