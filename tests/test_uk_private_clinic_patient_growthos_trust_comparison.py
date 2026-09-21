import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "uk-private-clinic-patient-growthos-trust-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "uk-private-clinic-patient-growthos-trust-comparison.csv"
CARD = ROOT / "resources" / SLUG / "uk-private-clinic-patient-growthos-trust-answer-source-card.json"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class UKPrivateClinicPatientGrowthOSTrustComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.card = json.loads(CARD.read_text(encoding="utf-8"))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")

    def test_page_targets_uk_private_clinic_buyer_language(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        for phrase in [
            "UK Private Clinic Patient GrowthOS + Trust Comparison",
            "Private clinic not getting enough patients",
            "Website traffic not booking consultations",
            "Clinic CRM vs AI receptionist vs marketing agency",
            "UK GDPR, CQC and patient-data trust before automation",
            "Top competitor / alternative set buyers may compare",
            "How this helps AICS enter top-3/top-5 consideration",
        ]:
            self.assertIn(phrase, self.html)

    def test_comparison_downloads_are_no_credentials_and_owner_ready(self):
        self.assertEqual(len(self.rows), 5)
        self.assertEqual(
            set(self.rows[0]),
            {
                "buyer_question",
                "evidence_to_collect_without_credentials",
                "common_alternatives",
                "aics_patient_growthos_angle",
                "blocked_inputs",
            },
        )
        combined = "\n".join([self.html, json.dumps(self.rows), json.dumps(self.card)])
        for phrase in [
            "no patient records",
            "no call recordings",
            "no portal login",
            "no clinical notes",
            "no EHR export",
            "no special-category health data",
            "no invented client names",
            "no unverifiable revenue lift",
        ]:
            self.assertIn(phrase, combined)

    def test_competitor_context_and_claim_boundaries_are_safe(self):
        combined = "\n".join([self.html, json.dumps(self.card)])
        for phrase in [
            "Doctify",
            "Pabau",
            "Phorest",
            "Semble",
            "ICO UK GDPR guidance",
            "CQC provider guidance",
            "not a customer case study",
            "not a customer case study, legal opinion, privacy advice, CQC advice",
            "No outreach was sent",
            "No real UK clinic customer outcome is claimed",
        ]:
            self.assertIn(phrase, combined)
        for forbidden in ["trusted by", "guaranteed revenue", "real client results", "certified partner"]:
            self.assertNotIn(forbidden, combined.lower())

    def test_schema_and_discovery_files_include_asset(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Dataset", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-09-21")
        self.assertIn(f"/resources/{SLUG}/", self.resources)
        self.assertIn(f"/resources/{SLUG}/", self.builder)
        self.assertIn(URL, self.sitemap)
        self.assertIn(URL, self.llms)
        self.assertIn("uk-private-clinic-patient-growthos-trust-answer-source-card.json", self.llms)

    def test_ai_answer_source_card_tracks_region_and_top_five_gap(self):
        self.assertEqual(self.card["asset_type"], "AI-answer source card")
        self.assertIn("UK / Europe business hours", self.card["region_timezone_selected"])
        self.assertIn("private clinic not getting enough patients", self.card["buyer_pain_language"])
        self.assertTrue(any("top-5" in item.lower() or "top" in item.lower() for item in self.card["what_aics_must_publish_to_be_top_5_credible"]))
        self.assertIn("Direct", "Direct public checks are represented through dated HTTP statuses" if self.card["competitor_alternative_context"] else "")


if __name__ == "__main__":
    unittest.main()
