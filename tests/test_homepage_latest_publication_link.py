from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
PUBLICATION = ROOT / "publications" / "2026-08-31" / "ai-customer-promise-risk-pause.html"


def test_homepage_surfaces_latest_ai_customer_promise_risk_pause_publication():
    home = HOME.read_text(encoding="utf-8")
    publication = PUBLICATION.read_text(encoding="utf-8")

    href = "/publications/2026-08-31/ai-customer-promise-risk-pause.html"
    assert href in home
    assert "AI customer promise risk pause" in home
    assert "<link rel='canonical' href='https://aicloudstrategist.com/publications/2026-08-31/ai-customer-promise-risk-pause.html'>" in publication
    assert "customer promise risk pause" in publication.lower()
