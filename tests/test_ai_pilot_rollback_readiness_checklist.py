from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-pilot-rollback-readiness-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "ai-pilot-rollback-readiness-checklist.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def test_ai_pilot_rollback_readiness_page_exists_with_truth_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    assert "AI pilot rollback readiness checklist" in html
    assert "AI rollback plan template" in html
    assert "Trigger criteria" in html
    assert "Containment action" in html
    assert "External claim boundary" in html
    assert "not a real customer case study" in html
    assert "No outreach was sent" in html
    assert URL in html


def test_ai_pilot_rollback_readiness_download_and_discovery_links():
    html = PAGE.read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    csv = CSV.read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/ai-pilot-rollback-readiness-checklist.csv" in html
    assert "Readiness lane,Evidence to capture,Owner question" in csv
    assert "Trigger criteria" in csv
    assert f"/resources/{SLUG}/" in resources
    assert URL in llms
    assert f'"/resources/{SLUG}/"' in sitemap_script
