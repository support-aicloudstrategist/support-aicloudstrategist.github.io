import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "customer-problem-search/aws-cloud-bill-too-high"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "aws-cloud-bill-owner-evidence-intake.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
CSV_URL = f"{URL}aws-cloud-bill-owner-evidence-intake.csv"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


class AwsCloudBillOwnerEvidenceIntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
        cls.llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    def test_page_links_downloadable_buyer_safe_intake(self):
        self.assertIn('href="/resources/customer-problem-search/aws-cloud-bill-too-high/aws-cloud-bill-owner-evidence-intake.csv"', self.html)
        self.assertIn("Download the buyer-safe cloud bill evidence intake CSV", self.html)
        self.assertIn(CSV_URL, self.llms)
        self.assertIn(URL, self.sitemap)

    def test_csv_has_owner_decision_and_claim_boundary_fields(self):
        self.assertEqual(len(self.rows), 6)
        self.assertEqual(
            set(self.rows[0]),
            {
                "evidence_area",
                "what_to_collect",
                "acceptable_redaction",
                "owner_to_confirm",
                "decision_boundary",
            },
        )
        for row in self.rows:
            self.assertTrue(row["what_to_collect"])
            self.assertTrue(row["acceptable_redaction"])
            self.assertTrue(row["owner_to_confirm"])
            self.assertTrue(row["decision_boundary"])
        boundaries = " ".join(row["decision_boundary"].lower() for row in self.rows)
        self.assertIn("no savings roi", boundaries)
        self.assertIn("production", boundaries)

    def test_dataset_json_ld_describes_csv_without_fake_claims(self):
        docs = json_ld_documents(self.html)
        graph_docs = [doc for doc in docs if isinstance(doc, dict) and "@graph" in doc]
        graph = graph_docs[0]["@graph"]
        dataset = next(item for item in graph if item.get("@type") == "Dataset")
        self.assertEqual(dataset["url"], CSV_URL)
        self.assertIn("Buyer-safe cloud bill evidence intake", dataset["description"])
        for forbidden in ["guaranteed savings", "saved ", "trusted by", "verified client result"]:
            self.assertNotIn(forbidden, self.html.lower())


if __name__ == "__main__":
    unittest.main()
