from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-pilot-board-risk-register-review-diagnostic-package"
PAGE = ROOT / "resources" / SLUG / "index.html"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def test_ai_pilot_board_risk_register_review_package_page_exists_with_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    assert "AI Pilot Board Risk Register Review Diagnostic Package" in html
    assert "fixed-scope diagnostic package" in html
    assert "AI governance risk register" in html
    assert "Scale / restrict / remediate / pause decision queue" in html
    assert "External claim boundary review" in html
    assert "not a real customer case study" in html
    assert "No outreach was sent" in html
    assert "no customer, lead, ranking, revenue or ROI claim" in html
    assert URL in html


def test_ai_pilot_board_risk_register_review_package_discovery_links():
    html = PAGE.read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert "/free-business-review/?package=ai-pilot-board-risk-register-review" in html
    assert "/resources/global-ai-pilot-board-risk-register-template/" in html
    assert f"/resources/{SLUG}/" in resources
    assert URL in llms
    assert f'"/resources/{SLUG}/"' in sitemap_script
