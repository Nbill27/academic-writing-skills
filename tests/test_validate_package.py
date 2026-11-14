import unittest
from scripts.validate_package import local_link_targets, parse_frontmatter


class ValidatorTests(unittest.TestCase):
    def test_frontmatter(self):
        parsed = parse_frontmatter('---\nname: outline\ndescription: "A skill"\n---\nbody')
        self.assertEqual(parsed["name"], "outline")
        self.assertEqual(parsed["description"], "A skill")

    def test_missing_frontmatter(self):
        self.assertEqual(parse_frontmatter("# no frontmatter"), {})

    def test_local_links_skip_external_and_anchors(self):
        text = "[local](refs/a.md) [external](https://example.com) [anchor](#x)"
        self.assertEqual(list(local_link_targets(text)), ["refs/a.md"])


if __name__ == "__main__":
    unittest.main()
