import unittest
from pathlib import Path


SKILLS = Path(__file__).resolve().parents[1] / "skills"
SHARED = ("design-principles.md", "audit-deliverable.md")
OWNERS = ("ui-design-engineer", "senior-product-experience-auditor")


class SharedReferenceTests(unittest.TestCase):
    """Both skills bundle the same references so each works when installed alone; the copies must not drift."""

    def test_bundled_copies_are_identical(self):
        for name in SHARED:
            copies = [(SKILLS / owner / "references" / name).read_bytes() for owner in OWNERS]
            self.assertEqual(copies[0], copies[1], f"{name} differs between {OWNERS[0]} and {OWNERS[1]}")


if __name__ == "__main__":
    unittest.main()
