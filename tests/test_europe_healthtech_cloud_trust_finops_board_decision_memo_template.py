import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthtech-cloud-trust-finops-board-decision-memo-template"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "board-decision-memo-template.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class EuropeHealthtechBoardDecisionMemoTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_has_single_h1(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("Europe Healthtech Cloud Trust + FinOps Board Decision Memo Template", self.html)

    def test_board_decision_language_and_cluster_links_exist(self):
        for phrase in [
            "board-safe memo structure",
            "cloud/AI cost-owner mapping",
            "GDPR/DPIA adviser-question review",
            "vendor-risk blockers",
            "human-review boundary checks",
            "stop/continue/investigate decisions",
            "/resources/europe-healthtech-cloud-trust-finops-diagnostic-package/",
            "/resources/europe-healthtech-cloud-trust-finops-evidence-room/",
            "board-decision-memo-template.csv",
            "Why this improves top-3/top-5 consideration",
        ]:
            self.assertIn(phrase, self.html)

    def test_claim_boundaries_prevent_fake_proof(self):
        for phrase in [
            "not a real client case study",
            "not a real client case study, testimonial",
            "not a real client case study, testimonial, production deployment",
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
            "No patient data",
            "No patient data, customer data, PHI/ePHI, health data, production credentials, real bills or real vendor files",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "gdpr certified", "real client results", "saved "]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_csv_template_has_decision_fields_and_boundaries(self):
        self.assertEqual(len(self.rows), 5)
        self.assertEqual(
            set(self.rows[0]),
            {
                "memo_section",
                "board_question",
                "evidence_source_needed",
                "accountable_owner",
                "adviser_question_status",
                "decision_options",
                "claim_boundary",
            },
        )
        for row in self.rows:
            self.assertTrue(row["decision_options"])
            self.assertTrue("claim" in row["claim_boundary"] or "advice" in row["claim_boundary"] or "certification" in row["claim_boundary"])

    def test_json_ld_and_discovery_wiring_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-08-28")
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(path, self.builder)
        self.assertIn(URL, self.sitemap)
        self.assertIn(f"Europe healthtech cloud trust FinOps board decision memo template: {URL}", self.llms)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()
