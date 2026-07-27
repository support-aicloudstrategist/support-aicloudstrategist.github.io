import hashlib
import re
import unittest
from pathlib import Path

import tinycss2


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
STYLES = ROOT / "css" / "homepage-enterprise.css"
SECTION_SHA256 = {
    "hero": "ffc176afec2844cf4de07825fea2fe4d193745331d829041559c8599c910f7bf",
    "services": "9f33638ecf0c196e6eab0a22ef819465159bcf8acbb5198f4363ce1974cf8bbd",
}
REFINEMENT_MARKER = "/* AICS Enterprise AI visual refinement — 2026-07-27"


def section_source(source, section_id):
    match = re.search(
        rf'(?ms)^    <section\b[^>]*\bid="{re.escape(section_id)}"[^>]*>.*?^    </section>\n?',
        source,
    )
    if not match:
        raise AssertionError(f"Missing section #{section_id}")
    return match.group(0)


def refinement_source(styles):
    start = styles.index(REFINEMENT_MARKER)
    end = styles.index("@keyframes eaConsoleBreathe", start)
    return styles[start:end]


def at_rule_content(styles, keyword, prelude_text):
    rules = tinycss2.parse_stylesheet(styles, skip_whitespace=True, skip_comments=True)
    for rule in rules:
        if (
            rule.type == "at-rule"
            and rule.lower_at_keyword == keyword
            and prelude_text in tinycss2.serialize(rule.prelude)
            and rule.content is not None
        ):
            return tinycss2.serialize(rule.content)
    raise AssertionError(f"Missing @{keyword} rule containing {prelude_text!r}")


def qualified_selectors(styles):
    def walk(rules):
        for rule in rules:
            if rule.type == "qualified-rule":
                yield tinycss2.serialize(rule.prelude).strip()
            elif (
                rule.type == "at-rule"
                and rule.lower_at_keyword in {"media", "supports", "layer"}
                and rule.content is not None
            ):
                nested = tinycss2.parse_rule_list(
                    rule.content,
                    skip_whitespace=True,
                    skip_comments=True,
                )
                yield from walk(nested)

    rules = tinycss2.parse_stylesheet(styles, skip_whitespace=True, skip_comments=True)
    yield from walk(rules)


class HomepageEnterpriseVisualRefinementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = HOME.read_text(encoding="utf-8")
        cls.styles = STYLES.read_text(encoding="utf-8")
        cls.refinement = refinement_source(cls.styles)
        cls.motion = cls.styles[cls.styles.index(REFINEMENT_MARKER):]

    def test_target_section_markup_and_copy_are_byte_for_byte_preserved(self):
        for section_id, expected_hash in SECTION_SHA256.items():
            with self.subTest(section=section_id):
                actual = hashlib.sha256(section_source(self.home, section_id).encode()).hexdigest()
                self.assertEqual(actual, expected_hash)

    def test_premium_visual_system_is_scoped_to_the_two_approved_targets(self):
        required_scopes = (
            "body.enterprise-homepage .ea-control-scene",
            "body.enterprise-homepage .ea-control-shell",
            "body.enterprise-homepage .ea-system-card",
            "body.enterprise-homepage .ea-control-grid",
            "body.enterprise-homepage .ea-services",
            "body.enterprise-homepage .ea-service-grid",
            "body.enterprise-homepage .ea-service-card",
            "body.enterprise-homepage .ea-service-visual",
        )
        for selector in required_scopes:
            with self.subTest(required_selector=selector):
                self.assertIn(selector, self.refinement)

        approved_roots = (
            "body.enterprise-homepage .ea-control",
            "body.enterprise-homepage .ea-window",
            "body.enterprise-homepage .ea-system",
            "body.enterprise-homepage .ea-stage",
            "body.enterprise-homepage .ea-signal",
            "body.enterprise-homepage .ea-services",
            "body.enterprise-homepage .ea-service",
            "body.enterprise-homepage .ea-card",
            "body.enterprise-homepage .ea-visual",
            "body.enterprise-homepage .ea-assure",
            "body.enterprise-homepage .ea-build",
            "body.enterprise-homepage .ea-buyer",
            "body.enterprise-homepage .ea-finance",
            "body.enterprise-homepage .ea-secure",
            "body.enterprise-homepage .ea-operate",
            "body.enterprise-homepage .ea-section-action",
        )
        for selector_list in qualified_selectors(self.refinement):
            for selector in selector_list.split(","):
                selector = selector.strip()
                with self.subTest(scoped_selector=selector):
                    self.assertTrue(
                        selector.startswith(approved_roots),
                        f"Visual refinement selector leaks outside approved targets: {selector}",
                    )

    def test_visual_system_has_purposeful_motion_and_reduced_motion_support(self):
        animation_names = (
            "eaConsoleBreathe",
            "eaDataFlow",
            "eaPanelScan",
            "eaNodePulse",
            "eaJunctionPulse",
            "eaStatusPulse",
        )
        for name in animation_names:
            with self.subTest(animation=name):
                self.assertIn(f"@keyframes {name}", self.styles)
                self.assertRegex(
                    self.motion,
                    re.compile(rf"animation(?:-name)?\s*:[^;}}]*\b{re.escape(name)}\b"),
                )

        reduced_body = at_rule_content(self.motion, "media", "prefers-reduced-motion: reduce")
        self.assertIn("body.enterprise-homepage *", reduced_body)
        self.assertIn("body.enterprise-homepage *::before", reduced_body)
        self.assertIn("body.enterprise-homepage *::after", reduced_body)
        self.assertRegex(reduced_body, r"animation-duration:\s*\.001ms\s*!important")
        self.assertRegex(reduced_body, r"animation-iteration-count:\s*1\s*!important")

    def test_cramped_five_up_desktop_override_is_removed(self):
        self.assertNotIn("Content-fitted five-up capability cards on desktop", self.styles)
        self.assertNotRegex(
            self.styles,
            re.compile(r"\.ea-service-grid\s*\{[^}]*repeat\(5,", re.S),
            "Enterprise AI cards must not regress to a cramped five-column desktop strip",
        )
        service_grid_re = re.compile(
            r"\.ea-service-grid\s*\{[^}]*grid-template-columns:\s*repeat\(6,\s*minmax\(0,\s*1fr\)\)",
            re.S,
        )
        self.assertRegex(self.refinement, service_grid_re)


if __name__ == "__main__":
    unittest.main()
