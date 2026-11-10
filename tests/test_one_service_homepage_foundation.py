from pathlib import Path
import json
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
SITEMAP = ROOT / "sitemap.xml"

EXPECTED_H1 = "Know where your cloud and AI money goes—and what you can safely do about it."
EXPECTED_CTA = "Request a Cloud & AI Cost Fit Review"
EXPECTED_ROUTES = {
    "https://aicloudstrategist.com/",
    "https://aicloudstrategist.com/cloud-ai-cost-governance-diagnostic/",
    "https://aicloudstrategist.com/resources/cloud-ai-economics-decision-pack/",
    "https://aicloudstrategist.com/resources/",
    "https://aicloudstrategist.com/about/",
    "https://aicloudstrategist.com/trust-data-handling/",
    "https://aicloudstrategist.com/request-fit-review/",
    "https://aicloudstrategist.com/company-details/",
    "https://aicloudstrategist.com/privacy",
    "https://aicloudstrategist.com/terms",
}


class OneServiceHomepageFoundationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = HOME.read_text(encoding="utf-8")
        cls.lower = cls.source.lower()

    def test_homepage_has_single_outcome_led_h1(self):
        h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", self.source, re.I | re.S)
        self.assertEqual(len(h1s), 1)
        text = re.sub(r"<[^>]+>", "", h1s[0]).strip()
        self.assertEqual(text, EXPECTED_H1)

    def test_primary_cta_is_exact_and_routes_to_dedicated_fit_review(self):
        normalized = self.source.replace("&amp;", "&")
        pattern = r'<a[^>]+href="/request-fit-review/"[^>]*>\s*' + re.escape(EXPECTED_CTA) + r"\s*</a>"
        self.assertRegex(normalized, re.compile(pattern, re.I))
        self.assertGreaterEqual(normalized.count(EXPECTED_CTA), 2)

    def test_one_primary_service_and_no_legacy_offer_language(self):
        self.assertIn("Cloud &amp; AI Cost Governance Diagnostic", self.source)
        for forbidden in ("Production AI Readiness", "Cloud &amp; AI Economics Review", "Two commercial decisions"):
            self.assertNotIn(forbidden, self.source)

    def test_public_page_is_company_first_and_has_no_person_schema(self):
        for forbidden in ("rajeev", "rajiv", "anushka", "ai-assisted", '"@type":"person"', '"@type": "person"'):
            self.assertNotIn(forbidden, self.lower)
        self.assertIn('"@type":"Organization"', self.source)
        self.assertIn('"@type":"Service"', self.source)

    def test_homepage_contains_complete_buyer_decision_sequence(self):
        section_ids = ["signals", "cost-map", "deliverables", "evidence", "process", "fit", "boundaries", "data-handling", "faq"]
        positions = []
        for section_id in section_ids:
            marker = f'id="{section_id}"'
            self.assertEqual(self.source.count(marker), 1, section_id)
            positions.append(self.source.index(marker))
        self.assertEqual(positions, sorted(positions))

    def test_claim_and_evidence_boundaries_are_visible(self):
        required = (
            "No guaranteed savings",
            "No production changes",
            "representative synthetic scenario",
            "not customer work",
            "30-day customer action plan",
        )
        for phrase in required:
            self.assertIn(phrase.lower(), self.lower)

    def test_nav_is_focused_and_uses_one_conversion_path(self):
        nav = re.search(r"<nav[^>]*>(.*?)</nav>", self.source, re.I | re.S)
        if nav is None:
            self.fail("Homepage navigation is missing")
        nav_source = nav.group(1)
        for href in (
            "/cloud-ai-cost-governance-diagnostic/",
            "/resources/cloud-ai-economics-decision-pack/",
            "/resources/",
            "/about/",
            "/request-fit-review/",
        ):
            self.assertIn(f'href="{href}"', nav_source)
        self.assertNotIn("/pricing/", nav_source)
        self.assertNotIn("/portfolio/", nav_source)

    def test_foundation_assets_are_route_local_and_progressive(self):
        self.assertIn('/css/cost-governance.css?v=20261110', self.source)
        self.assertIn('/js/cost-governance.js?v=20261110', self.source)
        self.assertIn('prefers-reduced-motion', (ROOT / "css" / "cost-governance.css").read_text(encoding="utf-8"))
        self.assertIn('<noscript>', self.lower)

    def test_sitemap_contains_only_approved_launch_routes(self):
        root = ET.parse(SITEMAP).getroot()
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        routes = {node.text for node in root.findall(".//s:loc", ns)}
        self.assertEqual(routes, EXPECTED_ROUTES)

    def test_structured_data_is_valid_json(self):
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', self.source, re.I | re.S)
        self.assertGreaterEqual(len(blocks), 1)
        graph = json.loads(blocks[0])
        self.assertEqual(graph["@context"], "https://schema.org")
        types = {item["@type"] for item in graph["@graph"]}
        self.assertTrue({"Organization", "WebSite", "Service"}.issubset(types))
        self.assertNotIn("Person", types)


if __name__ == "__main__":
    unittest.main()
