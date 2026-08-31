import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthtech-procurement-response-readiness-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "europe-healthtech-procurement-response-readiness-checklist.csv"
SVG = ROOT / "resources" / SLUG / "europe-healthtech-procurement-response-owner-dashboard.svg"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class EuropeHealthtechProcurementResponseReadinessChecklistTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.svg = SVG.read_text(encoding="utf-8")
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_single_h1(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("Europe healthtech procurement response readiness checklist", self.html)

    def test_buyer_language_and_cluster_links_exist(self):
        for phrase in [
            "healthtech procurement response deadline",
            "AI trust questionnaire submission gate",
            "GDPR DPIA procurement evidence",
            "EU AI Act owner signoff",
            "security questionnaire final review",
            "cloud and LLM cost evidence packet",
            "/resources/europe-healthtech-ai-trust-questionnaire-answer-bank-template/",
            "/resources/europe-healthtech-gdpr-dpia-security-questionnaire-source-map/",
            "/resources/europe-healthtech-eu-ai-act-high-risk-decision-log-template/",
            "/resources/europe-healthtech-cloud-trust-finops-diagnostic-package/",
            "Why this improves top-3/top-5 consideration",
            "Demo owner dashboard visual",
            "europe-healthtech-procurement-response-owner-dashboard.svg",
            "six submission gates",
            "unsupported-claim stops",
        ]:
            self.assertIn(phrase, self.html)

    def test_demo_owner_dashboard_svg_is_synthetic_and_linked(self):
        self.assertTrue(SVG.is_file())
        for phrase in [
            "DEMO / SYNTHETIC",
            "Europe healthtech procurement response gate",
            "No patient data",
            "no credentials",
            "not a client result",
            "not compliance proof",
        ]:
            self.assertIn(phrase, self.svg)
        self.assertIn('src="/resources/europe-healthtech-procurement-response-readiness-checklist/europe-healthtech-procurement-response-owner-dashboard.svg"', self.html)

    def test_csv_has_submission_gate_fields_and_boundaries(self):
        self.assertEqual(len(self.rows), 6)
        self.assertEqual(
            set(self.rows[0]),
            {
                "gate",
                "procurement_question",
                "evidence_packet",
                "accountable_owner",
                "submit_condition",
                "unsafe_claim_boundary",
            },
        )
        for row in self.rows:
            self.assertTrue(row["accountable_owner"])
            self.assertTrue(row["evidence_packet"])
            boundary = row["unsafe_claim_boundary"].lower()
            self.assertTrue(
                "claim" in boundary
                or "compliance" in boundary
                or "proof" in boundary
                or "evidence" in boundary
                or "verified" in boundary
            )

    def test_truth_boundaries_prevent_fake_proof(self):
        for phrase in [
            "not a real European healthtech case study",
            "not production data",
            "not patient data",
            "not personal data",
            "not health data",
            "not customer data",
            "not a testimonial",
            "not a certification",
            "not GDPR compliance proof",
            "not DPIA approval",
            "not EU AI Act compliance proof",
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
        self.assertEqual(article["dateModified"], "2026-08-31")
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(path, self.builder)
        self.assertIn(URL, self.sitemap)
        self.assertIn(f"Europe healthtech procurement response readiness checklist: {URL}", self.llms)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()
