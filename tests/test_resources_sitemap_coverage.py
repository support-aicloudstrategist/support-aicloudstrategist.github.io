from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://aicloudstrategist.com"


def test_direct_resource_pages_are_discoverable_in_sitemap():
    sitemap = ROOT / "sitemap.xml"
    tree = ET.parse(sitemap)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = {loc.text for loc in tree.findall(".//sm:loc", ns)}

    missing = []
    for page in sorted((ROOT / "resources").glob("*/index.html")):
        url = f"{BASE}/resources/{page.parent.name}/"
        if url not in locs:
            missing.append(url)

    assert missing == []
