from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://aicloudstrategist.com"
ROBOTS_RE = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)["\']', re.I)


def sitemap_locs():
    sitemap = ROOT / "sitemap.xml"
    tree = ET.parse(sitemap)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return {loc.text for loc in tree.findall(".//sm:loc", ns)}


def is_noindex(page: Path) -> bool:
    source = page.read_text(encoding="utf-8", errors="ignore")
    robots = ROBOTS_RE.search(source)
    return bool(robots and "noindex" in robots.group(1).lower())


def test_direct_resource_pages_are_discoverable_in_sitemap():
    locs = sitemap_locs()

    missing = []
    for page in sorted((ROOT / "resources").glob("*/index.html")):
        if is_noindex(page):
            continue
        url = f"{BASE}/resources/{page.parent.name}/"
        if url not in locs:
            missing.append(url)

    assert missing == []


def test_publication_support_urls_are_preserved_in_sitemap():
    locs = sitemap_locs()

    for url in [
        "https://support-aicloudstrategist.github.io/publications/2026-09-28/",
        "https://support-aicloudstrategist.github.io/publications/2026-09-28/meeting-notes-crm-handoff-gate.html",
        "https://support-aicloudstrategist.github.io/publications/2026-09-28/meeting-notes-crm-handoff-gate.png",
    ]:
        assert url in locs
