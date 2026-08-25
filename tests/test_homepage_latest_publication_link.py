from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
PUBLICATION = ROOT / "publications" / "2026-08-25" / "ai-vendor-access-review-board.html"


def test_homepage_surfaces_latest_ai_vendor_access_publication():
    home = HOME.read_text(encoding="utf-8")
    publication = PUBLICATION.read_text(encoding="utf-8")

    href = "/publications/2026-08-25/ai-vendor-access-review-board.html"
    assert href in home
    assert "The AI Vendor Access Review Board" in home
    assert "Public educational asset · 2026-08-25" in home
    assert "<link rel='canonical' href='https://aicloudstrategist.com/publications/2026-08-25/ai-vendor-access-review-board.html'>" in publication
