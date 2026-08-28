import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "uae-healthtech-no-credentials-patient-data-intake-policy"
PAGE = ROOT / "resources" / SLUG / "index.html"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class UaeHealthtechNoCredentialsPatientDataIntakePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_single_h1(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("UAE Healthtech No-Credentials Patient Data Intake Policy", self.html)

    def test_buyer_language_and_safe_intake_boundaries_exist(self):
        for phrase in [
            "UAE clinic patient data no-credentials intake",
            "Dubai healthtech cloud trust review",
            "AI receptionist patient data boundary",
            "clinic WhatsApp privacy follow-up",
            "patient data hosting UAE",
            "telehealth vendor security questionnaire",
            "FinOps Dubai",
            "Malaffi/NABIDH-aware integration handoff",
            "No credentials or secrets",
            "No patient-identifiable data",
            "No regulator-sensitive material by default",
            "Safe first-review inputs",
            "Why this improves top-3/top-5 consideration",
        ]:
            self.assertIn(phrase, self.html)

    def test_truth_boundaries_prevent_fake_proof(self):
        for phrase in [
            "not a real UAE hospital",
            "not patient data",
            "not health data",
            "not personal data",
            "not production data",
            "not a testimonial",
            "not a certification",
            "not PDPL compliance proof",
            "not DHA, DoH, MOHAP, Malaffi, NABIDH",
            "not legal advice",
            "not privacy advice",
            "not security advice",
            "not clinical advice",
            "not medical advice",
            "not diagnostic advice",
            "not billing advice",
            "not procurement advice",
            "not audit advice",
            "not savings evidence",
            "not ROI evidence",
            "not appointment-growth evidence",
            "not patient-outcome evidence",
            "not lead evidence",
            "not customer evidence",
            "not revenue evidence",
            "not ranking evidence",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "pdpl certified", "real client results", "saved "]:
            self.assertNotIn(forbidden, self.html.lower())

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
        self.assertIn(f"UAE healthtech no-credentials patient data intake policy: {URL}", self.llms)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()
