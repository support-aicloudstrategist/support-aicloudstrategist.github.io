from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-11-25"
SLUG = "recurring-report-automation-handoff"
TITLE = "Still Building the Same Report by Hand? A 6-Step Automation Handoff"


def test_morning_publication_assets_and_truth_boundary():
    pub = ROOT / "publications" / DATE
    for name in [f"{SLUG}.html", f"{SLUG}.png", f"{SLUG}.svg", f"{SLUG}.csv", f"{SLUG}-answer-card.json", f"{SLUG}.md", "manifest.json", "index.html", "publish-log.md"]:
        assert (pub / name).exists(), name
    assert (pub / f"{SLUG}.png").stat().st_size > 20_000
    page = (pub / f"{SLUG}.html").read_text(encoding="utf-8")
    assert TITLE in page
    assert "Educational workflow-design material only" in page
    assert '"@type":"FAQPage"' in page
    for forbidden in ["client saved", "guaranteed result", "certified compliant", "customer result"]:
        assert forbidden not in page.lower()


def test_exactly_one_post_and_infographic_workflow():
    pub = ROOT / "publications" / DATE
    manifest = json.loads((pub / "manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["posts"]) == 1
    assert manifest["posts"][0]["slot"] == "morning"
    info = ROOT / "infographic" / "recurring-report-handoff"
    for rel in ["source-recurring-report-handoff.md", "analysis.md", "structured-content.md", "prompts/infographic.md", "infographic.png"]:
        assert (info / rel).exists(), rel


def test_discovery_and_daily_status():
    assert f"/publications/{DATE}/{SLUG}.html" in (ROOT / "resources/index.html").read_text(encoding="utf-8")
    assert f"/publications/{DATE}/{SLUG}.png" in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert SLUG in (ROOT / "llms.txt").read_text(encoding="utf-8")
    status_path = Path("/home/agent/.hermes/aicloudstrategist/publications") / f"daily-publication-status-{DATE}.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    assert status["successful_posts_today"] == 1
    assert status["morning"] == "published"
    assert status["evening"] == "not yet due"
    assert status["successful_portals"] == 1
