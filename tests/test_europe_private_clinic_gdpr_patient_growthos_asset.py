import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-private-clinic-gdpr-patient-growthos-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class EuropePrivateClinicGDPRPatientGrowthOSAssetTests(unittest.TestCase):
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
        self.assertIn("Europe Private Clinic GDPR Patient GrowthOS Evidence Checklist", self.html)

    def test_buyer_research_and_competitor_language_are_present(self):
        for phrase in [
            "Region selected: Europe / UK-EU business day",
            "private clinic patient engagement software",
            "missed calls private clinic",
            "appointment follow-up GDPR",
            "Doctolib alternative",
            "Semble practice management",
            "Pabau clinic software",
            "Cliniko appointment reminders",
            "AI receptionist for clinics",
            "RGPD questions",
            "Pabau, Semble, Cliniko, Phreesia, Luma Health, Artera and HotDoc",
            "Doctolib returned HTTP 403",
            "did not show a readable AICS marker",
            "practice management, online booking, patient communication",
        ]:
            self.assertIn(phrase, self.html)

    def test_top_five_consideration_and_checklist_sections_exist(self):
        for phrase in [
            "What AICS must publish/build to enter top-3/top-5 consideration",
            "Evidence checklist before buying another platform",
            "Demand-source register",
            "Missed-call and callback queue",
            "Booking and no-show evidence",
            "GDPR/RGPD adviser queue",
            "AI receptionist boundary log",
            "Owner dashboard cadence",
            "Use this as a proof-before-platform filter",
        ]:
            self.assertIn(phrase, self.html)

    def test_claim_boundaries_prevent_fake_proof(self):
        for phrase in [
            "not a real European clinic case study",
            "not a testimonial",
            "not production data",
            "not patient data",
            "not GDPR compliance proof",
            "not UK GDPR compliance proof",
            "not RGPD compliance proof",
            "not booked-appointment evidence",
            "not no-show reduction evidence",
            "not revenue evidence",
            "not ROI evidence",
            "not ranking evidence",
            "not AI-accuracy evidence",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed appointments", "guaranteed no-show reduction", "real european clinic results", "gdpr certified"]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_json_ld_and_discovery_wiring_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-08-23")
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(f"Europe private clinic GDPR Patient GrowthOS evidence checklist: {URL}", self.llms)
        self.assertIn(URL.rstrip("/"), self.sitemap)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()
