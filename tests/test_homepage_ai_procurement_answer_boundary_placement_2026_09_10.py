from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
URL = "/publications/2026-09-10/ai-procurement-answer-boundary-card.html"


def test_ai_procurement_answer_boundary_card_is_in_evidence_grid_not_hero():
    html = INDEX.read_text(encoding="utf-8")
    assert html.count(URL) == 1
    assert 'data-homepage-publication="ai-procurement-answer-boundary-card"' in html

    hero_end = html.index('<section class="section ea-business-system" id="what-we-do">')
    evidence_start = html.index('<section class="section ea-evidence" id="evidence">')
    evidence_end = html.index('<section class="section ea-engagement" id="engagement">', evidence_start)

    assert URL not in html[:hero_end]
    assert URL in html[evidence_start:evidence_end]
    assert html.index(URL) > html.index('data-homepage-publication="clinic-intake-ai-safety-card"')
