import importlib.util
import subprocess
import sys
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

    def test_jsx_names_and_tailwind_candidates(self):
        kinds = self.inspect("Form.tsx", """<label>Name<input placeholder={hint} /></label>
          <input placeholder={hint} aria-labelledby="missing" />
          <input placeholder={hint} aria-label={name} />
          <div className="bg-gradient-to-r transition-all outline-none" />""")
        self.assertEqual(kinds.count("placeholder-label"), 0)
        self.assertEqual(kinds.count("label-unresolved"), 2)
        self.assertIn("gradient", kinds)

    def test_comments_and_reasoned_suppression(self):
        kinds = self.inspect("style.css", """/* .bad { color: #777; background: #fff; } */
          /* ui-lint: ok gradient -- existing brand hero */
          .hero { background: linear-gradient(red, blue); }
          .text { color: #777; background: #fff; }""")
        self.assertEqual(kinds, ["contrast"])

    def test_cli_rejects_missing_and_empty_inputs(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for path in (root / "missing", root):
                result = subprocess.run([sys.executable, str(SCRIPT), "--strict", str(path)], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("error:", result.stderr)
            result = subprocess.run([sys.executable, str(SCRIPT), "--allow-empty", str(root)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertIn("0 file(s)", result.stdout)

    def test_directory_excludes_generated_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "app.css").write_text(".ok { color: #000; background: #fff; }")
            (root / "node_modules").mkdir()
            (root / "node_modules" / "bad.css").write_text(".bad { color: #777; background: #fff; }")
            self.assertEqual(ui_lint.collect_files([root]), [root / "app.css"])

    def test_contrast_location_and_suppression_after_another_rule(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "rules.css"
            path.write_text(".first {color: #000;}\n/* ui-lint: ok contrast -- reviewed example */\n.second {color: #aaa; background: #fff;}\n")
            self.assertEqual(ui_lint.inspect(path), [])
            path.write_text(".first {color: #000;}\n/* no suppression */\n.second {color: #aaa; background: #fff;}\n")
            self.assertEqual([(line, kind) for line, kind, _ in ui_lint.inspect(path)], [(3, "contrast")])

    def test_data_id_and_empty_wrapping_label(self):
        kinds = self.inspect("fields.html", """<span data-id="email-label">Email</span>
          <input placeholder="Email" aria-labelledby="email-label">
          <label><input placeholder="Email"></label>""")
        self.assertEqual(kinds.count("label-unresolved"), 2)

    def test_html_and_trailing_scss_comments_are_ignored(self):
        kinds = self.inspect("page.html", "<!-- <input placeholder='Email'> -->")
        self.assertEqual(kinds, [])
        kinds = self.inspect("style.scss", ".ok { color: #000; } // transition-all should not count")
        self.assertEqual(kinds, [])


if __name__ == "__main__":
    unittest.main()
