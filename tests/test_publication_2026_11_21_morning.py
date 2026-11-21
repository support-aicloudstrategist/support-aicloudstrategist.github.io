from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-11-21"
SLUG = "ai-tool-pilot-brief"
TITLE = "Before You Buy an AI Tool: A 6-Box Pilot Brief"


def test_morning_assets_and_truth_boundary():
    pub = ROOT / "publications" / DATE
    for name in [f"{SLUG}.html", f"{SLUG}.png", f"{SLUG}.svg", f"{SLUG}.csv", f"{SLUG}-answer-card.json", "manifest.json", "index.html", "publish-log.md"]:
        assert (pub / name).exists(), name
    assert (pub / f"{SLUG}.png").stat().st_size > 20_000
    page = (pub / f"{SLUG}.html").read_text(encoding="utf-8")
    assert TITLE in page
    assert "Educational pilot-planning material only" in page
    assert "not a client case study, performance guarantee" in page
    assert '"@type":"FAQPage"' in page
    forbidden = ["client saved", "guaranteed result", "certified compliant", "customer result"]
    assert not any(term in page.lower() for term in forbidden)


def test_exactly_one_morning_post_and_discovery_entries():
    pub = ROOT / "publications" / DATE
    manifest = json.loads((pub / "manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["posts"]) == 1
    assert manifest["posts"][0]["slot"] == "morning"
    assert manifest["posts"][0]["slug"] == SLUG
    fragment = f"/publications/{DATE}/{SLUG}.html"
    for rel in ["resources/index.html", "llms.txt", "sitemap.xml"]:
        assert fragment in (ROOT / rel).read_text(encoding="utf-8")


def test_infographic_workflow_and_status():
    info = ROOT / "infographic" / "ai-tool-pilot-brief"
    for rel in ["source-ai-tool-pilot-brief.md", "analysis.md", "structured-content.md", "prompts/infographic.md", "infographic.png"]:
        assert (info / rel).exists(), rel
    status_path = Path("/home/agent/.hermes/aicloudstrategist/publications") / f"daily-publication-status-{DATE}.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    assert status["successful_posts"] == 1
    assert status["morning"]["status"] == "published"
    assert status["evening"]["status"] == "not yet due"
    assert status["successful_portal_count"] == 2
