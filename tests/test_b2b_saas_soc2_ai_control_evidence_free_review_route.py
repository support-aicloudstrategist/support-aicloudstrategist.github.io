from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FREE_REVIEW = ROOT / "free-business-review" / "index.html"
FREE_REVIEW_FLAT = ROOT / "free-business-review.html"
RESOURCE = "/resources/global-b2b-saas-soc2-ai-control-evidence-checklist/"


def test_free_review_surfaces_b2b_saas_soc2_ai_control_evidence_route():
    html = FREE_REVIEW.read_text(encoding="utf-8")
    flat = FREE_REVIEW_FLAT.read_text(encoding="utf-8")

    assert html == flat
    assert 'data-review-route="b2b-saas-soc2-ai-control-evidence"' in html
    assert "Healthtech / B2B SaaS" in html
    assert "AI Cloud Trust + SOC 2 AI control evidence review" in html
    assert RESOURCE in html
    assert "See the B2B SaaS SOC 2 AI control evidence checklist" in html
    assert "Request a fixed-scope diagnostic" not in html
