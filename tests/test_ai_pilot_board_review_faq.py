from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-pilot-board-review-faq"
PAGE = ROOT / "resources" / SLUG / "index.html"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def test_ai_pilot_board_review_faq_page_exists_with_truth_boundary():
    html = PAGE.read_text(encoding="utf-8")
    assert "AI pilot board review FAQ" in html
    assert "what evidence is needed before go-live" in html
    assert "Board evidence checklist" in html
    assert "Executive FAQ" in html
    assert "scale, restrict, remediate or pause" in html
    assert "not a real customer case study" in html
    assert "No outreach was sent" in html
    assert URL in html


def test_ai_pilot_board_review_faq_discovery_links():
    html = PAGE.read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert "/resources/global-ai-pilot-readiness-intake-questionnaire/" in html
    assert "/resources/global-ai-pilot-board-risk-register-template/" in html
    assert "/resources/global-ai-pilot-external-claim-approval-log-template/" in html
    assert f"/resources/{SLUG}/" in resources
    assert URL in llms
    assert f'"/resources/{SLUG}/"' in sitemap_script
