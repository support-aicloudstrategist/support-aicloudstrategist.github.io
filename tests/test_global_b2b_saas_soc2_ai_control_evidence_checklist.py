import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-b2b-saas-soc2-ai-control-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "b2b-saas-soc2-ai-control-evidence.csv"
SVG = ROOT / "resources" / SLUG / "b2b-saas-ai-control-evidence-risk-map.svg"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class B2BSaaSSoc2AiControlEvidenceChecklistTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    def test_page_is_indexable_canonical_and_single_h1(self):
        self.assertIn('<meta name="robots" content="index, follow"/>', self.html)
        self.assertIn(f'<link rel="canonical" href="{URL}"/>', self.html)
        self.assertEqual(self.html.count("<h1>"), 1)
        self.assertIn("B2B SaaS teams need SOC 2-ready AI control evidence", self.html)
        self.assertIn("enterprise security reviews stall deals", self.html)

    def test_buyer_language_and_revenue_bridge_exist(self):
        for phrase in [
            "SOC 2 AI controls",
            "AI security questionnaire answers",
            "SaaS AI trust center evidence",
            "enterprise vendor risk AI feature",
            "AI feature procurement blocker",
            "Where AICS fits before the security questionnaire stalls",
            "Why this improves revenue readiness",
            "/free-business-review/?package=b2b-saas-soc2-ai-control-evidence",
            "/resources/global-ai-vendor-security-questionnaire-answer-source-map/",
            "/resources/global-b2b-saas-soc2-ai-control-evidence-checklist/b2b-saas-ai-control-evidence-risk-map.svg",
            "Demo visual for internal forwarding",
            "unsupported SOC 2 / security / compliance / procurement claims blocked",
            "/resources/global-b2b-saas-security-questionnaire-vs-grc-trust-center-tools-comparison/",
            "/services/cloud-security/",
            f"/resources/{SLUG}/b2b-saas-soc2-ai-control-evidence.csv",
        ]:
            self.assertIn(phrase, self.html)

    def test_csv_has_owner_source_review_and_claim_boundary_fields(self):
        self.assertEqual(len(self.rows), 8)
        self.assertEqual(
            set(self.rows[0]),
            {
                "control_question",
                "evidence_owner",
                "approved_source_artifact",
                "review_gate",
                "revenue_risk",
                "unsafe_claim_boundary",
            },
        )
        for row in self.rows:
            self.assertTrue(row["evidence_owner"])
            self.assertTrue(row["approved_source_artifact"])
            self.assertTrue(row["review_gate"])
            self.assertIn("Do not", row["unsafe_claim_boundary"])

    def test_truth_boundaries_prevent_fake_compliance_or_revenue_proof(self):
        for phrase in [
            "not a real SaaS company",
            "not a real customer",
            "not customer data",
            "not an audit report",
            "not auditor evidence",
            "not SOC 2 evidence",
            "not SOC 2 certification",
            "not ISO 27001 proof",
            "not GDPR proof",
            "not HIPAA proof",
            "not DPDP proof",
            "not security proof",
            "not privacy proof",
            "not compliance proof",
            "not legal advice",
            "not procurement advice",
            "not auditor advice",
            "not revenue proof",
            "not ranking proof",
            "not demand proof",
            "not lead proof",
            "not customer proof",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "real client results", "saved customers", "saved revenue"]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_json_ld_and_discovery_wiring_are_valid(self):
        docs = json_ld_documents(self.html)
        types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Dataset", types)
        self.assertIn("FAQPage", types)
        self.assertIn("ImageObject", types)
        dataset = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Dataset")
        self.assertEqual(dataset["url"], f"{URL}b2b-saas-soc2-ai-control-evidence.csv")
        image = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "ImageObject")
        self.assertEqual(image["contentUrl"], f"{URL}b2b-saas-ai-control-evidence-risk-map.svg")
        self.assertIn(f"/resources/{SLUG}/", self.resources)
        self.assertIn("B2B SaaS SOC 2 AI Control Evidence Checklist", self.resources)
        self.assertIn(URL, self.llms)
        self.assertIn("B2B SaaS SOC 2 AI control evidence", self.llms)
        self.assertIn(URL, self.sitemap)

    def test_demo_svg_is_forwardable_and_boundary_safe(self):
        svg = SVG.read_text(encoding="utf-8")
        for phrase in [
            "Demo B2B SaaS AI Control Evidence Risk Map",
            "Buyer asks",
            "Evidence map",
            "Approved answer",
            "Do not claim",
            "not SOC 2 evidence",
            "not procurement approval",
            "Owner-evidence layer",
        ]:
            self.assertIn(phrase, svg)


if __name__ == "__main__":
    unittest.main()
