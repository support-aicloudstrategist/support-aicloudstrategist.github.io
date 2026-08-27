import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthtech-gdpr-dpia-security-questionnaire-source-map"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "europe-healthtech-gdpr-dpia-security-questionnaire-source-map.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class EuropeHealthtechGdprDpiaSecurityQuestionnaireSourceMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.csv_text = CSV.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    def test_page_is_indexable_and_targets_buyer_intent(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        for phrase in [
            "Europe healthtech GDPR, DPIA and security questionnaire source map",
            "European healthtech",
            "GDPR",
            "DPIA",
            "EU AI Act",
            "NHS DSPT/DTAC",
            "security questionnaire",
            "vendor-risk",
            "cloud/AI FinOps",
            "LLM cost governance",
            "no-credentials source-map review",
        ]:
            self.assertIn(phrase, self.html)

    def test_source_map_rows_and_safe_claim_boundaries_are_present(self):
        self.assertEqual(len(self.rows), 8)
        self.assertEqual(set(self.rows[0]), {"question_area", "buyer_language", "approved_source_to_prepare", "evidence_owner", "adviser_question", "unsafe_claim_to_block", "boundary_label"})
        for phrase in [
            "GDPR role and data scope",
            "DPIA readiness",
            "EU AI Act and human review",
            "NHS DSPT and DTAC evidence",
            "Subprocessors and data residency",
            "Security questionnaire",
            "Cloud and AI FinOps",
            "External claims",
            "Template row only; not GDPR advice or compliance proof",
            "Template row only; not ISO 27001 SOC 2 certification evidence",
            "Template row only; not savings ROI or revenue proof",
        ]:
            self.assertIn(phrase, self.csv_text)

    def test_competitor_context_and_claim_boundaries_prevent_fake_proof(self):
        for phrase in [
            "Apptio Cloudability",
            "CloudHealth",
            "CloudZero",
            "Vantage",
            "Datadog Cloud Cost Management",
            "Vanta",
            "Drata",
            "Secureframe",
            "OneTrust",
            "SafeBase",
            "Whistic",
            "proof-before-platform",
            "not a real European healthtech case study",
            "not production data",
            "not patient data",
            "not GDPR compliance proof",
            "not DPIA approval",
            "not EU AI Act compliance proof",
            "not NHS DSPT proof",
            "not DTAC proof",
            "not ISO 27001 proof",
            "not SOC 2 proof",
            "not legal advice",
            "not privacy advice",
            "not security advice",
            "not procurement advice",
            "not clinical advice",
            "not savings evidence",
            "not ROI evidence",
            "not lead evidence",
            "not customer evidence",
            "not revenue evidence",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "gdpr certified", "real client results", "saved ", "increased revenue"]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_json_ld_and_discovery_wiring_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Dataset", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-08-27")
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(path, self.sitemap_script)
        self.assertIn(URL, self.sitemap)
        self.assertIn("Europe healthtech GDPR + DPIA + security questionnaire source map", self.llms)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()
