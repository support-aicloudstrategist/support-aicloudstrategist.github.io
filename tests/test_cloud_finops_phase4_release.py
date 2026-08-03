import json
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
SERVICE_PATH = "/services/cloud-finops/"
PACK_PATH = "/resources/cloud-ai-economics-decision-pack/"
SERVICE_URL = f"https://aicloudstrategist.com{SERVICE_PATH}"
PACK_URL = f"https://aicloudstrategist.com{PACK_PATH}"


def source(path):
    return (ROOT / path).read_text(encoding="utf-8")


def json_ld_documents(html):
    documents = []
    for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S):
        documents.append(json.loads(raw))
    return documents


def graph_nodes(html):
    nodes = []
    for document in json_ld_documents(html):
        if isinstance(document, dict) and isinstance(document.get("@graph"), list):
            nodes.extend(document["@graph"])
        else:
            nodes.append(document)
    return nodes


class CloudFinOpsPhaseFourReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = source("services/cloud-finops/index.html")
        cls.pack = source("resources/cloud-ai-economics-decision-pack/index.html")
        cls.redirects = source("_redirects")
        cls.llms = source("llms.txt")
        cls.resources = source("resources/index.html")
        cls.services = source("services/index.html")
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        cls.sitemap_urls = [node.text for node in root.findall(".//s:loc", ns)]

    def test_flagship_metadata_matches_approved_enterprise_authority(self):
        self.assertIn("Enterprise FinOps Advisory", self.service)
        self.assertIn('<meta name="robots" content="index, follow, max-image-preview:large">', self.service)
        self.assertIn(f'<link rel="canonical" href="{SERVICE_URL}">', self.service)
        self.assertIn('<meta property="og:type" content="website">', self.service)
        self.assertIn(f'<meta property="og:url" content="{SERVICE_URL}">', self.service)
        self.assertIn('<meta property="og:site_name" content="AICloudStrategist">', self.service)
        self.assertIn('<meta name="twitter:title"', self.service)
        self.assertIn('<meta name="twitter:description"', self.service)
        self.assertNotIn("for growing teams", self.service[:6000].lower())
        self.assertNotIn("Cloud FinOps &amp; Cost Optimization Services", self.service[:1500])

    def test_flagship_json_ld_is_valid_connected_and_bounded(self):
        nodes = graph_nodes(self.service)
        by_type = {node.get("@type"): node for node in nodes if isinstance(node, dict)}
        for required_type in ["Organization", "WebSite", "WebPage", "BreadcrumbList", "Service"]:
            self.assertIn(required_type, by_type)
        service = by_type["Service"]
        self.assertEqual(service["name"], "Enterprise FinOps Advisory — Cloud & AI Economics")
        self.assertEqual(service["url"], SERVICE_URL)
        self.assertEqual(service["provider"]["@id"], "https://aicloudstrategist.com/#organization")
        self.assertEqual(service["areaServed"], "Global")
        self.assertIn("Cloud & AI Economics", service["serviceType"])
        self.assertNotIn("Offer", json.dumps(nodes))
        self.assertNotIn("AggregateRating", json.dumps(nodes))
        self.assertNotIn("Review", json.dumps(nodes))

    def test_decision_pack_is_an_indexable_connected_creative_work(self):
        self.assertIn('<meta name="robots" content="index, follow, max-image-preview:large">', self.pack)
        self.assertIn(f'<link rel="canonical" href="{PACK_URL}">', self.pack)
        self.assertIn('<meta property="og:site_name" content="AICloudStrategist">', self.pack)
        self.assertIn(f'<meta property="og:url" content="{PACK_URL}">', self.pack)
        self.assertIn('<meta name="twitter:title"', self.pack)
        self.assertNotIn(
            '<aside class="pack-callout',
            self.pack,
            "decision evidence notes must not create nested complementary landmarks",
        )
        nodes = graph_nodes(self.pack)
        by_type = {node.get("@type"): node for node in nodes if isinstance(node, dict)}
        for required_type in ["WebPage", "BreadcrumbList", "CreativeWork"]:
            self.assertIn(required_type, by_type)
        work = by_type["CreativeWork"]
        self.assertEqual(work["isPartOf"]["@id"], f"{SERVICE_URL}#service")
        self.assertEqual(work["encoding"]["contentUrl"], "https://aicloudstrategist.com/downloads/cloud-ai-economics-decision-pack.pdf")
        self.assertIn("synthetic", work["abstract"].lower())

    def test_sitemap_assigns_single_service_authority_and_indexes_pack(self):
        self.assertIn(SERVICE_URL, self.sitemap_urls)
        self.assertIn(PACK_URL, self.sitemap_urls)
        self.assertNotIn("https://aicloudstrategist.com/services/cloud-finops/cloud-cost-review/", self.sitemap_urls)
        self.assertNotIn("https://aicloudstrategist.com/cloud-trust-finops/", self.sitemap_urls)
        self.assertEqual(len(self.sitemap_urls), len(set(self.sitemap_urls)))

    def test_conflicting_legacy_routes_permanently_consolidate_to_flagship(self):
        expected = {
            "/services/cloud-finops/cloud-cost-review/": SERVICE_PATH,
            "/cloud-trust-finops/": SERVICE_PATH,
            "/ai-cloud-cost-review/": SERVICE_PATH,
            "/ai-cloud-cost-efficiency/": SERVICE_PATH,
            "/cloud-cost": SERVICE_PATH,
            "/finops": SERVICE_PATH,
        }
        rules = {}
        for line in self.redirects.splitlines():
            parts = line.strip().split()
            if len(parts) == 3 and not line.lstrip().startswith("#"):
                rules[parts[0]] = (parts[1], parts[2])
        for old, new in expected.items():
            self.assertEqual(rules.get(old), (new, "301"), old)

    def test_llm_and_hub_discovery_use_approved_category_and_pack(self):
        self.assertIn(f"Enterprise FinOps Advisory — Cloud & AI Economics: {SERVICE_URL}", self.llms)
        self.assertIn(f"Cloud & AI Economics Decision Pack: {PACK_URL}", self.llms)
        self.assertNotIn("Cross-discipline Cloud Trust & FinOps diagnostic", self.llms)
        self.assertIn(f'href="{PACK_PATH}"', self.resources)
        self.assertIn("Cloud &amp; AI Economics Decision Pack", self.resources)
        self.assertIn(f'href="{SERVICE_PATH}"', self.services)
        self.assertIn("Enterprise FinOps Advisory", self.services)

    def test_release_manifest_declares_routes_assets_and_production_hold(self):
        manifest = json.loads(source("release/cloud-finops-phase4-release.json"))
        self.assertEqual(manifest["authority_route"], SERVICE_PATH)
        self.assertEqual(manifest["evidence_route"], PACK_PATH)
        self.assertFalse(manifest["production_deployment_authorized"])
        self.assertEqual(manifest["required_routes"][SERVICE_PATH]["canonical"], SERVICE_URL)
        self.assertEqual(manifest["required_routes"][PACK_PATH]["canonical"], PACK_URL)
        for asset in manifest["required_assets"]:
            self.assertTrue((ROOT / asset).is_file(), asset)
        self.assertEqual(manifest["legacy_redirects"]["/cloud-trust-finops/"], SERVICE_PATH)

    def test_release_verifier_executes_successfully(self):
        import subprocess
        result = subprocess.run(
            ["python3", "scripts/verify_cloud_finops_release.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
