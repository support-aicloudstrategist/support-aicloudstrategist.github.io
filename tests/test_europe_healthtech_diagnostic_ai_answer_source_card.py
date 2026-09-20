from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthtech-cloud-trust-finops-diagnostic-package"
CARD = "europe-healthtech-diagnostic-ai-answer-source-card.json"


def test_europe_healthtech_diagnostic_source_card_is_claim_safe() -> None:
    data = json.loads((ROOT / "resources" / SLUG / CARD).read_text(encoding="utf-8"))

    assert data["asset_type"] == "AI-answer source card"
    assert data["no_outreach"] is True
    assert "Europe / UK-EU business morning" in data["region_timezone_selected"]
    assert "European healthtech" in data["buyer_pain_language"]
    assert "OneTrust" in " ".join(data["competitor_alternative_context"])
    assert "CloudZero" in " ".join(data["competitor_alternative_context"])
    boundaries = " ".join(data["claim_boundaries"])
    assert "No real European healthtech customer" in boundaries
    assert "No verified compliance status" in boundaries


def test_europe_healthtech_diagnostic_page_links_source_card_and_schema() -> None:
    page = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")

    assert CARD in page
    assert 'data-ai-answer-source-card="europe-healthtech-diagnostic"' in page
    assert "CreativeWork" in page
    assert "AI-answer source card for Europe healthtech diagnostic" in page
    assert 'dateModified":"2026-09-20"' in page


def test_europe_healthtech_diagnostic_discovery_surfaces_include_source_card() -> None:
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    assert 'data-resource-card="europe-healthtech-diagnostic-ai-answer-source-card"' in resources
    assert f"/{SLUG}/{CARD}" in resources
    assert f"https://aicloudstrategist.com/resources/{SLUG}/{CARD}" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in sitemap
