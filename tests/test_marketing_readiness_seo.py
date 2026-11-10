from pathlib import Path
import json
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ROUTES = {
    "https://aicloudstrategist.com/": ROOT / "index.html",
    "https://aicloudstrategist.com/cloud-ai-cost-governance-diagnostic/": ROOT / "cloud-ai-cost-governance-diagnostic" / "index.html",
    "https://aicloudstrategist.com/resources/cloud-ai-economics-decision-pack/": ROOT / "resources" / "cloud-ai-economics-decision-pack" / "index.html",
    "https://aicloudstrategist.com/resources/": ROOT / "resources" / "index.html",
    "https://aicloudstrategist.com/about/": ROOT / "about" / "index.html",
    "https://aicloudstrategist.com/trust-data-handling/": ROOT / "trust-data-handling" / "index.html",
    "https://aicloudstrategist.com/request-fit-review/": ROOT / "request-fit-review" / "index.html",
    "https://aicloudstrategist.com/company-details/": ROOT / "company-details" / "index.html",
    "https://aicloudstrategist.com/privacy": ROOT / "privacy.html",
    "https://aicloudstrategist.com/terms": ROOT / "terms.html",
}


class MarketingReadinessSeoContractTests(unittest.TestCase):
    def test_sitemap_is_unique_and_matches_launch_routes(self):
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        values = [node.text for node in root.findall(".//s:loc", ns)]
        self.assertEqual(len(values), len(set(values)))
        self.assertEqual(set(values), set(ROUTES))

    def test_every_indexed_page_has_canonical_metadata_and_single_h1(self):
        for canonical, path in ROUTES.items():
            with self.subTest(canonical=canonical):
                self.assertTrue(path.exists())
                source = path.read_text(encoding="utf-8")
                self.assertEqual(source.count(f'<link rel="canonical" href="{canonical}">'), 1)
                self.assertEqual(len(re.findall(r"<title>.+?</title>", source, re.I | re.S)), 1)
                self.assertEqual(len(re.findall(r'<meta name="description" content="[^"]{50,180}">', source, re.I)), 1)
                self.assertEqual(len(re.findall(r"<h1[^>]*>.*?</h1>", source, re.I | re.S)), 1)
                robots_meta = re.search(r'<meta name="robots"[^>]+>', source, re.I)
                self.assertIsNotNone(robots_meta)
                if robots_meta is not None:
                    self.assertNotIn('noindex', robots_meta.group(0).lower())

    def test_structured_data_is_valid_on_launch_pages(self):
        for canonical, path in ROUTES.items():
            source = path.read_text(encoding="utf-8")
            for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.I | re.S):
                with self.subTest(canonical=canonical):
                    json.loads(block)

    def test_robots_and_llms_describe_one_service(self):
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("Sitemap: https://aicloudstrategist.com/sitemap.xml", robots)
        self.assertIn("Disallow: /api/", robots)
        self.assertIn("Cloud & AI Cost Governance Diagnostic", llms)
        self.assertIn("Request a Cloud & AI Cost Fit Review", llms)
        for forbidden in ("Production AI Readiness", "two focused engagement paths", "/free-business-review/"):
            self.assertNotIn(forbidden, llms)

    def test_old_high_value_urls_have_specific_redirects(self):
        redirects = (ROOT / "_redirects").read_text(encoding="utf-8")
        expected = {
            "/services/cloud-ai-economics/": "/cloud-ai-cost-governance-diagnostic/",
            "/services/cloud-finops/": "/cloud-ai-cost-governance-diagnostic/",
            "/cloud-trust-finops/": "/cloud-ai-cost-governance-diagnostic/",
            "/portfolio/cloud-ai-economics-sample/": "/resources/cloud-ai-economics-decision-pack/",
            "/free-business-review/": "/request-fit-review/",
            "/pricing/": "/cloud-ai-cost-governance-diagnostic/",
            "/contact": "/request-fit-review/",
            "/resources/ai-cost-savings-claim-boundary-worksheet/": "/resources/cloud-ai-economics-decision-pack/",
            "/resources/global-ai-agent-cost-overrun-owner-evidence-checklist/": "/cloud-ai-cost-governance-diagnostic/",
            "/resources/global-enterprise-ai-cost-anomaly-approval-runbook/": "/cloud-ai-cost-governance-diagnostic/",
            "/resources/kubernetes-namespace-cost-owner-dashboard-demo/": "/resources/cloud-ai-economics-decision-pack/",
        }
        for old, new in expected.items():
            self.assertRegex(redirects, re.compile(rf"^{re.escape(old)}\s+{re.escape(new)}\s+301$", re.M))

    def test_edge_indexability_is_limited_to_launch_routes(self):
        source = (ROOT / "functions" / "_middleware.ts").read_text(encoding="utf-8")
        match = re.search(r"const indexableExact = new Set\(\[(.*?)\]\);", source, re.S)
        self.assertIsNotNone(match)
        indexable = match.group(1) if match else ""
        for route in ("/pricing", "/free-business-review", "/portfolio", "/services/production-ai-readiness", "/services/cloud-ai-economics"):
            self.assertNotIn(f'"{route}"', indexable)
        for route in ("/cloud-ai-cost-governance-diagnostic", "/request-fit-review", "/trust-data-handling"):
            self.assertIn(f'"{route}"', indexable)

    def test_edge_middleware_retires_legacy_documents_and_fixes_extensionless_html(self):
        source = (ROOT / "functions" / "_middleware.ts").read_text(encoding="utf-8")
        self.assertIn("legacyRedirects", source)
        self.assertIn('headers.set("Content-Type", "text/html; charset=utf-8")', source)
        self.assertIn('status: 301', source)
        self.assertIn('status: 404', source)
        self.assertIn('X-Robots-Tag", "noindex, nofollow, noarchive', source)

    def test_local_preview_does_not_send_analytics_events(self):
        source = (ROOT / "js" / "aics-analytics-shim.js").read_text(encoding="utf-8")
        self.assertIn("location.hostname==='127.0.0.1'", source)
        self.assertIn("location.hostname==='localhost'", source)

    def test_brand_links_keep_visible_text_as_accessible_name(self):
        for canonical, path in ROUTES.items():
            source = path.read_text(encoding="utf-8")
            with self.subTest(canonical=canonical):
                for tag in re.findall(r'<a[^>]*class="[^"]*brand[^"]*"[^>]*>', source, re.I):
                    self.assertNotIn('aria-label=', tag.lower())

    def test_security_headers_and_404_are_release_aligned(self):
        headers = (ROOT / "_headers").read_text(encoding="utf-8")
        for header in ("Content-Security-Policy", "Strict-Transport-Security", "X-Content-Type-Options", "X-Frame-Options", "Referrer-Policy"):
            self.assertIn(header, headers)
        page404 = (ROOT / "404.html").read_text(encoding="utf-8")
        self.assertIn('/css/cost-governance.css?v=20261110', page404)
        self.assertIn('href="/cloud-ai-cost-governance-diagnostic/"', page404)
        self.assertIn('href="/request-fit-review/"', page404)
        self.assertNotIn("Production AI", page404)


if __name__ == "__main__":
    unittest.main()
