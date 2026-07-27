import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
PILLAR_SHA256 = {
    "services": "9f33638ecf0c196e6eab0a22ef819465159bcf8acbb5198f4363ce1974cf8bbd",
    "business-growth-systems": "e3183c2547628f061048daac04d723d0db077a642e58e6c29ac825a66f3ea389",
    "ai-creative-studio": "06e48b46fd4e35cf974181c0a52fb9060869f380f5a0eadcebfce43827dadcd5",
}


def homepage_sections(source):
    match = re.search(r"<main\b[^>]*>(.*?)</main\s*>", source, re.I | re.S)
    if not match:
        raise AssertionError("Missing homepage <main>")
    return re.findall(r'^    <section\b[^>]*\bid="([^"]+)"', match.group(1), re.M)


def section_source(source, section_id):
    match = re.search(
        rf'(?ms)^    <section\b[^>]*\bid="{re.escape(section_id)}"[^>]*>.*?^    </section>\n?',
        source,
    )
    if not match:
        raise AssertionError(f"Missing section #{section_id}")
    return match.group(0)


class HomepageInformationArchitectureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = HOME.read_text(encoding="utf-8")

    def test_one_business_system_chapter_precedes_three_consecutive_pillars(self):
        self.assertEqual(
            homepage_sections(self.home),
            [
                "hero",
                "what-we-do",
                "services",
                "business-growth-systems",
                "ai-creative-studio",
                "production-readiness",
                "why-aics",
                "evidence",
                "engagement",
                "final-cta",
            ],
        )

    def test_shared_introduction_states_the_complete_business_hierarchy(self):
        introduction = section_source(self.home, "what-we-do")
        for text in (
            "What we do",
            "One AI Business System.",
            "Three connected solution pillars.",
            "AICloudStrategist helps organisations in three connected ways:",
            "Enterprise AI",
            "Business Growth Systems",
            "AI Creative Studio",
            "Start with one capability or combine multiple capabilities around a larger business initiative.",
        ):
            self.assertIn(text, introduction)
        self.assertIn('href="#services"', introduction)
        self.assertIn('href="#business-growth-systems"', introduction)
        self.assertIn('href="#ai-creative-studio"', introduction)

    def test_existing_pillar_sections_are_byte_for_byte_preserved(self):
        for section_id, expected_hash in PILLAR_SHA256.items():
            with self.subTest(section=section_id):
                actual = hashlib.sha256(section_source(self.home, section_id).encode()).hexdigest()
                self.assertEqual(actual, expected_hash)

    def test_homepage_anchor_contract_is_complete_and_unique(self):
        ids = re.findall(r'\bid="([^"]+)"', self.home)
        self.assertEqual(len(ids), len(set(ids)), "Homepage contains duplicate IDs")
        self.assertIn('<a class="btn btn-light" href="#what-we-do">Explore what we do</a>', self.home)
        for fragment in re.findall(r'href="#([^"]+)"', self.home):
            self.assertIn(fragment, ids, f"Broken homepage fragment #{fragment}")


if __name__ == "__main__":
    unittest.main()
