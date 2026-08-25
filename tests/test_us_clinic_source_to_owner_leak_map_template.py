import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-clinic-source-to-owner-leak-map-template"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "sample.csv"
SVG = ROOT / "resources" / SLUG / "demo-dashboard.svg"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class USClinicSourceToOwnerLeakMapTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.proof_pack = (ROOT / "resources" / "us-clinic-top-5-consideration-proof-pack" / "index.html").read_text(encoding="utf-8")
        with CSV.open(newline="", encoding="utf-8") as handle:
            cls.rows = list(csv.DictReader(handle))
        cls.svg = SVG.read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_single_h1_and_links_artifacts(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("US Clinic Source-to-Owner Leak Map Template", self.html)
        self.assertIn(f'/resources/{SLUG}/sample.csv', self.html)
        self.assertIn(f'/resources/{SLUG}/demo-dashboard.svg', self.html)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)

    def test_buyer_research_and_competitor_language_present(self):
        for phrase in [
            "Region and buyer pain language selected",
            "North America / United States healthcare clinics",
            "AI receptionist for medical office",
            "HIPAA compliant texting",
            "patient engagement platform",
            "front office automation",
            "missed call callback",
            "referral leakage",
            "NexHealth | Automate Your Front-Office",
            "Luma Health",
            "Phreesia",
            "Hyro",
            "Notable, Podium, Salesforce Health Cloud",
            "proof-before-platform",
        ]:
            self.assertIn(phrase, self.html)

    def test_csv_is_synthetic_and_covers_core_sources(self):
        self.assertEqual(len(self.rows), 10)
        self.assertEqual(set(self.rows[0]), {
            "synthetic_source",
            "synthetic_patient_request",
            "owner_state",
            "sla_status",
            "evidence_field_needed",
            "ai_boundary_or_human_review",
            "phi_minimisation_note",
            "buyer_question",
            "boundary_label",
        })
        sources = {row["synthetic_source"] for row in self.rows}
        for source in ["Google Business Profile call", "After-hours voicemail", "Referral fax/email", "Telehealth handoff", "Phone tree abandoned call"]:
            self.assertIn(source, sources)
        self.assertTrue(all("Simulated row only" in row["boundary_label"] for row in self.rows))
        self.assertTrue(any(row["owner_state"] == "No owner" for row in self.rows))
        self.assertTrue(any("AI" in row["ai_boundary_or_human_review"] for row in self.rows))

    def test_svg_is_demo_labelled_and_boundary_safe(self):
        for phrase in [
            "DEMO / INTERNAL / SIMULATED ONLY",
            "no real clinic, patient, PHI, HIPAA compliance",
            "Source-to-Owner Leak Map",
            "Owner-gap queue",
            "NexHealth",
            "Luma Health",
            "Phreesia",
        ]:
            self.assertIn(phrase, self.svg)

    def test_claim_boundaries_prevent_fake_proof(self):
        for phrase in [
            "not a real US clinic case study",
            "not a customer testimonial",
            "not a HIPAA compliance attestation",
            "not medical/legal/privacy/security advice",
            "not platform certification",
            "not evidence of bookings",
            "no-show reduction, revenue, ranking, patient outcome or AI accuracy",
            "All rows below are synthetic",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by us clinics", "guaranteed no-show reduction", "hipaa certified", "real patient results"]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_json_ld_article_faq_and_breadcrumb_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("FAQPage", types)
        self.assertIn("BreadcrumbList", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-08-25")
        self.assertIn("source-to-owner leak map", article["about"])
        self.assertIn("demo dashboard SVG", article["about"])

    def test_discovery_and_cluster_links_include_asset(self):
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(URL, self.llms)
        self.assertIn(path, self.proof_pack)
        self.assertIn('/free-business-review/?package=us-clinic-source-to-owner-leak-map', self.html)


if __name__ == "__main__":
    unittest.main()
