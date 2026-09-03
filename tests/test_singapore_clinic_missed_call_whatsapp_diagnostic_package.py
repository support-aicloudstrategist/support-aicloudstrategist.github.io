import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "singapore-clinic-missed-call-whatsapp-diagnostic-package"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "singapore-clinic-diagnostic-scope-matrix.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
CSV_URL = f"{URL}singapore-clinic-diagnostic-scope-matrix.csv"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class SingaporeClinicMissedCallWhatsappDiagnosticPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
        cls.pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
        cls.free_review = (ROOT / "free-business-review" / "index.html").read_text(encoding="utf-8")
        cls.free_review_flat = (ROOT / "free-business-review.html").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_structured(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Service", types)
        self.assertIn("Dataset", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-09-03")

    def test_buyer_language_and_alternatives(self):
        for phrase in [
            "Singapore clinic missed calls",
            "WhatsApp patient follow-up Singapore clinic",
            "private clinic appointment reminder Singapore",
            "clinic no-show follow-up Singapore",
            "patient recall queue",
            "clinic management software Singapore",
            "patient engagement software Singapore",
            "call answering service for clinic",
            "AI receptionist for clinics Singapore",
            "PDPA patient communication evidence",
            "No-credentials intake boundary",
            "Alternative-fit recommendation",
        ]:
            self.assertIn(phrase, self.html)

    def test_csv_template_and_discovery_surfaces(self):
        self.assertEqual(len(self.rows), 8)
        for column in [
            "lane",
            "buyer_question",
            "safe_first_review_input",
            "excluded_from_first_review",
            "deliverable",
            "owner_or_adviser_route",
            "unsupported_claim_stop",
        ]:
            self.assertIn(column, self.rows[0])
        self.assertIn(CSV_URL.replace("https://aicloudstrategist.com", ""), self.html)
        self.assertIn(f"/resources/{SLUG}/", self.resources)
        self.assertIn(f"/resources/{SLUG}/", self.builder)
        self.assertIn(URL, self.sitemap)
        self.assertIn("Singapore clinic missed-call and WhatsApp diagnostic package", self.llms)
        self.assertIn("data-revenue-bridge=\"singapore-clinic-missed-call-whatsapp-diagnostic-package\"", self.pricing)

    def test_free_review_routes_singapore_clinics_to_diagnostic_package(self):
        self.assertEqual(self.free_review, self.free_review_flat)
        workflow = self.free_review.split('id="diagnostic-bridge-title"', 1)[1].split('id="request-title"', 1)[0]
        for phrase in [
            'data-review-route="singapore-clinic-missed-call-whatsapp-diagnostic-package"',
            "Singapore private clinics",
            "Missed-call + WhatsApp patient follow-up diagnostic",
            "PDPA adviser questions",
            "no-patient-data boundaries",
            f"/resources/{SLUG}/",
            f"/resources/{SLUG}/singapore-clinic-diagnostic-scope-matrix.csv",
            "/resources/singapore-private-clinic-missed-call-whatsapp-owner-evidence-checklist/",
        ]:
            self.assertIn(phrase, workflow)

    def test_truth_boundaries_prevent_fake_proof(self):
        for phrase in [
            "buyer-sendable readiness package only",
            "not a real Singapore clinic case study",
            "not a testimonial",
            "not a certification",
            "not PDPA compliance proof",
            "not legal advice",
            "not privacy advice",
            "not security advice",
            "not medical advice",
            "not clinical advice",
            "not booked-appointment improvement evidence",
            "not a no-show reduction",
            "not revenue evidence",
            "not ROI evidence",
            "not ranking evidence",
            "not demand evidence",
            "not lead evidence",
            "not customer evidence",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "pdpa certified", "real client results", "saved $"]:
            self.assertNotIn(forbidden, self.html.lower())


if __name__ == "__main__":
    unittest.main()
