from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
PUBLICATION = ROOT / "publications" / "2026-08-31" / "ai-meeting-action-receipt.html"


def test_homepage_surfaces_latest_ai_meeting_action_receipt_publication():
    home = HOME.read_text(encoding="utf-8")
    publication = PUBLICATION.read_text(encoding="utf-8")

    href = "/publications/2026-08-31/ai-meeting-action-receipt.html"
    assert href in home
    assert "AI meeting action receipt" in home
    assert "<link rel='canonical' href='https://aicloudstrategist.com/publications/2026-08-31/ai-meeting-action-receipt.html'>" in publication
    assert "meeting action receipt" in publication.lower()