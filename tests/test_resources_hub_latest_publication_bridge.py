from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / "resources" / "index.html"
PUBLICATION = ROOT / "publications" / "2026-09-03" / "ai-procurement-answer-boundary-card.html"
CSV = ROOT / "publications" / "2026-09-03" / "ai-procurement-answer-boundary-card.csv"


def test_resources_hub_surfaces_latest_procurement_answer_boundary_publication():
    html = RESOURCES.read_text(encoding="utf-8")
    assert 'data-featured-publication="ai-procurement-answer-boundary-card"' in html
    assert "/publications/2026-09-03/ai-procurement-answer-boundary-card.html" in html
    assert "/publications/2026-09-03/ai-procurement-answer-boundary-card.csv" in html
    assert "separating answerable procurement questions from proof-needed" in html


def test_featured_publication_assets_exist_and_have_safe_boundary_language():
    page = PUBLICATION.read_text(encoding="utf-8")
    csv = CSV.read_text(encoding="utf-8")
    assert "The AI Procurement Answer Boundary Card" in page
    assert "not legal" in page
    assert "procurement-approval" in page
    assert "question_area,buyer_question,answer_route" in csv
