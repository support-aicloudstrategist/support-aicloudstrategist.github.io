import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-healthtech-hipaa-ai-procurement-evidence-source-map"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "hipaa-ai-procurement-evidence-source-map.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class USHealthtechHipaaAIProcurementEvidenceSourceMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))

    def test_page_is_indexable_and_has_core_healthtech_intent(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        for phrase in [
            "US healthtech HIPAA + AI procurement evidence source map",
            "North America / US business day",
            "healthtech SaaS",
            "digital-health",
            "patient-engagement",
            "RCM",
            "prior-authorization",
            "HIPAA/PHI",
            "BAA",
            "SOC 2",
            "HITRUST",
            "AI data-use",
            "human-review",
            "cloud-cost evidence",
        ]:
            self.assertIn(phrase, self.html)

    def test_buyer_language_competitors_and_top_five_wedge_are_present(self):
        for phrase in [
            "HIPAA AI vendor risk questionnaire",
            "PHI AI data use evidence",
            "BAA subprocessor register",
            "healthcare SaaS cloud cost allocation",
            "SOC 2 HITRUST evidence room",
            "AI human review clinical boundary",
            "patient engagement AI procurement",
            "LLM cost governance healthcare",
            "CloudZero",
            "IBM Apptio Cloudability",
            "VMware/CloudHealth",
            "Vantage",
            "Datadog Cloud Cost Management",
            "AWS Cost Explorer",
            "Azure Cost Management",
            "Vanta",
            "Drata",
            "Secureframe",
            "HITRUST",
            "OneTrust",
            "TrustArc",
            "Conveyor",
            "SafeBase",
            "Whistic",
            "AICS top-3/top-5 consideration wedge",
            "proof-before-platform",
            "What AICS must publish/build to enter top-3/top-5 consideration",
            "ONC privacy and security page",
            "FinOps Foundation capabilities",
            "HHS HIPAA page returned HTTP 403",
        ]:
            self.assertIn(phrase, self.html)

    def test_claim_boundaries_prevent_fake_proof(self):
        for phrase in [
            "synthetic field examples only",
            "not production data",
            "not patient data",
            "not PHI",
            "not customer data",
            "not a real healthtech case study",
            "not procurement-win evidence",
            "not HIPAA compliance proof",
            "not SOC 2 proof",
            "not HITRUST certification evidence",
            "not legal advice",
            "not privacy advice",
            "not security advice",
            "not audit advice",
            "not procurement advice",
            "not clinical advice",
            "not medical advice",
            "not billing advice",
            "not savings evidence",
            "not ROI evidence",
            "not revenue evidence",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "hipaa certified", "real client results", "saved ", "increased revenue"]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_csv_is_synthetic_and_usable(self):
        self.assertEqual(len(self.rows), 8)
        self.assertEqual(set(self.rows[0]), {"question_area", "buyer_language", "approved_source_to_prepare", "evidence_owner", "adviser_question", "unsafe_claim_to_block", "boundary_label"})
        csv_text = CSV.read_text(encoding="utf-8")
        for marker in [
            "Template row only; not HIPAA advice or compliance proof",
            "Template row only; not legal advice or contract approval",
            "Template row only; not certification evidence",
            "Template row only; not savings or ROI proof",
            "Template row only; not medical clinical billing or legal advice",
        ]:
            self.assertIn(marker, csv_text)

    def test_json_ld_and_discovery_wiring_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Dataset", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-08-26")
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(path, self.sitemap_script)
        self.assertIn(URL, self.sitemap)
        self.assertIn("US healthtech HIPAA + AI procurement evidence source map", self.llms)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()
