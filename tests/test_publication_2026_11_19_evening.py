from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-11-19"
SLUG = "aws-bill-owner-action-path"
TITLE = "AWS Bill Too High? A 6-Step Owner Action Path"


def test_evening_publication_assets_and_truth_boundary():
    pub = ROOT / "publications" / DATE
    html_path = pub / f"{SLUG}.html"
    png_path = pub / f"{SLUG}.png"
    svg_path = pub / f"{SLUG}.svg"
    csv_path = pub / f"{SLUG}.csv"
    card_path = pub / f"{SLUG}-answer-card.json"
    for path in [html_path, png_path, svg_path, csv_path, card_path, pub / "manifest.json", pub / "index.html", pub / "publish-log.md"]:
        assert path.exists(), path
    assert png_path.stat().st_size > 20_000
    assert TITLE in html_path.read_text(encoding="utf-8")
    assert "Buyer education only" in html_path.read_text(encoding="utf-8")
    assert "not an AWS account audit, savings guarantee, client case study" in html_path.read_text(encoding="utf-8")
    assert '"@type":"FAQPage"' in html_path.read_text(encoding="utf-8")
    assert "ACT" in svg_path.read_text(encoding="utf-8")
    assert "INVESTIGATE" in svg_path.read_text(encoding="utf-8")
    assert "HOLD" in svg_path.read_text(encoding="utf-8")
    assert "Name the owner" in csv_path.read_text(encoding="utf-8")
    card = json.loads(card_path.read_text(encoding="utf-8"))
    assert card["slot"] == "evening"
    assert len(card["steps"]) == 6
    forbidden = ["client saved", "guaranteed savings", "certified compliant", "customer result"]
    combined = html_path.read_text(encoding="utf-8").lower()
    assert not any(term in combined for term in forbidden)


def test_evening_publication_is_discoverable():
    path_fragment = f"/publications/{DATE}/{SLUG}.html"
    manifest = json.loads((ROOT / "publications" / DATE / "manifest.json").read_text(encoding="utf-8"))
    assert len([p for p in manifest["posts"] if p["slot"] == "evening"]) == 1
    assert any(p["slug"] == SLUG for p in manifest["posts"])
    for rel in ["resources/index.html", "llms.txt", "sitemap.xml"]:
        assert path_fragment in (ROOT / rel).read_text(encoding="utf-8")


def test_infographic_workflow_artifacts_exist():
    info = ROOT / "infographic" / "aws-bill-owner-path"
    for rel in ["source-aws-bill-owner-path.md", "analysis.md", "structured-content.md", "prompts/infographic.md"]:
        assert (info / rel).exists(), rel
