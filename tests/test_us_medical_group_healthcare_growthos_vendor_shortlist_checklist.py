import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-medical-group-healthcare-growthos-vendor-shortlist-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / f"{SLUG}.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def graph_nodes(docs):
    nodes = []
    for doc in docs:
        if isinstance(doc, dict) and isinstance(doc.get("@graph"), list):
            nodes.extend(doc["@graph"])
        else:
            nodes.append(doc)
    return nodes


class UsMedicalGroupHealthcareGrowthosVendorShortlistChecklistTests(unittest.TestCase):
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
        self.assertIn("US Medical Group Healthcare GrowthOS Vendor Shortlist Checklist", self.html)

    def test_buyer_language_and_competitor_context_exist(self):
        for phrase in [
            "Healthcare GrowthOS vendor shortlist",
            "Patient GrowthOS for medical groups",
            "AI medical receptionist comparison",
            "missed patient calls",
            "front-office automation",
            "HIPAA AI vendor risk",
            "PHI/ePHI boundary",
            "BAA/subprocessor evidence",
            "SOC 2/HITRUST readiness",
            "cloud cost optimization for healthcare",
            "Phreesia",
            "Luma Health",
            "NexHealth",
            "Weave",
            "ModMed/Klara",
            "Solutionreach",
            "Relatient",
            "Artera",
            "Hyro",
            "Assort Health",
            "Notable",
            "CloudZero",
            "IBM Apptio Cloudability",
            "Vantage",
            "Why this improves top-3/top-5 consideration",
        ]:
            self.assertIn(phrase, self.html)

    def test_csv_has_expected_shortlist_fields(self):
        self.assertEqual(len(self.rows), 8)
        self.assertEqual(
            set(self.rows[0]),
            {
                "shortlist_area",
                "buyer_question",
                "evidence_to_request",
                "owner",
                "functional_alternatives",
                "aics_position",
                "unsafe_claim_boundary",
            },
        )
        for row in self.rows:
            self.assertTrue(row["owner"])
            self.assertIn("AICS", row["aics_position"])
            self.assertIn("Do not", row["unsafe_claim_boundary"])

    def test_truth_boundaries_prevent_fake_proof(self):
        for phrase in [
            "not a real US medical group",
            "not patient data",
            "not PHI",
            "not ePHI",
            "not claims data",
            "not production data",
            "not a testimonial",
            "not a logo claim",
            "not a certification",
            "not HIPAA compliance proof",
            "not SOC 2 compliance proof",
            "not HITRUST compliance proof",
            "not BAA evidence",
            "not legal advice",
            "not privacy advice",
            "not security advice",
            "not clinical advice",
            "not medical advice",
            "not billing advice",
            "not coding advice",
            "not payer advice",
            "not procurement advice",
            "not audit advice",
            "not savings evidence",
            "not ROI evidence",
            "not appointment-growth evidence",
            "not no-show reduction evidence",
            "not patient-outcome evidence",
            "not lead evidence",
            "not customer evidence",
            "not revenue evidence",
            "not ranking evidence",
            "No outreach was sent",
        ]:
            self.assertIn(phrase, self.html)
        for forbidden in ["trusted by", "guaranteed compliance", "hipaa certified", "real client results", "saved "]:
            self.assertNotIn(forbidden, self.html.lower())

    def test_json_ld_and_discovery_wiring_are_valid(self):
        docs = json_ld_documents(self.html)
        nodes = graph_nodes(docs)
        types = {node.get("@type") for node in nodes if isinstance(node, dict)}
        doc_types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
        self.assertIn("Article", types)
        self.assertIn("Dataset", doc_types)
        self.assertIn("FAQPage", doc_types)
        article = next(node for node in nodes if isinstance(node, dict) and node.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"], URL)
        self.assertEqual(article["dateModified"], "2026-08-28")
        path = f"/resources/{SLUG}/"
        self.assertIn(path, self.resources)
        self.assertIn(path, self.builder)
        self.assertIn(URL, self.sitemap)
        self.assertIn(f"US medical group Healthcare GrowthOS vendor shortlist checklist: {URL}", self.llms)
        self.assertEqual(self.html.count('data-aics-navigation-mount'), 1)
        self.assertEqual(self.html.count('data-aics-global-footer'), 1)


if __name__ == "__main__":
    unittest.main()
