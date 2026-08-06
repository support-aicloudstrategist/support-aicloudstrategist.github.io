import hashlib
import re
import unittest
from pathlib import Path

import tinycss2


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
STYLES = ROOT / "css" / "homepage-enterprise.css"
HOME_SHA256 = "e989912338d9f7fd2d725d7ab22cc65f078460af36c3be95c518f856eed28874"
MARKER = "/* Production AI Control live refinement — 2026-08-06 */"


def selectors(styles):
    rules = tinycss2.parse_stylesheet(styles, skip_comments=True, skip_whitespace=True)

    def walk(items):
        for rule in items:
            if rule.type == "qualified-rule":
                yield tinycss2.serialize(rule.prelude).strip()
            elif rule.type == "at-rule" and rule.content is not None and rule.lower_at_keyword in {"media", "supports", "layer"}:
                yield from walk(tinycss2.parse_rule_list(rule.content, skip_comments=True, skip_whitespace=True))

    yield from walk(rules)


class HomepageControlLiveRefinementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home_bytes = HOME.read_bytes()
        cls.styles = STYLES.read_text(encoding="utf-8")
        if MARKER not in cls.styles:
            raise AssertionError("Missing Production AI Control live-refinement block")
        cls.refinement = cls.styles[cls.styles.index(MARKER):]

    def test_homepage_markup_and_copy_remain_byte_for_byte_unchanged(self):
        self.assertEqual(hashlib.sha256(self.home_bytes).hexdigest(), HOME_SHA256)

    def test_refinement_is_strictly_scoped_to_the_homepage_control_visual(self):
        for selector_list in selectors(self.refinement):
            for selector in selector_list.split(","):
                selector = selector.strip()
                with self.subTest(selector=selector):
                    self.assertTrue(
                        selector.startswith("body.enterprise-homepage .ea-control"),
                        f"Selector escapes the approved control-panel scope: {selector}",
                    )

    def test_mobile_system_copy_is_constrained_inside_the_card(self):
        self.assertRegex(
            self.refinement,
            re.compile(
                r"@media\s*\(max-width:\s*620px\).*?\.ea-system-card\s*>\s*div\s*\{[^}]*width:\s*100%[^}]*max-width:\s*100%",
                re.S,
            ),
        )
        self.assertRegex(
            self.refinement,
            re.compile(r"\.ea-system-card\s+h2\s*\{[^}]*overflow-wrap:\s*anywhere", re.S),
        )
        self.assertRegex(
            self.refinement,
            re.compile(
                r"\.ea-system-card\s+p\s*\{[^}]*width:\s*100%\s*!important[^}]*max-width:\s*100%\s*!important[^}]*font-size:\s*11px\s*!important",
                re.S,
            ),
        )

    def test_live_state_uses_purposeful_staggered_telemetry(self):
        required = (
            "--ea-node-accent",
            "animation: eaControlSignal",
            "animation: eaControlCardLive",
            "animation: eaControlStatusOrbit",
            "animation-delay:",
            "@keyframes eaControlSignal",
            "@keyframes eaControlCardLive",
            "@keyframes eaControlStatusOrbit",
        )
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, self.refinement)

    def test_motion_is_subtle_and_reduced_motion_remains_global(self):
        self.assertNotIn("filter: blur(48px)", self.refinement)
        reduced = self.styles[self.styles.index("@media (prefers-reduced-motion: reduce)"):]
        self.assertIn("animation-duration: .001ms !important", reduced)
        self.assertIn("animation-iteration-count: 1 !important", reduced)


if __name__ == "__main__":
    unittest.main()
