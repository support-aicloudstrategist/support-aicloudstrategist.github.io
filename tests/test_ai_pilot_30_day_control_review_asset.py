from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-pilot-post-launch-30-day-control-review-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "ai-pilot-30-day-control-review.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def test_ai_pilot_30_day_control_review_page_exists_with_truth_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    assert "AI pilot 30-day post-launch control review checklist" in html
    assert "AI pilot 30 day review checklist" in html
    assert "Cost and scale" in html
    assert "Data and access" in html
    assert "External claims" in html
    assert "not a real customer case study" in html
    assert "No outreach was sent" in html
    assert URL in html


def test_ai_pilot_30_day_control_review_download_and_discovery_links():
    html = PAGE.read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    csv = CSV.read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/ai-pilot-30-day-control-review.csv" in html
    assert "Review lane,Evidence to collect,Owner question" in csv
    assert "Decision record" in csv
    assert f"/resources/{SLUG}/" in resources
    assert URL in llms
