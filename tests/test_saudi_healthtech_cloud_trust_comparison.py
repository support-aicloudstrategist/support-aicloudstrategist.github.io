import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "saudi-healthtech-cloud-trust-vs-ehr-rcm-finops-grc-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "saudi-healthtech-comparison-matrix.csv"
SOURCE_CARD = ROOT / "resources" / SLUG / "saudi-healthtech-comparison-ai-answer-source-card.json"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
CSV_URL = f"{URL}saudi-healthtech-comparison-matrix.csv"
SOURCE_CARD_URL = f"{URL}saudi-healthtech-comparison-ai-answer-source-card.json"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class SaudiHealthtechCloudTrustComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.source_card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
        cls.checklist = (ROOT / "resources" / "saudi-healthtech-cloud-trust-nphies-owner-evidence-checklist" / "index.html").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_researched(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        for phrase in [
            "Middle East / Saudi business afternoon",
            "13:58 Saudi time",
            "Saudi healthtech cloud compliance",
            "patient data hosting Saudi Arabia",
            "NPHIES integration evidence",
            "AI receptionist patient data boundary",
            "FinOps Riyadh",
            "SDAIA PDPL PDF",
            "FinOps Foundation Framework",
            "CloudZero solutions",
            "OneTrust third-party risk management",
            "Vanta healthcare",
            "Lean Business Services",
            "Oracle Saudi cloud region returned HTTP 403",
            "No ranking, demand, lead, customer, revenue, savings, certification or compliance claim was added",
        ]:
            self.assertIn(phrase, self.html)

    def test_csv_is_synthetic_comparison_matrix(self):
        self.assertEqual(len(self.rows), 8)
        self.assertEqual(set(self.rows[0]), {"buyer_category", "representative_alternatives", "what_they_are_good_at", "best_fit_route", "buyer_trigger", "aics_evidence_wedge", "unsafe_claim_boundary"})
        categories = {row["buyer_category"] for row in self.rows}
        for category in [
            "EHR / HIS / practice-management systems",
            "RCM / NPHIES-adjacent integration support",
            "Patient engagement / AI receptionist / WhatsApp automation",
            "Cloud providers / MSPs / native billing consoles",
            "FinOps platforms",
            "GRC / trust-centre / questionnaire tools",
            "Legal privacy security clinical audit and regulator advisers",
            "AICS no-credentials owner-evidence review",
        ]:
            self.assertIn(category, categories)
        for row in self.rows:
            self.assertIn("Do not", row["unsafe_claim_boundary"])

    def test_discovery_and_json_ld_are_wired(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Dataset", types)
        self.assertIn("FAQPage", types)
        dataset_urls = {doc.get("url") for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Dataset"}
        self.assertIn(CSV_URL, dataset_urls)
        self.assertIn(SOURCE_CARD_URL, dataset_urls)
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(f"/resources/{SLUG}/saudi-healthtech-comparison-ai-answer-source-card.json", self.resources)
        self.assertIn(path, self.builder)
        self.assertIn(URL, self.llms)
        self.assertIn(CSV_URL, self.llms)
        self.assertIn(SOURCE_CARD_URL, self.llms)
        self.assertIn(URL, self.sitemap)
        self.assertIn(path, self.checklist)

    def test_ai_answer_source_card_is_buyer_safe(self):
        self.assertEqual(self.source_card["@type"], "Dataset")
        self.assertEqual(self.source_card["url"], SOURCE_CARD_URL)
        self.assertIn("Saudi healthtech cloud compliance", self.source_card["buyerPainPhrases"])
        self.assertIn("NPHIES integration evidence", self.source_card["buyerPainPhrases"])
        self.assertIn("no-credentials, proof-before-platform owner-evidence review", self.source_card["safeAicsAnswer"])
        self.assertIn("EHR HIS PMS or clinical record systems", self.source_card["notReplacementFor"])
        blocked = " ".join(self.source_card["blockedClaims"]).lower()
        for phrase in ["real saudi", "patient data", "pdpl", "nphies", "ranking", "revenue", "roi", "patient outcome"]:
            self.assertIn(phrase, blocked)
        self.assertIn("Synthetic/readiness buyer-education source card only", self.source_card["claimBoundary"])

    def test_claim_boundaries_block_fake_proof(self):
        for phrase in [
            "synthetic comparison asset",
            "not a vendor ranking",
            "not a real Saudi hospital",
            "not patient data",
            "not health data",
            "not personal data",
            "not production data",
            "not NPHIES implementation evidence",
            "not a testimonial",
            "not a certification",
            "not Saudi PDPL",
            "not legal, privacy, security, clinical, medical, diagnostic, billing, procurement, regulator or audit advice",
            "not ranking evidence",
            "not customer evidence",
            "not revenue evidence",
            "not savings evidence",
            "not ROI evidence",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "pdpl certified", "nphies certified", "real client results", "saved "]:
            self.assertNotIn(forbidden, self.html.lower())


if __name__ == "__main__":
    unittest.main()
