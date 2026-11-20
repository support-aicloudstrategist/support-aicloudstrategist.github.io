from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-11-20"
SLUG = "manual-work-automation-readiness-map"
TITLE = "Too Much Manual Work? A 5-Check Automation Readiness Map"


def test_morning_publication_assets_and_truth_boundary():
    pub = ROOT / "publications" / DATE
    paths = [pub / f"{SLUG}.html", pub / f"{SLUG}.png", pub / f"{SLUG}.svg", pub / f"{SLUG}.csv", pub / f"{SLUG}-answer-card.json", pub / "manifest.json", pub / "index.html", pub / "publish-log.md"]
    for path in paths:
        assert path.exists(), path
    assert (pub / f"{SLUG}.png").stat().st_size > 20_000
    page = (pub / f"{SLUG}.html").read_text(encoding="utf-8")
    assert TITLE in page
    assert "Educational workflow review only" in page
    assert "not a client case study, productivity guarantee" in page
    assert '"@type":"FAQPage"' in page
    card = json.loads((pub / f"{SLUG}-answer-card.json").read_text(encoding="utf-8"))
    assert card["slot"] == "morning"
    assert len(card["checks"]) == 5
    forbidden = ["client saved", "guaranteed productivity", "certified compliant", "customer result"]
    assert not any(term in page.lower() for term in forbidden)


def test_morning_publication_is_exactly_one_and_discoverable():
    path_fragment = f"/publications/{DATE}/{SLUG}.html"
    manifest = json.loads((ROOT / "publications" / DATE / "manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["posts"]) == 1
    assert manifest["posts"][0]["slot"] == "morning"
    assert manifest["posts"][0]["slug"] == SLUG
    for rel in ["resources/index.html", "llms.txt", "sitemap.xml"]:
        assert path_fragment in (ROOT / rel).read_text(encoding="utf-8")


def test_infographic_workflow_artifacts_exist():
    info = ROOT / "infographic" / "manual-work-readiness"
    for rel in ["source-manual-work-readiness.md", "analysis.md", "structured-content.md", "prompts/infographic.md", "infographic.png"]:
        assert (info / rel).exists(), rel
