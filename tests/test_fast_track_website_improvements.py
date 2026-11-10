import html
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8")


def visible_text(source):
    source = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", source, flags=re.I | re.S)
    source = re.sub(r"<[^>]+>", " ", source)
    return re.sub(r"\s+", " ", html.unescape(source)).strip()


class FastTrackWebsiteImprovementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = read("index.html")
        cls.service = read("cloud-ai-cost-governance-diagnostic/index.html")
        cls.resources = read("resources/index.html")
        cls.pack = read("resources/cloud-ai-economics-decision-pack/index.html")
        cls.form = read("request-fit-review/index.html")

    def test_homepage_keeps_primary_cta_before_commercial_facts(self):
        cta = 'data-aics-cta="primary-fit-review"'
        facts = 'class="hero-facts"'
        self.assertIn(cta, self.home)
        self.assertIn(facts, self.home)
        self.assertLess(self.home.index(cta), self.home.index(facts))
        copy = visible_text(self.home)
        for phrase in (
            "Typical scope",
            "10–15 business days after complete evidence intake",
            "Fixed fee after scope",
            "No contingent savings fee",
        ):
            self.assertIn(phrase, copy)

    def test_service_page_states_fit_nonfit_scope_turnaround_and_pricing(self):
        copy = visible_text(self.service)
        for phrase in (
            "Strong fit",
            "May not fit",
            "One agreed estate, billing period and decision question",
            "10–15 business days after complete evidence intake",
            "Fixed fee after scope",
            "No contingent savings fee",
        ):
            self.assertIn(phrase, copy)

    def test_resources_contains_only_real_linked_resource_cards(self):
        cards = re.findall(r'<article\b[^>]*data-resource-card[^>]*>(.*?)</article>', self.resources, re.I | re.S)
        self.assertEqual(len(cards), 3)
        for card in cards:
            self.assertRegex(card, r'<a\b[^>]*href="/[^"]+"')
        copy = visible_text(self.resources)
        for name in ("Decision Pack", "Diagnostic scope", "Trust & data handling"):
            self.assertIn(name, copy)
        self.assertNotIn("Guidance integrated into the diagnostic scope", copy)

    def test_decision_pack_starts_with_short_executive_summary_and_uses_30_day_plan(self):
        self.assertIn('id="executive-summary"', self.pack)
        self.assertLess(self.pack.index('id="executive-summary"'), self.pack.index('id="output-01"'))
        self.assertIn('data-decision-output="30-Day Action Plan"', self.pack)
        self.assertNotIn("90-Day Action Portfolio", self.pack)
        self.assertNotIn("Enterprise FinOps Advisory", self.pack)
        copy = visible_text(self.pack)
        for phrase in ("Decision now", "Why", "Owners required", "Next gate"):
            self.assertIn(phrase, copy)

    def test_fit_review_sets_response_expectation_next_to_form(self):
        copy = visible_text(self.form)
        self.assertIn(
            "We respond within 30 minutes during business hours, or by the next business morning.",
            copy,
        )
        self.assertIn("Do not upload billing files, credentials or confidential information", copy)


if __name__ == "__main__":
    unittest.main()
