import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "us-ai-startup-ai-spend-board-review-checklist" / "index.html"
URL = "https://aicloudstrategist.com/resources/us-ai-startup-ai-spend-board-review-checklist/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class USAIStartupAISpendBoardReviewChecklistTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.diagnostic = (ROOT / "resources" / "us-ai-startup-llm-gpu-finops-diagnostic-package" / "index.html").read_text(encoding="utf-8")
        cls.comparison = (ROOT / "resources" / "us-ai-startup-llm-gpu-finops-vs-cloud-cost-tools-comparison" / "index.html").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_single_h1(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("AI spend board review checklist", self.html)

    def test_board_review_evidence_and_boundaries_are_present(self):
        for phrase in [
            "Spend-source inventory",
            "AI workload classification",
            "Product and customer allocation",
            "Risk and data boundary",
            "Decision queue",
            "Proof log",
        ]:
            self.assertIn(phrase, self.html)
        for boundary in [
            "not a US AI startup client case study",
            "not a testimonial",
            "not a savings result",
            "not runway-extension evidence",
            "not investor-relations advice",
            "not legal, privacy, security, tax, accounting or compliance advice",
            "guaranteed savings",
        ]:
            self.assertIn(boundary, self.html)
        for forbidden in ["trusted by", "certified partner", "guaranteed 30%", "case study results"]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_paid_diagnostic_fit_gate_qualifies_revenue_ready_buyers(self):
        for phrase in [
            "When to request the paid diagnostic",
            "Fit signal",
            "What AICS needs first",
            "What the diagnostic can produce",
            "Board, investor or budget review is scheduled within 30 days",
            "Engineering and finance disagree on what spend is product-critical",
            "Tool purchase or commitment decision is being debated",
            "Not a fit yet",
            "No billing exports, no named decision owner",
            "scope-before-quote recommendation",
        ]:
            self.assertIn(phrase, self.html)

    def test_intake_worksheet_qualifies_scope_without_sensitive_data(self):
        for phrase in [
            "Copy/paste intake worksheet",
            "Review deadline",
            "Included systems",
            "Top spend drivers",
            "Decision needed",
            "Proof boundary",
            "Redaction gate",
            "no credentials, tokens, keys or private URLs",
            "qualified owner approves broader sharing",
        ]:
            self.assertIn(phrase, self.html)

    def test_json_ld_article_faq_and_breadcrumb_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("FAQPage", types)
        self.assertIn("BreadcrumbList", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertIn("GPU spend", article["about"])
        self.assertIn("AI unit economics", article["about"])

    def test_discovery_and_cluster_links_include_asset(self):
        path = "/resources/us-ai-startup-ai-spend-board-review-checklist/"
        self.assertIn(path, self.resources)
        self.assertIn(f"US AI startup AI spend board review checklist: {URL}", self.llms)
        self.assertIn(f"<loc>{URL}</loc>", self.sitemap)
        self.assertIn(path, self.diagnostic)
        self.assertIn(path, self.comparison)
        self.assertIn('/free-business-review/?package=us-ai-startup-ai-spend-board-review', self.html)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()
