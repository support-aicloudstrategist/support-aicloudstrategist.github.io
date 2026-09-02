from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL = "https://aicloudstrategist.com/roi-calculator/"


def test_roi_calculator_is_discoverable_from_tools_hub():
    html = (ROOT / "tools" / "index.html").read_text(encoding="utf-8")
    assert 'href="/roi-calculator/"' in html
    assert "Business ROI calculator" in html
    assert "Estimate payback, recovered revenue and savings" in html


def test_roi_calculator_is_in_sitemap_and_llms():
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert f"<loc>{URL}</loc>" in sitemap
    assert f"Business ROI calculator for proposal payback, recovered revenue, savings and shared-savings pricing estimates: {URL}" in llms


def test_roi_calculator_page_has_revenue_review_cta_and_claim_boundary():
    page = (ROOT / "roi-calculator" / "index.html").read_text(encoding="utf-8")
    assert "Request ROI Review" in page
    assert "This is an estimate, not a promise" in page
    assert "free-business-review/?service=roi-review" in page
