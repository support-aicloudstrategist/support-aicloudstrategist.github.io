import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
SITEMAP = ROOT / "sitemap.xml"
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}


class SeoFocusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = HOME.read_text(encoding="utf-8")
        cls.sitemap_root = ET.parse(SITEMAP).getroot()
        cls.urls = [node.text for node in cls.sitemap_root.findall(".//s:loc", NS)]
        cls.paths = [urlparse(url).path for url in cls.urls]

    def test_homepage_has_a_clear_primary_commercial_topic(self):
        self.assertIn(
            "<title>Enterprise AI Services &amp; Managed AI | AICloudStrategist</title>",
            self.home,
        )
        self.assertIn(
            "Build, govern and operate AI with confidence.",
            self.home,
        )
        self.assertIn('name="robots" content="index, follow, max-image-preview:large"', self.home)
        self.assertIn('property="og:title"', self.home)
        self.assertIn('name="twitter:card" content="summary_large_image"', self.home)
        self.assertEqual(self.home.count('<meta name="description"'), 1)
        self.assertEqual(len(re.findall(r'"@type"\s*:\s*"Organization"', self.home)), 1)
        self.assertEqual(len(re.findall(r'"@type"\s*:\s*"WebSite"', self.home)), 1)
        self.assertRegex(self.home, r'"@type"\s*:\s*"Service"')

    def test_sitemap_is_curated_unique_and_canonical(self):
        self.assertGreaterEqual(len(self.paths), 30)
        self.assertLessEqual(len(self.paths), 50)
        self.assertEqual(len(self.paths), len(set(self.paths)))
        forbidden = (
            "/api/",
            "/thank-you",
            "/simulated-",
            "/resources/verified-public-presence-authority-tracker/",
            "/resources/search-console-indexing-readiness/",
        )
        for path in self.paths:
            with self.subTest(path=path):
                self.assertFalse(path.endswith(".html"))
                self.assertFalse(any(token in path for token in forbidden))
                self.assertIsNone(
                    re.search(r"/publications/\d{4}-\d{2}-\d{2}/?$", path),
                    "date archive pages do not belong in the sitemap",
                )

    def test_sitemap_prioritizes_public_pillars_and_problem_led_paths(self):
        required = {
            "/",
            "/free-business-review/",
            "/services/ai-mlops/",
            "/services/ai-automation/",
            "/services/cloud-finops/",
            "/services/cloud-security/",
            "/services/devops-observability/",
            "/services/website-digital-presence/",
            "/services/lead-generation-seo/website-lead-capture/",
            "/services/workflow-automation/",
            "/ai-creative-studio/",
            "/growth-control-os/",
            "/trust-compliance/",
            "/resources/lead-follow-up-automation-guide/",
            "/resources/cloud-cost-optimization-finops-control/",
            "/resources/customer-problem-search/aws-cloud-bill-too-high/",
            "/resources/customer-problem-search/manual-work-wasting-staff-time/",
            "/resources/customer-problem-search/clinic-not-getting-patients/",
            "/resources/customer-problem-search/business-compliance-privacy-confusion/",
            "/resources/customer-problem-search/find-right-consultant-vendor/",
            "/resources/global-accounting-firm-tax-season-client-intake-follow-up-checklist/",
            "/resources/customer-problem-search/factory-manual-work-reduce/",
            "/resources/global-hotel-direct-booking-enquiry-follow-up-checklist/",
            "/resources/customer-problem-search/restaurant-local-service-customers-increase/",
            "/resources/uae-saas-cloud-trust-finops-readiness-checklist/",
            "/healthcare-growthos/",
            "/resources/us-clinic-ai-receptionist-hipaa-patient-follow-up-checklist/",
            "/resources/us-clinic-ai-receptionist-vs-patient-engagement-platforms-comparison/",
            "/resources/us-clinic-ai-receptionist-hipaa-patient-follow-up-diagnostic-package/",
            "/resources/us-clinic-top-5-consideration-proof-pack/",
            "/case-studies/",
            "/case-studies/aicloudstrategist-geo-turnaround/",
        }
        self.assertTrue(required.issubset(set(self.paths)))

    def test_sitemap_urls_map_to_indexable_local_canonicals(self):
        for path in self.paths:
            if path == "/":
                page = ROOT / "index.html"
            elif path.endswith("/"):
                page = ROOT / path.lstrip("/") / "index.html"
            else:
                candidates = [
                    ROOT / path.lstrip("/"),
                    ROOT / f"{path.lstrip('/')}.html",
                    ROOT / path.lstrip("/") / "index.html",
                ]
                page = next((candidate for candidate in candidates if candidate.is_file()), candidates[0])
            with self.subTest(path=path):
                self.assertTrue(page.is_file(), f"missing local page for {path}")
                html = page.read_text(encoding="utf-8")
                self.assertNotRegex(html, r'<meta[^>]+name=["\']robots["\'][^>]+noindex')
                canonical = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', html)
                self.assertIsNotNone(canonical, f"missing canonical for {path}")
                self.assertEqual(canonical.group(1), f"https://aicloudstrategist.com{path}")

    def test_cloud_finops_legacy_landing_page_consolidates_to_authority_route(self):
        html = (ROOT / "cloud-trust-finops" / "index.html").read_text(encoding="utf-8")
        redirects = (ROOT / "_redirects").read_text(encoding="utf-8")
        self.assertIn(
            '<link rel="canonical" href="https://aicloudstrategist.com/services/cloud-finops/">',
            html,
        )
        self.assertRegex(
            redirects,
            r"(?m)^/cloud-trust-finops/\s+/services/cloud-finops/\s+301$",
        )

    def test_simulated_cases_and_internal_status_pages_are_noindex(self):
        simulated = sorted((ROOT / "case-studies").glob("simulated-*/index.html"))
        self.assertGreater(len(simulated), 10)
        internal = [
            ROOT / "resources" / "verified-public-presence-authority-tracker" / "index.html",
            ROOT / "resources" / "search-console-indexing-readiness" / "index.html",
        ]
        for page in simulated + internal:
            with self.subTest(page=str(page.relative_to(ROOT))):
                html = page.read_text(encoding="utf-8")
                self.assertRegex(
                    html,
                    r'<meta\s+name=["\']robots["\']\s+content=["\']noindex,\s*follow["\']',
                )


if __name__ == "__main__":
    unittest.main()
