from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-pilot-board-risk-register-template"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "ai-pilot-board-risk-register.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def test_ai_pilot_board_risk_register_page_exists_with_truth_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    assert "AI pilot board risk register template" in html
    assert "AI governance risk register" in html
    assert "Cost and scale economics" in html
    assert "Rollback readiness" in html
    assert "External claim boundary" in html
    assert "not a real customer case study" in html
    assert "No outreach was sent" in html
    assert URL in html


def test_ai_pilot_board_risk_register_download_and_discovery_links():
    html = PAGE.read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    csv = CSV.read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/ai-pilot-board-risk-register.csv" in html
    assert "Risk lane,Board question,Evidence to attach" in csv
    assert "Vendor/procurement dependency" in csv
    assert f"/resources/{SLUG}/" in resources
    assert URL in llms
    assert f'"/resources/{SLUG}/"' in sitemap_script
