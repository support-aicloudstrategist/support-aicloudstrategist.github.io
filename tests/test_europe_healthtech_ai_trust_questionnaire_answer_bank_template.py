import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthtech-ai-trust-questionnaire-answer-bank-template"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "europe-healthtech-ai-trust-questionnaire-answer-bank-template.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class EuropeHealthtechAITrustQuestionnaireAnswerBankTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_single_h1(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("Europe healthtech AI trust questionnaire answer bank template", self.html)

    def test_buyer_language_and_cluster_links_exist(self):
        for phrase in [
            "AI security questionnaire taking too long",
            "GDPR DPIA answers for healthtech AI",
            "EU AI Act evidence owner handoff",
            "subprocessor and data residency questions",
            "cloud and LLM cost claim boundaries",
            "trust-centre answer source map",
            "/resources/europe-healthtech-gdpr-dpia-security-questionnaire-source-map/",
            "/resources/europe-healthtech-eu-ai-act-high-risk-decision-log-template/",
            "/resources/europe-healthtech-cloud-trust-finops-diagnostic-package/",
            "Why this improves top-3/top-5 consideration",
        ]:
            self.assertIn(phrase, self.html)

    def test_csv_has_answer_bank_fields_and_boundaries(self):
        self.assertEqual(len(self.rows), 6)
        self.assertEqual(
            set(self.rows[0]),
            {
                "question_area",
                "buyer_question",
                "approved_answer_owner",
                "evidence_source",
                "answer_status",
                "unsafe_claim_boundary",
            },
        )
        for row in self.rows:
            self.assertTrue(row["approved_answer_owner"])
            self.assertTrue(row["evidence_source"])
            boundary = row["unsafe_claim_boundary"].lower()
            self.assertTrue(
                "claim" in boundary
                or "compliance" in boundary
                or "certification" in boundary
                or "guarantee" in boundary
                or "commitment" in boundary
            )

    def test_truth_boundaries_prevent_fake_proof(self):
        for phrase in [
            "not a real client case study",
            "patient-data analysis",
            "legal/privacy/security/clinical advice",
            "GDPR/DPIA/EU AI Act compliance proof",
            "audit report",
            "certification",
            "procurement approval",
            "savings evidence",
            "ROI evidence",
            "revenue evidence",
            "ranking claim",
            "AI-accuracy evidence",
            "No patient data, customer data, PHI/ePHI, health data, production credentials, real bills or real vendor files",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "gdpr certified", "real client results", "saved "]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_json_ld_and_discovery_wiring_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Dataset", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-08-28")
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(path, self.builder)
        self.assertIn(URL, self.sitemap)
        self.assertIn(f"Europe healthtech AI trust questionnaire answer bank template: {URL}", self.llms)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()
