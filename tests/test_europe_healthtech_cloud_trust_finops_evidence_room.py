import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthtech-cloud-trust-finops-evidence-room"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "sample.csv"
OWNER_CSV = ROOT / "resources" / SLUG / "owner-dashboard.csv"
OWNER_SVG = ROOT / "resources" / SLUG / "owner-dashboard.svg"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class EuropeHealthtechCloudTrustFinOpsEvidenceRoomTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        cls.csv_rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.owner_rows = list(csv.DictReader(OWNER_CSV.open(newline="", encoding="utf-8")))
        cls.owner_svg = OWNER_SVG.read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_single_h1(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("European healthtech cloud trust + FinOps evidence room", self.html)

    def test_research_language_and_competitors_are_present(self):
        for phrase in [
            "Region selected:",
            "Europe / UK-EU business day",
            "healthtech cloud cost optimisation",
            "AI cloud FinOps",
            "LLM cost governance",
            "GDPR evidence",
            "DPIA questions",
            "security questionnaire evidence",
            "vendor risk management",
            "trust centre evidence",
            "DPA blocker",
            "EU AI Act evidence",
            "data residency",
            "subprocessor register",
            "human review",
            "clinical safety boundary",
            "Apptio Cloudability",
            "VMware/CloudHealth",
            "CloudZero",
            "Vantage",
            "Datadog Cloud Cost Management",
            "AWS Cost Explorer",
            "Azure Cost Management",
            "Vanta",
            "Drata",
            "Secureframe",
            "Sprinto",
            "OneTrust",
            "TrustArc",
            "Hyperproof",
            "Conveyor",
            "SafeBase",
            "Whistic",
        ]:
            self.assertIn(phrase, self.html)

    def test_top_five_consideration_and_outputs_exist(self):
        for phrase in [
            "AICS top-3/top-5 consideration wedge",
            "proof-before-platform",
            "Cloud and AI cost-owner allocation register",
            "AI usage / model / vendor dependency register",
            "Security-questionnaire evidence index",
            "Human-review, escalation and claim-control map",
            "Executive dashboard wireframe",
            "Owner dashboard demo artifacts",
            "synthetic owner dashboard CSV",
            "demo owner dashboard SVG",
            "adviser-question status",
            "human-review boundary",
            "Use this before buying another platform",
            "Europe procurement search-intent map",
            "EU AI Act overview",
            "ICO artificial-intelligence guidance hub",
            "NHS Data Security and Protection Toolkit",
            "UK DTAC returned HTTP 403",
            "healthcare SaaS FinOps cost allocation",
            "AI spend governance LLM cost owner dashboard",
            "GDPR AI data protection evidence healthtech",
            "NHS DSPT security questionnaire evidence",
            "Why this improves top-3/top-5 credibility",
            "what evidence supports the questionnaire answer",
        ]:
            self.assertIn(phrase, self.html)

    def test_claim_boundaries_prevent_fake_proof(self):
        for phrase in [
            "synthetic field examples only",
            "not a real European healthtech case study",
            "not a testimonial",
            "not production data",
            "not customer data",
            "not patient data",
            "not health data",
            "not GDPR compliance proof",
            "not EU AI Act compliance proof",
            "not healthcare compliance proof",
            "not security certification",
            "not audit advice",
            "not DPO advice",
            "not legal advice",
            "not medical advice",
            "not clinical advice",
            "not privacy advice",
            "not security advice",
            "not procurement-win evidence",
            "not savings evidence",
            "not revenue evidence",
            "not ROI evidence",
            "not ranking evidence",
            "not AI-accuracy evidence",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "gdpr certified", "eu ai act certified", "real client results", "saved "]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_csv_is_synthetic_and_usable(self):
        self.assertEqual(len(self.csv_rows), 8)
        self.assertEqual(set(self.csv_rows[0]), {"source", "synthetic_signal", "unit_metric", "evidence_gap", "decision_owner", "boundary_label"})
        self.assertTrue(all("claim" in row["boundary_label"] or "advice" in row["boundary_label"] or "certification" in row["boundary_label"] for row in self.csv_rows))

    def test_owner_dashboard_csv_and_svg_are_synthetic_and_claim_safe(self):
        self.assertEqual(len(self.owner_rows), 8)
        self.assertEqual(
            set(self.owner_rows[0]),
            {
                "dashboard_area",
                "synthetic_signal",
                "cost_owner",
                "evidence_owner",
                "adviser_question_status",
                "human_review_boundary",
                "decision_next_step",
                "boundary_label",
            },
        )
        for marker in [
            "Open question",
            "Human review required",
            "Demo row only",
            "no savings ROI or procurement claim",
            "no GDPR EU AI Act or DPIA advice",
            "no testimonial ranking customer result revenue",
        ]:
            self.assertIn(marker, OWNER_CSV.read_text(encoding="utf-8"))
        for marker in [
            "DEMO / SYNTHETIC ONLY",
            "no patient data, real client, savings, GDPR/EU AI Act proof, certification or clinical claim",
            "Proof-before-platform queue",
            "Unsupported claims",
        ]:
            self.assertIn(marker, self.owner_svg)
        self.assertIn("owner-dashboard.csv", self.html)
        self.assertIn("owner-dashboard.svg", self.html)

    def test_json_ld_and_discovery_wiring_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("FAQPage", types)
        article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-08-27")
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(f"Europe healthtech cloud trust FinOps evidence room: {URL}", self.llms)
        self.assertIn(URL, self.sitemap)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()
