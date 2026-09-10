from pathlib import Path
import csv
import json
import re

REPO = Path(__file__).resolve().parents[1]
DATE = "2026-09-10"
SLUG = "ai-procurement-answer-boundary-card"
TITLE = "AI Procurement Answer Boundary Card: 7 Checks Before Reusing Vendor Answers"
PUB = REPO / "publications" / DATE


def test_evening_publication_assets_exist_and_are_claim_safe():
    html = (PUB / f"{SLUG}.html").read_text(encoding="utf-8")
    csv_path = PUB / f"{SLUG}.csv"
    card = json.loads((PUB / f"{SLUG}-answer-card.json").read_text(encoding="utf-8"))

    assert TITLE in html
    assert "Request a no-credentials answer boundary review" in html
    assert "No credentials, secrets, production logs, customer records or payment" in html
    assert "guaranteed-performance advice" in html
    assert (PUB / f"{SLUG}.png").stat().st_size > 10000
    assert (PUB / f"{SLUG}.svg").stat().st_size > 10000
    assert card["topic"] == TITLE
    assert card["url"].endswith(f"/{SLUG}.html")
    assert "no legal, compliance, audit, certification" in card["safe_scope"]

    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    assert len(rows) == 7
    assert rows[0]["check"] == "Confirm current source"
    assert rows[-1]["check"] == "Review after send"


def test_evening_publication_is_discoverable_from_hub_llms_manifest_and_sitemap():
    resources = (REPO / "resources" / "index.html").read_text(encoding="utf-8")
    home = (REPO / "index.html").read_text(encoding="utf-8")
    llms = (REPO / "llms.txt").read_text(encoding="utf-8")
    sitemap = (REPO / "sitemap.xml").read_text(encoding="utf-8")
    manifest = json.loads((PUB / "manifest.json").read_text(encoding="utf-8"))
    index = (PUB / "index.html").read_text(encoding="utf-8")

    rel = f"/publications/{DATE}/{SLUG}.html"
    abs_url = f"https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html"
    assert rel in resources
    assert rel in home
    assert abs_url in llms
    assert abs_url in sitemap
    assert f"https://aicloudstrategist.com/publications/{DATE}/{SLUG}.csv" in sitemap
    assert any(post["slot"] == "evening" and post["slug"] == SLUG for post in manifest["posts"])
    assert re.search(r"Evening: <a href='ai-procurement-answer-boundary-card.html'", index)
