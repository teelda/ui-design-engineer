import unittest
from pathlib import Path


SKILLS = Path(__file__).resolve().parents[1] / "skills"
SHARED = ("design-principles.md", "house-bar.md")
OWNERS = ("ui-design-engineer", "senior-product-experience-auditor")


class SharedReferenceTests(unittest.TestCase):
    """Both skills bundle the same references so each works when installed alone; the copies must not drift."""

    def test_bundled_copies_are_identical(self):
        for name in SHARED:
            copies = [(SKILLS / owner / "references" / name).read_bytes() for owner in OWNERS]
            self.assertEqual(copies[0], copies[1], f"{name} differs between {OWNERS[0]} and {OWNERS[1]}")

    def test_house_bar_is_linked_from_both_skills(self):
        for owner in OWNERS:
            self.assertIn("references/house-bar.md", (SKILLS / owner / "SKILL.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
