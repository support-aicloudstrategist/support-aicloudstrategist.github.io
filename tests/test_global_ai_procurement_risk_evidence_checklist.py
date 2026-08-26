from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-ai-procurement-risk-evidence-checklist" / "index.html"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def test_ai_procurement_risk_page_has_buyer_search_and_truth_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    required = [
        "AI procurement risk evidence checklist",
        "AI procurement checklist",
        "AI vendor risk review",
        "AI procurement risk evidence",
        "AI tool approval checklist",
        "AI vendor due diligence",
        "AI security questionnaire",
        "data access",
        "cost exposure",
        "production ownership",
        "not a real client case study",
        "not vendor ranking",
        "not ROI proof",
        "not a guarantee",
        "No outreach was sent",
        "FAQPage",
    ]
    for marker in required:
        assert marker in html


def test_ai_procurement_risk_page_has_actionable_review_lanes():
    html = PAGE.read_text(encoding="utf-8")
    for lane in [
        "Business use case",
        "Data boundary",
        "Vendor evidence",
        "Model and output risk",
        "Cost exposure",
        "Production ownership",
    ]:
        assert lane in html
    assert html.count("<tr><td><strong>") >= 6
    assert "/free-business-review/?package=ai-procurement-evidence-review" in html


def test_ai_procurement_risk_asset_is_discoverable_from_public_indexes():
    slug = "/resources/global-ai-procurement-risk-evidence-checklist/"
    assert slug in RESOURCES.read_text(encoding="utf-8")
    assert "https://aicloudstrategist.com/resources/global-ai-procurement-risk-evidence-checklist/" in LLMS.read_text(encoding="utf-8")
    assert "https://aicloudstrategist.com/resources/global-ai-procurement-risk-evidence-checklist/" in SITEMAP.read_text(encoding="utf-8")
