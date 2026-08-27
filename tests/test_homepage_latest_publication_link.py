from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
PUBLICATION = ROOT / "publications" / "2026-08-27" / "ai-prompt-scope-box.html"


def test_homepage_surfaces_latest_ai_prompt_scope_box_publication():
    home = HOME.read_text(encoding="utf-8")
    publication = PUBLICATION.read_text(encoding="utf-8")

    href = "/publications/2026-08-27/ai-prompt-scope-box.html"
    assert href in home
    assert "The AI Prompt Scope Box" in home
    assert "Public educational asset · 2026-08-27" in home
    assert "<link rel='canonical' href='https://aicloudstrategist.com/publications/2026-08-27/ai-prompt-scope-box.html'>" in publication
