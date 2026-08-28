from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
PUBLICATION = ROOT / "publications" / "2026-08-28" / "automation-readiness-traffic-light.html"


def test_homepage_surfaces_latest_automation_readiness_traffic_light_publication():
    home = HOME.read_text(encoding="utf-8")
    publication = PUBLICATION.read_text(encoding="utf-8")

    href = "/publications/2026-08-28/automation-readiness-traffic-light.html"
    assert href in home
    assert "automation readiness traffic light" in home
    assert "<link rel='canonical' href='https://aicloudstrategist.com/publications/2026-08-28/automation-readiness-traffic-light.html'>" in publication
