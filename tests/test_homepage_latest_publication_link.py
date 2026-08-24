from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
PUBLICATION = ROOT / "publications" / "2026-08-24" / "ai-reply-safety-stoplight.html"


def test_homepage_surfaces_latest_ai_reply_safety_publication():
    home = HOME.read_text(encoding="utf-8")
    publication = PUBLICATION.read_text(encoding="utf-8")

    href = "/publications/2026-08-24/ai-reply-safety-stoplight.html"
    assert href in home
    assert "The AI Reply Safety Stoplight" in home
    assert "Public educational asset · 2026-08-24" in home
    assert "<link rel='canonical' href='https://aicloudstrategist.com/publications/2026-08-24/ai-reply-safety-stoplight.html'>" in publication
