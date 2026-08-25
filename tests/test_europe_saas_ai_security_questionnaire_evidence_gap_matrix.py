import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-saas-ai-security-questionnaire-evidence-gap-matrix"
PAGE = ROOT / "resources" / SLUG / "index.html"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class EuropeSaaSAISecurityQuestionnaireEvidenceGapMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_single_h1(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("Europe SaaS AI Security Questionnaire Evidence Gap Matrix", self.html)

    def test_research_language_and_competitors_are_present(self):
        for phrase in [
            "Region selected:",
            "Europe / UK-EU business day",
            "AI security questionnaire",
            "EU AI Act evidence",
            "GDPR AI data processing",
            "vendor risk questionnaire",
            "trust center",
            "security questionnaire automation",
            "DPA/MSA blocker",
            "model inventory",
            "human review",
            "cloud AI cost allocation",
            "Vanta",
            "Drata",
            "Secureframe",
            "Sprinto",
            "OneTrust",
            "TrustArc",
            "HTTP 404",
        ]:
            self.assertIn(phrase, self.html)

    def test_top_five_consideration_and_matrix_sections_exist(self):
        for phrase in [
            "What AICS must publish/build to enter top-3/top-5 consideration",
            "Evidence gap matrix before buying another GRC or trust-centre tool",
            "AI-use register",
            "Data-flow evidence map",
            "Human-review boundary log",
            "Security-questionnaire source-of-truth pack",
            "FinOps ownership register",
            "Use this as proof-before-platform filter",
        ]:
            self.assertIn(phrase, self.html)

    def test_claim_boundaries_prevent_fake_proof(self):
        for phrase in [
            "not a real European SaaS case study",
            "not a testimonial",
            "not production data",
            "not customer data",
            "not GDPR compliance proof",
            "not EU AI Act compliance proof",
            "not security certification",
            "not legal advice",
            "not DPO advice",
            "not audit advice",
            "not procurement-win evidence",
            "not revenue evidence",
            "not ROI evidence",
            "not ranking evidence",
            "not AI-accuracy evidence",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "gdpr certified", "eu ai act certified", "real client results"]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_json_ld_and_discovery_wiring_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-08-25")
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(f"Europe SaaS AI security questionnaire evidence gap matrix: {URL}", self.llms)
        self.assertIn(URL, self.sitemap)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()
