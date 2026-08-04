import hashlib
import json
import re
import unittest
from pathlib import Path

import tinycss2


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / "tests/fixtures/site-visual-consistency-baseline.json").read_text())
CSS_PATH = ROOT / "css/enterprise-brand-system.css"
ASSET = "/css/enterprise-brand-system.css?v=20260804-v1"


def sha(value):
    return hashlib.sha256(value.encode()).hexdigest()


def extract(source, pattern, label, flags=re.I | re.S):
    match = re.search(pattern, source, flags)
    if not match:
        raise AssertionError(f"Missing {label}")
    return match.group(1) if match.lastindex else match.group(0)


def forms(source):
    return "".join(re.findall(r"<form\b[^>]*>.*?</form\s*>", source, re.I | re.S))


def executable_inline_scripts(source):
    blocks = []
    for attrs, body in re.findall(r"<script\b([^>]*)>(.*?)</script\s*>", source, re.I | re.S):
        lowered = attrs.lower()
        if "application/ld+json" not in lowered and "application/json" not in lowered:
            blocks.append(body)
    return "".join(blocks)


def seo(source):
    pattern = (
        r"<title\b[^>]*>.*?</title\s*>|"
        r"<meta\b[^>]*(?:name=[\"']description[\"']|property=[\"']og:|name=[\"']twitter:)[^>]*>|"
        r"<link\b[^>]*rel=[\"']canonical[\"'][^>]*>|"
        r"<script\b[^>]*type=[\"']application/ld\+json[\"'][^>]*>.*?</script\s*>"
    )
    return "".join(re.findall(pattern, source, re.I | re.S))


class SiteVisualConsistencyContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {path: (ROOT / path).read_text() for path in FIXTURE["pages"]}
        cls.css = CSS_PATH.read_text() if CSS_PATH.exists() else ""

    def test_content_seo_forms_scripts_and_body_structure_are_frozen(self):
        for path, expected in FIXTURE["pages"].items():
            source = self.sources[path]
            actual = {
                "main_sha256": sha(extract(source, r"<main\b[^>]*>.*?</main\s*>", "main")),
                "body_inner_sha256": sha(extract(source, r"<body\b[^>]*>(.*)</body\s*>", "body inner")),
                "forms_sha256": sha(forms(source)),
                "executable_inline_scripts_sha256": sha(executable_inline_scripts(source)),
                "seo_sha256": sha(seo(source)),
            }
            self.assertEqual(actual, expected, path)

    def test_every_target_uses_one_last_loaded_canonical_visual_layer(self):
        for path, source in self.sources.items():
            body = extract(source, r"<body\b([^>]*)>", "body attributes")
            self.assertRegex(body, r'class=["\'][^"\']*\baics-brand-system\b')
            stylesheets = re.findall(
                r'<link\b[^>]*rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)',
                source,
                re.I,
            )
            self.assertEqual(stylesheets.count(ASSET), 1, path)
            self.assertEqual(stylesheets[-1], ASSET, path)

    def test_homepage_remains_the_unmodified_reference(self):
        source = (ROOT / "index.html").read_text()
        self.assertNotIn(ASSET, source)
        self.assertNotIn("aics-brand-system", extract(source, r"<body\b([^>]*)>", "homepage body"))
        homepage_css = (ROOT / "css/homepage-enterprise.css").read_text()
        for token in (
            "--ea-bg: #030711",
            "--ea-border: rgba(148, 190, 220, 0.17)",
            "--ea-text: #f5fbff",
            "--ea-muted: #aebed0",
            "--ea-cyan: #67e8f9",
            "--ea-blue: #60a5fa",
            "--ea-violet: #a78bfa",
        ):
            self.assertIn(token, homepage_css)

    def test_shared_layer_uses_homepage_type_and_colour_tokens(self):
        required = (
            "/* AICS enterprise brand system v1 */",
            "--aics-bg:#030711",
            "--aics-text:#f5fbff",
            "--aics-text-secondary:#b8c8d9",
            "--aics-muted:#aebed0",
            "--aics-cyan:#67e8f9",
            "--aics-blue:#60a5fa",
            "--aics-violet:#a78bfa",
            "--aics-border:rgba(148,190,220,.17)",
            "Inter,ui-sans-serif,system-ui,-apple-system,\"Segoe UI\",Roboto,Arial,sans-serif",
            "font-size:clamp(50px,6.5vw,88px)",
            "font-size:clamp(36px,4.8vw,66px)",
            "font-size:clamp(30px,8.4vw,34px)",
            "font-size:clamp(32px,3vw,38px)",
            "font-size:clamp(26px,8vw,32px)",
            "line-height:.98",
            "letter-spacing:-.06em",
        )
        for value in required:
            self.assertIn(value, self.css)

    def test_motion_is_restrained_progressive_and_reduced_motion_safe(self):
        self.assertIn("@keyframes aicsSectionReveal", self.css)
        self.assertIn("animation-timeline:view()", self.css)
        self.assertIn("prefers-reduced-motion:reduce", self.css)
        self.assertIn("animation:none!important", self.css)
        self.assertIn("transition:none!important", self.css)
        self.assertIn("scroll-behavior:auto!important", self.css)
        self.assertIn(".paa-gate-ring{animation:none;}", self.css)
        self.assertNotRegex(self.css, r"(?i)bounce|spin|rotate\(")
        self.assertNotIn("transition:all", self.css.replace(" ", ""))

    def test_shared_layer_is_scoped_and_does_not_rebuild_page_layouts(self):
        self.assertTrue(self.css)
        self.assertNotIn("backdrop-filter", self.css)
        self.assertNotIn("will-change", self.css)
        self.assertNotIn("grid-template", self.css)
        self.assertNotIn("position:", self.css)
        def check_rules(rules):
            for rule in rules:
                if rule.type == "qualified-rule":
                    group = tinycss2.serialize(rule.prelude).strip()
                    for selector in group.split(","):
                        selector = selector.strip()
                        self.assertTrue(
                            selector.startswith("body.aics-brand-system")
                            or selector.startswith("html:has(body.aics-brand-system)"),
                            selector,
                        )
                elif rule.type == "at-rule" and rule.content is not None:
                    if rule.lower_at_keyword == "keyframes":
                        continue
                    check_rules(tinycss2.parse_rule_list(rule.content, skip_comments=True, skip_whitespace=True))

        check_rules(tinycss2.parse_stylesheet(self.css, skip_comments=True, skip_whitespace=True))


if __name__ == "__main__":
    unittest.main()
