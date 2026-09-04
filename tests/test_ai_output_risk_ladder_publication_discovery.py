from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-04"
SLUG = "ai-output-risk-ladder"
URL = f"https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html"
CSV_URL = f"https://aicloudstrategist.com/publications/{DATE}/{SLUG}.csv"
PATH = f"/publications/{DATE}/{SLUG}.html"
CSV_PATH = f"/publications/{DATE}/{SLUG}.csv"


def test_resource_hub_features_ai_output_risk_ladder_publication():
    html = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert 'data-featured-publication="ai-output-risk-ladder"' in html
    assert PATH in html
    assert CSV_PATH in html
    assert "Featured: The AI Output Risk Ladder" in html
    assert "needs owner review, or must stop before touching customers, money" in html


def test_llms_txt_routes_ai_output_risk_ladder_for_answer_engines():
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in llms
    assert CSV_URL in llms
    assert "safe educational AI output risk ladder" in llms
    assert "reusable worksheet for use, review, and stop rules" in llms


def test_ai_output_risk_ladder_assets_are_indexable_and_claim_safe():
    page = (ROOT / "publications" / DATE / f"{SLUG}.html").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    csv = (ROOT / "publications" / DATE / f"{SLUG}.csv").read_text(encoding="utf-8")
    assert f"<loc>{URL}</loc>" in sitemap
    assert f"<link rel='canonical' href='{URL}'>" in page
    assert "level,name,use,review,stop" in csv
    assert "customer-result" in page
    assert "not legal, compliance, medical, financial, security" in page
    for forbidden in ["trusted by", "increased revenue", "guaranteed compliance"]:
        assert forbidden not in page.lower()
