from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-11-21"
SLUG = "ai-workflow-auto-act-or-ask-first"
TITLE = "AI Workflow Decision: Auto-Act or Ask First?"


def test_evening_assets_and_truth_boundary():
    pub = ROOT / "publications" / DATE
    for name in [f"{SLUG}.html", f"{SLUG}.png", f"{SLUG}.svg", f"{SLUG}.csv", f"{SLUG}-answer-card.json", f"{SLUG}.md"]:
        assert (pub / name).exists(), name
    assert (pub / f"{SLUG}.png").stat().st_size > 20_000
    page = (pub / f"{SLUG}.html").read_text(encoding="utf-8")
    assert TITLE in page
    assert "Educational workflow-design material only" in page
    assert "Local policy and authorized human owners always override" in page
    assert '"@type":"FAQPage"' in page
    forbidden = ["client saved", "guaranteed result", "certified compliant", "customer result achieved"]
    assert not any(term in page.lower() for term in forbidden)


def test_exactly_two_daily_posts_and_slots():
    pub = ROOT / "publications" / DATE
    manifest = json.loads((pub / "manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["posts"]) == 2
    assert [item["slot"] for item in manifest["posts"]] == ["morning", "evening"]
    assert manifest["posts"][1]["slug"] == SLUG
    index = (pub / "index.html").read_text(encoding="utf-8")
    assert "ai-tool-pilot-brief.html" in index
    assert f"{SLUG}.html" in index


def test_infographic_workflow_discovery_and_status():
    info = ROOT / "infographic" / "ai-workflow-decision"
    for rel in ["source-ai-workflow-decision.md", "analysis.md", "structured-content.md", "prompts/infographic.md", "infographic.png"]:
        assert (info / rel).exists(), rel
    fragment = f"/publications/{DATE}/{SLUG}.html"
    for rel in ["resources/index.html", "llms.txt", "sitemap.xml"]:
        assert fragment in (ROOT / rel).read_text(encoding="utf-8")
    status_path = Path("/home/agent/.hermes/aicloudstrategist/publications") / f"daily-publication-status-{DATE}.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    assert status["successful_posts"] == 2
    assert status["morning"]["status"] == "published"
    assert status["evening"]["status"] == "published"
    assert status["successful_portal_count"] == 2
