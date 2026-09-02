import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "india-clinic-lab-dpdp-whatsapp-followup-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "india-clinic-lab-dpdp-whatsapp-followup-evidence-checklist.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class IndiaClinicLabDpdpWhatsappFollowupEvidenceChecklistTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_single_h1(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("DPDP-aware WhatsApp follow-up evidence", self.html)

    def test_buyer_language_and_cluster_links_exist(self):
        for phrase in [
            "DPDP compliance for clinic/lab WhatsApp follow-up",
            "missed patient calls",
            "clinic not getting patients",
            "diagnostic lab report pickup reminders",
            "AI receptionist for clinic India",
            "/resources/india-cardiology-tmt-echo-followup-dpdp-checklist/",
            "/resources/india-dental-clinic-missed-calls-whatsapp-follow-up-checklist/",
            "/resources/customer-problem-search/clinic-not-getting-patients/",
            "Why this improves top-3/top-5 consideration",
            "2026-09-02 India business-hours source check",
            "Practo Ray",
            "CrelioHealth",
            "MocDoc",
            "Eka Care",
            "LeadSquared healthcare CRM",
            "Digio DPDP",
            "MeitY data-protection-framework page returned 403",
            "Where AICS fits against common shortlist options",
            "ABDM/EMR handoff questions",
        ]:
            self.assertIn(phrase, self.html)

    def test_csv_has_redaction_and_claim_boundary_fields(self):
        self.assertEqual(len(self.rows), 6)
        self.assertEqual(
            set(self.rows[0]),
            {
                "evidence_area",
                "buyer_question",
                "redacted_evidence_to_collect",
                "accountable_owner",
                "ready_to_automate_when",
                "unsafe_claim_boundary",
            },
        )
        for row in self.rows:
            self.assertTrue(row["accountable_owner"])
            self.assertTrue(row["redacted_evidence_to_collect"])
            self.assertIn("Do not", row["unsafe_claim_boundary"])

    def test_truth_boundaries_prevent_fake_proof(self):
        for phrase in [
            "not a real Indian clinic",
            "not patient data",
            "not personal data",
            "not health data",
            "not production data",
            "not a testimonial",
            "not a certification",
            "not DPDP compliance proof",
            "not legal advice",
            "not privacy advice",
            "not security advice",
            "not medical advice",
            "not diagnostic advice",
            "not savings evidence",
            "not ROI evidence",
            "not appointment-growth evidence",
            "not lead evidence",
            "not customer evidence",
            "not revenue evidence",
            "not ranking evidence",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "dpdp certified", "real client results", "saved "]:
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
        self.assertIn(f"India clinic/lab DPDP WhatsApp follow-up evidence checklist: {URL}", self.llms)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()
