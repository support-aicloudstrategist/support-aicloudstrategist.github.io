from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-04"
SLUG = "ai-change-approval-card"
URL = f"https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html"
CSV_URL = f"https://aicloudstrategist.com/publications/{DATE}/{SLUG}.csv"
PATH = f"/publications/{DATE}/{SLUG}.html"
CSV_PATH = f"/publications/{DATE}/{SLUG}.csv"


def test_resource_hub_features_latest_change_approval_publication():
    html = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert 'data-featured-publication="ai-change-approval-card"' in html
    assert PATH in html
    assert CSV_PATH in html
    assert "Featured: The AI Change Approval Card" in html
    assert "human approval before it touches customers, money, credentials, policy" in html


def test_llms_txt_routes_ai_change_approval_for_answer_engines():
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in llms
    assert CSV_URL in llms
    assert "safe educational AI change-approval checklist" in llms
    assert "approval-required triggers, human owners, evidence needed" in llms


def test_publication_assets_are_indexable_and_claim_safe():
    page = (ROOT / "publications" / DATE / f"{SLUG}.html").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert f"<loc>{URL}</loc>" in sitemap
    assert f"<link rel='canonical' href='{URL}'>" in page
    assert "approval_required" in (ROOT / "publications" / DATE / f"{SLUG}.csv").read_text(encoding="utf-8")
    assert "not legal, compliance, medical, financial, security" in page
    assert "customer-result" in page
    for forbidden in ["trusted by", "increased revenue", "guaranteed compliance"]:
        assert forbidden not in page.lower()
