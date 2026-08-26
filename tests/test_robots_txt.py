from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROBOTS = ROOT / "robots.txt"
SITEMAP = ROOT / "sitemap.xml"


def test_robots_txt_allows_indexing_and_advertises_sitemap():
    robots = ROBOTS.read_text(encoding="utf-8")

    assert "User-agent: *" in robots
    assert "Allow: /" in robots
    assert "Disallow: /api/" in robots
    assert "Disallow: /preview/" in robots
    assert "Disallow: /resources/" not in robots
    assert "Disallow: /services/" not in robots
    assert "Sitemap: https://aicloudstrategist.com/sitemap.xml" in robots


def test_robots_sitemap_target_exists_locally():
    sitemap = SITEMAP.read_text(encoding="utf-8")
    assert "<urlset" in sitemap
    assert "https://aicloudstrategist.com/" in sitemap
