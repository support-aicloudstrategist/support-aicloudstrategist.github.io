from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
PUBLICATION = ROOT / "publications" / "2026-09-02" / "ai-reply-triage-board.html"
MANIFEST = ROOT / "publications" / "2026-09-02" / "manifest.json"
PNG = ROOT / "publications" / "2026-09-02" / "ai-reply-triage-board.png"


def test_homepage_surfaces_latest_ai_reply_triage_board_publication():
    home = HOME.read_text(encoding="utf-8")
    publication = PUBLICATION.read_text(encoding="utf-8")

    href = "/publications/2026-09-02/ai-reply-triage-board.html"
    assert href in home
    assert "The AI Reply Triage Board" in home
    assert "<link rel='canonical' href='https://aicloudstrategist.com/publications/2026-09-02/ai-reply-triage-board.html'>" in publication
    assert "ai reply triage board" in publication.lower()
    assert "not legal, compliance, medical, financial" in publication


def test_evening_publication_has_infographic_and_two_daily_manifest_slots():
    manifest = MANIFEST.read_text(encoding="utf-8")
    assert '"slot": "morning"' in manifest
    assert '"slot": "evening"' in manifest
    assert "ai-task-intake-gate" in manifest
    assert "ai-reply-triage-board" in manifest
    assert PNG.exists()
    assert PNG.stat().st_size > 1000
