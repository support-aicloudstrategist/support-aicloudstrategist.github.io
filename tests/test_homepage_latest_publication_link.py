from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
DATE = "2026-09-03"
SLUG = "ai-source-evidence-card"
TITLE = "The AI Source Evidence Card"
PUBLICATION = ROOT / "publications" / DATE / f"{SLUG}.html"
MANIFEST = ROOT / "publications" / DATE / "manifest.json"
PNG = ROOT / "publications" / DATE / f"{SLUG}.png"


def test_homepage_surfaces_latest_ai_source_evidence_card_publication():
    home = HOME.read_text(encoding="utf-8")
    publication = PUBLICATION.read_text(encoding="utf-8")

    href = f"/publications/{DATE}/{SLUG}.html"
    assert href in home
    assert f'<h3><a href="{href}">{TITLE}</a></h3>' in home
    assert TITLE in home
    assert f"<link rel='canonical' href='https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'>" in publication
    assert "ai source evidence card" in publication.lower()
    assert "not legal, compliance, medical, financial" in publication


def test_morning_publication_has_infographic_and_manifest_evidence():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    latest = [entry for entry in manifest if entry["slot"] == "morning" and entry["slug"] == SLUG]
    assert latest
    assert latest[0]["title"] == TITLE
    assert latest[0]["url"] == f"https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html"
    assert PNG.exists()
    assert PNG.stat().st_size > 1000
