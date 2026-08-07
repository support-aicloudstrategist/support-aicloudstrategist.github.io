import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTACT = ROOT / "contact.html"
VISUAL_CSS = ROOT / "css" / "contact-enterprise-visual.css"


def block(source, pattern, label):
    match = re.search(pattern, source, flags=re.S)
    if match is None:
        raise AssertionError(f"Missing frozen {label} block")
    return match.group(0)


class EnterpriseContactVisualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = CONTACT.read_text(encoding="utf-8")
        cls.visual_css = VISUAL_CSS.read_text(encoding="utf-8")
        cls.visual_sources = cls.source + "\n" + cls.visual_css

    def test_conversion_content_and_behavior_remain_byte_frozen(self):
        frozen = {
            "form": (
                r'<form\b[^>]*id="contactForm"[^>]*>.*?</form>',
                "d382577f85f5b6fb523cdae32fca21ba5ea6f96e6261f468b56a9c848b6816a6",
            ),
            "submit_script": (
                r"const contactForm = document.getElementById\('contactForm'\);.*?// reveal \+ timeline draw",
                "2f33f97539908d42524e541534ebf243fbc16b9cbd1b3a4dcfbd7122df2756e9",
            ),
            "hero": (
                r'<section class="subhero">.*?</section>',
                "af2054ff8229a5f966311575ad1d8255ec08d07223022702e2fde15583f46ff8",
            ),
            "timeline": (
                r'<div>\s*<div class="section-head">.*?</div>\s*</div>\s*\n\s*<div class="form-wrap',
                "4b50296f546625b38d64cf8f1d17f1c8e19c40688811b41705afc74aae6f4def",
            ),
        }
        for label, (pattern, expected) in frozen.items():
            value = block(self.source, pattern, label)
            if label == "timeline":
                value = value.rsplit('\n\n        <div class="form-wrap', 1)[0]
            with self.subTest(block=label):
                self.assertEqual(hashlib.sha256(value.encode()).hexdigest(), expected)

    def test_new_contact_strip_has_exactly_three_accessible_channels(self):
        strip = block(
            self.source,
            r'<nav class="contact-choice-strip".*?</nav>',
            "contact choice strip",
        )
        self.assertEqual(strip.count('class="contact-choice"'), 3)
        self.assertEqual(strip.count('class="contact-choice-icon"'), 3)
        self.assertEqual(strip.count('<svg'), 3)
        self.assertNotRegex(strip, r'[💬☎✉]')
        self.assertIn('href="https://wa.me/', strip)
        self.assertIn('href="mailto:contact@aicloudstrategist.com"', strip)
        self.assertIn('href="tel:+', strip)
        for label in ("WhatsApp", "Email", "Call"):
            self.assertIn(f'<span class="contact-choice-label">{label}</span>', strip)

    def test_visual_system_is_scoped_premium_and_not_template_glass(self):
        self.assertIn("enterprise contact visual refinement v1", self.visual_css)
        for selector in (
            ".contact-choice-strip",
            ".contact-choice",
            ".contact-choice-icon",
            ".contact-choice-arrow",
        ):
            self.assertIn(selector, self.visual_css)
        self.assertNotIn("backdrop-filter", self.visual_sources)
        self.assertNotIn("conic-gradient", self.visual_sources)
        self.assertNotIn("text-overflow:ellipsis", self.visual_css)
        self.assertNotIn("@keyframes spin", self.visual_sources)
        self.assertIn("prefers-reduced-motion:reduce", self.visual_css)
        self.assertIn(".contact-choice{transition:none!important;}", self.visual_css)
        self.assertIn(".reveal{opacity:1;transform:none;transition:none;}", self.visual_css)
        self.assertIn(".timeline::after{height:calc(100% - 12px);}", self.visual_css)

    def test_mobile_conversion_priority_is_preserved(self):
        self.assertIn(".contact-layout .form-wrap{order:-1}", self.source)
        self.assertIsNotNone(
            re.search(
                r"@media\(max-width:600px\).*?\.contact-choice-strip\{grid-template-columns:1fr;",
                self.visual_css,
                flags=re.S,
            )
        )


if __name__ == "__main__":
    unittest.main()
