from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-pilot-remediation-decision-log-template"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "ai-pilot-remediation-decision-log.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def test_ai_pilot_remediation_decision_log_page_exists_with_truth_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    assert "AI pilot remediation decision log template" in html
    assert "AI incident remediation evidence log" in html
    assert "Decision type" in html
    assert "Retest and monitoring" in html
    assert "Scale decision impact" in html
    assert "Claim boundary" in html
    assert "not a real customer case study" in html
    assert "No outreach was sent" in html
    assert URL in html


def test_ai_pilot_remediation_decision_log_download_and_discovery_links():
    html = PAGE.read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    csv = CSV.read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/ai-pilot-remediation-decision-log.csv" in html
    assert "Decision lane,Evidence to capture,Owner question" in csv
    assert "Retest and monitoring" in csv
    assert f"/resources/{SLUG}/" in resources
    assert URL in llms
