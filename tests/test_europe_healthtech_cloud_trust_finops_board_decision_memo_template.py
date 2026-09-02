import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthtech-cloud-trust-finops-board-decision-memo-template"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / f"{SLUG}.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class EuropeHealthtechCloudTrustFinopsBoardMemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")

    def test_page_is_indexable_and_targets_europe_buyer_language(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        for phrase in [
            "Europe healthtech cloud trust + AI FinOps board decision memo template",
            "healthtech cloud cost optimisation",
            "AI spend governance",
            "LLM cost allocation",
            "GDPR/DPIA evidence",
            "EU AI Act readiness questions",
            "security questionnaire evidence",
            "NHS DSPT evidence",
            "human-review escalation",
            "CFO, CTO, DPO, CISO",
            "Why this memo helps AICS enter top-3/top-5 consideration",
            f"/resources/{SLUG}/{SLUG}.csv",
        ]:
            self.assertIn(phrase, self.html)

    def test_csv_is_owner_evidence_ready(self):
        self.assertEqual(len(self.rows), 6)
        self.assertEqual(
            set(self.rows[0]),
            {"section", "board_question", "evidence_to_attach", "owner", "claim_boundary"},
        )
        for row in self.rows:
            self.assertTrue(row["board_question"].endswith("?"))
            self.assertTrue(row["evidence_to_attach"])
            self.assertTrue(row["owner"])
            self.assertRegex(row["claim_boundary"], r"No|Do not")

    def test_claim_boundaries_prevent_fake_healthtech_or_compliance_claims(self):
        for phrase in [
            "not a real client case study",
            "not a platform partnership",
            "not a legal opinion",
            "not privacy advice",
            "not security advice",
            "not clinical advice",
            "not audit advice",
            "not procurement advice",
            "does not claim superiority",
            "does not claim savings",
            "ROI",
            "GDPR compliance",
            "EU AI Act compliance",
            "NHS DSPT compliance",
            "ISO 27001",
            "SOC 2",
            "HITRUST",
            "certification",
            "ranking",
            "procurement approval",
            "patient outcomes",
            "AI accuracy",
            "customers",
            "testimonials",
            "logos",
            "production-data access",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed", "real client results", "nhs approved", "gdpr compliant", "eu ai act compliant", "certified partner"]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_json_ld_and_discovery_wiring_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Dataset", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-09-02")
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(path, self.builder)
        self.assertIn(URL, self.sitemap)
        self.assertIn("Europe healthtech cloud trust FinOps board decision memo template", self.llms)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()
