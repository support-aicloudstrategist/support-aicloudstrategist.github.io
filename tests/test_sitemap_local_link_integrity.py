from pathlib import Path
from urllib.parse import urlsplit
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_HOST = "aicloudstrategist.com"
SITEMAP = ROOT / "sitemap.xml"


class SitemapLocalLinkIntegrityTests(unittest.TestCase):
    def test_sitemap_is_well_formed_unique_and_maps_to_published_assets(self):
        source = SITEMAP.read_text(encoding="utf-8")
        root = ET.fromstring(source)
        urls = [
            element.text.strip()
            for element in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
            if element.text
        ]
        self.assertGreaterEqual(len(urls), 50)
        self.assertEqual(len(urls), len(set(urls)), "sitemap contains duplicate URLs")

        missing = []
        for raw_url in urls:
            parsed = urlsplit(raw_url)
            self.assertEqual(parsed.scheme, "https", raw_url)
            self.assertEqual(parsed.netloc, CANONICAL_HOST, raw_url)
            self.assertFalse(parsed.query or parsed.fragment, raw_url)
            route = parsed.path or "/"
            candidates = (
                [ROOT / route.lstrip("/") / "index.html"]
                if route.endswith("/")
                else [ROOT / route.lstrip("/"), ROOT / route.lstrip("/") / "index.html"]
            )
            if not any(candidate.is_file() for candidate in candidates):
                missing.append(raw_url)

        self.assertEqual([], missing, f"sitemap contains unpublished local routes: {missing}")

    def test_sitemap_has_no_redirect_sources(self):
        redirects = (ROOT / "_redirects").read_text(encoding="utf-8")
        redirect_sources = {
            match.group("source")
            for match in re.finditer(
                r"^(?P<source>/\S+)\s+\S+\s+30[18](?:\s|$)", redirects, re.MULTILINE
            )
        }
        sitemap_urls = {
            urlsplit(element.text.strip()).path
            for element in ET.fromstring(SITEMAP.read_text(encoding="utf-8")).findall(
                "{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
            )
            if element.text
        }
        self.assertEqual(set(), redirect_sources & sitemap_urls)


if __name__ == "__main__":
    unittest.main()
