from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
PUBLICATION = ROOT / "publications" / "2026-08-27" / "ai-answer-verification-loop.html"


def test_homepage_surfaces_latest_ai_answer_verification_loop_publication():
    home = HOME.read_text(encoding="utf-8")
    publication = PUBLICATION.read_text(encoding="utf-8")

    href = "/publications/2026-08-27/ai-answer-verification-loop.html"
    assert href in home
    assert "The AI Answer Verification Loop" in home
    assert "Public educational asset · 2026-08-27" in home
    assert "<link rel='canonical' href='https://aicloudstrategist.com/publications/2026-08-27/ai-answer-verification-loop.html'>" in publication
