from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-pilot-incident-override-log-template"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "ai-pilot-incident-override-log.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def test_ai_pilot_incident_override_log_page_exists_with_truth_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    assert "AI pilot incident and human override log template" in html
    assert "AI pilot incident override log template" in html
    assert "Human override" in html
    assert "Rollback and containment" in html
    assert "External claim boundary" in html
    assert "not a real customer case study" in html
    assert "No outreach was sent" in html
    assert URL in html


def test_ai_pilot_incident_override_log_download_and_discovery_links():
    html = PAGE.read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    csv = CSV.read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/ai-pilot-incident-override-log.csv" in html
    assert "Log lane,Evidence to capture,Owner question" in csv
    assert "Human override" in csv
    assert f"/resources/{SLUG}/" in resources
    assert URL in llms
